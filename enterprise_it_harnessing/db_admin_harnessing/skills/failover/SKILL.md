---
name: failover
description: Planned or emergency replica promotion.
---

Failover is containment, not diagnosis.

1. Confirm replica lag and that the intended target is healthy.
2. State RPO/RTO impact in one sentence before calling `failover_instance`.
3. After promotion, verify writes and that old-primary clients fail or reconnect.
4. Do not fail back immediately. Capture the timeline first.

If lag is large, a failover will lose data. Say so and wait for the operator.
