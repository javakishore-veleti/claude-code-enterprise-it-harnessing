---
name: lag-shopify-orders
description: Shopify order webhook lag
---

HMAC path lag → retry pile-up.
1. consumer_lag
2. Check shopify-idempotency Redis.
