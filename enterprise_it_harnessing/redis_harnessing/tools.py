"""Redis tools. redis-cli is common; cloud describe is optional."""

from __future__ import annotations

import os
from typing import Any

from enterprise_it_harnessing.shared.auth import detect_provider, resolve_identity
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"redis_failover"}


def _base() -> list[str]:
    url = os.getenv("REDIS_URL")
    if url:
        return ["redis-cli", "-u", url]
    return ["redis-cli"]


def redis_info(inp: dict[str, Any]) -> str:
    section = inp.get("section", "replication")
    return run_argv(_base() + ["INFO", section])


def redis_slowlog(inp: dict[str, Any]) -> str:
    count = str(inp.get("count", 16))
    return run_argv(_base() + ["SLOWLOG", "GET", count])


def redis_describe_cloud(inp: dict[str, Any]) -> str:
    cache_id = inp["target"]
    provider = detect_provider()
    if provider == "aws":
        return run_argv(aws.elasticache_describe(cache_id))
    if provider == "azure":
        return run_argv(azure.redis_show(cache_id, inp.get("resource_group", "")))
    if provider == "gcp":
        return run_argv(gcp.memorystore_describe(cache_id, inp.get("region") or resolve_identity().region))
    return run_argv(["echo", f"self-hosted redis at REDIS_URL for {cache_id}"])


def redis_failover(inp: dict[str, Any]) -> str:
    return run_argv(_base() + ["CLUSTER", "FAILOVER"])


TOOLS = [
    {
        "name": "redis_info",
        "description": "INFO section (replication, memory, clients, stats). Never FLUSHALL.",
        "input_schema": {
            "type": "object",
            "properties": {"section": {"type": "string"}, "target": {"type": "string"}},
        },
    },
    {
        "name": "redis_slowlog",
        "description": "Read SLOWLOG. Use this before blaming the application.",
        "input_schema": {
            "type": "object",
            "properties": {"count": {"type": "integer"}, "target": {"type": "string"}},
        },
    },
    {
        "name": "redis_describe_cloud",
        "description": "Describe ElastiCache, Azure Cache, or Memorystore. No-op for self-hosted.",
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
        "description": "CLUSTER FAILOVER. Requires approval. Denied if FLUSH* is requested.",
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
