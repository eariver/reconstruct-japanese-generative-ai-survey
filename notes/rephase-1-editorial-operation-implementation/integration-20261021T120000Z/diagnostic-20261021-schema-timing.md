# Schema cache timing — actual measured (no faster-before-data claim beyond measured)

Command (read-only, no DST writes, exit 0):
`PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/opencode/int-pycache timeout 120 python3 -c "...validate_instance 1+19 vs 20 misses..."`
- `FIRST_MISS 0.015s CACHE_SIZE=1` (first compile + check_schema)
- `HITS_19 0.019s AVG=0.001s CACHE_SIZE=1` (19 reuses, same content, same path)
- `MISSES_20_NOCACHE 0.285s AVG=0.014s` (20 clears to simulate old no-cache path, same new code)

Interpretation (measured, not optimality claim):
- Cached reuse avoids redundant `check_schema` (metaschema `urljoin`) + `Draft202012Validator` compile (registry `$id` `urljoin`) on every call; fresh instance + format validation still runs via reused validator (`iter_errors`).
- 14x per-call for same-schema repeats in isolation (0.001s vs 0.014s). Full receipt (40s) does many distinct schemas first time (misses) + many instance validations with `$ref` `urljoin` on every `iter_errors` (not cached – only validator object cached, not instance results). Cache does not skip instance `$ref` lookups, so full-receipt improvement is less than 14x; measured full-receipt repeat still ~40s in v2 diagnostic (see sampler stacks with `urljoin` during `iter_errors`). No claim that cache alone brings 40s→seconds; it removes only compile+metaschema redundancy, preserving fresh-bytes + fresh-instance semantics.
- Bounded LRU 64, key `(abs_path, content_sha, jsonschema_version, draft2020-12, default-formats)`; external `$ref` (non-`#`) skips cache entirely (see `test_external_file_ref_never_cached`).
