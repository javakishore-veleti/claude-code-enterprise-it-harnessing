"""Kafka tools bound to named FOREX, checkout, and Shopify webhook topics."""

from __future__ import annotations

import json
from typing import Any

from enterprise_it_harnessing.catalog import BUSINESS_UNITS, KAFKA_TOPICS, SERVICES, list_kafka_topics
from enterprise_it_harnessing.shared.cli import run_argv

MUTATING = {"kafka_create_topic"}


def _topic(name: str) -> dict[str, Any] | None:
    if name in KAFKA_TOPICS:
        return {"topic": name, **KAFKA_TOPICS[name]}
    svc = SERVICES.get(name)
    if not svc:
        return None
    matches = [t for t, m in KAFKA_TOPICS.items() if name in m["producers"] + m["consumers"]]
    if not matches:
        return None
    return {"topic": matches[0], "via_service": name, **KAFKA_TOPICS[matches[0]]}


def _bootstrap(meta: dict[str, Any], override: str | None) -> str:
    if override:
        return override
    cluster = meta.get("cluster", "")
    return {
        "msk-forex-markets": "b-1.forex-markets.kafka:9092",
        "msk-forex-settlement": "b-1.forex-settlement.kafka:9092",
        "eventhubs-ecom-retail": "ecom-retail.servicebus.windows.net:9093",
        "eventhubs-ecom-quote": "ecom-quote.servicebus.windows.net:9093",
        "pubsub-fulfillment": "pubsub.googleapis.com:443",
        "msk-customer": "b-1.customer.kafka:9092",
        "eventhubs-support": "support.servicebus.windows.net:9093",
        "eventhubs-advisor": "advisor.servicebus.windows.net:9093",
        "pubsub-research": "pubsub.googleapis.com:443",
        "msk-shopify-webhooks": "b-1.shopify-webhooks.kafka:9092",
    }.get(cluster, "localhost:9092")


def kafka_list_topics(inp: dict[str, Any]) -> str:
    if inp.get("business_unit") or not inp.get("bootstrap"):
        return list_kafka_topics(inp)
    return run_argv(["kafka-topics.sh", "--bootstrap-server", inp["bootstrap"], "--list"])


def kafka_describe_topic(inp: dict[str, Any]) -> str:
    meta = _topic(inp["topic"])
    if not meta:
        return json.dumps({"ok": False, "error": f"unknown topic {inp['topic']}", "hint": "call list_kafka_topics"})
    bootstrap = _bootstrap(meta, inp.get("bootstrap"))
    raw = run_argv(
        ["kafka-topics.sh", "--bootstrap-server", bootstrap, "--describe", "--topic", meta["topic"]]
    )
    return json.dumps({"catalog": meta, "bootstrap": bootstrap, "result": raw}, default=str)


def kafka_consumer_lag(inp: dict[str, Any]) -> str:
    group = inp["group"]
    meta = _topic(inp.get("topic") or group)
    bootstrap = _bootstrap(meta or {}, inp.get("bootstrap"))
    raw = run_argv(
        [
            "kafka-consumer-groups.sh",
            "--bootstrap-server",
            bootstrap,
            "--group",
            group,
            "--describe",
        ]
    )
    note = ""
    if meta and meta["topic"].startswith("fx."):
        note = "FOREX: lag on fx.trades.captured or fx.orders.routed is a trade-processing incident."
    elif meta and meta["topic"].startswith("shopify.webhooks"):
        note = "Shopify: lag here means webhook retries will pile up; check shopify-idempotency Redis."
    elif meta and meta["topic"].startswith("ecom.checkout"):
        note = "Checkout saga lag risks double-charge; pause payments-adapter before rewind."
    return json.dumps({"group": group, "catalog": meta, "note": note, "result": raw}, default=str)


def kafka_create_topic(inp: dict[str, Any]) -> str:
    topic = inp["topic"]
    if topic.startswith("fx.") or topic.startswith("shopify."):
        return json.dumps(
            {
                "ok": False,
                "error": "FOREX and Shopify topic creates go through change-management, not this REPL.",
            }
        )
    bu = inp.get("business_unit", "ecommerce-retail")
    cluster = BUSINESS_UNITS.get(bu, {}).get("kafka", "")
    bootstrap = _bootstrap({"cluster": cluster}, inp.get("bootstrap"))
    raw = run_argv(
        [
            "kafka-topics.sh",
            "--bootstrap-server",
            bootstrap,
            "--create",
            "--topic",
            topic,
            "--partitions",
            str(inp.get("partitions", 12)),
            "--replication-factor",
            str(inp.get("replication_factor", 3)),
        ]
    )
    return json.dumps({"topic": topic, "cluster": cluster, "result": raw}, default=str)


TOOLS = [
    {
        "name": "kafka_list_topics",
        "description": "List catalogued topics for a business unit (fx.trades.captured, shopify.webhooks.orders, ecom.checkout.saga).",
        "input_schema": {
            "type": "object",
            "properties": {"business_unit": {"type": "string"}, "bootstrap": {"type": "string"}},
        },
    },
    {
        "name": "kafka_describe_topic",
        "description": "Describe a named enterprise topic or the primary topic of a microservice.",
        "input_schema": {
            "type": "object",
            "properties": {"topic": {"type": "string"}, "bootstrap": {"type": "string"}},
            "required": ["topic"],
        },
    },
    {
        "name": "kafka_consumer_lag",
        "description": "Consumer-group lag. Groups follow services: fx-matching-engine, shopify-order-sync, orders-workflow.",
        "input_schema": {
            "type": "object",
            "properties": {
                "group": {"type": "string"},
                "topic": {"type": "string"},
                "bootstrap": {"type": "string"},
            },
            "required": ["group"],
        },
    },
    {
        "name": "kafka_create_topic",
        "description": "Create a non-FOREX, non-Shopify topic. Requires approval. FOREX/Shopify creates are denied here.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "business_unit": {"type": "string"},
                "bootstrap": {"type": "string"},
                "partitions": {"type": "integer"},
                "replication_factor": {"type": "integer"},
            },
            "required": ["topic"],
        },
    },
]

DISPATCH = {
    "kafka_list_topics": kafka_list_topics,
    "kafka_describe_topic": kafka_describe_topic,
    "kafka_consumer_lag": kafka_consumer_lag,
    "kafka_create_topic": kafka_create_topic,
}
