"""Enterprise service catalog: 10 business units, ~100 microservices, dedicated clouds."""

from __future__ import annotations

import json
from typing import Any

# Ten BUs. Each owns its cloud account and its own k8s / Kafka / Redis / data plane.
BUSINESS_UNITS: dict[str, dict[str, str]] = {
    "forex-markets": {
        "name": "FOREX Markets",
        "domain": "forex-trade-processing",
        "cloud": "aws",
        "account": "aws-forex-markets-prod",
        "cluster": "eks-forex-markets-prod",
        "kafka": "msk-forex-markets",
        "redis": "elasticache-forex-quotes",
        "elk": "es-forex-prod",
        "grafana": "grafana-forex-prod",
    },
    "forex-settlement": {
        "name": "FOREX Risk & Settlement",
        "domain": "forex-banks-middleware",
        "cloud": "aws",
        "account": "aws-forex-settlement-prod",
        "cluster": "eks-forex-settlement-prod",
        "kafka": "msk-forex-settlement",
        "redis": "elasticache-forex-risk",
        "elk": "es-forex-prod",
        "grafana": "grafana-forex-prod",
    },
    "ecommerce-retail": {
        "name": "Retail e-Commerce",
        "domain": "ecommerce-middleware",
        "cloud": "azure",
        "account": "az-ecom-retail-prod",
        "cluster": "aks-ecom-retail-prod",
        "kafka": "eventhubs-ecom-retail",
        "redis": "azurecache-ecom-cart",
        "elk": "es-ecom-prod",
        "grafana": "grafana-ecom-prod",
    },
    "ecommerce-quote": {
        "name": "B2B Quote",
        "domain": "ecommerce-middleware",
        "cloud": "azure",
        "account": "az-ecom-quote-prod",
        "cluster": "aks-ecom-quote-prod",
        "kafka": "eventhubs-ecom-quote",
        "redis": "azurecache-ecom-quote",
        "elk": "es-ecom-prod",
        "grafana": "grafana-ecom-prod",
    },
    "fulfillment": {
        "name": "Fulfillment & Shipping",
        "domain": "ecommerce-middleware",
        "cloud": "gcp",
        "account": "gcp-fulfillment-prod",
        "cluster": "gke-fulfillment-prod",
        "kafka": "pubsub-fulfillment",
        "redis": "memorystore-fulfillment",
        "elk": "es-ecom-prod",
        "grafana": "grafana-ecom-prod",
    },
    "customer-profile": {
        "name": "Customer Identity & Profile",
        "domain": "customer",
        "cloud": "aws",
        "account": "aws-customer-profile-prod",
        "cluster": "eks-customer-profile-prod",
        "kafka": "msk-customer",
        "redis": "elasticache-profile-session",
        "elk": "es-customer-prod",
        "grafana": "grafana-customer-prod",
    },
    "customer-support": {
        "name": "Customer Support",
        "domain": "customer",
        "cloud": "azure",
        "account": "az-customer-support-prod",
        "cluster": "aks-customer-support-prod",
        "kafka": "eventhubs-support",
        "redis": "azurecache-support",
        "elk": "es-customer-prod",
        "grafana": "grafana-customer-prod",
    },
    "customer-advisor": {
        "name": "Customer Advisor Support",
        "domain": "customer",
        "cloud": "azure",
        "account": "az-customer-advisor-prod",
        "cluster": "aks-customer-advisor-prod",
        "kafka": "eventhubs-advisor",
        "redis": "azurecache-advisor",
        "elk": "es-customer-prod",
        "grafana": "grafana-customer-prod",
    },
    "product-research": {
        "name": "Product Research & Catalog Science",
        "domain": "product-research",
        "cloud": "gcp",
        "account": "gcp-product-research-prod",
        "cluster": "gke-product-research-prod",
        "kafka": "pubsub-research",
        "redis": "memorystore-research",
        "elk": "es-ecom-prod",
        "grafana": "grafana-ecom-prod",
    },
    "shopify-merchants": {
        "name": "Shopify Headless Merchant Integration",
        "domain": "shopify-headless",
        "cloud": "aws",
        "account": "aws-shopify-merchants-prod",
        "cluster": "eks-shopify-merchants-prod",
        "kafka": "msk-shopify-webhooks",
        "redis": "elasticache-shopify-idempotency",
        "elk": "es-shopify-prod",
        "grafana": "grafana-shopify-prod",
    },
}

