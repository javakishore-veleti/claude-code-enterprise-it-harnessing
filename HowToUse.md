# How To Use

From the repository root.

```bash
export ANTHROPIC_API_KEY=...
export CLOUD_PROVIDER=aws   # optional: aws | azure | gcp
```

| If you are | Open |
| --- | --- |
| SRE | [HowToUse_SRE.md](HowToUse_SRE.md) |
| DB | [HowToUse_DB.md](HowToUse_DB.md) |
| Kubernetes | [HowToUse_K8s.md](HowToUse_K8s.md) |
| Redis | [HowToUse_Redis.md](HowToUse_Redis.md) |
| Kafka / Event Bus | [HowToUse_Kafka.md](HowToUse_Kafka.md) |
| ELK / Search | [HowToUse_ELK.md](HowToUse_ELK.md) |

`--interactive` keeps the session. Leave it off for one turn then exit.
`list-*` / `resolve-*` do not call the model. Playbooks do.
