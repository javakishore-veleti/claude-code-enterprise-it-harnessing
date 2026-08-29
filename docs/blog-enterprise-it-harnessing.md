# Enterprise IT Harnessing on a live FOREX, e-commerce, and Shopify estate

~3 minute read.

This blog is about **Enterprise IT Harnessing** capabilities.

<h3 style="color:#2563eb;font-weight:600;margin:1em 0 0.35em">My GitHub repository</h3>

This post discusses my GitHub repo [claude-code-enterprise-it-harnessing](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing) that implements those capabilities.

This blog post considers an Enterprise <span style="color:#2563eb">IT team that supports</span> <span style="color:#dc2626">FOREX back-office trade processing</span>, <span style="color:#2563eb">e-Commerce business</span> middleware (quote through order, shipment, and fulfillment), and <span style="color:#2563eb">Shopify as a SaaS</span> integration — on a mixed stack of Kubernetes, buses, Redis, databases, and search — and still needs **one unified harness** for observe, diagnose, fail over, roll back, search, and silence.

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

Those six files stay the catalog / playbook launchers. **Jobs** are a second launcher per role — `*-job.sh` — fifteen industry functions each. Claude gets the skill injected (`--with-skill`). Hooks stay in that role’s `permissions.yaml`. Existing `./harness-sre.sh` commands are unchanged.

| Job launcher | What it does | Example |
| --- | --- | --- |
| [`./harness-sre-job.sh`](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_SRE_Jobs.md) | 15 SRE jobs: matching rejects, FIX drops, CLS halt, checkout saga, HMAC storm, AS/400 timeout, ticket SLA, quote-to-order, fulfillment stall, consent writes, matching rollback, FOREX page, Shopify blast radius, idempotency replay | `./harness-sre-job.sh matching-reject-spike` |
| [`./harness-db-job.sh`](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_DB_Jobs.md) | 15 DBA jobs: trades lag, CLS-paused risk failover, orders snapshot, Shopify sync drain, consent ledger, quote locks, fulfillment slow query, advisor PII, ticket lag, research restore, profile backups, FIX-window snapshot, orders failover, inbox bloat, netting locks | `./harness-db-job.sh trades-replica-lag` |
| [`./harness-k8s-job.sh`](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_K8s_Jobs.md) | 15 cluster jobs: CrashLoop matching / HMAC, checkout OOM, Shopify ImagePull, fulfillment Pending, EKS/AKS/GKE creds, webhook-retry and session-manager restart, reject / HMAC / AS400 logs, settlement pods, orders-api describe | `./harness-k8s-job.sh crashloop-matching` |
| [`./harness-redis-job.sh`](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_Redis_Jobs.md) | 15 cache jobs: FX book lag / failover, cart eviction / failover, Shopify idempotency freeze / failover, risk-limits memory, quote hot keys, fulfillment locks, sessions, SLA clocks, advisor presence, SLOWLOG on FX / cart / idemp | `./harness-redis-job.sh fx-book-lag` |
| [`./harness-kafka-job.sh`](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_Kafka_Jobs.md) | 15 bus jobs: matching / STP / checkout (no rewind) / Shopify / legacy lag, FOREX and saga describe, under-replicated partitions, HMAC poison pill, research topic create, orders-workflow lag, settlement describe | `./harness-kafka-job.sh lag-checkout-no-rewind` |
| [`./harness-elk-job.sh`](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_ELK_Jobs.md) | 15 search jobs: matching rejects, FIX disconnect, HMAC, saga_failed, AS/400, SLA, carrier timeout, FOREX/Shopify ES health, FOREX alerts, HMAC stay firing, silence orders only, FOREX/Shopify ingest pipelines, FOREX dashboards | `./harness-elk-job.sh search-hmac-failed` |

Full job tables: [SRE](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_SRE_Jobs.md) · [DB](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_DB_Jobs.md) · [K8s](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_K8s_Jobs.md) · [Redis](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_Redis_Jobs.md) · [Kafka](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_Kafka_Jobs.md) · [ELK](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/HowToUse_ELK_Jobs.md). Repo: [claude-code-enterprise-it-harnessing](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing).

Catalog dumps (`list-units`, `list-topics`) do not call a model. Playbooks and jobs do. Cloud (AWS, Azure, GCP) only changes identity and CLI argv.

The default loop in the repo is Claude. The harness is the product: the catalog, the permission files, the leases, and the six launchers. Those stay if the client is replaced.

## What users can do

From the repository root, after setting `ANTHROPIC_API_KEY` (and optionally `CLOUD_PROVIDER`):

