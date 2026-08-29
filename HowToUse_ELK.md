# How To Use — ELK / Search

Catalog / playbooks: `./harness-elk.sh`. Jobs (15, skill + hooks): `./harness-elk-job.sh` — [HowToUse_ELK_Jobs.md](HowToUse_ELK_Jobs.md).

`repl` opens a session. Playbooks print and exit unless you add `--interactive`.

| Command | Output | When to use |
| --- | --- | --- |
| `./harness-elk.sh` | npm script list | See every ELK command |
| `./harness-elk.sh repl` | `elk >>` prompt | Empty search session |
| `./harness-elk.sh identity` | Cloud identity JSON | Same dump, no model |
| `./harness-elk.sh skills` | elasticsearch-query, grafana-alerts | See search runbooks |
| `./harness-elk.sh list-units` | BUs → ES / Grafana names | Which stack |
| `./harness-elk.sh list-forex-markets` | FOREX services (index pick) | FOREX index names |
| `./harness-elk.sh list-shopify-merchants` | Shopify services | Shopify index names |
| `./harness-elk.sh es-health-forex` | Cluster health `es-forex-prod` | FOREX ES down / yellow |
| `./harness-elk.sh es-health-ecom` | Cluster health `es-ecom-prod` | E-com ES down / yellow |
| `./harness-elk.sh es-health-customer` | Cluster health `es-customer-prod` | Customer ES down / yellow |
| `./harness-elk.sh es-health-shopify` | Cluster health `es-shopify-prod` | Shopify ES down / yellow |
| `./harness-elk.sh search-forex-trades` | Hits on `forex-trades` (`error`) | Trade-capture errors |
| `./harness-elk.sh search-forex-fix` | Hits on `forex-fix` (`disconnect`) | FIX session drops |
| `./harness-elk.sh search-fx-matching` | Hits for matching-engine (`reject`) | Matching rejects |
| `./harness-elk.sh search-orders` | Hits on `orders` (`saga_failed`) | Checkout saga failed |
| `./harness-elk.sh search-shipping` | Hits on `shipping` (`carrier_timeout`) | Carrier timeouts |
| `./harness-elk.sh search-support` | Hits on `support` (`sla_breach`) | SLA breaches |
| `./harness-elk.sh search-shopify-webhooks` | Hits on `shopify-webhooks` (`hmac_failed`) | HMAC failures |
| `./harness-elk.sh search-shopify-legacy` | Hits on `shopify-legacy` (SOAP / AS400) | Legacy bridge errors |
| `./harness-elk.sh dashboards-forex` | Grafana folder FOREX | Find FOREX dashboards |
| `./harness-elk.sh dashboards-ecom` | Grafana folder e-com | Find e-com dashboards |
| `./harness-elk.sh dashboards-fulfillment` | Grafana folder fulfillment | Find fulfillment dashboards |
| `./harness-elk.sh dashboards-customer` | Grafana folder customer | Find customer dashboards |
| `./harness-elk.sh dashboards-shopify` | Grafana folder Shopify | Find Shopify dashboards |
| `./harness-elk.sh alerts-forex` | FOREX alert rules | Which FOREX alerts fire |
| `./harness-elk.sh alerts-ecom` | E-com alert rules | Which e-com alerts fire |
| `./harness-elk.sh alerts-shopify` | Shopify alerts (keep HMAC firing) | Shopify alert list |
| `./harness-elk.sh silence-orders-noise` | Silence proposal (asks for approval) | Noisy orders warning only |
| `./harness-elk.sh pipeline-shopify` | Ingest / HMAC pipeline check | Events not reaching ES |
| `./harness-elk.sh pipeline-forex` | Trade-capture pipeline into `es-forex-prod` | Trades not reaching ES |
