---
name: topic-lifecycle
description: Create topics with explicit partitions and replication. Never delete from this harness.
---

1. Confirm retention, keying, and consumer fan-out before `kafka_create_topic`.
2. Replication factor 3 is the default for production-shaped clusters.
3. Describe after create and check ISR.
4. If create fails on a managed bus, you may need a cloud-specific quota or naming rule — report the CLI error, do not invent a second API.
