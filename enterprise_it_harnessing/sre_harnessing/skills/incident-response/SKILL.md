---
name: incident-response
description: Sev-classified incident loop for SRE — detect, contain, diagnose, communicate, recover.
---

Observe before you change anything. Call `resolve_service`, then `observe_health` and `fetch_logs`.

1. Name the user-visible symptom and the SLO at risk (FOREX rejects, checkout saga, Shopify HMAC, ticket SLA).
2. Bound blast radius to one business unit and its dedicated cluster/account.
3. Contain with the smallest reversible action. Prefer rollback or traffic shift over config rewrites.
4. Matching-engine reject spikes and Shopify HMAC failures start at Sev2. Do not page CLS/settlement without that context.
5. `page_oncall` and `rollback_deploy` require approval.
6. After recovery, write a six-line timeline: detect, contain, cause, fix, verify, follow-up.

Never run host-destructive commands. Never delete Kubernetes namespaces from this harness.