# About 10 services per unit → 100 microservices across FOREX, e-commerce, customer, research, Shopify.
_SERVICES: list[tuple[str, str, str]] = [
    # FOREX Markets — trade processing middleware for banks
    ("forex-markets", "fx-price-gateway", "Ingest bank and LP quotes"),
    ("forex-markets", "fx-matching-engine", "Match client FX orders"),
    ("forex-markets", "fx-order-router", "Route fills to bank venues"),
    ("forex-markets", "fx-trade-capture", "Normalize executed trades"),
    ("forex-markets", "fx-market-data", "Distribute tick and book updates"),
    ("forex-markets", "fx-session-manager", "Bank trading-session windows"),
    ("forex-markets", "fx-stp-adapter", "Straight-through processing to banks"),
    ("forex-markets", "fx-fix-gateway", "FIX 4.4 / 5.0 session layer"),
    ("forex-markets", "fx-rfq-engine", "Request-for-quote for bank desks"),
    ("forex-markets", "fx-audit-trail", "Immutable trade audit"),
    # FOREX settlement
    ("forex-settlement", "fx-risk-limits", "Pre-trade credit and position limits"),
    ("forex-settlement", "fx-netting", "Multilateral netting"),
    ("forex-settlement", "fx-settlement-instruction", "SSI generation"),
    ("forex-settlement", "fx-nostro-recon", "Nostro / vostro reconciliation"),
    ("forex-settlement", "fx-cls-adapter", "CLS settlement adapter"),
    ("forex-settlement", "fx-pnl-engine", "Intraday PnL"),
    ("forex-settlement", "fx-margin-calc", "Margin and collateral"),
    ("forex-settlement", "fx-confirmations", "Trade confirmations"),
    ("forex-settlement", "fx-regulatory-report", "MiFID / EMIR reporting"),
    ("forex-settlement", "fx-exception-queue", "Failed-settlement work queue"),
    # Retail e-commerce
    ("ecommerce-retail", "catalog-api", "Product catalog read API"),
    ("ecommerce-retail", "catalog-indexer", "Search index publisher"),
    ("ecommerce-retail", "pricing-engine", "List and promo pricing"),
    ("ecommerce-retail", "cart-service", "Cart persistence"),
    ("ecommerce-retail", "checkout-orchestrator", "Checkout saga"),
    ("ecommerce-retail", "orders-api", "Order create / read"),
    ("ecommerce-retail", "orders-workflow", "Order state machine"),
    ("ecommerce-retail", "payments-adapter", "PSP integration"),
    ("ecommerce-retail", "inventory-reservation", "Soft inventory hold"),
    ("ecommerce-retail", "promo-engine", "Coupons and campaigns"),
    # B2B quote
    ("ecommerce-quote", "quote-api", "B2B quote create"),
    ("ecommerce-quote", "quote-pricing", "Contract and tier pricing"),
    ("ecommerce-quote", "quote-approval", "Internal quote approval"),
    ("ecommerce-quote", "quote-expiry", "Quote TTL worker"),
    ("ecommerce-quote", "quote-to-order", "Convert accepted quote"),
    ("ecommerce-quote", "contract-catalog", "Account-specific catalog"),
    ("ecommerce-quote", "rfq-intake", "Inbound RFQ from partners"),
    ("ecommerce-quote", "margin-guard", "Floor-price enforcement"),
    ("ecommerce-quote", "quote-pdf", "Quote document render"),
    ("ecommerce-quote", "partner-portal-bff", "B2B portal BFF"),
    # Fulfillment
    ("fulfillment", "allocation-engine", "Warehouse allocation"),
    ("fulfillment", "wms-adapter", "Warehouse management adapter"),
    ("fulfillment", "pick-pack", "Pick and pack tasks"),
    ("fulfillment", "shipping-rates", "Carrier rate shop"),
    ("fulfillment", "shipping-label", "Label generation"),
    ("fulfillment", "carrier-webhook", "Carrier scan events"),
    ("fulfillment", "tracking-api", "Shipment tracking"),
    ("fulfillment", "returns-intake", "RMA intake"),
    ("fulfillment", "asn-service", "Advance shipping notices"),
    ("fulfillment", "last-mile-router", "Last-mile carrier select"),
    # Customer profile
    ("customer-profile", "identity-service", "AuthN / token issue"),
    ("customer-profile", "profile-api", "Customer profile CRUD"),
    ("customer-profile", "address-book", "Saved addresses"),
    ("customer-profile", "preferences", "Comms and locale prefs"),
    ("customer-profile", "consent-ledger", "GDPR / consent"),
    ("customer-profile", "loyalty-points", "Loyalty balance"),
    ("customer-profile", "household-graph", "Linked accounts"),
    ("customer-profile", "kyc-adapter", "KYC vendor"),
    ("customer-profile", "device-fingerprint", "Device risk"),
    ("customer-profile", "profile-search", "Agent profile lookup"),
    # Customer support
    ("customer-support", "ticket-api", "Support tickets"),
    ("customer-support", "ticket-router", "Skill-based routing"),
    ("customer-support", "knowledge-search", "Help-center search"),
    ("customer-support", "chat-gateway", "Live chat"),
    ("customer-support", "case-timeline", "Case event log"),
    ("customer-support", "sla-watchdog", "SLA breach detector"),
    ("customer-support", "csat-collector", "CSAT surveys"),
    ("customer-support", "macro-engine", "Agent macros"),
    ("customer-support", "channel-email", "Email channel"),
    ("customer-support", "channel-voice", "Voice / CCaaS adapter"),
    # Advisor
    ("customer-advisor", "advisor-workspace", "Advisor desktop BFF"),
    ("customer-advisor", "next-best-action", "Recommended offer"),
    ("customer-advisor", "advisor-notes", "Secure notes"),
    ("customer-advisor", "call-assist", "In-call assist"),
    ("customer-advisor", "escalation-bridge", "Warm transfer"),
    ("customer-advisor", "advisor-authz", "Desk entitlements"),
    ("customer-advisor", "script-engine", "Guided scripts"),
    ("customer-advisor", "opportunity-feed", "Advisor opportunities"),
    ("customer-advisor", "compliance-tracker", "Regulated advice log"),
    ("customer-advisor", "advisor-analytics", "Handle-time analytics"),
    # Product research
    ("product-research", "research-ingest", "Vendor and trend ingest"),
    ("product-research", "assortment-planner", "Assortment proposals"),
    ("product-research", "attribute-enrichment", "Catalog attributes"),
    ("product-research", "competitor-price", "Competitive price crawl"),
    ("product-research", "trend-signals", "Demand signals"),
    ("product-research", "sample-tracker", "Physical sample lab"),
    ("product-research", "supplier-score", "Supplier quality"),
    ("product-research", "catalog-draft", "Draft SKU pipeline"),
    ("product-research", "image-studio", "Asset pipeline"),
    ("product-research", "launch-calendar", "Merch launch calendar"),
    # Shopify headless — webhooks + legacy / on-prem sync
    ("shopify-merchants", "shopify-oauth", "Merchant OAuth / app install"),
    ("shopify-merchants", "shopify-webhook-ingress", "HMAC-verified webhook intake"),
    ("shopify-merchants", "shopify-webhook-retry", "At-least-once retry"),
    ("shopify-merchants", "shopify-product-sync", "Product → catalog-api / on-prem PIM"),
    ("shopify-merchants", "shopify-inventory-sync", "Inventory both ways"),
    ("shopify-merchants", "shopify-order-sync", "Orders → orders-api / ERP"),
    ("shopify-merchants", "shopify-customer-sync", "Customers → profile-api"),
    ("shopify-merchants", "shopify-fulfillment-push", "Fulfillment back to Shopify"),
    ("shopify-merchants", "shopify-legacy-bridge", "On-prem SOAP / AS/400 adapter"),
    ("shopify-merchants", "shopify-idempotency", "Webhook idempotency keys"),
]


