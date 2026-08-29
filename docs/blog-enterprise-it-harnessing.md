# Enterprise IT Harnessing on a live FOREX, e-commerce, and Shopify estate

~2 minute read.

This blog is about **Enterprise IT Harnessing** capabilities.

<h3 style="color:#2563eb;font-weight:600;margin:1em 0 0.35em">My GitHub repository</h3>

This post discusses my GitHub repo [claude-code-enterprise-it-harnessing](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing) that implements those capabilities.

This blog post considers an Enterprise IT team that supports FOREX back-office trade processing, e-commerce business middleware (quote through order, shipment, and fulfillment), and Shopify as a SaaS integration — on a mixed stack of Kubernetes, buses, Redis, databases, and search — and still needs **one unified harness** for observe, diagnose, fail over, roll back, search, and silence.

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

## Value of Enterprise IT Harnessing

This is the value of the *capability* — one loop, role-scoped surfaces, policy before execution — for an Enterprise IT team that already runs FOREX, e-commerce, and Shopify-style estates. It is not a list of features of one git repository.

### For the operator

- Work stays inside the role: SRE, Event Bus, Search, Kubernetes, Redis, or DB. A cache failover and a deploy rollback are not the same action.
- Support work uses production names the team already knows, not a shared admin shell across every stack.
- Observe, search, and inventory can stay read-only. Mutations that affect customers wait for a person.

### For the incident

- The same matching-engine or checkout-saga name is what health, logs, lag, and rollback all resolve.
- Two people (or two agents) cannot mutate the same cluster, topic, instance, or cache at the same time.
- Irreversible wipes are out of scope for the role. They are not something the model is asked to “be careful” about.

### For the estate

- Ten business units can keep dedicated accounts and clusters. Harnessing does not flatten them into one kubeconfig.
- FOREX, e-commerce, and Shopify stay separate product domains. The harness is shared; the blast radius is not.
- AWS, Azure, and GCP can use the same permission model. Each role still has its own tool list.

### For the organization

- Policy lives next to the tools (deny / allow / ask), not in a runbook paragraph or a system prompt.
- The decision client can change. The surfaces, names, and deny rules do not have to.
- MTTR is repeatable on named SLOs because the path is the same playbook, not a new shell session each time.
