# How To Use — Kafka / Event Bus

Catalog / playbooks: `./harness-kafka.sh`. Jobs (15, skill + hooks): `./harness-kafka-job.sh` — [HowToUse_Kafka_Jobs.md](HowToUse_Kafka_Jobs.md).

`repl` opens a session. Playbooks print and exit unless you add `--interactive`.

| Command | Output | When to use |
| --- | --- | --- |
| `./harness-kafka.sh` | Command names only | See every Kafka command |
| `./harness-kafka.sh repl` | `kafka >>` prompt | Empty bus session |
| `./harness-kafka.sh identity` | Cloud identity JSON | Same dump, no model |
| `./harness-kafka.sh skills` | topic-lifecycle, consumer-lag | See bus runbooks |
| `./harness-kafka.sh list-units` | BUs → bus names | Which MSK / Event Hubs / Pub/Sub |
| `./harness-kafka.sh list-topics` | All named topics | Estate map |
| `./harness-kafka.sh topics-forex-markets` | `fx.quotes.raw`, `fx.trades.captured`, … | FOREX markets topics |
| `./harness-kafka.sh topics-forex-settlement` | Settlement + risk.breaches | FOREX settlement topics |
| `./harness-kafka.sh topics-ecom-retail` | orders.created, checkout.saga | Retail topics |
| `./harness-kafka.sh topics-ecom-quote` | quotes.accepted | Quote topics |
| `./harness-kafka.sh topics-fulfillment` | shipments.scanned | Fulfillment topics |
| `./harness-kafka.sh topics-customer-profile` | profile.changed | Profile topics |
| `./harness-kafka.sh topics-customer-support` | tickets.opened | Support topics |
| `./harness-kafka.sh topics-customer-advisor` | nba.emitted | Advisor topics |
| `./harness-kafka.sh topics-product-research` | signals.ingested | Research topics |
| `./harness-kafka.sh topics-shopify-merchants` | webhooks.orders / products / legacy | Shopify topics |
| `./harness-kafka.sh describe-fx-trades` | Topic describe `fx.trades.captured` | Trade-capture partitions |
| `./harness-kafka.sh describe-fx-orders` | Topic describe `fx.orders.routed` | Matching input topic |
| `./harness-kafka.sh describe-fx-settlement` | Topic describe settlement instructions | CLS / settlement topic |
| `./harness-kafka.sh describe-checkout-saga` | Topic describe `ecom.checkout.saga` | Checkout bus |
| `./harness-kafka.sh describe-shopify-orders` | Topic describe `shopify.webhooks.orders` | Shopify order webhooks |
| `./harness-kafka.sh describe-shopify-legacy` | Topic describe `shopify.legacy.outbound` | Legacy outbound |
| `./harness-kafka.sh lag-fx-matching` | Consumer lag matching-engine | Matching behind `fx.orders.routed` |
| `./harness-kafka.sh lag-fx-stp` | Consumer lag STP adapter | Bank STP behind trades |
| `./harness-kafka.sh lag-orders-workflow` | Consumer lag orders-workflow | Order state machine behind |
| `./harness-kafka.sh lag-checkout` | Consumer lag payments-adapter (do not rewind) | Checkout lag; no rewind |
| `./harness-kafka.sh lag-shopify-orders` | Consumer lag shopify-order-sync | Shopify orders behind |
| `./harness-kafka.sh lag-shopify-products` | Consumer lag shopify-product-sync | Shopify products behind |
| `./harness-kafka.sh lag-legacy-bridge` | Consumer lag fulfillment-push | Legacy outbound behind |
| `./harness-kafka.sh create-research-topic` | Topic-create proposal (asks for approval) | Research only; FOREX/Shopify denied |
