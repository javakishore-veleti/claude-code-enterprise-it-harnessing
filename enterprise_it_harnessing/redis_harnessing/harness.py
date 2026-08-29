#!/usr/bin/env python3
"""Redis admin production harness."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enterprise_it_harnessing.redis_harnessing.tools import DISPATCH, MUTATING, TOOLS
from enterprise_it_harnessing.shared.runner import run_harness

SYSTEM = (
    "You are the Redis harness for named caches: elasticache-forex-quotes, elasticache-forex-risk, "
    "azurecache-ecom-cart, elasticache-shopify-idempotency, and the other BU caches in the catalog. "
    "FLUSHALL is denied. Failover of FX books, carts, or Shopify idempotency keys has extra drain notes."
)


def main() -> None:
    run_harness(
        name="redis-harness",
        prompt="redis",
        domain_dir=Path(__file__).parent,
        extra_tools=TOOLS,
        extra_dispatch=DISPATCH,
        mutating=MUTATING,
        system=SYSTEM,
    )


if __name__ == "__main__":
    main()
