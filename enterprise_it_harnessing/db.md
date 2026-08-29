# DB admin harness — command table

Use this profile for the **ten named production databases** (one primary per business unit). Engines differ (Aurora, Azure SQL, Cloud SQL); the loop does not: describe → backups → snapshot → lag → failover.

Folder: `enterprise_it_harnessing/db_admin_harnessing/`  
Launcher: `./harness-db.sh <command>` from the repo root. Append `--interactive` on a playbook to keep that session open.

| Instance | Business unit | Engine | Owner services |
| --- | --- | --- | --- |
| `rds-fx-trades-prod` | forex-markets | Aurora PostgreSQL | trade-capture, FIX, audit |
| `rds-fx-risk-prod` | forex-settlement | Aurora PostgreSQL | limits, CLS, regulatory |
| `azsql-orders-prod` | ecommerce-retail | Azure SQL | orders, checkout, payments |
| `azsql-quotes-prod` | ecommerce-quote | Azure SQL | quotes, contracts |
| `cloudsql-fulfillment-prod` | fulfillment | Cloud SQL | allocation, WMS, tracking |
| `rds-profile-prod` | customer-profile | Aurora PostgreSQL | identity, consent, loyalty |
| `azsql-support-prod` | customer-support | Azure SQL | tickets, SLA |
| `azsql-advisor-prod` | customer-advisor | Azure SQL | notes, compliance |
| `cloudsql-research-prod` | product-research | Cloud SQL | assortment, drafts |
| `rds-shopify-sync-prod` | shopify-merchants | Aurora PostgreSQL | webhook inbox, legacy map |

| Command | What it does |
| --- | --- |
| `./harness-db.sh` | List every DBA npm script |
| `./harness-db.sh repl --interactive` | Empty DBA session |
| `./harness-db.sh identity` | Cloud principal (`--tool`) |
| `./harness-db.sh skills` | backup-restore, failover |
| `./harness-db.sh list-units` | 10 BUs and accounts |
| `./harness-db.sh list-databases` | All 10 named instances |
| `./harness-db.sh list-forex-dbs` | FOREX markets databases |
| `./harness-db.sh list-shopify-dbs` | Shopify sync database |
| `./harness-db.sh resolve-fx-trades` | Catalog row for `rds-fx-trades-prod` |
| `./harness-db.sh resolve-orders` | Catalog row for `azsql-orders-prod` |
| `./harness-db.sh resolve-shopify-sync` | Catalog row for `rds-shopify-sync-prod` |
| `./harness-db.sh describe-fx-trades` | Describe FOREX trade DB |
| `./harness-db.sh describe-fx-risk` | Describe risk / CLS DB |
| `./harness-db.sh describe-orders` | Describe orders / checkout DB |
| `./harness-db.sh describe-quotes` | Describe B2B quote DB |
| `./harness-db.sh describe-fulfillment` | Describe fulfillment Cloud SQL |
| `./harness-db.sh describe-profile` | Describe profile / consent DB |
| `./harness-db.sh describe-support` | Describe support tickets DB |
| `./harness-db.sh describe-advisor` | Describe advisor compliance DB |
| `./harness-db.sh describe-research` | Describe research Cloud SQL |
| `./harness-db.sh describe-shopify-sync` | Describe Shopify webhook inbox DB |
| `./harness-db.sh backups-fx-trades` | List FOREX trade snapshots |
| `./harness-db.sh backups-orders` | List orders snapshots |
| `./harness-db.sh backups-shopify-sync` | List Shopify sync snapshots |
| `./harness-db.sh replication-fx-trades` | Replica lag (Sev2 if > 5s) |
| `./harness-db.sh replication-orders` | Replica lag on orders |
| `./harness-db.sh snapshot-fx-trades` | Propose snapshot before FIX release (approval) |
| `./harness-db.sh snapshot-orders` | Propose snapshot before checkout deploy (approval) |
| `./harness-db.sh failover-fx-risk` | Propose risk-DB failover; pause CLS first (approval) |
| `./harness-db.sh failover-shopify-sync` | Propose sync-DB failover; drain webhooks first (approval) |

`DROP` / `TRUNCATE` / instance delete are denied in `permissions.yaml`.
