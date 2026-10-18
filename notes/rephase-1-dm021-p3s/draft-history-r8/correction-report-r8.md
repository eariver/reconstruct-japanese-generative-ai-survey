# P3S R8 correction report — O7 test-only repair (pre-execution)

2026-10-18. Implements root-selected O7 correction
(`astra-batch-b-resolution-selection.md`) on the R7 candidate. Module
(`7059166e…`) and schema (`4fa61723…`) UNCHANGED — no implementation defect.
Only `tests/test_survey_editorial_staged_source_v2.py` changed: 142747 B
`cf2bddd6…` → 144795 B `955f6fb5…`, 2535 → 2570 lines (+35), still 26 test
methods (no method added/removed; no new constant). No imports, no
test/fixture runs in this unit, no network/commit/push; no
`verification-tools/` or root-doc edits. R7 bytes preserved in
`draft-history-r8/prior-bytes-r8/` + `static21-r7-preserved.json`;
R5–R7 reports untouched.

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (unchanged) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 144795 | 0o664 | `955f6fb5dd65e2e731d9de38e093f42d499d1f425186848834ecaf109cd800e9` |

Module AST-OK (25 defs), test outer AST-OK (49 defs, 26 test methods +
helpers), schema Draft202012Validator.check_schema OK. Every embedded child
program AST-OK via literal-eval + `ast.parse` (no fixture execution):
`_P3S_MATERIALIZE_SCRIPT` 1120 (`55884c2b…`), `_P3S_VERIFY_SCRIPT` 729
(`2497eb0fae67…`), `_P3S_FAULT_SCRIPT` 11997 (`a6ecf378…`),
`_R1_FIXTURE_PREPARE_SCRIPT` 3473 (`5f469984…`) — all four byte-identical
R7→R8. No `...[truncated` markers; single `__main__` only. Status 105 rows
(3M + 18A + 84 pyc).

## Evidence-transfer body hashes (R7→R8, scoped)

AST-body (`ast.dump`, `include_attributes=False`) comparison R7 prior vs R8
current (49 funcs each):

- CHANGED exactly 1: `EditorialStagedSourceV2Tests.test_o7_scope_refusals`
  `8750e5f13cb9` → `98ee94fb2ed0`.
- All other 48 funcs IDENTICAL, including O1/O2/O3/O4/O5/O6a/O6b/O8/O9 and
  all 24 shared helpers (`_lf_prepare`, `_weekly_prepare`,
  `_weekly_prepare_from`, `_capture`, `_scope_for`, `_materialize`,
  `_verify`, `_retamper_manifest`, `_snapshot`, `_assert_no_write`,
  `_assert_no_write_except`, `_assert_owned_delta_only`,
  `_run_p3s_fixture`, `_launch_durable_child`, `_durable_base`,
  `_make_p3s_source_root`, `_copy_base`, `_run_fixture_code`,
  `_commit_r1_nonemitted_comment`, `_run_git`, `_fresh_lf_root`,
  `_fault_run`; full verified list equal).

Module/schema bodies unchanged (`diff -q` identical). R7 O4/O5/O6a/O6b
successes stay bound to R7; transfer qualification (scoped) is for root
selection, not claimed here — no new runtime PASS claimed in this unit.

## O7 repair detail (prescribed test-only, actual APIs inspected)

Replaced unsupported `NEEDS_SCOPE_DETAIL` (schema rejects as
`SCOPE_ORDINARY_INVALID`, historical R7 failure) with valid
`REQUIRES_OWNER_DECISION` for the existing non-authorizing-decision case:

```python
ordinary = p1t._scope_review_for(..., "scope-ordinary.json",
                                 decision="REQUIRES_OWNER_DECISION")
# assert parsed decision == REQUIRES_OWNER_DECISION
# OBSERVER_REFUSED/OBSERVE/REFUSED_PRE_WRITE + SCOPE_NOT_WITHIN_AUTHORITY
# (P1 _validate_scope:1813-1815 raises SCOPE_NOT_WITHIN_AUTHORITY after
# schema passes; P2V _wrap_p1 preserves code; P3S wraps as OBSERVER_REFUSED)
```

Added separate valid ordinary-review-without-block case (P1
`_validate_scope:1808-1810` returns `RESULT_REQUIRED` when block is None;
P2V `426-431` returns `NEEDS_SCOPE`; P3S `799-800` raises
`OBSERVER_NOT_BOUND`):

```python
template = p1t._scope_review_for(..., "scope-template-noblock.json")  # default WITHIN
template_obj = core.load_json(template); assert block present
del template_obj["editorial_correction_scope"]
template_obj["review_sha256"] = core.sha256_object(
    {k: v for k, v in template_obj.items() if k != "review_sha256"})
core.write_json(noblock, template_obj); template.unlink()
assert no block; loader accepts; P3S OBSERVER_NOT_BOUND
```

Public ordinary loader acceptance uses actual P1 API args (inspected
`survey_editorial_correction_proposal_v2.py:1795-1799`,
`survey_reader_surface_gate_v2.py:958-967`, P1T `441-445`):

```python
state_obj = core.load_json(prep["state_path"])
profile_obj = core.load_json(root / state_obj["profile"]["path"])
proposed_reader_ref = prep["prepared"]["proposal"]["proposed"]["proposed_reader_ref"]
authority = p1t.reader_gate.load_and_validate_reader_surface_semantic_review(
    root, noblock,
    expected_issue_id=state_obj.get("issue_id"),
    expected_publication_profile=profile_obj.get("publication_profile"),
    expected_surface_path=proposed_reader_ref["path"],
    expected_surface_sha256=proposed_reader_ref["sha256"],
    require_pass=True)
assert authority["decision"] == "PASS"  # ordinary valid, not editorial auth
# then P3S exact OBSERVER_NOT_BOUND/OBSERVE/REFUSED_PRE_WRITE + fault-present no-write
```

Kept missing (`WRITER_FAILED/PIN`), malformed (`SCOPE_UNREADABLE`), stale
(`SCOPE_STALE_UPSTREAM`) distinctions and `base` restored equality
(ordinary + noblock records removed before final comparison; malformed via
`finally`). Unsupported enum failure remains historical only.

## Static21 / caches (NEW, read-only)

`draft-history-r8/static21.json` 3670 B `267dc51e…`: canonical flat JSON
(outer sorted, inner `sha256/bytes/mode`), exact 21 entries (18 inherited +
3 new). New3: module `7059166e…` 126181 B, test `955f6fb5…` 144795 B,
schema `4fa61723…` 5627 B, all `0o664`. Inherited18 18/18 match
`expected18-source-correction-v5.json`; 84 caches 84/84 match
`cache-inventory-static.json`; 0 mismatches, no baselining.

## Remaining concerns (no execution in this unit; for root selection)

- O7 noblock relies on `write_bytes`/`core.write_json` truncating in place
  so `snap_noblock`/`base` equalities hold — matches O6b/O4 restore
  precedent, but runtime proof awaits the single authorized remainder batch.
- No execution PASS claimed: all 26 methods unaudited at runtime post-edit;
  R7 batch-B O4–O6b successes + O7 failure preserved in
  `smoke-r7-batch-b-20261018T090542Z/`; a qualified scoped remainder
  (O7–O9) is for root selection, not claimed here.
