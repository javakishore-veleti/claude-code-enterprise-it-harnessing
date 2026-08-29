---
name: elasticsearch-query
description: Query FOREX, e-commerce, customer, and Shopify Elasticsearch stacks without dumping the index.
---

1. Call `list_business_units` or `resolve_service` so you know which stack (`es-forex-prod`, `es-ecom-prod`, `es-customer-prod`, `es-shopify-prod`).
2. Prefer aliases over raw index names:
   - `forex-trades` / `forex-fix` for bank trade processing
   - `orders` / `shipping` for retail and fulfillment
   - `support` for tickets
   - `shopify-webhooks` / `shopify-legacy` for merchant HMAC intake and on-prem bridge
3. Keep `size` at 20 or below. Return a count, a few example ids, and the first error message — not the hit array.
4. HMAC failures on `shopify-webhook-ingress` and reject codes on `fx-matching-engine` are Sev2 until proven otherwise.
