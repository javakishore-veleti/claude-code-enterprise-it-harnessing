# Enterprise IT Harnessing — platform diagrams

Audience-specific views of the same platform. The model does not change. What changes is the **tool surface**, **permission profile**, and **named estate** each operator is allowed to touch.

| Audience | Diagram | Question it answers |
| --- | --- | --- |
| SVP of Engineering | [Strategic](#strategic-diagram-svp-of-engineering) | What do we operate, who is accountable, and how is blast radius bounded? |
| SVP / Chief Architect | [Enterprise architecture](#enterprise-architecture-100-microservices) | How do FOREX, e-commerce, and Shopify roll up to 100+ microservices? |
| Engineering Manager & Chief Architect | [Architecture](#architecture-engineering-manager--chief-architect) | How do launchers, profiles, the shared kernel, and cloud identity compose? |
| SRE, DBA, Kubernetes, Redis, Kafka, ELK | [Role-specific](#role-specific-diagrams) | What can this role observe, mutate, and never do? |

The same diagrams are summarized in the [root README](../README.md#strategic-diagram-svp-of-engineering).

---

## Strategic diagram (SVP of Engineering)

One enterprise. Three product domains. Ten business units with **dedicated cloud accounts and clusters**. Six role-scoped harnesses. One Claude decision loop. Governance is structural: deny / allow / ask, isolation leases on mutations, and an audit event bus.

```mermaid
flowchart TB
  subgraph Outcomes["What leadership gets"]
    O1["Faster, consistent MTTR on named production services"]
    O2["Dual-control for customer-facing mutations"]
    O3["Role-scoped blast radius — not a shared admin shell"]
  end

  subgraph Estate["The estate we actually run"]
    FX["FOREX bank middleware<br/>matching · FIX · CLS · regulatory"]
    EC["E-commerce middleware<br/>catalog · quote · orders · fulfillment · customer"]
    SH["Shopify headless merchants<br/>HMAC webhooks · idempotency · legacy / AS400"]
  end

  subgraph Units["10 business units · dedicated accounts"]
    U1["forex-markets · forex-settlement"]
    U2["ecommerce-retail · ecommerce-quote · fulfillment"]
    U3["customer-profile · support · advisor · research"]
    U4["shopify-merchants"]
  end

  subgraph Platform["Enterprise IT Harnessing Platform"]
    Model["One Claude decision loop"]
    Catalog["Named catalog ~100 microservices<br/>fx-matching-engine · orders-api · shopify-webhook-ingress"]
    Profiles["Six operator surfaces<br/>SRE · Event Bus · Search · Kubernetes · Redis · DB"]
    Gov["Governance: permissions.yaml · isolation leases · audit events"]
  end

  FX --> Units
  EC --> Units
  SH --> Units
  Units --> Catalog
  Catalog --> Model
  Model --> Profiles
  Profiles --> Gov
  Gov --> Outcomes
```

```mermaid
flowchart LR
  subgraph Profiles["Operator surfaces — same loop, different blast radius"]
    SRE["SRE<br/>SLO / incident / rollback"]
    DBA["DBA<br/>snapshot / failover / explain"]
    K8S["Kubernetes<br/>pods / drain / rollout"]
    RDS["Redis<br/>INFO / hot keys / failover"]
    KFK["Kafka<br/>lag / ACL / rebalance"]
    ELK["ELK + Grafana<br/>search / alerts / silence"]
  end
```

**Read this as a control model, not a chatbot.** Operators do not get a generic `bash` session against production. They get a catalog of **named** services (`fx-matching-engine`, not `service-1`), a permission file that **denies** irreversible wipes, and a lease so two agents cannot mutate the same cluster, topic, or cache at once.

---

## Enterprise architecture (100+ microservices)

The catalog in `enterprise_it_harnessing/catalog.py` is ten services per business unit. Domains roll up as **20 + 70 + 10 = 100**. Each unit also owns a dedicated Kubernetes cluster, bus, Redis, database, and ELK/Grafana stack — that data plane is why the estate is described as **100+**.

```mermaid
flowchart TB
  ENT["Enterprise estate · 100+ microservices"]

  subgraph FOREX["FOREX bank middleware · 20"]
    FM["forex-markets · 10 · AWS EKS<br/>price · match · FIX · STP · RFQ · audit"]
    FS["forex-settlement · 10 · AWS EKS<br/>risk · netting · CLS · PnL · MiFID / EMIR"]
  end

  subgraph ECOM["E-commerce middleware · 70"]
    ER["ecommerce-retail · 10 · Azure AKS<br/>catalog · cart · checkout · orders · payments"]
    EQ["ecommerce-quote · 10 · Azure AKS<br/>B2B quote · contract · RFQ · margin"]
    FF["fulfillment · 10 · GCP GKE<br/>WMS · pick-pack · ship · track · returns"]
    CP["customer-profile · 10 · AWS EKS<br/>identity · consent · loyalty · KYC"]
    CS["customer-support · 10 · Azure AKS<br/>tickets · chat · SLA · voice"]
    CA["customer-advisor · 10 · Azure AKS<br/>NBA · workspace · compliance"]
    PR["product-research · 10 · GCP GKE<br/>assortment · trends · launch calendar"]
  end

  subgraph SHOP["Shopify headless merchants · 10"]
    SM["shopify-merchants · 10 · AWS EKS<br/>HMAC ingress · product/order/customer sync<br/>idempotency · SOAP / AS400 bridge"]
  end

  ENT --> FOREX
  ENT --> ECOM
  ENT --> SHOP
  SM -->|"catalog / orders / profile"| ER
  SM --> CP
  ER -->|"allocation / ship"| FF
  FM -->|"fills / SSI"| FS
```

| Domain | Business units | Services | Sum |
| --- | --- | --- | --- |
| FOREX bank middleware | `forex-markets`, `forex-settlement` | 10 + 10 | **20** |
| E-commerce middleware | retail, quote, fulfillment, profile, support, advisor, research | 10 × 7 | **70** |
| Shopify headless merchants | `shopify-merchants` | 10 | **10** |
| **Enterprise** | **10 BUs** | | **100+** |

### Platform plane under those 100 services

```mermaid
flowchart TB
  subgraph App["Application plane · 100 microservices"]
    FX20["FOREX · 20"]
    EC70["E-commerce · 70"]
    SH10["Shopify · 10"]
  end

  subgraph Plane["Per-BU platform plane · dedicated, not shared"]
    K8["Kubernetes · EKS / AKS / GKE"]
    BUS["Event bus · MSK / Event Hubs / Pub/Sub"]
    CACHE["Redis · ElastiCache / Azure Cache / Memorystore"]
    DB["Databases · RDS / Azure SQL / Cloud SQL"]
    OBS["ELK + Grafana"]
  end

  subgraph Harness["Root launchers overlay the same names"]
    H["./harness-sre.sh · ./harness-db.sh · ./harness-k8s.sh<br/>./harness-redis.sh · ./harness-kafka.sh · ./harness-elk.sh"]
  end

  FX20 --> K8
  EC70 --> K8
  SH10 --> K8
  K8 --- BUS
  BUS --- CACHE
  CACHE --- DB
  DB --- OBS
  H --> App
  H --> Plane
```

Dump the rollup from the repo root (no model): `./harness-sre.sh list-units`.

---

## Architecture (Engineering Manager & Chief Architect)

The platform is a **harness**, not an agent framework. The model decides. The harness executes, constrains, and names the world. The [enterprise architecture](#enterprise-architecture-100-microservices) above is the estate those tools resolve — FOREX (20) + e-commerce (70) + Shopify (10) = **100+** named microservices on dedicated per-BU platforms.

```mermaid
flowchart TB
  subgraph Launch["Launch plane"]
    SH["Root launchers<br/>harness-sre.sh · harness-db.sh · harness-k8s.sh<br/>harness-redis.sh · harness-kafka.sh · harness-elk.sh"]
    NPM["npm run harness:* · per-profile package.json<br/>25+ named commands each"]
  end

  subgraph Profile["Role profile — the only extension point"]
    Tools["Typed tools<br/>observe · failover · lag · search"]
    Skills["On-demand skills<br/>incident-response · backup-restore · eviction"]
    Perms["permissions.yaml<br/>always_deny · always_allow · ask_user"]
    Tasks["Named playbooks<br/>observe-fx-matching · failover-*"]
    AuthY["providers/auth.yaml<br/>AWS · Azure · GCP identity"]
  end

  subgraph Kernel["Shared kernel — one implementation"]
    Runner["Streaming runner + prompt cache"]
    Guard["Permission guard before every tool"]
    Lease["Isolation leases on mutating tools"]
    Ident["Cloud identity resolver"]
    Bus["Event bus / audit"]
    Cat["Service catalog<br/>list_business_units · resolve_service"]
    MCP["MCP runtime for real CLIs"]
  end

  subgraph World["The world the model may touch"]
    Cloud["Cloud CLIs: aws · az · gcloud · kubectl"]
    Data["Named clusters, topics, caches, indexes, instances"]
    Model["Claude model — decisions only"]
  end

  SH --> Profile
  NPM --> Profile
  Profile --> Kernel
  Kernel --> Model
  Guard --> Cloud
  Lease --> Data
  Cat --> Data
  Ident --> Cloud
  MCP --> Cloud
```

### Control-plane contract

| Layer | What it owns | What it must not own |
| --- | --- | --- |
| Model | Which tool to call, in what order, when to stop | Branching logic, raw shell interpolation, implicit prod access |
| Profile | Tool list, skills, deny/ask rules, named playbooks | A second agent framework |
| Shared kernel | Guard, leases, identity, catalog, events, MCP | Domain runbooks or BU-specific resource names |
| Catalog | 10 BUs, ~100 services, dedicated accounts/clusters | Guessed hostnames or “cluster-1” |

Catalog dumps (`list-units`, `resolve-*`) use `--tool` and **do not** call the model. Playbooks (`observe-*`, `incident-*`, `failover-*`) use `--once` and do.

Mutations fail closed: a dirty or already-leased target is refused. Leases live under `.harness_isolation/` (gitignored).

```mermaid
sequenceDiagram
  participant Op as Operator
  participant L as harness-*.sh
  participant R as Shared runner
  participant G as Guard + lease
  participant M as Claude
  participant C as Cloud / cluster

  Op->>L: observe-fx-matching / failover-*
  L->>R: profile tools + skills + permissions
  R->>M: system prompt + catalog + skill index
  M->>R: tool call (typed)
  R->>G: check_permission + acquire lease if mutating
  alt denied or leased
    G-->>M: Blocked by policy / lease conflict
  else allowed
    G->>C: argv CLI or MCP (no shell interpolation)
    C-->>G: structured result
    G-->>M: observation
  end
  M-->>Op: next step or stop
```

---

## Role-specific diagrams

Each role keeps the same loop and the same catalog. The **smallest** tool set that role needs is what gets registered. Cloud (AWS / Azure / GCP) only changes identity and CLI argv.

```mermaid
flowchart TB
  subgraph Shared["Every role"]
    Loop["Claude loop"]
    Cat["Named catalog · 10 BUs"]
    Id["cloud_identity"]
    Pol["permissions.yaml"]
    Ls["Isolation lease on mutations"]
  end

  Loop --> SRE
  Loop --> DBA
  Loop --> K8S
  Loop --> REDIS
  Loop --> KAFKA
  Loop --> ELK
  Cat --> SRE
  Cat --> DBA
  Cat --> K8S
  Cat --> REDIS
  Cat --> KAFKA
  Cat --> ELK
```

### SRE

**When:** microservice SLO — FOREX matching / FIX, checkout saga, Shopify HMAC ingress, support tickets.

```mermaid
flowchart LR
  subgraph Allow["Always allow"]
    A1["observe_health"]
    A2["fetch_logs"]
    A3["resolve_service"]
  end
  subgraph Ask["Ask operator"]
    Q1["rollback_deploy"]
    Q2["page_oncall"]
    Q3["kubectl drain / scale"]
  end
  subgraph Deny["Always deny"]
    D1["namespace / PV delete"]
    D2["FLUSHALL / DROP / terraform destroy"]
  end
  Skills["Skills: incident-response · deploy-rollback"]
  Allow --> Skills
  Skills --> Ask
  Ask --> Deny
```

Launch: [`./harness-sre.sh`](../harness-sre.sh) · commands: [`enterprise_it_harnessing/sre.md`](../enterprise_it_harnessing/sre.md)

### Database administrator

**When:** RDS / Aurora / Azure SQL / Cloud SQL / Spanner — snapshot, failover, parameter group, slow-query explain. Never raw `DROP` in production.

```mermaid
flowchart LR
  subgraph Allow["Always allow"]
    A1["describe instance"]
    A2["explain / slow query"]
    A3["list snapshots"]
  end
  subgraph Ask["Ask operator"]
    Q1["failover"]
    Q2["parameter-group change"]
    Q3["restore"]
  end
  subgraph Deny["Always deny"]
    D1["DROP DATABASE"]
    D2["untargeted wipe"]
  end
  Skills["Skills: backup-restore"]
```

Launch: [`./harness-db.sh`](../harness-db.sh) · commands: [`enterprise_it_harnessing/db.md`](../enterprise_it_harnessing/db.md)

### Kubernetes cluster admin

**When:** EKS / AKS / GKE / on-prem kubeconfig. Read-only `get` / `describe` is open. Drain, cordon, delete, and rollout undo require an operator.

```mermaid
flowchart LR
  subgraph Allow["Always allow"]
    A1["kubectl get / describe / logs / top"]
  end
  subgraph Ask["Ask operator"]
    Q1["drain · cordon · scale"]
    Q2["rollout undo"]
  end
  subgraph Deny["Always deny"]
    D1["delete ns / pv / pvc"]
  end
  Skills["Skills: cluster-context"]
```

Launch: [`./harness-k8s.sh`](../harness-k8s.sh) · commands: [`enterprise_it_harnessing/k8s.md`](../enterprise_it_harnessing/k8s.md)

### Redis admin

**When:** ElastiCache / Azure Cache / Memorystore — `INFO`, slowlog, replica lag, eviction storms, hot keys. `FLUSHALL` is denied in production.

```mermaid
flowchart LR
  subgraph Allow["Always allow"]
    A1["INFO · slowlog · lag"]
  end
  subgraph Ask["Ask operator"]
    Q1["failover"]
    Q2["ACL change"]
  end
  subgraph Deny["Always deny"]
    D1["FLUSHALL / FLUSHDB"]
  end
  Skills["Skills: eviction"]
```

Launch: [`./harness-redis.sh`](../harness-redis.sh) · commands: [`enterprise_it_harnessing/redis.md`](../enterprise_it_harnessing/redis.md)

### Kafka / bus admin

**When:** MSK / Event Hubs / Pub/Sub — consumer lag, ACLs, poison-pill recovery, long rebalances as background work.

```mermaid
flowchart LR
  subgraph Allow["Always allow"]
    A1["describe topic"]
    A2["consumer lag"]
  end
  subgraph Ask["Ask operator"]
    Q1["ACL change"]
    Q2["partition reassignment"]
  end
  subgraph Deny["Always deny"]
    D1["untargeted topic wipe"]
  end
  Skills["Skills: consumer-lag · topic-lifecycle"]
```

Launch: [`./harness-kafka.sh`](../harness-kafka.sh) · commands: [`enterprise_it_harnessing/kafka.md`](../enterprise_it_harnessing/kafka.md)

### ELK + Grafana

**When:** Elasticsearch aliases (`forex-trades`, `shopify-webhooks`, `orders`) and Grafana folders per business unit. Silences require approval.

```mermaid
flowchart LR
  subgraph Allow["Always allow"]
    A1["search named alias"]
    A2["list alerts"]
  end
  subgraph Ask["Ask operator"]
    Q1["silence / mute"]
  end
  subgraph Deny["Always deny"]
    D1["delete index / wipe data stream"]
  end
  Skills["Skills: elasticsearch-query · grafana-alerts"]
```

Launch: [`./harness-elk.sh`](../harness-elk.sh) · commands: [`enterprise_it_harnessing/elk.md`](../enterprise_it_harnessing/elk.md)
