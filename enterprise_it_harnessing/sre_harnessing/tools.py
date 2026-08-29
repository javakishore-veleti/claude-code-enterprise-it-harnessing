"""SRE tools scoped to a named enterprise microservice and its business unit."""

from __future__ import annotations

import json
from typing import Any

from enterprise_it_harnessing.catalog import BUSINESS_UNITS, SERVICES
from enterprise_it_harnessing.shared.cli import run_argv
from enterprise_it_harnessing.shared.providers import aws, azure, gcp

MUTATING = {"rollback_deploy", "page_oncall"}

# What SRE needs from list-units: Sev2 names, pager, next command — not a generic org chart.
_SRE_BY_UNIT: dict[str, dict[str, Any]] = {
    "forex-markets": {
        "sev2": ["fx-matching-engine", "fx-fix-gateway"],
        "slo": "reject-rate, FIX session drops",
        "observe": "./harness-sre.sh observe-fx-matching",
        "incident": "./harness-sre.sh incident-forex-matching",
    },
    "forex-settlement": {
        "sev2": ["fx-cls-adapter", "fx-risk-limits"],
        "slo": "CLS drain, limit-check latency",
        "observe": "./harness-sre.sh list-forex-settlement",
        "incident": "./harness-sre.sh incident-forex-matching",
    },
    "ecommerce-retail": {
        "sev2": ["checkout-orchestrator", "orders-api", "payments-adapter"],
        "slo": "checkout saga, order create",
        "observe": "./harness-sre.sh observe-checkout",
        "incident": "./harness-sre.sh incident-orders-saga",
    },
    "ecommerce-quote": {
        "sev2": ["quote-api", "quote-to-order"],
        "slo": "quote accept → order",
        "observe": "./harness-sre.sh list-ecommerce-quote",
        "incident": "./harness-sre.sh incident-orders-saga",
    },
    "fulfillment": {
        "sev2": ["allocation-engine", "tracking-api"],
        "slo": "allocate → ship",
        "observe": "./harness-sre.sh list-fulfillment",
        "incident": "./harness-sre.sh incident-orders-saga",
    },
    "customer-profile": {
        "sev2": ["identity-service", "consent-ledger"],
        "slo": "login, consent writes",
        "observe": "./harness-sre.sh list-customer-profile",
        "incident": "./harness-sre.sh incident-orders-saga",
    },
    "customer-support": {
        "sev2": ["ticket-api", "sla-watchdog"],
        "slo": "ticket create, SLA breach",
        "observe": "./harness-sre.sh observe-ticket-api",
        "incident": "./harness-sre.sh incident-orders-saga",
    },
    "customer-advisor": {
        "sev2": ["advisor-workspace"],
        "slo": "advisor desktop up",
        "observe": "./harness-sre.sh list-customer-advisor",
        "incident": "./harness-sre.sh incident-orders-saga",
    },
    "product-research": {
        "sev2": [],
        "slo": "ingest lag (not customer-facing Sev2)",
        "observe": "./harness-sre.sh list-product-research",
        "incident": "./harness-sre.sh list-product-research",
    },
    "shopify-merchants": {
        "sev2": ["shopify-webhook-ingress", "shopify-legacy-bridge"],
        "slo": "HMAC failures, SOAP / AS400 sync",
        "observe": "./harness-sre.sh observe-shopify-webhooks",
        "incident": "./harness-sre.sh incident-shopify-hmac",
    },
}


def list_sre_units(_: dict[str, Any]) -> str:
    rows = []
    for slug, unit in BUSINESS_UNITS.items():
        sre = _SRE_BY_UNIT[slug]
        service_count = sum(1 for s in SERVICES.values() if s["business_unit"] == slug)
        rows.append(
            {
                "slug": slug,
                "pager": f"{slug}-sre",
                "sev2": sre["sev2"],
                "slo": sre["slo"],
                "observe": sre["observe"],
                "incident": sre["incident"],
                "account": unit["account"],
                "cluster": unit["cluster"],
                "cloud": unit["cloud"],
                "elk": unit["elk"],
                "services": service_count,
                "blast_radius": f"{unit['account']} only — do not page or rollback another BU",
            }
        )
    return json.dumps(
        {
            "value": (
                "SRE uses this to pick the right pager, Sev2 name, and observe command "
                "before touching a cluster. Accounts are dedicated; a Shopify HMAC page "
                "must not land on FOREX matching."
            ),
            "business_units": rows,
            "total_services": len(SERVICES),
        },
        indent=2,
    )


