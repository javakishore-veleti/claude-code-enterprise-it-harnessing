---
name: replication
description: Replica lag and failover for standalone, ElastiCache, Azure Cache, Memorystore.
---

1. `redis_info` replication — role, master_link_status, lag.
2. If lag is growing, do not fail over. Find the writer or network cause first.
3. `redis_failover` only with operator approval and a named target.
4. Verify the new master and that replicas reattach.
