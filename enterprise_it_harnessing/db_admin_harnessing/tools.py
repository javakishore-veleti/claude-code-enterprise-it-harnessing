"""Database admin tools. Engine operations are common; cloud CLIs differ."""

from __future__ import annotations

from typing import Any

from enterprise_it_harnessing.shared.auth import detect_provider
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"create_snapshot", "failover_instance"}


def describe_instance(inp: dict[str, Any]) -> str:
    instance = inp["instance"]
    provider = detect_provider()
    if provider == "aws":
        return run_argv(aws.rds_describe(instance))
    if provider == "azure":
        return run_argv(azure.sql_show(instance, inp.get("resource_group", "")))
    if provider == "gcp":
        return run_argv(gcp.sql_describe(instance))
    return run_argv(["echo", f"describe local engine instance {instance}"])


def list_backups(inp: dict[str, Any]) -> str:
    instance = inp["instance"]
    provider = detect_provider()
    if provider == "aws":
        return run_argv(aws.rds_snapshots(instance))
    if provider == "azure":
        return run_argv(azure.sql_list_backups(instance, inp.get("resource_group", "")))
    if provider == "gcp":
        return run_argv(gcp.sql_backups(instance))
    return run_argv(["echo", f"list backups for {instance}"])


def create_snapshot(inp: dict[str, Any]) -> str:
    instance = inp["instance"]
    snap = inp.get("snapshot_id", f"{instance}-manual")
    if detect_provider() == "aws":
        return run_argv(aws.rds_snapshot(instance, snap))
    return run_argv(["echo", f"create snapshot {snap} for {instance}"])


def failover_instance(inp: dict[str, Any]) -> str:
    return run_argv(["echo", f"failover {inp['instance']} — provider-specific promote/replica step"])


TOOLS = [
    {
        "name": "describe_instance",
        "description": "Describe a database instance (RDS, Azure SQL, Cloud SQL, or local).",
        "input_schema": {
            "type": "object",
            "properties": {
                "instance": {"type": "string"},
                "resource_group": {"type": "string"},
            },
            "required": ["instance"],
        },
    },
    {
        "name": "list_backups",
        "description": "List snapshots or automated backups for an instance.",
        "input_schema": {
            "type": "object",
            "properties": {"instance": {"type": "string"}, "resource_group": {"type": "string"}},
            "required": ["instance"],
        },
    },
    {
        "name": "create_snapshot",
        "description": "Create a manual snapshot before a risky change. Requires approval.",
        "input_schema": {
            "type": "object",
            "properties": {"instance": {"type": "string"}, "snapshot_id": {"type": "string"}},
            "required": ["instance"],
        },
    },
    {
        "name": "failover_instance",
        "description": "Promote a replica / fail over. Requires approval. Never the first step.",
        "input_schema": {
            "type": "object",
            "properties": {"instance": {"type": "string"}},
            "required": ["instance"],
        },
    },
]

DISPATCH = {
    "describe_instance": describe_instance,
    "list_backups": list_backups,
    "create_snapshot": create_snapshot,
    "failover_instance": failover_instance,
}
