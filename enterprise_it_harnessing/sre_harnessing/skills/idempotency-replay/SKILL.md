---
name: idempotency-replay
description: Shopify idempotency replay
---

shopify:idemp:* keys. Replay = dual order write.
1. resolve shopify-idempotency, shopify-webhook-ingress
2. Observe. Freeze ingress before cache failover
3. FLUSHALL is denied.
