---
name: fx-book-lag
description: FX book replica lag
---

FOREX books. Stale book = bad fills.
1. redis_info replication
2. Sev if lag > 2s
3. Failover is a different job.
