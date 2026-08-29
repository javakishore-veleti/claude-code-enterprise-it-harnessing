---
name: incident-response
description: Sev-classified incident loop for SRE — detect, contain, diagnose, communicate, recover.
---

Observe before you change anything. Call `observe_health` and `fetch_logs` first.

1. Name the user-visible symptom and the SLO at risk.
2. Bound blast radius (one region, one cluster, one dependency).
3. Contain with the smallest reversible action. Prefer rollback or traffic shift over config rewrites.
4. Do not page until severity is justified. `page_oncall` requires approval.
5. After recovery, write a six-line timeline: detect, contain, cause, fix, verify, follow-up.

Never run host-destructive commands. Never delete Kubernetes namespaces from this harness.
