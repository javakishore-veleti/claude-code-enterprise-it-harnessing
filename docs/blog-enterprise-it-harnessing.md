# Enterprise IT harnessing on a live FOREX, e-commerce, and Shopify estate

~2 minute read.

This blog is about **Enterprise IT harnessing** capabilities.

This post discusses my [GitHub repository](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing) that implements those capabilities.

This blog post considers an Enterprise IT team that supports several product domains, SaaS services (Shopify headless merchants among them), and a mixed tech stack — Kubernetes, event buses, Redis, databases, and search — and still needs **one unified harness** for the support work those roles actually do: observe, diagnose, fail over, roll back, search, and silence.

The domains do not share a single admin shell. They share dedicated cloud accounts, many stacks, and a rule that production changes stay inside a role.

The estate this post uses as the working example:

| Domain | What the business actually does |
| --- | --- |
| FOREX bank middleware | Price, match, FIX, STP, risk limits, netting, CLS, regulatory reporting |
| E-commerce microservices | Catalog, quote, cart, checkout, orders, payments, fulfillment, profile, support, advisor, research |
| Shopify headless merchants | HMAC webhooks, product/order/customer sync, idempotency, SOAP / AS/400 bridge |

- A Redis failover is not an SRE rollback.
- A Kafka ACL change is not a `DROP DATABASE`.
- A Grafana silence is not a namespace delete.
- Harnessing is the layer that makes that split structural.
- One decision loop.
- Six operator surfaces — SRE, Event Bus, Search, Kubernetes, Redis, and DB.
- Each surface has its own tools, runbooks, and `permissions.yaml` (deny / allow / ask).
- Mutating tools take an isolation lease on the target so two agents cannot change the same cluster, topic, or cache at once.

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
