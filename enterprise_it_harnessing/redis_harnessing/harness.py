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
    "You are a Redis administrator harness. "
    "Prefer redis_info and redis_slowlog. "
    "FLUSHALL is denied. "
    "Self-hosted, ElastiCache, Azure Cache, and Memorystore share the same operational loop."
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
