#!/usr/bin/env python3
"""Kafka / MSK / Event Hubs / Pub/Sub admin harness."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enterprise_it_harnessing.kafka_harnessing.tools import DISPATCH, MUTATING, TOOLS
from enterprise_it_harnessing.shared.runner import run_harness

SYSTEM = (
    "You are the streaming harness for named topics: fx.trades.captured, fx.orders.routed, "
    "ecom.checkout.saga, shopify.webhooks.orders, shopify.legacy.outbound, and the rest of the catalog. "
    "Each BU owns its bus (MSK, Event Hubs, or Pub/Sub). "
    "FOREX and Shopify topic creates are denied in this profile. Topic delete is always denied."
)


def main() -> None:
    run_harness(
        name="kafka-harness",
        prompt="kafka",
        domain_dir=Path(__file__).parent,
        extra_tools=TOOLS,
        extra_dispatch=DISPATCH,
        mutating=MUTATING,
        system=SYSTEM,
    )


if __name__ == "__main__":
    main()
