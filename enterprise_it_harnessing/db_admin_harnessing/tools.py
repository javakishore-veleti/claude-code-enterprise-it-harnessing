"""DBA tools bound to named FOREX, e-commerce, customer, and Shopify databases."""

from __future__ import annotations

import json
from typing import Any

from enterprise_it_harnessing.catalog import DATABASES, SERVICES, resolve_database
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"create_snapshot", "failover_instance"}


def _resolve(name: str) -> dict[str, Any] | None:
    if name in DATABASES:
        return {"instance": name, **DATABASES[name]}
    svc = SERVICES.get(name)
    if not svc:
        return None
    matches = [n for n, d in DATABASES.items() if d["business_unit"] == svc["business_unit"]]
    if not matches:
        return None
    return {"instance": matches[0], "via_service": name, **DATABASES[matches[0]]}


def describe_instance(inp: dict[str, Any]) -> str:
    rec = _resolve(inp["instance"])
    if not rec:
        return resolve_database(inp)
    instance = rec["instance"]
    cloud = rec["cloud"]
    if cloud == "aws":
        raw = run_argv(aws.rds_describe(instance))
    elif cloud == "azure":
        raw = run_argv(azure.sql_show(instance, inp.get("resource_group", rec["business_unit"])))
    elif cloud == "gcp":
        raw = run_argv(gcp.sql_describe(instance))
    else:
        raw = run_argv(["echo", f"describe {instance}"])
    return json.dumps({"catalog": rec, "probe": raw}, default=str)


def list_backups(inp: dict[str, Any]) -> str:
    rec = _resolve(inp["instance"])
    if not rec:
        return resolve_database(inp)
    instance = rec["instance"]
    cloud = rec["cloud"]
    if cloud == "aws":
        raw = run_argv(aws.rds_snapshots(instance))
    elif cloud == "azure":
        raw = run_argv(azure.sql_list_backups(instance, inp.get("resource_group", rec["business_unit"])))
    elif cloud == "gcp":
        raw = run_argv(gcp.sql_backups(instance))
    else:
        raw = run_argv(["echo", f"list backups for {instance}"])
    return json.dumps({"catalog": rec, "backups": raw}, default=str)


def create_snapshot(inp: dict[str, Any]) -> str:
    rec = _resolve(inp["instance"])
    if not rec:
        return resolve_database(inp)
    instance = rec["instance"]
    snap = inp.get("snapshot_id", f"{instance}-manual")
    if rec["cloud"] == "aws":
        raw = run_argv(aws.rds_snapshot(instance, snap))
    else:
        raw = run_argv(["echo", f"create snapshot {snap} for {instance} on {rec['cloud']}"])
    return json.dumps({"ok": True, "catalog": rec, "snapshot": snap, "result": raw}, default=str)


def failover_instance(inp: dict[str, Any]) -> str:
    rec = _resolve(inp["instance"])
    if not rec:
        return resolve_database(inp)
    if rec["instance"] in {"rds-fx-trades-prod", "rds-fx-risk-prod"}:
        note = "FOREX: confirm matching-engine and CLS adapters are paused or read-only before promote."
    elif rec["instance"] == "rds-shopify-sync-prod":
        note = "Shopify: drain webhook-ingress before failover so HMAC retries do not dual-write."
    else:
        note = "Confirm replica lag is near zero before promote."
    return json.dumps(
        {
            "ok": True,
            "action": "failover",
            "catalog": rec,
            "note": note,
        }
    )


def replication_lag(inp: dict[str, Any]) -> str:
    rec = _resolve(inp["instance"])
    if not rec:
        return resolve_database(inp)
    return json.dumps(
        {
            "ok": True,
            "catalog": rec,
            "check": "replica_lag_seconds",
            "hint": "Treat > 5s as Sev2 on fx-trades / orders / shopify-sync.",
        }
    )


TOOLS = [
    {
        "name": "describe_instance",
        "description": "Describe a catalogued database (rds-fx-trades-prod, azsql-orders-prod, rds-shopify-sync-prod) or an owning microservice.",
        "input_schema": {
            "type": "object",
            "properties": {"instance": {"type": "string"}, "resource_group": {"type": "string"}},
            "required": ["instance"],
        },
    },
    {
        "name": "list_backups",
        "description": "List snapshots for a named enterprise database.",
        "input_schema": {
            "type": "object",
            "properties": {"instance": {"type": "string"}, "resource_group": {"type": "string"}},
            "required": ["instance"],
        },
    },
    {
        "name": "create_snapshot",
        "description": "Manual snapshot before a FOREX, orders, or Shopify release. Requires approval.",
        "input_schema": {
            "type": "object",
            "properties": {"instance": {"type": "string"}, "snapshot_id": {"type": "string"}},
            "required": ["instance"],
        },
    },
    {
        "name": "failover_instance",
        "description": "Promote replica. FOREX and Shopify have extra drain notes. Requires approval.",
        "input_schema": {
            "type": "object",
            "properties": {"instance": {"type": "string"}},
            "required": ["instance"],
        },
    },
    {
        "name": "replication_lag",
        "description": "Report replica lag policy for a named database.",
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
    "replication_lag": replication_lag,
}
