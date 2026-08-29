# Enterprise IT harnessing on a live FOREX, e-commerce, and Shopify estate

~2 minute read.

Repo: [github.com/javakishore-veleti/claude-code-enterprise-it-harnessing](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing)

Enterprise IT is not one cluster and one on-call rotation. It is several product domains on dedicated cloud accounts, each with its own Kubernetes, bus, cache, database, and search stack.

The domains this work is built against:

| Domain | What the business actually does |
| --- | --- |
| FOREX bank middleware | Price, match, FIX, STP, risk limits, netting, CLS, regulatory reporting |
| E-commerce microservices | Catalog, quote, cart, checkout, orders, payments, fulfillment, profile, support, advisor, research |
| Shopify headless merchants | HMAC webhooks, product/order/customer sync, idempotency, SOAP / AS/400 bridge |

Those domains do not share an admin shell. They share a constraint: production changes have to stay inside a role. A Redis failover is not an SRE rollback. A Kafka ACL change is not a `DROP DATABASE`. A Grafana silence is not a namespace delete.

**Enterprise IT harnessing** is the layer that makes that constraint structural. One decision loop. Six operator surfaces — SRE, Event Bus, Search, Kubernetes, Redis, and DB. Each surface has its own tools, runbooks, and `permissions.yaml` (deny / allow / ask). Mutating tools take an isolation lease on the target so two agents cannot change the same cluster, topic, or cache at once.

The git repository is that harness. It is not a monorepo of one hundred microservices. Those applications already run in production across ten business units. The harness resolves the names the company already uses — `fx-matching-engine`, `orders-api`, `shopify-webhook-ingress` — and launches from the repo root:

```bash
./harness-sre.sh observe-fx-matching
./harness-db.sh describe-fx-trades
./harness-k8s.sh pods-shopify-merchants
./harness-kafka.sh lag-shopify-orders
./harness-redis.sh info-shopify-idemp
./harness-elk.sh search-shopify-webhooks
```

Catalog dumps (`list-units`, `list-topics`) do not call a model. Playbooks do. Cloud (AWS, Azure, GCP) only changes identity and CLI argv.

The default loop in the repo is Claude. The harness is the product: the catalog, the permission files, the leases, and the six launchers. Those stay if the client is replaced.

Repo, diagrams, and command tables: [claude-code-enterprise-it-harnessing](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing).
