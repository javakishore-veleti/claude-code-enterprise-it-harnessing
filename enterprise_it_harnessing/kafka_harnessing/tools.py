"""Kafka / bus admin tools. Topics and lag are common; cloud listing differs."""

from __future__ import annotations

from typing import Any

from enterprise_it_harnessing.shared.auth import detect_provider
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"kafka_create_topic"}


def kafka_list_topics(inp: dict[str, Any]) -> str:
    bootstrap = inp.get("bootstrap")
    if bootstrap:
        return run_argv(["kafka-topics.sh", "--bootstrap-server", bootstrap, "--list"])
    provider = detect_provider()
    if provider == "aws":
        return run_argv(aws.msk_clusters())
    if provider == "azure":
        return run_argv(azure.eventhubs_list(inp.get("resource_group", "")))
    if provider == "gcp":
        return run_argv(gcp.pubsub_topics())
    return run_argv(["echo", "set bootstrap or CLOUD_PROVIDER to list topics"])


def kafka_describe_topic(inp: dict[str, Any]) -> str:
    bootstrap = inp.get("bootstrap", "localhost:9092")
    return run_argv(
        ["kafka-topics.sh", "--bootstrap-server", bootstrap, "--describe", "--topic", inp["topic"]]
    )


def kafka_consumer_lag(inp: dict[str, Any]) -> str:
    bootstrap = inp.get("bootstrap", "localhost:9092")
    return run_argv(
        [
            "kafka-consumer-groups.sh",
            "--bootstrap-server",
            bootstrap,
            "--group",
            inp["group"],
            "--describe",
        ]
    )


def kafka_create_topic(inp: dict[str, Any]) -> str:
    bootstrap = inp.get("bootstrap", "localhost:9092")
    partitions = str(inp.get("partitions", 3))
    return run_argv(
        [
            "kafka-topics.sh",
            "--bootstrap-server",
            bootstrap,
            "--create",
            "--topic",
            inp["topic"],
            "--partitions",
            partitions,
            "--replication-factor",
            str(inp.get("replication_factor", 3)),
        ]
    )


TOOLS = [
    {
        "name": "kafka_list_topics",
        "description": "List topics, MSK clusters, Event Hubs namespaces, or Pub/Sub topics.",
        "input_schema": {
            "type": "object",
            "properties": {"bootstrap": {"type": "string"}, "resource_group": {"type": "string"}},
        },
    },
    {
        "name": "kafka_describe_topic",
        "description": "Describe a topic: partitions, ISR, replication.",
        "input_schema": {
            "type": "object",
            "properties": {"topic": {"type": "string"}, "bootstrap": {"type": "string"}},
            "required": ["topic"],
        },
    },
    {
        "name": "kafka_consumer_lag",
        "description": "Describe a consumer group and partition lag.",
        "input_schema": {
            "type": "object",
            "properties": {"group": {"type": "string"}, "bootstrap": {"type": "string"}},
            "required": ["group"],
        },
    },
    {
        "name": "kafka_create_topic",
        "description": "Create a topic. Requires approval. Prefer this over raw kafka-topics.sh via bash.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
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
