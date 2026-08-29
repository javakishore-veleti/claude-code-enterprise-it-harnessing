# How To Use — Kafka / Event Bus jobs

`./harness-kafka-job.sh` is the **job** launcher. `./harness-kafka.sh` stays the catalog / playbook launcher. Existing commands are unchanged.

Each job injects its skill into Claude (`--with-skill`). Hooks stay in that role’s `permissions.yaml` (deny / allow / ask).
Answers use **Input / What it is doing / What it found / Final output** unless you ask for another format.

| Command | Job (what Claude follows) | When to use |
| --- | --- | --- |
| `./harness-kafka-job.sh` | Lists the 15 jobs | See every job |
| `./harness-kafka-job.sh lag-matching` | Matching-engine consumer lag | fx.orders.routed / fx-matching-engine |
| `./harness-kafka-job.sh lag-stp` | Bank STP consumer lag | fx.trades.captured / fx-stp-adapter |
| `./harness-kafka-job.sh lag-checkout-no-rewind` | Checkout saga lag — no rewind | ecom.checkout.saga / payments-adapter |
| `./harness-kafka-job.sh lag-shopify-orders` | Shopify order webhook lag | shopify.webhooks.orders |
| `./harness-kafka-job.sh lag-shopify-products` | Shopify product webhook lag | shopify.webhooks.products |
| `./harness-kafka-job.sh lag-legacy-outbound` | Legacy outbound lag | shopify.legacy.outbound |
| `./harness-kafka-job.sh describe-fx-trades` | Describe fx.trades.captured | under-replicated FOREX trades |
| `./harness-kafka-job.sh describe-checkout-saga` | Describe checkout saga topic | ecom.checkout.saga |
| `./harness-kafka-job.sh ur-partitions-forex` | Under-replicated FOREX partitions | MSK forex-markets URPs |
| `./harness-kafka-job.sh poison-shopify-hmac` | Poison HMAC / order webhook | bad record on shopify.webhooks.orders |
| `./harness-kafka-job.sh create-research-topic` | Create research lab topic | research.samples.lab only |
| `./harness-kafka-job.sh lag-orders-workflow` | Orders workflow lag | ecom.orders.created |
| `./harness-kafka-job.sh describe-settlement` | Describe settlement instructions | fx.settlement.instructions |
| `./harness-kafka-job.sh lag-fx-orders` | Describe + lag fx.orders.routed | matching input topic health |
| `./harness-kafka-job.sh shopify-retry-pileup` | Shopify retry pile-up on the bus | ingress retries + lag |

