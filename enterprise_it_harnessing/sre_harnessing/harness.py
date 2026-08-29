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
    "You are the SRE harness for a 10-BU estate: FOREX bank trade-processing, "
    "e-commerce catalog/quote/orders/fulfillment, customer profile/support/advisor, "
    "product research, and Shopify headless merchant webhooks plus legacy/on-prem sync. "
    "Resolve the microservice first. FOREX matching-engine and Shopify HMAC ingress are Sev2 by default. "
    "Load incident-response or deploy-rollback before mutating. Cloud only changes identity and CLI argv."
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
