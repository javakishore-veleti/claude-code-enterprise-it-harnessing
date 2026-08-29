---
name: deploy-rollback
description: Decide when a deploy rollback is safer than a forward fix.
---

Use this skill when error rate or latency stepped at a release boundary.

1. Identify the current revision and the last known-good revision.
2. Confirm the change window and whether a feature flag can disable the new path instead.
3. Call `rollback_deploy` only after the operator approves.
4. Re-run `observe_health` after rollback. If health does not recover, you have a deeper dependency failure — stop rolling and escalate.

Do not "fix forward" in production from this harness unless the operator explicitly asks.
