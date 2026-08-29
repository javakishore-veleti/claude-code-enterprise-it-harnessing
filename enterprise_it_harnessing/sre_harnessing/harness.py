#!/usr/bin/env python3
"""SRE production harness. Loop from core; tools, skills, and policy are SRE-specific."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enterprise_it_harnessing.shared.runner import run_harness
from enterprise_it_harnessing.sre_harnessing.tools import DISPATCH, MUTATING, TOOLS

SYSTEM = (
    "You are a production SRE harness operator. "
    "You observe services, contain incidents, and only mutate after policy allows. "
    "Load incident-response or deploy-rollback before acting on a live issue. "
    "Cloud provider is an identity concern; the incident loop stays the same."
)


def main() -> None:
    run_harness(
        name="sre-harness",
        prompt="sre",
        domain_dir=Path(__file__).parent,
        extra_tools=TOOLS,
        extra_dispatch=DISPATCH,
        mutating=MUTATING,
        system=SYSTEM,
    )


if __name__ == "__main__":
    main()
