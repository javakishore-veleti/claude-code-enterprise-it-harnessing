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
    "You are the DBA harness for named production databases: "
    "rds-fx-trades-prod, rds-fx-risk-prod, azsql-orders-prod, azsql-quotes-prod, "
    "cloudsql-fulfillment-prod, rds-profile-prod, azsql-support-prod, azsql-advisor-prod, "
    "cloudsql-research-prod, rds-shopify-sync-prod. "
    "Call list_databases / resolve_database first. Snapshot before failover. "
    "FOREX and Shopify failovers have extra drain notes. DROP/TRUNCATE are denied."
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