def _index() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for bu, service, purpose in _SERVICES:
        unit = BUSINESS_UNITS[bu]
        out[service] = {
            "service": service,
            "purpose": purpose,
            "business_unit": bu,
            **unit,
        }
    return out


SERVICES = _index()


def list_business_units(_: dict[str, Any] | None = None) -> str:
    rows = [
        {
            "slug": slug,
            "name": u["name"],
            "domain": u["domain"],
            "cloud": u["cloud"],
            "account": u["account"],
            "cluster": u["cluster"],
            "services": sum(1 for s in SERVICES.values() if s["business_unit"] == slug),
        }
        for slug, u in BUSINESS_UNITS.items()
    ]
    return json.dumps({"business_units": rows, "total_services": len(SERVICES)}, indent=2)


def list_services(inp: dict[str, Any]) -> str:
    bu = inp.get("business_unit")
    domain = inp.get("domain")
    rows = []
    for svc in SERVICES.values():
        if bu and svc["business_unit"] != bu:
            continue
        if domain and svc["domain"] != domain:
            continue
        rows.append(svc)
    return json.dumps({"count": len(rows), "services": rows}, indent=2)


def resolve_service(inp: dict[str, Any]) -> str:
    name = inp["service"]
    svc = SERVICES.get(name)
    if not svc:
        return json.dumps({"ok": False, "error": f"unknown service '{name}'", "hint": "call list_services"})
    return json.dumps({"ok": True, **svc}, indent=2)


