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
    "You are a streaming-platform administrator harness. "
    "Prefer typed kafka_* tools. "
    "Topic delete is denied. "
    "Self-hosted Kafka, MSK, Event Hubs, and Pub/Sub share list/describe/lag; only auth and inventory CLIs change."
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
