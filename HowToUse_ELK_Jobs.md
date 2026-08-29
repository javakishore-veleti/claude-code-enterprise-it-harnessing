# How To Use — ELK / Search jobs

`./harness-elk-job.sh` is the **job** launcher. `./harness-elk.sh` stays the catalog / playbook launcher. Existing commands are unchanged.

Each job injects its skill into Claude (`--with-skill`). Hooks stay in that role’s `permissions.yaml` (deny / allow / ask).
Answers use **Input / What it is doing / What it found / Final output** (bullets + Summary). Token cost is printed from `model_costs.json`.

| Command | Job (what Claude follows) | When to use |
| --- | --- | --- |
| `./harness-elk-job.sh` | Lists the 15 jobs | See every job |
| `./harness-elk-job.sh search-matching-rejects` | Search matching rejects | fx-matching-engine reject |
| `./harness-elk-job.sh search-fix-disconnect` | Search FIX disconnects | forex-fix disconnect |
| `./harness-elk-job.sh search-hmac-failed` | Search HMAC failures | shopify-webhooks hmac_failed |
| `./harness-elk-job.sh search-saga-failed` | Search checkout saga_failed | orders alias |
| `./harness-elk-job.sh search-as400` | Search SOAP / AS400 | shopify-legacy |
| `./harness-elk-job.sh search-sla-breach` | Search support SLA breach | support alias |
| `./harness-elk-job.sh search-carrier-timeout` | Search carrier timeouts | shipping alias |
| `./harness-elk-job.sh es-health-forex` | ES health FOREX stack | es-forex-prod |
| `./harness-elk-job.sh es-health-shopify` | ES health Shopify stack | es-shopify-prod |
| `./harness-elk-job.sh alerts-forex` | FOREX Grafana alerts | grafana-forex-prod |
| `./harness-elk-job.sh alerts-hmac-keep-firing` | Shopify alerts — keep HMAC firing | HMAC rules must stay firing |
| `./harness-elk-job.sh silence-orders-only` | Silence noisy orders warning only | never matching / HMAC |
| `./harness-elk-job.sh pipeline-forex` | FOREX trade-capture ingest pipeline | forex-trades into es-forex-prod |
| `./harness-elk-job.sh pipeline-shopify` | Shopify HMAC ingest pipeline | events reaching es-shopify-prod |
| `./harness-elk-job.sh dashboards-forex` | FOREX Grafana dashboards | grafana-forex-prod folder |

