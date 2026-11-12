# Supplement-carry §6 corrected return (views + empty_ctx + fixture + parent control, no full PASS)

Workcopy: `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work`
Base: isolated epoch `5eef790bd8d492c557cc4db9c29425e3e410d47d` (new root, NOT 409 ancestry; base blobs `e6c56ba3`/`37f22ab` are 40-char Git blobs vs final139 SHA256 `0974c709`/`388c899`). Baseline untouched (no amend/replace); changes uncommitted.

Corrected source (post §6):
- `scripts/survey_research_authority_v2.py` worktree `d50282bf0812a4d07e3da13cf3574961add0466cd27a3ef3c648b89fe40330dd` (base-staged `e6c56ba3…`)
- `scripts/survey_prearchitecture_acceptance_v2.py` worktree `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90` (base-staged `37f22ab4…`, unchanged since prior correction)
- `tests/test_dm022_supplement_carry_v2.py` NEW `5d5d3aadec70bc5d5c22fdec3e3c65d4f38d73aa995d326d8927fb8f73e26f00` (14 tests)
- Diff: `corrected-implementation-v2.diff` (39144B, 2 files, 453+/23-); prior diffs preserved (`initial-implementation.diff`, `corrected-implementation.diff`).
- Proof-copy original: LOW `0974c709…` (218692B), HIGH `388c899…` (92741B) — parent control source pins.

§6 code:
- LOW prove: narrow OLD/NEW unaffected View semantic comparison (actual accepted Views under exact acceptance refs, fully bound SHA/file metadata, no ignored materiality/profile_annotations). Affected views must differ; unaffected views must be byte- and doc-identical. Acceptance-set digest projections (`view_set_sha256` etc.) remain allowed mechanical propagation, not blanket view semantic permission. No broader schema/history redesign; contradiction returns case (refusal, no silent weakening).
- Empty ctx: removed guessed mutable `empty_ctx` dict; null case now uses canonical `_resolve_phase_supplement_context(repo_root, {}, implementation_sha=None, ...)` no-supp branch factory (exact `MappingProxyType` empties, no third shape). Preserves no-supp operation/history.
- Fixture: `_build_request` accepts `prior_records_by_did` and preserves ALL unaffected record fields verbatim (deepcopy prior, rebind supplement IDs only), not only claims. Replaced/novel rev2 tests pass prior rev1 records for unaffected, so unaffected views/cards/ledger byte-identical. `_assert_full_unaffected` asserts nonempty unaffected, task identity + Discovery binding identical, cards byte-identical, views byte-identical, ledger rows identical for unaffected, `rows_checked == len(tasks)+len(ledger rows)`, mechanical allowlist exactly 9 fields.
- New negative: view-field-only change (materiality_rationale mutated for beta, cards/ledger same) => `prove`/`adopt` refuses `unaffected Discovery beta-source view semantic drift`, State/guard preserved, inert R partials (candidate files from prepare remain, no State/guard writes, no cleanup).
- Late drifts (seam fault only, real validators run): request file valid-JSON edit before HIGH manifest (HIGH late recheck refuses), Raw/COPY/basis/supplement-manifest mutated during LOW builder via patched `_check_fields` (pin/supplement recheck refuses). Explicit State unchanged + guard absent where applicable.

Tests (14 OK, 30.058s, exit 0):
- Preserved initial 4 + new: Weekly DERIVED + Thematic replaced (same+replaced Raw, full rows), real decoy (a) unrelated SizedRef refuses prepare, (b) manifest field swapped refuses prove, late request/Raw/COPY/basis/supplement-manifest refuses, view-field-only refuses.
- New batch raw: `corrected-batch-v2-raw.txt` (argv/env/PID/source hashes/loaded modules/START/EXIT/END + unittest stdout/stderr). Pre/post source hashes identical (`d50282/f312/5d5d3a`), no mutation during tests.
- Parent red control re-bound to original final139: `baseline-control-original-final139-raw.txt` (1 test, exit 1) — thematic novel positive fails on proof-copy original (`0974c709`/`388c899`, test `5d5d3a…`) with actual `source_bindings must explicitly select task-bound sources` (card build, not token), ARGV/env/PID/source hashes/loaded modules/START/END bound, traceback paths are proof-copy (not workcopy imports), separate process. Prior `baseline-control-raw.txt` (workcopy checkout control) preserved as historical observation.
- No full suite, no CURRENT proof, no delivery, no real 409/160. Prior raws/fixtures preserved; unexpected contract failure: none new (view drift now enforced; fixture corrected to preserve ALL fields). If historical valid-history contradicts exact view comparison in real 409/160, return case before broadening (not implemented).
