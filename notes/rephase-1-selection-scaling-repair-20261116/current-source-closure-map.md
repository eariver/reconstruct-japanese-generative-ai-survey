# Current source closure map

Source observation only. No fresh source certification. No Git, repo imports, app runtime, tests, network, subagents, or candidate/source writes.

## Required emphasis

- `scripts/run_selection_architecture_v2_interactive.py` has **no closure ROW** but is **control-root bound** under `implementation_control_roots: scripts`.
- Actual G76 replay/current-proof closure is **70 per route / 73 union**.
- Actual reader closures are **Weekly 36 / Longform 41** for G76.
- Actual contract pipeline is **76 paths with no scripts**.
- Low/historical DM022 source 7 (`_MAPPED_DM022_CODESET`) is **unchanged**: 2 modules + 5 schemas.
- **No new membership is needed** for the mapped existing 4 files; runner remains non-row control-bound.
- **No fresh source certification** is claimed.

## Returned findings

Source observation only (candidate root `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`). No Git, repo imports, app runtime, tests, network, or writes.

### 1. Exact membership of the proposed edit targets

| Path | Fixed-registry membership |
|---|---|
| `scripts/run_selection_architecture_v2_interactive.py` | **ABSENT from every source/closure registry.** Only tests/docs reference it (e.g. `tests/test_run_selection_architecture_v2_interactive.py:5`). |
| `scripts/survey_architecture_v2_base.py` | `scripts/survey_versioned_renewal_history_v2.py:303-334` `_OLD_PY_30` (30 py); `scripts/survey_editorial_staged_source_v2.py:103-139` `_SHARED_PY_G71` (35 py). Therefore present in G76 replay. |
| `scripts/survey_architecture_v2.py` (wrapper) | Same two sets as base. Wrapper imports base at `survey_architecture_v2.py:23`; runner imports wrapper at `run_selection_architecture_v2_interactive.py:22`. |
| `scripts/survey_review_attention_v2.py` | Same two sets (`_OLD_PY_30`, `_SHARED_PY_G71`); therefore present in G76 replay. Runner imports it at line 26; calls `build_attention`/`validate_attention` at lines 447–448. |
| `scripts/survey_research_authority_v2.py` | `survey_versioned_renewal_history_v2.py:374-377` `_NEW_DM022_MODULES_2` (2 py); `survey_editorial_staged_source_v2.py:92-95` `_DM022_PY_2` (2 py); `survey_weekly_derivation_v2.py:70-78` and `survey_longform_generated_v2.py:92-100` `_DM022_7`; `survey_research_authority_v2.py:587-599` `_MAPPED_DM022_CODESET` (7 total paths). **Not** in `_OLD_PY_30` / `_SHARED_PY_G71`. |

`_FAMILY_PY_2` (`survey_discovery_v2.py`, `survey_x_intake_v2.py`, history lines 378–381) contains none of the five targets. Config `contract_files.pipeline` (`config/survey-production-v2.json:7-84`) contains **0 scripts** and none of the five targets.

### 2. Counts that matter

- Historical G67: 30 py + 14 schemas + route3 + staged1 + style1 + recipe1 = **50/route**, 53 union.
- G71: 35 py + 22 schemas + 6 non-py/schema = **63/route**, **66 union**.
- G76 current replay/current proof: 37 py (35+2 DM022) + 27 schemas (22+5 DM022) + route3 + staged1 + style1 + recipe1 = **70/route**, **73 union**. See `survey_editorial_staged_source_v2.py:173-250`; `survey_versioned_renewal_history_v2.py:1545-1570` and `1573-1603`; source proof comment `survey_versioned_renewal_source_v2.py:1539-1542`.
- Weekly reader closure: G71 **29**, G76 **36** (`survey_weekly_derivation_v2.py:39-81`).
- Longform reader closure: G71 **34**, G76 **41** (`survey_longform_generated_v2.py:56-103`).
- Current contract pipeline: **76** = `_OLD_PIPELINE_67` (67, history line 99) + `_NEW_SCHEMAS_4` (4) + `_NEW_DM022_SCHEMAS_5` (5) = 76 unique, no scripts (`survey_versioned_renewal_history_v2.py:1690-1696`; config verified 76 unique).

### 3. Do not conflate the three “7/76” things

