# Kafka harness — command table

Use this profile for the **named enterprise topics**. Each BU owns its bus: MSK (FOREX, customer, Shopify), Event Hubs (e-com, support, advisor), Pub/Sub (fulfillment, research).

Folder: `enterprise_it_harnessing/kafka_harnessing/`  
Launcher: `./harness-kafka.sh <command>` from the repo root. Append `--interactive` on a playbook to keep that session open.

FOREX and Shopify **topic creates are denied** in this profile. Topic **delete** is always denied. Checkout-saga rewind is unsafe (double-charge).

| Command | What it does | Topic / group |
| --- | --- | --- |
| `./harness-kafka.sh` | List every Kafka npm script | — |
| `./harness-kafka.sh repl` | Interactive streaming-admin session | all buses |
| `./harness-kafka.sh identity` | Cloud principal (`--tool`) | — |
| `./harness-kafka.sh skills` | topic-lifecycle, consumer-lag | — |
| `./harness-kafka.sh list-units` | BUs → Kafka cluster names | catalog |
| `./harness-kafka.sh list-topics` | All named topics | estate |
| `./harness-kafka.sh topics-forex-markets` | `fx.quotes.raw`, `fx.trades.captured`, … | `msk-forex-markets` |
| `./harness-kafka.sh topics-forex-settlement` | settlement + risk.breaches | `msk-forex-settlement` |
| `./harness-kafka.sh topics-ecom-retail` | orders.created, checkout.saga | `eventhubs-ecom-retail` |
| `./harness-kafka.sh topics-ecom-quote` | quotes.accepted | `eventhubs-ecom-quote` |
| `./harness-kafka.sh topics-fulfillment` | shipments.scanned | `pubsub-fulfillment` |
| `./harness-kafka.sh topics-customer-profile` | profile.changed | `msk-customer` |
| `./harness-kafka.sh topics-customer-support` | tickets.opened | `eventhubs-support` |
| `./harness-kafka.sh topics-customer-advisor` | nba.emitted | `eventhubs-advisor` |
| `./harness-kafka.sh topics-product-research` | signals.ingested | `pubsub-research` |
| `./harness-kafka.sh topics-shopify-merchants` | webhooks.orders / products / legacy | `msk-shopify-webhooks` |
| `./harness-kafka.sh describe-fx-trades` | Describe `fx.trades.captured` | FOREX markets |
| `./harness-kafka.sh describe-fx-orders` | Describe `fx.orders.routed` | matching-engine |
| `./harness-kafka.sh describe-fx-settlement` | Describe settlement instructions | FOREX settlement |
| `./harness-kafka.sh describe-checkout-saga` | Describe checkout saga bus | retail e-com |
| `./harness-kafka.sh describe-shopify-orders` | Describe Shopify order webhooks | Shopify |
| `./harness-kafka.sh describe-shopify-legacy` | Describe legacy outbound | on-prem bridge |
| `./harness-kafka.sh lag-fx-matching` | Lag for matching-engine | `fx.orders.routed` |
| `./harness-kafka.sh lag-fx-stp` | Lag for bank STP | `fx.trades.captured` |
| `./harness-kafka.sh lag-orders-workflow` | Lag for order state machine | `ecom.orders.created` |
| `./harness-kafka.sh lag-checkout` | Lag for payments-adapter (do not rewind) | `ecom.checkout.saga` |
| `./harness-kafka.sh lag-shopify-orders` | Lag for order-sync | `shopify.webhooks.orders` |
| `./harness-kafka.sh lag-shopify-products` | Lag for product-sync | `shopify.webhooks.products` |
| `./harness-kafka.sh lag-legacy-bridge` | Lag for fulfillment push to Shopify | `shopify.legacy.outbound` |
| `./harness-kafka.sh create-research-topic` | Propose a research topic (approval; not FOREX/Shopify) | product-research |
