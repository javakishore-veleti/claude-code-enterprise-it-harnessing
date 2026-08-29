# Enterprise IT harnessing on a live FOREX, e-commerce, and Shopify estate

~2 minute read.

This blog is about **Enterprise IT harnessing** capabilities.

This post discusses my GitHub repository [claude-code-enterprise-it-harnessing](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing) that implements those capabilities.

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

## What users can do

From the repository root, after setting `ANTHROPIC_API_KEY` (and optionally `CLOUD_PROVIDER`):

- Print the command list for a role: `./harness-sre.sh`, `./harness-db.sh`, and the other four launchers.
- Dump the live estate without calling a model: `list-units`, `list-databases`, `list-topics`, `list-caches`, `resolve-*`.
- Open an interactive session for one role: `./harness-sre.sh repl` (same pattern for db, k8s, redis, kafka, elk).
- Run a named playbook against a production name: `observe-fx-matching`, `describe-fx-trades`, `pods-shopify-merchants`, `lag-shopify-orders`, `info-shopify-idemp`, `search-shopify-webhooks`.
- Read that role’s `permissions.yaml` to see what is denied, allowed, or asked before a tool runs.
- Pin AWS, Azure, or GCP; identity and CLI argv change, the tool list does not.
- Add a capability by registering one typed tool and, if it mutates, a deny/ask rule and a lease. No second orchestration graph.

Command tables: [sre](../enterprise_it_harnessing/sre.md) · [db](../enterprise_it_harnessing/db.md) · [k8s](../enterprise_it_harnessing/k8s.md) · [redis](../enterprise_it_harnessing/redis.md) · [kafka](../enterprise_it_harnessing/kafka.md) · [elk](../enterprise_it_harnessing/elk.md). Repo: [claude-code-enterprise-it-harnessing](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing).

## Value of such Enterprise IT harnessing capabilities

- Production names (`fx-matching-engine`) instead of `service-1`. The harness maps an estate that already exists; it does not invent one.
- Six surfaces, one loop. An SRE session cannot issue `FLUSHALL`. A Redis session cannot drain a node.
- Irreversible wipes (`DROP DATABASE`, namespace / PV delete, `FLUSHALL`) are denied in configuration, not left to the model.
- Customer-facing mutations (rollback, failover, ACL, silence) require an operator.
- Two mutating runs cannot take the same cluster, topic, instance, or cache while a lease is held.
- Catalog dumps do not call a model. Playbooks do.
- AWS, Azure, and GCP share the permission engine. They do not share a tool list.
- Deny rules stay in the harness if the decision client is replaced. They do not move into prompt text.
