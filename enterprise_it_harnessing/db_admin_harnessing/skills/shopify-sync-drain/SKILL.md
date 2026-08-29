---
name: shopify-sync-drain
description: Shopify sync DB drain + failover
---

Webhook inbox. Dual-write if you fail over hot.
1. Drain ingress (SRE)
2. list_backups
3. failover after approval.