CATALOG_TOOLS = [
    {
        "name": "list_business_units",
        "description": "List the 10 enterprise business units, their dedicated cloud accounts, and clusters.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "list_services",
        "description": "List microservices. Filter by business_unit slug or domain (forex-trade-processing, ecommerce-middleware, shopify-headless, ...).",
        "input_schema": {
            "type": "object",
            "properties": {
                "business_unit": {"type": "string"},
                "domain": {"type": "string"},
            },
        },
    },
    {
        "name": "resolve_service",
        "description": "Resolve a microservice to its BU, cloud account, k8s cluster, Kafka, Redis, and ELK stack.",
        "input_schema": {
            "type": "object",
            "properties": {"service": {"type": "string"}},
            "required": ["service"],
        },
    },
    {
        "name": "list_databases",
        "description": "List named production databases (fx trades/risk, orders, quotes, Shopify sync, ...).",
        "input_schema": {"type": "object", "properties": {"business_unit": {"type": "string"}}},
    },
    {
        "name": "resolve_database",
        "description": "Resolve a database instance or owning microservice to engine, cloud account, and owner services.",
        "input_schema": {
            "type": "object",
            "properties": {"instance": {"type": "string"}},
            "required": ["instance"],
        },
    },
    {
        "name": "list_kafka_topics",
        "description": "List named enterprise topics (fx.trades.captured, shopify.webhooks.orders, ecom.checkout.saga, ...).",
        "input_schema": {"type": "object", "properties": {"business_unit": {"type": "string"}}},
    },
    {
        "name": "list_redis_caches",
        "description": "List named Redis caches (FX books, carts, Shopify idempotency, ...).",
        "input_schema": {"type": "object", "properties": {"business_unit": {"type": "string"}}},
    },
]

# Named data stores, buses, and caches — one primary per business unit, plus FOREX/Shopify extras.
DATABASES: dict[str, dict[str, Any]] = {
    "rds-fx-trades-prod": {
        "business_unit": "forex-markets",
        "engine": "aurora-postgresql",
        "cloud": "aws",
        "account": "aws-forex-markets-prod",
        "purpose": "Trade capture, FIX sessions, audit trail",
        "owner_services": ["fx-trade-capture", "fx-fix-gateway", "fx-audit-trail"],
    },
    "rds-fx-risk-prod": {
        "business_unit": "forex-settlement",
        "engine": "aurora-postgresql",
        "cloud": "aws",
        "account": "aws-forex-settlement-prod",
        "purpose": "Limits, netting, CLS, regulatory reports",
        "owner_services": ["fx-risk-limits", "fx-netting", "fx-cls-adapter", "fx-regulatory-report"],
    },
    "azsql-orders-prod": {
        "business_unit": "ecommerce-retail",
        "engine": "azure-sql",
        "cloud": "azure",
        "account": "az-ecom-retail-prod",
        "purpose": "Orders, checkout saga, payments ledger",
        "owner_services": ["orders-api", "orders-workflow", "checkout-orchestrator", "payments-adapter"],
    },
    "azsql-quotes-prod": {
        "business_unit": "ecommerce-quote",
        "engine": "azure-sql",
        "cloud": "azure",
        "account": "az-ecom-quote-prod",
        "purpose": "B2B quotes, contracts, approvals",
        "owner_services": ["quote-api", "quote-approval", "quote-to-order", "contract-catalog"],
    },
    "cloudsql-fulfillment-prod": {
        "business_unit": "fulfillment",
        "engine": "cloud-sql-postgres",
        "cloud": "gcp",
        "account": "gcp-fulfillment-prod",
        "purpose": "Allocation, WMS, tracking, returns",
        "owner_services": ["allocation-engine", "wms-adapter", "tracking-api", "returns-intake"],
    },
    "rds-profile-prod": {
        "business_unit": "customer-profile",
        "engine": "aurora-postgresql",
        "cloud": "aws",
        "account": "aws-customer-profile-prod",
        "purpose": "Identity, profile, consent, loyalty",
        "owner_services": ["identity-service", "profile-api", "consent-ledger", "loyalty-points"],
    },
    "azsql-support-prod": {
        "business_unit": "customer-support",
        "engine": "azure-sql",
        "cloud": "azure",
        "account": "az-customer-support-prod",
        "purpose": "Tickets, SLA, CSAT",
        "owner_services": ["ticket-api", "ticket-router", "sla-watchdog"],
    },
    "azsql-advisor-prod": {
        "business_unit": "customer-advisor",
        "engine": "azure-sql",
        "cloud": "azure",
        "account": "az-customer-advisor-prod",
        "purpose": "Advisor notes, compliance, opportunities",
        "owner_services": ["advisor-workspace", "advisor-notes", "compliance-tracker"],
    },
    "cloudsql-research-prod": {
        "business_unit": "product-research",
        "engine": "cloud-sql-postgres",
        "cloud": "gcp",
        "account": "gcp-product-research-prod",
        "purpose": "Assortment, attributes, launch calendar",
        "owner_services": ["assortment-planner", "attribute-enrichment", "catalog-draft"],
    },
    "rds-shopify-sync-prod": {
        "business_unit": "shopify-merchants",
        "engine": "aurora-postgresql",
        "cloud": "aws",
        "account": "aws-shopify-merchants-prod",
        "purpose": "Webhook inbox, idempotency, legacy mapping",
        "owner_services": ["shopify-webhook-ingress", "shopify-idempotency", "shopify-legacy-bridge"],
    },
}

