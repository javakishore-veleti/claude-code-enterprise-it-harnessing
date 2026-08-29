---
name: crashloop
description: CrashLoopBackOff triage that stays read-only until asked to bounce.
---

Always pin `--context`. Mixing prod and lab contexts is the most common harness failure.

1. `kube_get pods` in the namespace.
2. `kube_describe` the crashing pod — look at Last State and Events, not just Ready.
3. `kube_logs` with a short tail. Summarize; do not paste megabytes into the parent context.
4. Restart only with `kube_rollout_restart` after approval. A bounce that loops again is a config or dependency problem.

Do not delete namespaces, PVCs, or nodes.
