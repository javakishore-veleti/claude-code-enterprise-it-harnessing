---
name: backup-restore
description: Snapshot and restore discipline for RDS, Azure SQL, Cloud SQL, and local engines.
---

Never change a production instance without a restore point you have just confirmed.

1. `describe_instance` — engine, Multi-AZ / HA, storage, maintenance window.
2. `list_backups` — age of the newest snapshot versus RPO.
3. `create_snapshot` if the newest point is older than policy. Wait for available.
4. Apply the change only after the operator approves.
5. Verify with a read-only canary query. Do not run DDL that this harness denies.

DROP, TRUNCATE, and instance-delete are structurally denied.
