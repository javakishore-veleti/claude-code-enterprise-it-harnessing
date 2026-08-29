#!/usr/bin/env python3
"""ELK + Grafana harness for FOREX, e-commerce, customer, and Shopify stacks."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enterprise_it_harnessing.elk_harnessing.tools import DISPATCH, MUTATING, TOOLS
from enterprise_it_harnessing.shared.runner import run_harness

SYSTEM = (
    "You are the observability harness operator for Elasticsearch and Grafana. "
    "Stacks are dedicated: es-forex-prod, es-ecom-prod, es-customer-prod, es-shopify-prod. "
    "Use aliases forex-trades, forex-fix, shopify-webhooks, orders, shipping, support. "
    "Never silence fx-matching-engine or Shopify HMAC-failure alerts without a written reason. "
    "Keep es_search_index size small. Load elasticsearch-query or grafana-alerts before acting."
)


def main() -> None:
    run_harness(
        name="elk-harness",
        prompt="elk",
        domain_dir=Path(__file__).parent,
        extra_tools=TOOLS,
        extra_dispatch=DISPATCH,
        mutating=MUTATING,
        system=SYSTEM,
    )


if __name__ == "__main__":
    main()
