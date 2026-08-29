---
name: consumer-lag
description: Diagnose a stuck consumer group without deleting topics.
---

Topic delete is denied.

1. `kafka_list_topics` or the cloud inventory for the bus you are on.
2. `kafka_describe_topic` — under-replicated partitions first.
3. `kafka_consumer_lag` — which partition is falling behind, and is the member alive?
4. Recommend scale, pause, or skip. Do not reset offsets unless the operator asks in a later change.

MSK, Event Hubs, and Pub/Sub change listing and auth, not this loop.