- **DM022 source 7** = 2 modules + 5 schemas: `_NEW_DM022_MODULES_2`/`_DM022_PY_2` plus `_NEW_DM022_SCHEMAS_5`/`_DM022_SCHEMAS_5`; exact pin set `_MAPPED_DM022_CODESET` (7).
- **`DM022_SEVEN_SLOTS`** in the runner (`run_selection_architecture_v2_interactive.py:35-43`) = 7 downstream artifact slots (matrix, selection, architecture, review summary, attention, input, audit). These are not source-closure members and must not be added to source registries.
- **Pipeline 76** = 67 old contract paths + 4 renewal schemas + 5 DM022 schemas. It includes the five DM022 schemas but **not** the two DM022 modules.

### 4. Transitive import behavior

No registry uses transitive AST autodiscovery:

- P3S replay: `_route_code_deps` (`survey_editorial_staged_source_v2.py:173-250`) ASTs only its **own** file (lines 217–241); allowed imports are the fixed G76 shared set plus itself. File-pin-only members need not be imported.
- Weekly: `_verify_actual_import_closure` (`survey_weekly_derivation_v2.py:765-808`) ASTs only the weekly module; allowed = fixed G76/G71 canonical + six control-bound loaders (`agent`, `agent_tool`, `drafting`, `evidence`, `production`, `schema`).
- Longform: same pattern (`survey_longform_generated_v2.py:551-588`) with six control-bound loaders.
- History/current proof: no AST at all. `_expected_receipt_closure` and `_verify_receipt_closure_exact` (`survey_versioned_renewal_history_v2.py:1545-1570`, `1766-1802`) compare fixed tuples and blobs; `_verify_staged_code_deps_exact` does the same for replay (`1805-1860`).
- `_FINITE_BATCH_PATHS` (`survey_versioned_renewal_history_v2.py:924-942`) is a Git batching optimization, not closure authority. Unknown paths use the single-path fallback (`_git_show_blob` lines 1142–1151).

### 5. What registry must change for the proposed runner edit?

**Membership-wise: none of the existing closure registries must change** for:

- runner adding a direct `survey_architecture_v2_base` import — base is already a G76 replay member via `_OLD_PY_30`/`_SHARED_PY_G71`;
- adding a private payload helper inside `survey_review_attention_v2.py` — path is already a G76 replay member;
- editing `survey_research_authority_v2.py` — already a G76 replay member via the DM022 sets.

No existing list contains the runner, and its direct imports are not AST-audited by any closure registry. The runner is instead covered by `implementation_control_roots: ["config", "schemas", "scripts", ".github/workflows"]` (config line 101).

Do **not** add base/attention/runner to `_MAPPED_DM022_CODESET`: that set is exactly the 2 DM022 modules + 5 schemas and is required to equal DM022 manifest `tool_pins` exactly (`survey_research_authority_v2.py:587-599`).

If the helper becomes a **new module**, or the runner itself is deliberately promoted into replay closure, that is **not a silent append**: no existing G76 list contains it, and adding it changes G76 from 37→38 py / 70→71 per-route / 73→74 union plus history/staged/Astra membership. That requires an explicit expansion decision, not an existing-list edit.

### 6. Fresh CURRENT proof inclusion of new bytes

`verify_renewal_source_proof` (`survey_versioned_renewal_source_v2.py:1533`) does:

1. Derive current family from disk (`_derive_current_family_from_disk`, history `1731-1763`): G76 requires config pipeline exactly 76 plus renewal7 and DM0227 files present.
2. Require `proof.dependency_closure` names exactly equal `_expected_receipt_closure(route, G76)` = 70/route, 73 union (source `1691-1698`).
3. Require each closure row live SHA match, then require `proof.dependency_closure == basis.current_tool_epoch.closure` (source `1700-1720`).
4. Recompute `contract_identity` from config pipeline76/quality3 and compare to proof/basis (source `1721-1733`).
5. Call `_verify_current_tools_committed` (source `251-326`; call at `1740`):
   - basis epoch must exist and be ancestor of HEAD;
   - committed diff epoch→HEAD over all control roots including `scripts` must be quiet;
   - working tree/staged/untracked control changes refuse;
   - every closure row must match SHA at **both** epoch and HEAD, mode `100644`.

Consequence: edited base/attention/research-authority bytes are included by **closure row hashes** (new SHAs, same membership) and by the `scripts` control diff. The edited runner is not a closure row but is still included by the `scripts` control-root diff/dirty/untracked checks — so it must be committed in a new basis epoch. Uncommitted runner bytes, or any script change after the basis epoch, cause `BASIS_CURRENT_TOOL_DRIFT`. No membership expansion is needed for that coverage, but a new basis/proof with fresh SHAs is required.
