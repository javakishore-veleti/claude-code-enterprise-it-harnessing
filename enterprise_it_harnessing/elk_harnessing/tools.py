"""ELK + Grafana tools bound to enterprise indices and dashboard folders."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import quote

from enterprise_it_harnessing.catalog import BUSINESS_UNITS, SERVICES
from enterprise_it_harnessing.shared.cli import run_argv

MUTATING = {"grafana_silence_alert"}

INDEX_ALIASES = {
    "forex-trades": "forex-trade-processing-fx-trade-capture-*",
    "forex-fix": "forex-trade-processing-fx-fix-gateway-*",
    "shopify-webhooks": "shopify-headless-shopify-webhook-ingress-*",
    "shopify-legacy": "shopify-headless-shopify-legacy-bridge-*",
    "orders": "ecommerce-middleware-orders-api-*",
    "shipping": "ecommerce-middleware-tracking-api-*",
    "support": "customer-ticket-api-*",
}


def _es() -> str:
    return os.getenv("ELASTICSEARCH_URL", "https://es.internal:9200")


def _grafana() -> str:
    return os.getenv("GRAFANA_URL", "https://grafana.internal")


def es_cluster_health(inp: dict[str, Any]) -> str:
    bu = inp.get("business_unit")
    stack = BUSINESS_UNITS.get(bu, {}).get("elk") if bu else None
    url = f"{_es()}/_cluster/health"
    return run_argv(["curl", "-sS", "-m", "15", url]) + (
        f"\n# stack={stack or 'default'} bu={bu or 'all'}"
    )


def es_search_index(inp: dict[str, Any]) -> str:
    alias = inp.get("alias") or inp.get("index")
    index = INDEX_ALIASES.get(alias or "", alias or "")
    if inp.get("service") and inp["service"] in SERVICES:
        svc = SERVICES[inp["service"]]
        index = f"{svc['domain']}-{svc['service']}-*"
    query = inp.get("query", "*")
    url = f"{_es()}/{quote(index, safe='*-_')}/_search?q={quote(query)}&size={inp.get('size', 20)}"
    return json.dumps({"index": index, "query": query, "result": json.loads(run_argv(["curl", "-sS", "-m", "20", url]))}, default=str)


def grafana_list_dashboards(inp: dict[str, Any]) -> str:
    folder = inp.get("folder")
    if inp.get("business_unit") and inp["business_unit"] in BUSINESS_UNITS:
        folder = BUSINESS_UNITS[inp["business_unit"]]["grafana"]
    q = quote(folder or "prod")
    return run_argv(["curl", "-sS", "-m", "15", f"{_grafana()}/api/search?query=&folderIds=&tag={q}"])


def grafana_list_alerts(inp: dict[str, Any]) -> str:
    folder = inp.get("business_unit", "")
    return run_argv(["curl", "-sS", "-m", "15", f"{_grafana()}/api/v1/provisioning/alert-rules"]) + (
        f"\n# filter_hint={folder}"
    )


def grafana_silence_alert(inp: dict[str, Any]) -> str:
    return json.dumps(
        {
            "ok": True,
            "action": "silence",
            "alert": inp["alert"],
            "minutes": inp.get("minutes", 30),
            "reason": inp.get("reason", "operator approved"),
        }
    )


TOOLS = [
    {
        "name": "es_cluster_health",
        "description": "Elasticsearch cluster health for a BU stack (es-forex-prod, es-ecom-prod, es-shopify-prod, es-customer-prod).",
        "input_schema": {
            "type": "object",
            "properties": {"business_unit": {"type": "string"}},
        },
    },
    {
        "name": "es_search_index",
        "description": "Search a named alias (forex-trades, shopify-webhooks, orders, shipping, support) or a catalogued service index. Keep size small.",
        "input_schema": {
            "type": "object",
            "properties": {
                "alias": {"type": "string"},
                "index": {"type": "string"},
                "service": {"type": "string"},
                "query": {"type": "string"},
                "size": {"type": "integer"},
            },
        },
    },
    {
        "name": "grafana_list_dashboards",
        "description": "List Grafana dashboards for a business unit folder (grafana-forex-prod, grafana-shopify-prod, ...).",
        "input_schema": {
            "type": "object",
            "properties": {"business_unit": {"type": "string"}, "folder": {"type": "string"}},
        },
    },
    {
        "name": "grafana_list_alerts",
        "description": "List Grafana alert rules. Filter mentally by BU after resolve_service.",
        "input_schema": {
            "type": "object",
            "properties": {"business_unit": {"type": "string"}},
        },
    },
    {
        "name": "grafana_silence_alert",
        "description": "Silence a Grafana alert. Requires approval. Never silence FOREX matching-engine or Shopify webhook HMAC failures without a reason.",
        "input_schema": {
            "type": "object",
            "properties": {
                "alert": {"type": "string"},
                "minutes": {"type": "integer"},
                "reason": {"type": "string"},
            },
            "required": ["alert"],
        },
    },
]

DISPATCH = {
    "es_cluster_health": es_cluster_health,
    "es_search_index": es_search_index,
    "grafana_list_dashboards": grafana_list_dashboards,
    "grafana_list_alerts": grafana_list_alerts,
    "grafana_silence_alert": grafana_silence_alert,
}
