# Enterprise IT harnessing

Production profiles on top of the s01–s23 loop. The learning sessions stay in the repo root. This folder is what you run when the operator is an SRE, DBA, Kubernetes admin, Redis admin, or Kafka admin.

The model is unchanged. Each profile swaps **tools**, **skills**, **permissions**, and **auth**. Cloud (AWS, Azure, GCP) almost never gets its own task list — only a different way to prove identity and a different CLI argv for the same semantic operation.

## Ideas taken from the sessions (not copied)

| Session | Primitive kept here |
| --- | --- |
| s01 / s13 | Perception-action loop via `core.stream_loop` |
| s02 / s14 | Dispatch map of typed tools; prefer them over raw bash |
| s03 / s07 | Task graphs in `tasks/common.yaml` |
| s04 | Noisy logs stay summarized; parent context stays clean |
| s05 | `list_skills` / `load_skill` against each profile's `skills/` |
| s08 | Long cloud CLIs time out instead of hanging the loop |
| s12 / s23 | Isolation leases: dirty-check, conflict, stale-prune — on **resources**, not git worktrees |
| s15 | Per-profile `permissions.yaml` |
| s16 | Audit events on every tool |
| s20 | Ephemeral prompt cache on system + last tool |
| s21 / s22 | Ready for MCP servers and Redis mailboxes; not required to start |

## Run

```bash
export ANTHROPIC_API_KEY=...
# optional: pin the cloud; otherwise auto-detect from env
export CLOUD_PROVIDER=aws   # or azure or gcp

npm run harness:sre
npm run harness:db
npm run harness:k8s
npm run harness:redis
npm run harness:kafka
```

| Profile | npm | Auth that changes | Tasks that stay common |
| --- | --- | --- | --- |
| SRE | `npm run harness:sre` | CloudWatch / Azure Monitor / Cloud Monitoring credentials | detect → contain → diagnose → recover |
| DB admin | `npm run harness:db` | RDS / Azure SQL / Cloud SQL identity | describe, backup, snapshot, failover |
| Kubernetes | `npm run harness:k8s` | kubeconfig via EKS, AKS, GKE, or on-prem | get, describe, logs, rollout |
| Redis | `npm run harness:redis` | `REDIS_URL` or ElastiCache / Azure Cache / Memorystore | INFO, SLOWLOG, failover |
| Kafka | `npm run harness:kafka` | bootstrap, MSK, Event Hubs, or Pub/Sub | list, describe, lag, create |

Leases are stored under `.harness_isolation/` (gitignored). Mutations on a dirty or already-leased target fail closed.
