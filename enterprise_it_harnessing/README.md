# Enterprise IT Harnessing

Audience diagrams: [SVP strategic](../docs/platform-diagrams.md#strategic-diagram-svp-of-engineering) · [enterprise architecture 100+](../docs/platform-diagrams.md#enterprise-architecture-100-microservices) · [EM / Chief Architect](../docs/platform-diagrams.md#architecture-engineering-manager--chief-architect) · [role-specific](../docs/platform-diagrams.md#role-specific-diagrams)

From the **repository root**: `./harness-sre.sh`, `./harness-db.sh`, `./harness-k8s.sh`, `./harness-redis.sh`, `./harness-kafka.sh`, `./harness-elk.sh`. Examples: `./harness-sre.sh list-units`, `./harness-sre.sh observe-fx-matching`. Full run book: [root README — How to launch](../README.md#how-to-launch-from-the-repository-root).

This package is the operator surface for a **single enterprise** that runs about **100 microservices** across **10 business units**. Each unit owns a dedicated cloud account and its own Kubernetes, Kafka/Event Hubs/Pub/Sub, Redis, Elasticsearch, and Grafana stack.

The model does not change. Each profile (`sre_harnessing`, `db_admin_harnessing`, `kubernetes_harnessing`, `redis_harnessing`, `kafka_harnessing`, `elk_harnessing`) swaps **tools**, **skills**, **permissions**, and **named catalog resources**. Cloud (AWS, Azure, GCP) only changes identity and CLI argv.

Do not treat these profiles as generic admin toys. Tools resolve `fx-matching-engine`, `shopify-webhook-ingress`, `rds-fx-trades-prod`, `ecom.checkout.saga`, and `elasticache-shopify-idempotency` — not abstract “service-1”.

## The estate

Three product domains share the same harnessing folders:

| Domain | What it is | Typical services |
| --- | --- | --- |
| **FOREX trade-processing middleware (banks)** | Price, match, route, capture, FIX, STP, then risk / netting / CLS / regulatory | `fx-matching-engine`, `fx-fix-gateway`, `fx-cls-adapter`, `fx-regulatory-report` |
| **E-commerce middleware (microservices)** | Product catalog, quote, orders, shipping, fulfillment, customer profile, support, advisor, product research | `catalog-api`, `quote-api`, `orders-api`, `checkout-orchestrator`, `tracking-api`, `ticket-api`, `advisor-workspace` |
| **Shopify headless merchants** | Shopify data into legacy and on-prem systems; HMAC webhooks; idempotency; SOAP / AS/400 bridge | `shopify-webhook-ingress`, `shopify-order-sync`, `shopify-legacy-bridge`, `shopify-idempotency` |

### Ten business units (dedicated accounts and clusters)

| Slug | Cloud account | Kubernetes | Bus | Redis | ELK / Grafana |
| --- | --- | --- | --- | --- | --- |
| `forex-markets` | `aws-forex-markets-prod` | `eks-forex-markets-prod` | `msk-forex-markets` | `elasticache-forex-quotes` | `es-forex-prod` / `grafana-forex-prod` |
| `forex-settlement` | `aws-forex-settlement-prod` | `eks-forex-settlement-prod` | `msk-forex-settlement` | `elasticache-forex-risk` | `es-forex-prod` / `grafana-forex-prod` |
| `ecommerce-retail` | `az-ecom-retail-prod` | `aks-ecom-retail-prod` | `eventhubs-ecom-retail` | `azurecache-ecom-cart` | `es-ecom-prod` / `grafana-ecom-prod` |
| `ecommerce-quote` | `az-ecom-quote-prod` | `aks-ecom-quote-prod` | `eventhubs-ecom-quote` | `azurecache-ecom-quote` | `es-ecom-prod` / `grafana-ecom-prod` |
| `fulfillment` | `gcp-fulfillment-prod` | `gke-fulfillment-prod` | `pubsub-fulfillment` | `memorystore-fulfillment` | `es-ecom-prod` / `grafana-ecom-prod` |
| `customer-profile` | `aws-customer-profile-prod` | `eks-customer-profile-prod` | `msk-customer` | `elasticache-profile-session` | `es-customer-prod` / `grafana-customer-prod` |
| `customer-support` | `az-customer-support-prod` | `aks-customer-support-prod` | `eventhubs-support` | `azurecache-support` | `es-customer-prod` / `grafana-customer-prod` |
| `customer-advisor` | `az-customer-advisor-prod` | `aks-customer-advisor-prod` | `eventhubs-advisor` | `azurecache-advisor` | `es-customer-prod` / `grafana-customer-prod` |
| `product-research` | `gcp-product-research-prod` | `gke-product-research-prod` | `pubsub-research` | `memorystore-research` | `es-ecom-prod` / `grafana-ecom-prod` |
| `shopify-merchants` | `aws-shopify-merchants-prod` | `eks-shopify-merchants-prod` | `msk-shopify-webhooks` | `elasticache-shopify-idempotency` | `es-shopify-prod` / `grafana-shopify-prod` |

The catalog lives in `catalog.py` (~10 services per unit). Call `list_business_units`, `list_services`, or `resolve_service` before guessing an account or cluster.

## How to launch

Each profile has its **own `package.json`** (25+ named commands). A **root `.sh`** in this repo forwards to that file.

```bash
export ANTHROPIC_API_KEY=...
# optional: pin identity; otherwise auto-detect
export CLOUD_PROVIDER=aws   # or azure or gcp

./harness-sre.sh                 # list SRE commands
./harness-sre.sh repl            # interactive SRE session
./harness-sre.sh observe-fx-matching

./harness-db.sh describe-fx-trades
./harness-k8s.sh pods-shopify-merchants
./harness-kafka.sh lag-shopify-orders
./harness-redis.sh info-shopify-idemp
./harness-elk.sh search-shopify-webhooks
```

Catalog dumps (`list-units`, `list-topics`, `resolve-*`) use `--tool` and do **not** call the model. Playbooks (`observe-*`, `incident-*`, `failover-*`) use `--once` and do.

Same thing via npm at the repo root:

```bash
npm run harness:sre -- observe-fx-matching
npm run harness:elk -- search-forex-trades
```

Or from this folder:

```bash
npm run sre -- list-units
npm run elk -- repl
```

## Profile docs (command tables)

| Profile | Folder | Root launcher | Command table |
| --- | --- | --- | --- |
| SRE | [`sre_harnessing/`](sre_harnessing/) | [`../harness-sre.sh`](../harness-sre.sh) | [sre.md](sre.md) |
| DB admin | [`db_admin_harnessing/`](db_admin_harnessing/) | [`../harness-db.sh`](../harness-db.sh) | [db.md](db.md) |
| Kubernetes | [`kubernetes_harnessing/`](kubernetes_harnessing/) | [`../harness-k8s.sh`](../harness-k8s.sh) | [k8s.md](k8s.md) |
| Redis | [`redis_harnessing/`](redis_harnessing/) | [`../harness-redis.sh`](../harness-redis.sh) | [redis.md](redis.md) |
| Kafka | [`kafka_harnessing/`](kafka_harnessing/) | [`../harness-kafka.sh`](../harness-kafka.sh) | [kafka.md](kafka.md) |
| ELK + Grafana | [`elk_harnessing/`](elk_harnessing/) | [`../harness-elk.sh`](../harness-elk.sh) | [elk.md](elk.md) |

Leases live under `.harness_isolation/` (gitignored). Mutations on a dirty or already-leased target fail closed.

## How to extend a profile

`./harness-sre.sh observe-fx-matching` means: run the **npm script** named `observe-fx-matching` in `sre_harnessing/package.json`. The same pattern applies to db, k8s, redis, kafka, and elk. That script name is not a second command — it is the playbook. Root launchers already forward; you do not add another `.sh` per playbook.

To add a capability to an existing role (example: SRE):

1. **Tool** — implement a function in `sre_harnessing/tools.py`, add its schema to `TOOLS` and the function to `DISPATCH`. If it mutates, add the name to `MUTATING`.
2. **Policy** — add a deny / allow / ask pattern in `sre_harnessing/permissions.yaml`. Do not put deny rules in the system prompt.
3. **Skill** (optional) — add `sre_harnessing/skills/<name>/SKILL.md` if the model needs a runbook.
4. **Playbook** — add a script in `sre_harnessing/package.json` that calls `../../run.sh enterprise_it_harnessing/sre_harnessing/harness.py` with `--tool` (no model) or `--once` (model). Then `./harness-sre.sh your-script` works from the repo root.
5. **Catalog** — if the target is a new production name, add it in `catalog.py` (`_SERVICES`, or databases / topics / caches). Tools should resolve that name, not `service-1`.

To add a **new role**, copy a profile folder (tools, permissions, skills, `package.json`, `harness.py`), register it in `_invoke.sh`’s profile list, and add a root `harness-<role>.sh` that calls `_invoke.sh <folder>`. Cloud identity stays in `shared/`; only argv changes for AWS / Azure / GCP.
