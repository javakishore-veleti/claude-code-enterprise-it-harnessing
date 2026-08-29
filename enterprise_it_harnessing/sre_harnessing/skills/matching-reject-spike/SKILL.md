---
name: matching-reject-spike
description: FOREX matching reject spike
---

Sev2. Bound to forex-markets / eks-forex-markets-prod.
1. resolve_service fx-matching-engine
2. observe_health
3. fetch_logs
4. Contain. page_oncall and rollback_deploy need approval.
Do not page CLS. Do not touch shopify-merchants.
