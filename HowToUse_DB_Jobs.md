# How To Use — DB jobs

`./harness-db-job.sh` is the **job** launcher. `./harness-db.sh` stays the catalog / playbook launcher. Existing commands are unchanged.

Each job injects its skill into Claude (`--with-skill`). Hooks stay in that role’s `permissions.yaml` (deny / allow / ask).
Answers use **Input / What it is doing / What it found / Final output** (bullets + Summary). Token cost is printed from `model_costs.json`.

| Command | Job (what Claude follows) | When to use |
| --- | --- | --- |
| `./harness-db-job.sh` | Lists the 15 jobs | See every job |
| `./harness-db-job.sh trades-replica-lag` | FOREX trades replica lag | rds-fx-trades-prod lag > 5s Sev2 |
| `./harness-db-job.sh risk-failover-pause-cls` | Risk DB failover after CLS pause | rds-fx-risk-prod emergency |
| `./harness-db-job.sh orders-snapshot-checkout` | Orders snapshot before checkout deploy | azsql-orders-prod pre-release |
| `./harness-db-job.sh shopify-sync-drain` | Shopify sync DB drain + failover | rds-shopify-sync-prod |
| `./harness-db-job.sh consent-ledger-check` | Consent ledger integrity | rds-profile-prod consent writes |
| `./harness-db-job.sh quotes-blocking` | B2B quotes blocking sessions | azsql-quotes-prod locks |
| `./harness-db-job.sh fulfillment-slow-query` | Fulfillment Cloud SQL slow query | cloudsql-fulfillment-prod |
| `./harness-db-job.sh advisor-pii-access` | Advisor notes PII access check | azsql-advisor-prod |
| `./harness-db-job.sh support-ticket-db-lag` | Support tickets replica lag | azsql-support-prod |
| `./harness-db-job.sh research-restore-lab` | Research DB restore (lab) | cloudsql-research-prod only |
| `./harness-db-job.sh profile-backup-verify` | Profile / consent backup verify | rds-profile-prod snapshots |
| `./harness-db-job.sh trades-pre-fix-snapshot` | Trades snapshot before FIX release | rds-fx-trades-prod pre-FIX |
| `./harness-db-job.sh orders-failover` | Orders DB failover | azsql-orders-prod |
| `./harness-db-job.sh shopify-inbox-bloat` | Shopify webhook inbox bloat | rds-shopify-sync-prod growth |
| `./harness-db-job.sh netting-lock` | FOREX netting lock / risk DB | rds-fx-risk-prod netting |