- Print the command list for a role: `./harness-sre.sh`, `./harness-db.sh`, and the other four launchers.
- Dump the live estate without calling a model: `list-units`, `list-databases`, `list-topics`, `list-caches`, `resolve-*`.
- Open an interactive session for one role: `./harness-sre.sh repl --interactive` (same pattern for db, k8s, redis, kafka, elk).
- Run a named playbook against a production name: `observe-fx-matching`, `describe-fx-trades`, `pods-shopify-merchants`, `lag-shopify-orders`, `info-shopify-idemp`, `search-shopify-webhooks`.
- Run an industry **job** (skill + hooks): `./harness-sre-job.sh matching-reject-spike`, `./harness-db-job.sh trades-replica-lag`, and the other four `*-job.sh` launchers (15 jobs each).
- Bare `./harness-*.sh` / `./harness-*-job.sh` lists **command names only**. A job answer uses **Input / What it is doing / What it found / Final output** (bullets + Summary) unless you specify another format. **Tokens** are printed after, from the API counts and root [`model_costs.json`](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing/blob/main/model_costs.json).
- Read that role’s `permissions.yaml` to see what is denied, allowed, or asked before a tool runs.
- Pin AWS, Azure, or GCP; identity and CLI argv change, the tool list does not.
- Add a capability by registering one typed tool and, if it mutates, a deny/ask rule and a lease. No second orchestration graph.

How to use (commands): [HowToUse.md](../HowToUse.md) · [SRE](../HowToUse_SRE.md) · [DB](../HowToUse_DB.md) · [K8s](../HowToUse_K8s.md) · [Redis](../HowToUse_Redis.md) · [Kafka](../HowToUse_Kafka.md) · [ELK](../HowToUse_ELK.md). Jobs: [SRE](../HowToUse_SRE_Jobs.md) · [DB](../HowToUse_DB_Jobs.md) · [K8s](../HowToUse_K8s_Jobs.md) · [Redis](../HowToUse_Redis_Jobs.md) · [Kafka](../HowToUse_Kafka_Jobs.md) · [ELK](../HowToUse_ELK_Jobs.md). Repo: [claude-code-enterprise-it-harnessing](https://github.com/javakishore-veleti/claude-code-enterprise-it-harnessing).

## Example: FOREX trades replica lag

`rds-fx-trades-prod` is the Aurora store for FOREX trade capture, FIX sessions, and the audit trail. Sev2 is lag **> 5s**. The job injects the `trades-replica-lag` skill, probes CloudWatch `ReplicaLag`, and does **not** fail over from this job.

```bash
./harness-db-job.sh trades-replica-lag
```

This is a live run. The probe returned no datapoints — that is a monitoring gap, not a fabricated 0s or a confirmed Sev2.

```text
## Input
Check replica lag on `rds-fx-trades-prod` (Aurora, forex-markets: fx-trade-capture / fx-fix-gateway / fx-audit-trail). Sev2 threshold >5s.

## What it is doing
Ran `trades-replica-lag` skill: resolved database, then queried CloudWatch `ReplicaLag` metric for the instance.

## What it found
- CloudWatch returned **no datapoints** for the last 10-minute window — `value_seconds: null`, so lag could not be measured (not a confirmed 0s or a confirmed breach).
- No sev2 determination possible from this probe (`sev2: null`).
- Possible causes: metric not yet published, monitoring gap, or instance/replica not emitting this dimension currently — needs verification, not assumed healthy.

## Final output
- **Severity:** Unable to classify — no data returned, treat as **monitoring gap requiring follow-up**, not a confirmed Sev2 or all-clear.
- **Next action:** Re-run `replication_lag` shortly / widen the CloudWatch time window, and confirm the replica instance identifier and metric emission are correct before declaring status.
- **Constraint:** Per skill, do not failover without a snapshot job first — and with no lag data at all, there's no diagnostic basis for containment action right now.

**Summary:** Replica lag for rds-fx-trades-prod is indeterminate (no CloudWatch datapoints), so no severity can be assigned yet and no failover should be considered until data is confirmed.

## Tokens
- model: `claude-sonnet-5`
- source: `model_costs.json`
- unit: USD per_1m_tokens
- input: 1751 tokens @ $2.00/1M = $0.003502
- output: 660 tokens @ $10.00/1M = $0.006600
- cache write: 3401 tokens @ $2.50/1M = $0.008502
- cache read: 3401 tokens @ $0.20/1M = $0.000680
- overall: $0.019285 USD
```

Default model is `claude-sonnet-5` (`MODEL_ID`). Token **counts** come from the API `usage` object (summed across tool turns). **Cost** is `tokens / 1_000_000 × unit rate` from the JSON list at the repo root. Override the model and add a row if the client changes.

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
