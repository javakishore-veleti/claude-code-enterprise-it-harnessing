# How To Use

From the repository root.

```bash
export ANTHROPIC_API_KEY=...
export CLOUD_PROVIDER=aws   # optional: aws | azure | gcp
```

`repl` opens a session. On a playbook, `--interactive` is optional: omit it to print and exit; add it to keep that session.

Bare `./harness-*.sh` / `./harness-*-job.sh` lists **command names only**. Answers use this structure unless you ask for another format:

1. **Input** — what you asked
2. **What it is doing** — skill and tools
3. **What it found** — measured values
4. **Final output** — bullets, then a one-line **Summary**
5. **Tokens** — model from `MODEL_ID` (default `claude-sonnet-5`), counts from the API, cost from root [`model_costs.json`](model_costs.json)

| If you are | Catalog / playbooks | Jobs (15, skill + hooks) |
| --- | --- | --- |
| SRE | [HowToUse_SRE.md](HowToUse_SRE.md) · `./harness-sre.sh` | [HowToUse_SRE_Jobs.md](HowToUse_SRE_Jobs.md) · `./harness-sre-job.sh` |
| DB | [HowToUse_DB.md](HowToUse_DB.md) · `./harness-db.sh` | [HowToUse_DB_Jobs.md](HowToUse_DB_Jobs.md) · `./harness-db-job.sh` |
| Kubernetes | [HowToUse_K8s.md](HowToUse_K8s.md) · `./harness-k8s.sh` | [HowToUse_K8s_Jobs.md](HowToUse_K8s_Jobs.md) · `./harness-k8s-job.sh` |
| Redis | [HowToUse_Redis.md](HowToUse_Redis.md) · `./harness-redis.sh` | [HowToUse_Redis_Jobs.md](HowToUse_Redis_Jobs.md) · `./harness-redis-job.sh` |
| Kafka / Event Bus | [HowToUse_Kafka.md](HowToUse_Kafka.md) · `./harness-kafka.sh` | [HowToUse_Kafka_Jobs.md](HowToUse_Kafka_Jobs.md) · `./harness-kafka-job.sh` |
| ELK / Search | [HowToUse_ELK.md](HowToUse_ELK.md) · `./harness-elk.sh` | [HowToUse_ELK_Jobs.md](HowToUse_ELK_Jobs.md) · `./harness-elk-job.sh` |
