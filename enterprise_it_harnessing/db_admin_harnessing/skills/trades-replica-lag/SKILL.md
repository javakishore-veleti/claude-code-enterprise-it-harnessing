---
name: trades-replica-lag
description: FOREX trades replica lag
---

Aurora trades. Lag hurts FIX audit.
1. resolve_database rds-fx-trades-prod
2. replication_lag
3. Do not failover without a snapshot job.
