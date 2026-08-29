---
name: legacy-as400-timeout
description: Shopify AS/400 / SOAP timeout
---

On-prem SOAP / AS400. shopify-merchants only.
1. resolve shopify-legacy-bridge
2. observe_health, fetch_logs soap/as400
3. Do not FLUSHALL idempotency Redis.