KAFKA_TOPICS: dict[str, dict[str, Any]] = {
    "fx.quotes.raw": {"business_unit": "forex-markets", "cluster": "msk-forex-markets", "producers": ["fx-price-gateway"], "consumers": ["fx-matching-engine", "fx-market-data"]},
    "fx.orders.routed": {"business_unit": "forex-markets", "cluster": "msk-forex-markets", "producers": ["fx-order-router"], "consumers": ["fx-matching-engine", "fx-stp-adapter"]},
    "fx.trades.captured": {"business_unit": "forex-markets", "cluster": "msk-forex-markets", "producers": ["fx-trade-capture"], "consumers": ["fx-audit-trail", "fx-stp-adapter"]},
    "fx.fix.sessions": {"business_unit": "forex-markets", "cluster": "msk-forex-markets", "producers": ["fx-fix-gateway"], "consumers": ["fx-session-manager"]},
    "fx.settlement.instructions": {"business_unit": "forex-settlement", "cluster": "msk-forex-settlement", "producers": ["fx-settlement-instruction"], "consumers": ["fx-cls-adapter", "fx-nostro-recon"]},
    "fx.risk.breaches": {"business_unit": "forex-settlement", "cluster": "msk-forex-settlement", "producers": ["fx-risk-limits"], "consumers": ["fx-exception-queue", "fx-margin-calc"]},
    "ecom.orders.created": {"business_unit": "ecommerce-retail", "cluster": "eventhubs-ecom-retail", "producers": ["orders-api"], "consumers": ["orders-workflow", "inventory-reservation"]},
    "ecom.checkout.saga": {"business_unit": "ecommerce-retail", "cluster": "eventhubs-ecom-retail", "producers": ["checkout-orchestrator"], "consumers": ["payments-adapter", "orders-workflow"]},
    "ecom.quotes.accepted": {"business_unit": "ecommerce-quote", "cluster": "eventhubs-ecom-quote", "producers": ["quote-approval"], "consumers": ["quote-to-order"]},
    "fulfillment.shipments.scanned": {"business_unit": "fulfillment", "cluster": "pubsub-fulfillment", "producers": ["carrier-webhook"], "consumers": ["tracking-api", "last-mile-router"]},
    "customer.profile.changed": {"business_unit": "customer-profile", "cluster": "msk-customer", "producers": ["profile-api"], "consumers": ["consent-ledger", "shopify-customer-sync"]},
    "support.tickets.opened": {"business_unit": "customer-support", "cluster": "eventhubs-support", "producers": ["ticket-api"], "consumers": ["ticket-router", "sla-watchdog"]},
    "advisor.nba.emitted": {"business_unit": "customer-advisor", "cluster": "eventhubs-advisor", "producers": ["next-best-action"], "consumers": ["advisor-workspace", "opportunity-feed"]},
    "research.signals.ingested": {"business_unit": "product-research", "cluster": "pubsub-research", "producers": ["research-ingest"], "consumers": ["trend-signals", "assortment-planner"]},
    "shopify.webhooks.orders": {"business_unit": "shopify-merchants", "cluster": "msk-shopify-webhooks", "producers": ["shopify-webhook-ingress"], "consumers": ["shopify-order-sync", "shopify-idempotency"]},
    "shopify.webhooks.products": {"business_unit": "shopify-merchants", "cluster": "msk-shopify-webhooks", "producers": ["shopify-webhook-ingress"], "consumers": ["shopify-product-sync"]},
    "shopify.legacy.outbound": {"business_unit": "shopify-merchants", "cluster": "msk-shopify-webhooks", "producers": ["shopify-legacy-bridge"], "consumers": ["shopify-fulfillment-push"]},
}

