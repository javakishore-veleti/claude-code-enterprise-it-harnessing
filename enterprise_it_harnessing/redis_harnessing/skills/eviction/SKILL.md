---
name: eviction
description: Diagnose Redis eviction and hot-key pressure without flushing data.
---

FLUSHALL is denied. Do not look for a workaround.

1. `redis_info` memory — used_memory, evicted_keys, maxmemory_policy.
2. `redis_slowlog` — repeated large keys or KEYS-style work.
3. `redis_describe_cloud` when the node is ElastiCache, Azure Cache, or Memorystore.
4. Recommend a policy or scaling change. Do not delete keys in bulk from this harness.
