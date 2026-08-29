# Enterprise IT harnessing

This folder is what you run when the operator is an SRE, DBA, Kubernetes admin, Redis admin, or Kafka admin.

The model is unchanged. Each profile swaps **tools**, **skills**, **permissions**, and **auth**. Cloud (AWS, Azure, GCP) almost never gets its own task list — only a different way to prove identity and a different CLI argv for the same semantic operation.

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
