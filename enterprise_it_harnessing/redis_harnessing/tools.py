"""Redis tools bound to named caches: FX books, carts, Shopify idempotency keys."""

from __future__ import annotations

import json
import os
from typing import Any

from enterprise_it_harnessing.catalog import BUSINESS_UNITS, REDIS_CACHES, SERVICES
from enterprise_it_harnessing.shared.auth import resolve_identity
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"redis_failover"}


def _cache(name: str) -> dict[str, Any] | None:
    if name in REDIS_CACHES:
        return {"cache": name, **REDIS_CACHES[name], **BUSINESS_UNITS[REDIS_CACHES[name]["business_unit"]]}
    if name in BUSINESS_UNITS:
        cache = BUSINESS_UNITS[name]["redis"]
        return {"cache": cache, **REDIS_CACHES.get(cache, {}), **BUSINESS_UNITS[name]}
    svc = SERVICES.get(name)
    if svc:
        cache = svc["redis"]
        return {"cache": cache, "via_service": name, **REDIS_CACHES.get(cache, {}), **svc}
    return None


def _base(cache: str | None = None) -> list[str]:
    url = os.getenv("REDIS_URL")
    if url:
        return ["redis-cli", "-u", url]
    if cache:
        return ["redis-cli", "-h", cache]
    return ["redis-cli"]


def redis_info(inp: dict[str, Any]) -> str:
    rec = _cache(inp.get("target") or inp.get("section") or "") if inp.get("target") else None
    if inp.get("target"):
        rec = _cache(inp["target"])
        if not rec:
            return json.dumps({"ok": False, "error": f"unknown cache {inp['target']}"})
    section = inp.get("section", "replication")
    raw = run_argv(_base((rec or {}).get("cache")) + ["INFO", section])
    return json.dumps({"catalog": rec, "section": section, "result": raw}, default=str)


def redis_slowlog(inp: dict[str, Any]) -> str:
    rec = _cache(inp["target"]) if inp.get("target") else None
    raw = run_argv(_base((rec or {}).get("cache")) + ["SLOWLOG", "GET", str(inp.get("count", 16))])
    return json.dumps({"catalog": rec, "result": raw}, default=str)


def redis_describe_cloud(inp: dict[str, Any]) -> str:
    rec = _cache(inp["target"])
    if not rec:
        return json.dumps({"ok": False, "error": f"unknown cache {inp['target']}"})
    cache_id = rec["cache"]
    cloud = rec.get("cloud")
    if cloud == "aws":
        raw = run_argv(aws.elasticache_describe(cache_id))
    elif cloud == "azure":
        raw = run_argv(azure.redis_show(cache_id, inp.get("resource_group", rec.get("business_unit", ""))))
    elif cloud == "gcp":
        raw = run_argv(gcp.memorystore_describe(cache_id, inp.get("region") or resolve_identity().region))
    else:
        raw = run_argv(["echo", f"self-hosted redis {cache_id}"])
    return json.dumps({"catalog": rec, "result": raw}, default=str)


def redis_failover(inp: dict[str, Any]) -> str:
    rec = _cache(inp["target"])
    if not rec:
        return json.dumps({"ok": False, "error": f"unknown cache {inp['target']}"})
    note = "Confirm replica is healthy."
    if rec["cache"] == "elasticache-forex-quotes":
        note = "FOREX: matching-engine will stale-book if failover exceeds 2s — page forex-markets-sre."
    elif rec["cache"] == "elasticache-shopify-idempotency":
        note = "Shopify: failover can replay webhooks; freeze shopify-webhook-ingress first."
    elif rec["cache"] == "azurecache-ecom-cart":
        note = "Cart failover drops checkout locks — pause checkout-orchestrator."
    raw = run_argv(_base(rec["cache"]) + ["CLUSTER", "FAILOVER"])
    return json.dumps({"catalog": rec, "note": note, "result": raw}, default=str)


TOOLS = [
    {
        "name": "redis_info",
        "description": "INFO on a named cache (elasticache-forex-quotes, azurecache-ecom-cart, elasticache-shopify-idempotency) or a microservice.",
        "input_schema": {
            "type": "object",
            "properties": {"section": {"type": "string"}, "target": {"type": "string"}},
        },
    },
    {
        "name": "redis_slowlog",
        "description": "SLOWLOG for a named cache. Check shopify:idemp:* and fx:book:* before blaming the app.",
        "input_schema": {
            "type": "object",
            "properties": {"count": {"type": "integer"}, "target": {"type": "string"}},
        },
    },
    {
        "name": "redis_describe_cloud",
        "description": "Describe ElastiCache / Azure Cache / Memorystore for a catalogued cache.",
        "input_schema": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "resource_group": {"type": "string"},
                "region": {"type": "string"},
            },
            "required": ["target"],
        },
    },
    {
        "name": "redis_failover",
        "description": "CLUSTER FAILOVER on a named cache. Requires approval. FOREX/Shopify/cart have extra drain notes.",
        "input_schema": {
            "type": "object",
            "properties": {"target": {"type": "string"}},
            "required": ["target"],
        },
    },
]

DISPATCH = {
    "redis_info": redis_info,
    "redis_slowlog": redis_slowlog,
    "redis_describe_cloud": redis_describe_cloud,
    "redis_failover": redis_failover,
}
