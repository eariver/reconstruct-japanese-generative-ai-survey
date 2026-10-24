# Versioned renewal M1 — evidence (scoped, no genuine PASS)

## Command 1: M1 unittest (isolated workspace)
- workdir: `.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work`
- command: `python3 -m unittest tests.test_versioned_renewal_m1 -v`
- child exit: 0
- raw (7 tests, 0.275s):
  test_amended_branches ... ok
  test_closure_63_66 ... ok (DeprecationWarning jsonschema.__version__ only)
  test_high_preserves_live_validation ... ok
  test_new_schemas_parse ... ok
  test_no_forbidden_imports_layer ... ok
  test_pipeline_71 ... ok
  test_stale_refusal_without_proof ... ok
  Ran 7 tests OK
- Binds: 4 new schemas parse + "" pointer, 5 amended branches (Gate 5 variants, revalidation 3 branches), closure 63/66, pipeline 71, HIGH LIVE validate_agent_state preserved without verify_state_basis/Path fix, Layer AST no banned imports, renewal keyword signatures.

## Command 2: closure + pipeline (isolated workspace)
- command: python3 snippet `_route_code_deps` + CURRENT_CLOSURE + pipeline len
- child exit: 0
- raw: WEEKLY_GENERATED_V2 63 (new present True), LONGFORM_GENERATED_V1 63, union 66 (per-route 63 True, union 66 True), weekly closure 29, longform 34, pipeline 71.
- Binds: planned replay63/route + union66 are membership plans VERIFIED as actual imports/transitives/$refs (not blind numeric goals); pipeline 67→71 schemas-only.

## Command 3: P3S gate (isolated workspace)
- command: `python3 -c "import tests.test_group_c_editorial_consumers_v2 as t; t.test_p3s50_and_recipe_binding()"`
- child exit: 0, raw: `p3s50 test PASS (now 35/22)`.
- Binds: _SHARED_PY 35 / _SHARED_SCHEMAS 22, staged len 63.

## Failures/errors/skips
- None in M1 scoped set. Full oracle matrix (bootstrap, U/C with genuine changed tools, repeat C→U→U, renewal→editorial, normal direct lifecycle with real PDF, R1×2 anchor, failure/resume, affected regressions) NOT executed — explicit next work, not skipped silently.
- pytest/pip absent in environment; used stdlib unittest + python3 -c (allowed local parsing). No network. No saved historical runners executed. No fixture objects in reconstruct DB. Proof-copy unchanged.

## Isolation observations (before executing candidate code)
- Proof-copy HEAD/status recorded pre/post identical. Isolated DB independent (no alternates, distinct inodes, inert origin, fixture identity, no GIT_* env). No blanket untracked/cache/tmp copy (rsync excludes). No Git DB in notes/. Ordinary commit/push Human-owned; isolated fixture commits done before authorities.
