# ELK + Grafana harness — command table

Use this profile for **Elasticsearch stacks and Grafana folders** that sit beside the 10 business units. Indices are not generic `logs-*`; they are FOREX trades/FIX, orders/shipping, support tickets, and Shopify HMAC / legacy.

Folder: `enterprise_it_harnessing/elk_harnessing/`  
Launcher: `./harness-elk.sh <command>` from the repo root.

Set `ELASTICSEARCH_URL` and `GRAFANA_URL` when talking to a real stack. `--tool` catalog commands work without them.

| Stack | Business units | Grafana folder |
| --- | --- | --- |
| `es-forex-prod` | forex-markets, forex-settlement | `grafana-forex-prod` |
| `es-ecom-prod` | ecommerce-retail, ecommerce-quote, fulfillment, product-research | `grafana-ecom-prod` |
| `es-customer-prod` | customer-profile, customer-support, customer-advisor | `grafana-customer-prod` |
| `es-shopify-prod` | shopify-merchants | `grafana-shopify-prod` |

| Alias | Backing index pattern | Use |
| --- | --- | --- |
| `forex-trades` | `forex-trade-processing-fx-trade-capture-*` | Bank trade capture |
| `forex-fix` | `forex-trade-processing-fx-fix-gateway-*` | FIX session drops |
| `orders` | `ecommerce-middleware-orders-api-*` | Checkout / order saga |
| `shipping` | `ecommerce-middleware-tracking-api-*` | Carrier / tracking |
| `support` | `customer-ticket-api-*` | SLA / tickets |
| `shopify-webhooks` | `shopify-headless-shopify-webhook-ingress-*` | HMAC failures |
| `shopify-legacy` | `shopify-headless-shopify-legacy-bridge-*` | SOAP / AS/400 |

| Command | What it does |
| --- | --- |
| `./harness-elk.sh` | List every ELK/Grafana npm script |
| `./harness-elk.sh repl` | Interactive observability session |
| `./harness-elk.sh identity` | Cloud principal (`--tool`) |
| `./harness-elk.sh skills` | elasticsearch-query, grafana-alerts |
| `./harness-elk.sh list-units` | BUs → ES / Grafana names |
| `./harness-elk.sh list-forex-markets` | FOREX services (for index pick) |
| `./harness-elk.sh list-shopify-merchants` | Shopify services |
| `./harness-elk.sh es-health-forex` | Cluster health `es-forex-prod` |
| `./harness-elk.sh es-health-ecom` | Cluster health `es-ecom-prod` |
| `./harness-elk.sh es-health-customer` | Cluster health `es-customer-prod` |
| `./harness-elk.sh es-health-shopify` | Cluster health `es-shopify-prod` |
| `./harness-elk.sh search-forex-trades` | Search trade-capture errors |
| `./harness-elk.sh search-forex-fix` | Search FIX disconnects |
| `./harness-elk.sh search-fx-matching` | Search matching-engine rejects |
| `./harness-elk.sh search-orders` | Search `saga_failed` |
| `./harness-elk.sh search-shipping` | Search carrier timeouts |
| `./harness-elk.sh search-support` | Search SLA breaches |
| `./harness-elk.sh search-shopify-webhooks` | Search `hmac_failed` |
| `./harness-elk.sh search-shopify-legacy` | Search SOAP / AS/400 |
| `./harness-elk.sh dashboards-forex` | Grafana folder FOREX |
| `./harness-elk.sh dashboards-ecom` | Grafana folder e-com |
| `./harness-elk.sh dashboards-fulfillment` | Grafana folder fulfillment (shared e-com) |
| `./harness-elk.sh dashboards-customer` | Grafana folder customer |
| `./harness-elk.sh dashboards-shopify` | Grafana folder Shopify |
| `./harness-elk.sh alerts-forex` | List FOREX alert rules |
| `./harness-elk.sh alerts-ecom` | List e-com alert rules |
| `./harness-elk.sh alerts-shopify` | List Shopify alerts (keep HMAC firing) |
| `./harness-elk.sh silence-orders-noise` | Propose silence (approval; never HMAC / matching-engine) |
| `./harness-elk.sh pipeline-shopify` | Ingest lag / HMAC pipeline check |
| `./harness-elk.sh pipeline-forex` | Trade-capture pipeline into `es-forex-prod` |