def _svc(name: str) -> dict[str, Any] | None:
    return SERVICES.get(name)


def observe_health(inp: dict[str, Any]) -> str:
    svc = _svc(inp["service"])
    if not svc:
        return json.dumps({"ok": False, "error": f"unknown service {inp['service']}"})
    cloud = svc["cloud"]
    if cloud == "aws":
        raw = run_argv(aws.cloudwatch_alarms(svc["service"]))
    elif cloud == "azure":
        raw = run_argv(azure.monitor_metrics(inp.get("resource_id") or svc["service"]))
    elif cloud == "gcp":
        raw = run_argv(gcp.monitoring_uptime(svc["service"]))
    else:
        raw = run_argv(["echo", f"no probe for {svc['service']}"])
    return json.dumps({"service": svc, "probe": json.loads(raw)}, default=str)


def fetch_logs(inp: dict[str, Any]) -> str:
    svc = _svc(inp["service"])
    if not svc:
        return json.dumps({"ok": False, "error": f"unknown service {inp['service']}"})
    since = inp.get("since", "15m")
    return json.dumps(
        {
            "ok": True,
            "service": svc["service"],
            "business_unit": svc["business_unit"],
            "elk": svc["elk"],
            "index_hint": f"{svc['domain']}-{svc['service']}-*",
            "since": since,
            "next": "Use the ELK harness es_search_index for the actual query.",
        }
    )


def rollback_deploy(inp: dict[str, Any]) -> str:
    svc = _svc(inp["service"])
    if not svc:
        return json.dumps({"ok": False, "error": f"unknown service {inp['service']}"})
    revision = inp.get("revision", "previous")
    return json.dumps(
        {
            "ok": True,
            "action": "rollback",
            "service": svc["service"],
            "cluster": svc["cluster"],
            "account": svc["account"],
            "revision": revision,
            "note": "Operator approval required. Isolation lease is taken on the service name.",
        }
    )


def page_oncall(inp: dict[str, Any]) -> str:
    svc = _svc(inp.get("service", "")) if inp.get("service") else None
    return json.dumps(
        {
            "ok": True,
            "severity": inp.get("severity", "sev2"),
            "summary": inp["summary"],
            "business_unit": (svc or {}).get("business_unit"),
            "pager": f"{(svc or {}).get('business_unit', 'platform')}-sre",
        }
    )


TOOLS = [
    {
        "name": "list_sre_units",
        "description": "SRE estate map: Sev2 services, pager, SLO, next observe/incident command, dedicated account blast radius.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "observe_health",
        "description": "Health/alarms for a catalogued microservice (e.g. fx-matching-engine, shopify-webhook-ingress, orders-api). Resolves its BU cloud account automatically.",
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "resource_id": {"type": "string"},
            },
            "required": ["service"],
        },
    },
    {
        "name": "fetch_logs",
        "description": "Point at the correct ELK index for a microservice. Does not dump raw logs into context.",
        "input_schema": {
            "type": "object",
            "properties": {"service": {"type": "string"}, "since": {"type": "string"}},
            "required": ["service"],
        },
    },
    {
        "name": "rollback_deploy",
        "description": "Roll back a named microservice on its dedicated cluster. Requires approval.",
        "input_schema": {
            "type": "object",
            "properties": {"service": {"type": "string"}, "revision": {"type": "string"}},
            "required": ["service"],
        },
    },
    {
        "name": "page_oncall",
        "description": "Page the BU SRE rotation (forex-markets-sre, shopify-merchants-sre, ...). Requires approval.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "severity": {"type": "string"},
                "service": {"type": "string"},
            },
            "required": ["summary"],
        },
    },
]

DISPATCH = {
    "list_sre_units": list_sre_units,
    "observe_health": observe_health,
    "fetch_logs": fetch_logs,
    "rollback_deploy": rollback_deploy,
    "page_oncall": page_oncall,
}