REDIS_CACHES: dict[str, dict[str, Any]] = {
    "elasticache-forex-quotes": {"business_unit": "forex-markets", "use": "Hot FX books and RFQ cache", "hot_keys": "fx:book:*"},
    "elasticache-forex-risk": {"business_unit": "forex-settlement", "use": "Intraday limits and margin", "hot_keys": "fx:limit:*"},
    "azurecache-ecom-cart": {"business_unit": "ecommerce-retail", "use": "Carts and checkout locks", "hot_keys": "cart:*"},
    "azurecache-ecom-quote": {"business_unit": "ecommerce-quote", "use": "Quote drafts and floor prices", "hot_keys": "quote:*"},
    "memorystore-fulfillment": {"business_unit": "fulfillment", "use": "Allocation locks and rate shop", "hot_keys": "alloc:*"},
    "elasticache-profile-session": {"business_unit": "customer-profile", "use": "Sessions and device risk", "hot_keys": "sess:*"},
    "azurecache-support": {"business_unit": "customer-support", "use": "Ticket macros and SLA clocks", "hot_keys": "sla:*"},
    "azurecache-advisor": {"business_unit": "customer-advisor", "use": "Advisor workspace presence", "hot_keys": "adv:*"},
    "memorystore-research": {"business_unit": "product-research", "use": "Trend signal windows", "hot_keys": "signal:*"},
    "elasticache-shopify-idempotency": {"business_unit": "shopify-merchants", "use": "Webhook HMAC idempotency keys", "hot_keys": "shopify:idemp:*"},
}


def list_databases(inp: dict[str, Any] | None = None) -> str:
    inp = inp or {}
    bu = inp.get("business_unit")
    rows = [ {"name": n, **d} for n, d in DATABASES.items() if not bu or d["business_unit"] == bu ]
    return json.dumps({"count": len(rows), "databases": rows}, indent=2)


def resolve_database(inp: dict[str, Any]) -> str:
    name = inp["instance"]
    if name in DATABASES:
        return json.dumps({"ok": True, "instance": name, **DATABASES[name]}, indent=2)
    svc = SERVICES.get(name)
    if svc:
        matches = [n for n, d in DATABASES.items() if d["business_unit"] == svc["business_unit"]]
        return json.dumps({"ok": True, "service": name, "databases": matches, **svc}, indent=2)
    return json.dumps({"ok": False, "error": f"unknown instance '{name}'"})


def list_kafka_topics(inp: dict[str, Any] | None = None) -> str:
    inp = inp or {}
    bu = inp.get("business_unit")
    rows = [{"topic": t, **meta} for t, meta in KAFKA_TOPICS.items() if not bu or meta["business_unit"] == bu]
    return json.dumps({"count": len(rows), "topics": rows}, indent=2)


def list_redis_caches(inp: dict[str, Any] | None = None) -> str:
    inp = inp or {}
    bu = inp.get("business_unit")
    rows = [{"cache": n, **c} for n, c in REDIS_CACHES.items() if not bu or c["business_unit"] == bu]
    return json.dumps({"count": len(rows), "caches": rows}, indent=2)


CATALOG_DISPATCH = {
    "list_business_units": list_business_units,
    "list_services": list_services,
    "resolve_service": resolve_service,
    "list_databases": list_databases,
    "resolve_database": resolve_database,
    "list_kafka_topics": list_kafka_topics,
    "list_redis_caches": list_redis_caches,
}
