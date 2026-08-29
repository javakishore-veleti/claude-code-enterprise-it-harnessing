# How To Use — DB

`repl` opens a session. Playbooks print and exit unless you add `--interactive`.

| Command | Output | When to use |
| --- | --- | --- |
| `./harness-db.sh` | npm script list | See every DBA command |
| `./harness-db.sh repl` | `db >>` prompt | Empty DBA session |
| `./harness-db.sh identity` | Cloud identity JSON | Same dump, no model |
| `./harness-db.sh skills` | backup-restore, failover | See DBA runbooks |
| `./harness-db.sh list-units` | 10 BUs and accounts | Estate map |
| `./harness-db.sh list-databases` | All 10 named instances | Which DB is which |
| `./harness-db.sh list-forex-dbs` | FOREX trade / risk DBs | FOREX databases |
| `./harness-db.sh list-shopify-dbs` | Shopify sync DB | Shopify database |
| `./harness-db.sh resolve-fx-trades` | Catalog row for `rds-fx-trades-prod` | Before describe / backup |
| `./harness-db.sh resolve-orders` | Catalog row for `azsql-orders-prod` | Before describe / backup |
| `./harness-db.sh resolve-shopify-sync` | Catalog row for `rds-shopify-sync-prod` | Before describe / failover |
| `./harness-db.sh describe-fx-trades` | Instance describe (trade capture / FIX) | FOREX trade DB status |
| `./harness-db.sh describe-fx-risk` | Instance describe (limits / CLS) | Risk DB status |
| `./harness-db.sh describe-orders` | Instance describe (orders / checkout) | Orders DB status |
| `./harness-db.sh describe-quotes` | Instance describe (B2B quotes) | Quote DB status |
| `./harness-db.sh describe-fulfillment` | Instance describe (Cloud SQL) | Fulfillment DB status |
| `./harness-db.sh describe-profile` | Instance describe (consent-ledger) | Profile DB status |
| `./harness-db.sh describe-support` | Instance describe (tickets) | Support DB status |
| `./harness-db.sh describe-advisor` | Instance describe (compliance notes) | Advisor DB status |
| `./harness-db.sh describe-research` | Instance describe (Cloud SQL) | Research DB status |
| `./harness-db.sh describe-shopify-sync` | Instance describe (webhook inbox) | Shopify DB status |
| `./harness-db.sh backups-fx-trades` | Snapshot list for trade DB | Before FIX release |
| `./harness-db.sh backups-orders` | Snapshot list for orders DB | Before checkout deploy |
| `./harness-db.sh backups-shopify-sync` | Snapshot list for sync DB | Before Shopify change |
| `./harness-db.sh replication-fx-trades` | Replica lag (Sev2 if > 5s) | FOREX lag |
| `./harness-db.sh replication-orders` | Replica lag on orders | Orders lag |
| `./harness-db.sh snapshot-fx-trades` | Snapshot proposal (asks for approval) | Before FIX release |
| `./harness-db.sh snapshot-orders` | Snapshot proposal (asks for approval) | Before checkout deploy |
| `./harness-db.sh failover-fx-risk` | Failover proposal; pause CLS first | Risk DB emergency |
| `./harness-db.sh failover-shopify-sync` | Failover proposal; drain webhooks first | Sync DB emergency |
