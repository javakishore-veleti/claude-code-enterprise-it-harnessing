# How To Use — Redis jobs

`./harness-redis-job.sh` is the **job** launcher. `./harness-redis.sh` stays the catalog / playbook launcher. Existing commands are unchanged.

Each job injects its skill into Claude (`--with-skill`). Hooks stay in that role’s `permissions.yaml` (deny / allow / ask).

| Command | Job (what Claude follows) | When to use |
| --- | --- | --- |
| `./harness-redis-job.sh` | Lists the 15 jobs | See every job |
| `./harness-redis-job.sh fx-book-lag` | FX book replica lag | elasticache-forex-quotes fx:book:* |
| `./harness-redis-job.sh fx-book-failover` | FX book failover | promote FX quotes cache |
| `./harness-redis-job.sh cart-eviction` | Cart eviction storm | azurecache-ecom-cart cart:* |
| `./harness-redis-job.sh cart-failover-pause` | Cart failover after checkout pause | azurecache-ecom-cart |
| `./harness-redis-job.sh shopify-idemp-freeze` | Freeze Shopify idemp before failover | shopify:idemp:* |
| `./harness-redis-job.sh shopify-idemp-failover` | Shopify idempotency failover | elasticache-shopify-idempotency |
| `./harness-redis-job.sh risk-limits-memory` | FX risk limits memory | elasticache-forex-risk fx:limit:* |
| `./harness-redis-job.sh quote-cache-hot` | B2B quote cache hot keys | azurecache-ecom-quote quote:* |
| `./harness-redis-job.sh fulfillment-lock-pileup` | Fulfillment alloc lock pile-up | memorystore-fulfillment alloc:* |
| `./harness-redis-job.sh session-clients` | Profile session client pile-up | elasticache-profile-session sess:* |
| `./harness-redis-job.sh support-sla-clock` | Support SLA clock cache | azurecache-support sla:* |
| `./harness-redis-job.sh advisor-presence` | Advisor presence cache | azurecache-advisor adv:* |
| `./harness-redis-job.sh slowlog-fx` | SLOWLOG FX books | slow FX Redis commands |
| `./harness-redis-job.sh slowlog-cart` | SLOWLOG carts | slow cart commands |
| `./harness-redis-job.sh slowlog-idemp` | SLOWLOG Shopify idemp | slow idempotency commands |

