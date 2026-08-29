# How To Use — Redis

`--interactive` is optional. Omit it to print and exit.

| Command | Output | When to use |
| --- | --- | --- |
| `./harness-redis.sh` | npm script list | See every Redis command |
| `./harness-redis.sh repl` | Cloud identity JSON | Confirm who you are; no session |
| `./harness-redis.sh repl --interactive` | `redis >>` prompt | Empty Redis session |
| `./harness-redis.sh identity` | Cloud identity JSON | Same dump, no model |
| `./harness-redis.sh skills` | replication, eviction | See Redis runbooks |
| `./harness-redis.sh list-units` | BUs → cache names | Which cache |
| `./harness-redis.sh list-caches` | All 10 named caches | Estate map |
| `./harness-redis.sh caches-forex-markets` | FOREX quote cache | FX books cache |
| `./harness-redis.sh caches-shopify` | Shopify idempotency cache | HMAC idempotency keys |
| `./harness-redis.sh info-fx-quotes` | INFO replication on FX books | Stale book / lag |
| `./harness-redis.sh info-fx-risk` | INFO memory on limits cache | Limits pressure |
| `./harness-redis.sh info-ecom-cart` | INFO memory on carts | Cart eviction |
| `./harness-redis.sh info-ecom-quote` | INFO on quote cache | Quote cache health |
| `./harness-redis.sh info-fulfillment` | INFO clients on allocation locks | Lock pile-up |
| `./harness-redis.sh info-profile-session` | INFO clients on sessions | Session pile-up |
| `./harness-redis.sh info-support` | INFO on SLA clocks | Support cache |
| `./harness-redis.sh info-advisor` | INFO on advisor presence | Advisor cache |
| `./harness-redis.sh info-research` | INFO on trend windows | Research cache |
| `./harness-redis.sh info-shopify-idemp` | INFO on `shopify:idemp:*` | Duplicate webhooks |
| `./harness-redis.sh slowlog-fx-quotes` | SLOWLOG on FX books | Slow FX commands |
| `./harness-redis.sh slowlog-ecom-cart` | SLOWLOG on carts | Slow cart commands |
| `./harness-redis.sh slowlog-shopify-idemp` | SLOWLOG on Shopify keys | Slow idempotency |
| `./harness-redis.sh describe-fx-quotes` | ElastiCache describe | Cloud-side FX cache |
| `./harness-redis.sh describe-ecom-cart` | Azure Cache describe | Cloud-side cart cache |
| `./harness-redis.sh describe-fulfillment` | Memorystore describe | Cloud-side fulfillment cache |
| `./harness-redis.sh describe-shopify-idemp` | ElastiCache describe | Cloud-side Shopify keys |
| `./harness-redis.sh memory-fx-quotes` | Eviction runbook on FX books | FX memory pressure |
| `./harness-redis.sh memory-ecom-cart` | Eviction runbook on carts | Cart eviction; pause checkout |
| `./harness-redis.sh replication-fx-quotes` | Replica lag on FX books | FX replica lag |
| `./harness-redis.sh failover-fx-quotes` | Failover proposal (asks for approval) | FX books emergency |
| `./harness-redis.sh failover-shopify-idemp` | Failover proposal; freeze ingress first | Shopify keys emergency |
| `./harness-redis.sh failover-ecom-cart` | Failover proposal; pause checkout first | Cart emergency |
