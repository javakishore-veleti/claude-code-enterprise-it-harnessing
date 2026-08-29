# Redis harness — command table

Use this profile for the **ten named caches**. `FLUSHALL` is denied. Failover of FX books, carts, or Shopify idempotency keys has extra drain notes in the tools themselves.

Folder: `enterprise_it_harnessing/redis_harnessing/`  
Launcher: `./harness-redis.sh <command>` from the repo root.

| Cache | Business unit | Hot keys / risk |
| --- | --- | --- |
| `elasticache-forex-quotes` | forex-markets | `fx:book:*` — stale book if failover > 2s |
| `elasticache-forex-risk` | forex-settlement | `fx:limit:*` |
| `azurecache-ecom-cart` | ecommerce-retail | `cart:*` — pause checkout on failover |
| `azurecache-ecom-quote` | ecommerce-quote | `quote:*` |
| `memorystore-fulfillment` | fulfillment | `alloc:*` |
| `elasticache-profile-session` | customer-profile | `sess:*` |
| `azurecache-support` | customer-support | `sla:*` |
| `azurecache-advisor` | customer-advisor | `adv:*` |
| `memorystore-research` | product-research | `signal:*` |
| `elasticache-shopify-idempotency` | shopify-merchants | `shopify:idemp:*` — freeze webhook-ingress before failover |

| Command | What it does |
| --- | --- |
| `./harness-redis.sh` | List every Redis npm script |
| `./harness-redis.sh repl` | Interactive Redis-admin session |
| `./harness-redis.sh identity` | Cloud principal (`--tool`) |
| `./harness-redis.sh skills` | replication, eviction |
| `./harness-redis.sh list-units` | BUs → cache names |
| `./harness-redis.sh list-caches` | All 10 named caches |
| `./harness-redis.sh caches-forex-markets` | FOREX quote cache |
| `./harness-redis.sh caches-shopify` | Shopify idempotency cache |
| `./harness-redis.sh info-fx-quotes` | INFO replication on FX books |
| `./harness-redis.sh info-fx-risk` | INFO memory on limits cache |
| `./harness-redis.sh info-ecom-cart` | INFO memory on carts |
| `./harness-redis.sh info-ecom-quote` | INFO on quote cache |
| `./harness-redis.sh info-fulfillment` | INFO clients on allocation locks |
| `./harness-redis.sh info-profile-session` | INFO clients on sessions |
| `./harness-redis.sh info-support` | INFO on SLA clocks |
| `./harness-redis.sh info-advisor` | INFO on advisor presence |
| `./harness-redis.sh info-research` | INFO on trend windows |
| `./harness-redis.sh info-shopify-idemp` | INFO on webhook idempotency keys |
| `./harness-redis.sh slowlog-fx-quotes` | SLOWLOG on FX books |
| `./harness-redis.sh slowlog-ecom-cart` | SLOWLOG on carts |
| `./harness-redis.sh slowlog-shopify-idemp` | SLOWLOG on Shopify keys |
| `./harness-redis.sh describe-fx-quotes` | ElastiCache describe FX quotes |
| `./harness-redis.sh describe-ecom-cart` | Azure Cache describe carts |
| `./harness-redis.sh describe-fulfillment` | Memorystore describe fulfillment |
| `./harness-redis.sh describe-shopify-idemp` | ElastiCache describe Shopify keys |
| `./harness-redis.sh memory-fx-quotes` | Eviction runbook on FX books |
| `./harness-redis.sh memory-ecom-cart` | Eviction runbook on carts |
| `./harness-redis.sh replication-fx-quotes` | Replica lag on FX books |
| `./harness-redis.sh failover-fx-quotes` | Propose FX-book failover (approval) |
| `./harness-redis.sh failover-shopify-idemp` | Propose Shopify key failover (approval) |
| `./harness-redis.sh failover-ecom-cart` | Propose cart failover (approval) |
