#!/usr/bin/env python3
"""Kubernetes production harness for on-prem, EKS, AKS, and GKE."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enterprise_it_harnessing.kubernetes_harnessing.tools import DISPATCH, MUTATING, TOOLS
from enterprise_it_harnessing.shared.runner import run_harness

SYSTEM = (
    "You are the Kubernetes harness for ten dedicated clusters "
    "(eks-forex-markets-prod, eks-forex-settlement-prod, aks-ecom-retail-prod, "
    "aks-ecom-quote-prod, gke-fulfillment-prod, eks-customer-profile-prod, "
    "aks-customer-support-prod, aks-customer-advisor-prod, gke-product-research-prod, "
    "eks-shopify-merchants-prod). Namespace equals the business-unit slug. "
    "Pass service= or business_unit= so context is filled. Never delete namespaces."
)


def main() -> None:
    run_harness(
        name="k8s-harness",
        prompt="k8s",
        domain_dir=Path(__file__).parent,
        extra_tools=TOOLS,
        extra_dispatch=DISPATCH,
        mutating=MUTATING,
        system=SYSTEM,
    )


if __name__ == "__main__":
    main()
