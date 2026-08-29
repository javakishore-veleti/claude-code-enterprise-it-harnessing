#!/usr/bin/env python3
"""Database-admin production harness."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enterprise_it_harnessing.db_admin_harnessing.tools import DISPATCH, MUTATING, TOOLS
from enterprise_it_harnessing.shared.runner import run_harness

SYSTEM = (
    "You are a production database administrator harness. "
    "Describe and list backups before any mutation. "
    "Load backup-restore or failover before those operations. "
    "AWS, Azure, and GCP only change authentication and CLI argv."
)


def main() -> None:
    run_harness(
        name="db-admin-harness",
        prompt="db",
        domain_dir=Path(__file__).parent,
        extra_tools=TOOLS,
        extra_dispatch=DISPATCH,
        mutating=MUTATING,
        system=SYSTEM,
    )


if __name__ == "__main__":
    main()
