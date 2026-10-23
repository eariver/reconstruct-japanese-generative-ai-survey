# Independent pre-integration draft review — Groups L/C only (not H)

Fresh author-independent reviewer. Scope is **L (low-level identity/chain/anchor/seal + agent integration) and C (core/stage/profiled Freeze/config/orchestrator/handoff/human-gate/export + P1/P2V/P2R/P3S + R1/wrapper/build refusal) only**. H files (`scripts/survey_editorial_publication_v2.py`, four H schemas, Reader/Gate branches, Weekly/Longform receipt dispatch, `survey_quality_v2` deterministic inputs) are **not reviewed here**; H2 is actively correcting them per root `astra-draft-review-r1.md` §§1–7. No duplicate H review. No test execution, no imports, no Git writes, no network. Read-only file reads via read tool; no source pollution. This is a correctness review of actual field/API/loop/branch behavior, not a presence/shape pass-by-comments.

Governing read:

- `outputs/rephase-1-editorial-operation-contract-decision.md` (d880f53e, 191 lines, §§1–10).
- `notes/rephase-1-editorial-operation-implementation/astra-implementation-selection.md` (§§1–5, frozen L APIs, closure rule).
- `notes/rephase-1-editorial-operation-implementation/map-resolution-20261021.md` (§§2–4 frozen ownership/registry/closures, §5 legacy shape, §6 spec/toolchain/build-record).
- `notes/rephase-1-editorial-operation-implementation/astra-draft-review-r1.md` (H stubs + L/C integration requirements §§15–22).
- `notes/rephase-1-editorial-operation-contract/README.md` + `astra-review-resolution.md` + technical Overriding qualification + operation §9 addendum (cumulative legacy, versioned KEEP selected not observed).
- `notes/rephase-1-editorial-operation-implementation/implementation-map-20261020.md` (§§1–16, pre-code return).
- Group reports as claims only (not evidence): `group-l/group-l-sha-diff-20261021T120000Z.md`, `group-l/group-l-test-20261021T120000Z.md` (10 cheap tests), `group-c/report.md` (§§1–6, 5 cheap tests), `group-h-report-20261021.md` (read only to avoid overlap).

Actual roots (read-only):

- Shared DST: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`.
- Original source22: `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`.

Exact read coverage (DST unless noted):

- `scripts/survey_publication_set_v2.py:1–1066` (all).
- `schemas/editorial-publication-set-v2.schema.json:1–92` (all); `schemas/publication-surface-revalidation.schema.json:1–246` (all) vs original `schemas/publication-surface-revalidation.schema.json:1–161` (all).
- `scripts/survey_agent_control_v2.py:1–120,95–450,445–795,795–1445,1445–1845,1845–2295` (branch dispatch, `_validate_checkpoint_record`, `_validate_agent_state`, `_resolve_checkpoint_artifact`, `_check_immutable`, `_check_chain`, `_resolve`, `_validate_stage_artifacts`, `approve_publication_preview`, `revalidate_publication_surface` writer refusal).
- `scripts/survey_schema_v2.py:1–81`; `scripts/survey_production_v2.py:42–62,116–270,780–859`.
- `scripts/survey_stage_validation_v2.py:38–105,152–300`.
- `scripts/survey_profiled_freeze_v2.py:22–80`; `scripts/survey_orchestrator_v2.py:131–233`; `scripts/survey_handoff_v2.py:54–123`; `scripts/survey_human_gate_v2.py:205–324`.
- `.github/workflows/survey-production-v2-export-publication-preview.yml:1–219`.
- `scripts/survey_editorial_correction_proposal_v2.py:55–90,427–490,642–730,726–975,1490–1739,1843–1998`.
- `scripts/survey_editorial_current_authority_v2.py:101–214`.
- `scripts/survey_editorial_staged_source_v2.py:1–60,60–168`.
- `scripts/survey_weekly_mechanical_refresh_v2.py:823–926`; `scripts/run_semantic_publication_v2_interactive.py:1–92`; `scripts/survey_semantic_quality_v2.py:171–210`.
- `config/survey-production-v2.json:1–30` (head only; full 62→67 count taken from C report claim, not re-audited here).

NOT re-read in full: full P1 `_Collector`/`_pipeline_data` internals beyond cited ranges, full P2V observation body beyond early pins, full R1 writer beyond preflight, full freeze/orchestrator/handoff/human-gate call-site enumeration beyond cited resolvers, Weekly/Longform derivation closures, H schemas/runtime. No whole-candidate audit, no implementation acceptance, no production adoption claim.

Verdict: **CHANGES_REQUIRED** — L/C drafts are not ready for combined-source freeze or long fixture runs. Findings below are load-bearing field/API/loop/malformed-branch defects. Cheap `10/5` checks are not behavioral integration (see §7).

## 1. L low-level identity — blocking

### 1.1 `_canonical7_from_validation` reads original live bytes, breaks after legacy R1

`scripts/survey_publication_set_v2.py:797–820`.

- Reads each validation-checkpoint row via `_repo_file` + `sha256_file == sha` against the **original validation record**, refusing on drift.
- After a valid legacy `R1×2` refresh, live publication bytes equal the latest legacy effective (`new_sha`), not the original checkpoint SHA. Original rows are stale by design; cumulative legacy semantics (Overriding qualification: every link checked against same original `prior_record`, effective derived from latest legacy) require the anchor, not live-original equality.
- `resolve_publication_selection:880` calls this unconditionally before branching to legacy/editorial. A healthy post-R1 State therefore fails selection before anchor derivation.
- Contract §§4–5: canonical anchor is original checkpoint or latest legacy before first activation; materialized canonical files checked against anchor effective rows, new set refs separately. The current code checks live-original equality before apply.
- Impact: `R1×2→correction` order (required §9 oracle) cannot reach correction; legacy-prefix selection fail-closes on healthy input. Must accommodate stale original via chain-derived anchor effective, not live-original expectation.

### 1.2 `before_active_digest` does not enforce exactly seven

`scripts/survey_publication_set_v2.py:162–195`.

- Iterates `sorted(effective7)` and hashes `{effective: rows, candidate}`, but never checks `set(effective7) == set(PUBLICATION_ROLES_7)` or `len == 7`.
- Caller can supply 6/8/wrong names and still obtain a digest that later compares equal to a stored `before_active_digest`, breaking the contract §4.3 “canonical SHA of sorted effective seven + observed Candidate/null” binding.
- Impact: digest agreement is self-consistent but not bound to the required seven-role domain; wrong-shape digests pass shape checks elsewhere.

### 1.3 Legacy branch in selection omits live drift checks

`scripts/survey_publication_set_v2.py:926–963`.

- Superseded rows (`927–935`): takes `new_sha256`/`byte_count` from the record with **no live file hash/size check**.
- Preserved rows (`938–946`): stats live size but **never checks live SHA == record SHA**.
- Missing rows fall back to `canonical7` (`947–949`) without verifying that fallback is legitimate (non-cumulative record).
- Contract §§4–5/7: both old-byte drift and new-set drift refuse; historical + active identity checks before projection. Current legacy selection trusts record bytes for superseded and size-only for preserved.
- Impact: drifted/missing live canonical bytes after legacy R1 pass selection; stale canonical accepted as healthy before-State.

### 1.4 Fallback unknown pointer in selection

`scripts/survey_publication_set_v2.py:839–857`.

- When `_default_candidate_path` raises (profile/source unresolvable), returns `CANONICAL` empty with fallback `root/sources/<issue_id|unknown>/publication/v2/publication-candidate-v2.json`, including literal `"unknown"` when `issue_id` missing.
- Contract §6 + selection §2: “All actual reads validate shape/hash/path/branch/anchor; invalid pointer never falls back” and “no caller-verified objects; defaultpath never permission”.
- Impact: profile drift / missing issue identity is masked as healthy canonical-empty instead of fail-closed refusal; downstream C resolvers treat it as canonical no-op (see §3.1).

### 1.5 Alias laundering in `_repo_file` + missing duplicate-key/FIFO discipline

`scripts/survey_publication_set_v2.py:86–93`; `scripts/survey_production_v2.py:260–269`; `scripts/survey_schema_v2.py:71–81`.

- `_repo_file` calls `core.repo_local_path` which does `(root/value).resolve()` then `relative_to(root)`, then checks `resolved.is_symlink()`. Resolving first erases alias components: `a/link→../b/file` resolves inside root, `is_symlink()` on the canonical target is false, so the alias passes. No ancestor `lstat` walk (contrast P1 `_Collector._check_ancestors` and agent `_reject_symlink_ancestors_reval`, which are not used here).
- `core.repo_local_path` also does not refuse FIFO/socket/device beyond `is_file()` (which is false for FIFO, so refused, but only after resolve; ancestor FIFO directory still laundered).
- `schema_gate.load_and_validate_json` and `core.load_json` use `json.loads` without `object_pairs_hook` duplicate-key refusal. Contract §4 requires “strict objects, duplicate-key refusal”. Current loaders keep last-wins silently before schema validation.
- Impact: symlink-ancestor escape laundered to canonical path; duplicate-key payloads pass schema then hash binding, violating “strict exact types/duplicate keys before file reads, raw lexical no alias/FIFO fail-close”.

### 1.6 Retained Profile cross-binding missing; before-Candidate not cross-bound

`scripts/survey_publication_set_v2.py:619–705` (`_validate_proposal_retention_identity`), `708–784` (`_recompute_before_digest`).

- Checks `proposal.basis.state_ref == before_state_ref` (`637–639`), `retention.basis.state_ref == before_state_ref` (`661–662`), State COPY row bytes == `before_state_ref` (`676–705`). Does **not** check retained Profile (P2R `KEEP Profile` match, staged `KEEP Profile` match per P3S `verify_staged_source:1876–1884` pattern) against the bound proposal/State Profile.
- Contract §4.3 line 85 + §5 line 100: `before_state_ref` must equal bound proposal basis + P2R retained COPY **and** `supersedes`/before-Candidate/digest must agree with **both retained-before derivation and freshly observed current-before**. Current code verifies `before_candidate_ref` file exists/hashes (`580–581`) and recomputes digest from the record’s own `before_candidate_ref` (`736–783`), i.e. self-consistency, not independent retained-before (P1 `candidate-observed`) vs fresh current-before agreement. No check that `before_candidate_ref.path/sha` equals P1-observed candidate or current-before candidate pin.
- Impact: swapped/foreign before-Candidate with matching digest self-consistency passes; retained-Profile substitution not detected.

### 1.7 `_recompute_before_digest` fills missing seven from original instead of refusing

`scripts/survey_publication_set_v2.py:767–769`.

- After deriving legacy effective from latest legacy, fills any missing `PUBLICATION_ROLES_7` from `original_7` with comment “should not happen if cumulative valid”.
- Contract §5: each legacy link’s row union must equal original under its own semantics; non-cumulative record is refusal, not repair.
- Impact: non-cumulative legacy (missing role) is silently repaired to a digest that then matches a similarly repaired selection, hiding anchor error. Must refuse.

### 1.8 `validate_seal` cross-bindings incomplete; staged trio `main` vs `primary` unbound

`scripts/survey_publication_set_v2.py:248–293`.

- Verifies 15-role existence/SHA/bytes (`239–246`), generic `issue_id` agreement for JSON roles (`249–258`, skipping non-JSON without enforcing which roles must be JSON), QA bundle PDF binding (`270–271`), QA `PASS` + result refs (`272–280`), candidate PDF binding (`291–293`).
- Does **not** verify per contract §4.2: each path against §2 (proposal/staged refs or supplied immutable review ref); staged trio (`bibliography`/`style` vs staged manifest declared trio, `main` not `primary`); build-record `declared_inputs/outputs` vs seal `publication-pdf/build-log/pdf-digest`; manuscript `editorial_source` proof refs vs seal `proposal_ref/staged_manifest_ref`; Gate derivation receipt/scope/trio/manuscript binding vs seal; semantic/visual review `reader_manuscript/source/pdf` binding vs seal active seven; `page_count` agreement across bundle/candidate/seal.
- `_validate_proposal_retention_identity` loads staged manifest but only checks `proposal_ref` path/sha equality when dict (`642–644`), `scope_review_ref` existence (`645–648`), `retention_manifest_ref` existence (`650–653`) — never checks staged `main.tex`/`references.bib`/`jgaisurvey.sty` refs against seal `bibliography`/`style`/`validated-source`, nor recipe/build-record binding.
- Impact: wrong-seal/wrong-manuscript/wrong-Gate with matching PDF SHA passes seal; equal-SHA different reviewed path (required §9 negative) not detected at seal layer. Root R1 §H2 already flags `P3S.outputs` uses `main` not `primary` with explicit `main→receipt.primary` mapping required — L seal layer does not enforce it.

## 2. L agent integration — blocking

### 2.1 `_check_editorial_rows` is table-only; full retained-COPY/digest deferred by comment

`scripts/survey_agent_control_v2.py:95–148`.

- Validates seal via `pubset.validate_seal` (`116`), no-second-table (`120–121`), no fake legacy keys (`123–125`), `prior_checkpoint` equality (`133–134`), anchor kind shape (`138–140`), live seal re-validate (`143–147`).
- Does **not** verify `before_state_ref` vs proposal/retained COPY, `supersedes`/before-Candidate/digest agreement, or anchor equality against chain-derived identity. Comments at `126–137` state “Full digest + retained-COPY proof runs inside validate_activation_record … this row check covers table binding only” and “Full equality is enforced in `_resolve`”.
- `_check_revalidation_chain:1205–1207` calls this for every linked editorial record with `live=False`. Historical editorial links therefore never get retained-COPY/digest verification in the chain walk; only the head record gets full proof in `_resolve:1377–1381` (`pubset.validate_activation_record` on pointer path).
- Contract §§4–5: historical validation reads retained COPY, equality mandatory on orphan resume; chain walk must validate each link under its own branch semantics. Current chain trusts linked editorial bytes after table check.
- Impact: forged historical editorial link with valid seal table but wrong `before_state`/digest passes chain; orphan-resume equality not enforced for non-head links.

### 2.2 `_resolve_checkpoint_artifact` never passes revalidation; legacy superseded mapping lost

`scripts/survey_agent_control_v2.py:653–655` vs `363–400`.

- `_validate_checkpoint_record` has editorial guard (`390–395`: no superseded allowance even when `authority.path == prior_checkpoint.path`) and legacy superseded mapping (`396–400`: only when `revalidation is not None and authority.path == prior_checkpoint.path`).
- `_resolve_checkpoint_artifact:653–655` calls `_validate_checkpoint_record(..., pending_basis=...)` without `revalidation`, so legacy path never gets superseded mapping. After legacy R1, live files equal `new_sha`, but check compares live vs original `artifact.sha256` (`409–411`), reporting drift on healthy legacy-adopted bytes.
- Same root cause as §1.1 but on the read path: `resolve_checkpoint_artifact(validation,role)` + stage `_prior_artifacts` cannot return active projection after historical check because historical check itself fails post-R1.
- Impact: normal stage/Preview path fails closed on healthy post-R1 State; active vs historical readback distinction (§9 oracle) untestable.

### 2.3 Chain cycle uses digest only; depth off-by-one; head sequence not pinned to file

`scripts/survey_agent_control_v2.py:1140–1146,1155–1162,1212–1214,1117–1128`.

- Cycle key is `sha256_file(link path)` digest only. Two different record paths with identical bytes (same digest) falsely report cycle; same path with different bytes at different times (should be collision-refused, but if it happened) would not be caught as duplicate link. Low `_walk_chain_backwards:324` correctly uses `(path,sha256)`. Agent must match.
- Depth: `for _ in range(32)` over links plus head allows 33 records; contract says bounded depth 32 total. Must enforce total chain length, not links-only.
- Head sequence derived from `state.publication_revalidation_provenance.path` (`1119`) but never verified that head file bytes equal pointer SHA beyond initial `_load_revalidation_record` (which does check). However `_check_revalidation_chain` does not re-verify head file identity after chain walk (TOCTOU between head load and link walk). `_resolve` does not repeat stable pin checks immediately before first record write / before State replace for the read path (those are H activation duties, but read path should still pin head bytes through walk).
- Impact: malformed-branch negatives (cycle/depth/sequence per §9) not exact; duplicate-link detection differs between L and agent, allowing chain-shape bypass.

### 2.4 `_validate_stage_artifacts` candidate-only; seven-role projection missing

`scripts/survey_agent_control_v2.py:1438–1475`.

- Resolves `publication-candidate` via `pubset.resolve_publication_artifact_path` and compares path equality (`1455–1470`); other roles retain exact canonical template behavior (`1472–1474`).
- Contract §8: `_resolve_checkpoint_artifact` + stage `_prior_artifacts` return **active projection only after historical + active identity checks** for exactly seven publication roles; no research/Architecture/Draft rebinding. Candidate-only check leaves six active roles on canonical paths.
- Impact: stage validation passes stale canonical `publication-pdf/manuscript/bundle/reviews/Gate` in `VERSIONED_ACTIVE` as long as Candidate is active; active-vs-historical drift (§9) not detected.

## 3. C consumers — blocking fail-open fallbacks + missing projection

### 3.1 Every State-aware resolver swallows selection errors and returns canonical base

- `scripts/survey_stage_validation_v2.py:52–55` (`_active_selection`), `78–88` (`_require_active_candidate_binding` hasattr fallback + `except Exception` → raise only after fallback, but `_active_selection` already swallowed), `231–287` (`_prior_artifacts` seal `except Exception → StageValidationError` is correct, but prior-candidate check only).
- `scripts/survey_production_v2.py:32–39` (`_active_selection_or_none`), `42–62` (`_resolve_active_candidate_path:59–60 `except Exception: pass`` → `61–62` canonical default).
- `scripts/survey_profiled_freeze_v2.py:28–47` (`except Exception: pass` → canonical default).
- `scripts/survey_orchestrator_v2.py:148–150,169–170` (`except Exception: return base`), `219–231` (`except Exception: pass` after `except ValueError: raise` — invalid pointer that raises non-`ValueError` e.g. `PublicationSetError(ValueError)` is `ValueError` so re-raised, but `OSError`/`KeyError` from corrupted State/config silently passes).
- `scripts/survey_handoff_v2.py:65–67,83–84`; `scripts/survey_human_gate_v2.py:231–233,249–250,295–296` (same pattern).
- `scripts/survey_editorial_correction_proposal_v2.py:64–66` (`_versioned_active_selection`), `681` (`except Exception: _ver = None`).
- `scripts/survey_editorial_current_authority_v2.py:115–116` (`except Exception: return False`), `scripts/survey_weekly_mechanical_refresh_v2.py:839–840` (`except Exception: return`), `scripts/run_semantic_publication_v2_interactive.py:31–32,54–55`, `scripts/survey_semantic_quality_v2.py:180–181`.

Contract §6 + map-resolution §2: “All actual reads validate shape/hash/path/branch/anchor; invalid pointer never falls back” and “External callers NEVER supply `active_set`/verified-dict/pending boolean; L re-derives everything”. Current C pattern is `try selection except Exception: return canonical base / None → canonical no-op`. Invalid/drifted/unknown-branch pointers become healthy canonical instead of fail-closed refusal.

Impact: highest-priority integration blocker. Corrupted/unknown activation pointers, drifted seals, and unknown branches are laundered to canonical behavior in stage/State/Preview/Freeze/config/orchestrator/handoff/human-gate/R1/wrapper paths. Required §9 negatives (State/predecessor drift, unconsumed/unknown record branch, inert valid set not adopted) cannot pass on public callers; they pass standalone validators only.

### 3.2 `resolve_stage_artifact_path` absent; three duplicate candidate-only wrappers

Per `group-c/report.md` §5 + root R1 §15: frozen `resolve_stage_artifact_path(root,cfg,state,profile,name,template)->Path` is absent in `survey_publication_set_v2.py` (only `resolve_publication_artifact_path` at `998–1035` exists). C maintains three near-identical `resolve_*_artifact_path` copies (orchestrator `131–170`, handoff `54–84`, human-gate `220–250`) plus two more in production/freeze, each with own `hasattr(_setmod,"resolve_publication_artifact_path")` fallback to `sel.candidate_path` raw handling (`orchestrator:159–166`, `handoff:74–81`, `human-gate:240–247`, `production:54–58`, `freeze:38–44`).

Contract §8 requires **one role-aware path resolver with State argument**; fixed DRAFT templates unchanged; publication-candidate token derives active or canonical default; recompute+compare in loaders not only producers. Current state is N parallel tables with divergent swallow semantics, not one resolver. `candidate_path` raw handling duplicates L internals (absolute vs relative, `Path` vs `str`) and diverges from L frozen return keys (`candidate_path: Path` absolute per L `980,991`; C compares via `PurePosixPath` in workflow, see §3.4).

Impact: loader/producer divergence; stale canonical refused in one caller but accepted in another; future H/C caller added against a different copy bypasses the frozen boundary.

### 3.3 Stage `_prior_artifacts` does not project active seven

`scripts/survey_stage_validation_v2.py:231–287`.

- Validates seal (`278–282`) and requires prior `publication-candidate == active` (`284–286`), but returns `result` built from historical checkpoint provenance (`245–269`) unchanged. For `VERSIONED_ACTIVE`, six other publication roles (`reader-manuscript/validated-source/publication-pdf/quality-regression-bundle/semantic-review/visual-review/reader-surface-gate`) remain historical canonical paths.
- Task requirement restated in this review brief: “actual stage prior projects active7 (not just Candidate check)”.
- Impact: normal `VALIDATED_DRAFT`/`RELEASE_CANDIDATE` semantic checks + Preview/Freeze builders consume stale canonical bytes while Candidate is active; active-vs-historical readback distinction fails on public stage path.

### 3.4 Export workflow State discovery + manual-input branch malformed

`.github/workflows/survey-production-v2-export-publication-preview.yml:75–143`.

- `_state_bound_candidate:75–83` globs `sources/*/production-state.json` only. Profile `source_root` for Special issues may live under different roots (prompt flags “profile special under sources?/specials paths”); discovery hardcodes `sources/*`, missing actual issue/source path per Profile. Returns `(states, None)` unused; no per-issue State selection, no `publication_revalidation_provenance` watch beyond trigger paths.
- Manual-input check `100–112`: `_expected = _sel.get('candidate_path')` is an absolute `Path` (L `980,991`); `candidate_rel = PurePosixPath(requested)` is repo-relative. `PurePosixPath(_expected) != candidate_rel` (`105`) is always true (absolute vs relative), so every manual input with matching `issue_id` is reported mismatch, while mismatched-issue stale canonical with non-matching `issue_id` is silently skipped (`111–112` issue guard). `except Exception: pass` (`118–119`) swallows selection/IO errors to canonical fallback.
- Pull-request branch `135–142`: enforces `len(candidates)==1` but not single-issue/single-State/single-revalidation. Two issues changing one candidate each but only one candidate file in diff due to path filter (`sources/*/publication/v2/editorial-corrections/` trailing-slash pathspec) still exports ambiguously. Inert `publication-set.json` without activation is only refused for manual inputs (`114–115`), not for pull-request diffs (where `candidates` counts only `*publication-candidate-v2.json`, so a lone `publication-set.json` change gives `candidates==[]` → generic “exactly one” error, not explicit inert-set refusal).
- Impact: exact State-bound Candidate selection not proven; ambiguous/mismatched inputs not fail-closed per §8; inert set exportable via path-filter gap.

### 3.5 P1 versioned shape mismatch + KEEP not implemented + ordinary receipt after activation

`scripts/survey_editorial_correction_proposal_v2.py`.

- Shape: `_active_effective:447` requires `set(info) == {"path","sha256","origin"}`, but L `resolve_publication_selection:978` returns `{"path","sha256","byte_count","origin"}` (4 keys). Every `VERSIONED_ACTIVE` repeat fails with `VERSIONED_ROW_SHAPE` before any byte check. Exact frozen-key mismatch, not a future test gap.
- KEEP: `_build_graph:683–690` discards from `mutable` only `ORIGINAL`-origin paths + versioned Candidate. In `VERSIONED_ACTIVE`, L `effective7` rows are all `origin: ACTIVE` (`975–978`), so nothing is discarded; prior immutable versioned publication/staged/seal/Candidate bytes remain `COPY_BEFORE_REPLACEMENT` instead of required `KEEP_IMMUTABLE` (§5 line 100). Mutable live State remains COPY (correct), but versioned priors are misclassified as mutable, breaking repeat-correction retention + byte-check semantics.
- Ordinary receipt: `_dispatch_generated_receipt:72–89` returns `None` for old kinds (fallback to ordinary `validate_receipt:1517–1520`); `_final_full_receipt_recheck:1732–1735` unconditionally calls ordinary `weekly/longform_generated.validate_receipt` for `WEEKLY/ LONGFORM` routes even when `_versioned_active_selection` is active. Contract §§3/5/8 + brief: “no ordinary validate after capture; P2V receipt replay never after activation; second pre-Preview correction resolves active-set before-graph”. Current P1 re-runs ordinary current-before receipt validation on the post-activation State, i.e. ordinary receipt after activation.
- Impact: repeat correction (§9 required positive) cannot pass; versioned retention misclassified; ordinary-vs-editorial receipt boundary violated on the public P1 caller (not merely standalone validator).

### 3.6 P2V `receipt_kind` caller param is policy bypass — remove

`scripts/survey_editorial_current_authority_v2.py:119–140`.

- Adds `receipt_kind: str | None = None` to `observe_current_authority:132–135`, with `_require_not_ordinary_receipt_after_activation:119–130` refusing only when caller passes `'WEEKLY'/'LONGFORM'`.
- Root R1 §18 explicitly flags this: “P2V derives mode/receipt from actual State/proposal, never accepts mode selection from caller”. Caller-supplied kind is a caller-verified/policy token contrary to fixed no-caller-token boundary (§6: “no caller-verified objects”).
- `_is_versioned_active_state:101–116` live-loads config via `read_bytes().decode` + `resolve_publication_selection`, swallowing all errors to `False`. Ordinary receipt after activation with corrupted selection therefore proceeds (fail-open) instead of refusing.
- Impact: policy bypass; `WEEKLY` caller omitting `receipt_kind` (default `None`) bypasses refusal entirely — the guard is opt-in, not enforced. Must derive from State/proposal refs, not caller string.

### 3.7 P3S exact-50 vs frozen-37 contradiction; dynamic closure unproven

`scripts/survey_editorial_staged_source_v2.py:92–168` vs map-resolution §4.

- C asserts `_SHARED_PY 30 + _SHARED_SCHEMAS 14 + route3 + staged1 + style1 + recipe1 = 50` (`161–167`). Map-resolution §4 freezes Weekly `8→8`, Longform `14→14`, P3S `37→37` unchanged, with a **separate** editorial 12-closure, on grounds that `verify_staged_source` top-level imports (`41–48`: `p1mod/retention/longform_derivation/longform_generated/production/surface_gate/schema_gate/weekly` — all already in old 27) never import set/editorial/current-authority, and historical scope explicitly never calls P2V/current-State/HEAD.
- Actual top-level imports confirm map-resolution: no `survey_publication_set_v2` / `survey_editorial_publication_v2` / `survey_editorial_current_authority_v2` at top level. New 50 adds `SET_MODULE`, `EDITORIAL_OP_MODULE`, `P2V_MODULE` (via `_SHARED_PY` entries `survey_publication_set_v2`, `survey_editorial_publication_v2`, `survey_editorial_current_authority_v2`) + 5 new schemas + `RECIPE_PATH=.latexmkrc` without a top-level edge. `materialize` calls P2V via **function-local lazy import** (docstring `8–10`), i.e. dynamic edge, while `verify` must not. Single 50-set conflates materialize vs verifier closures; `RECIPE_PATH` (editorial build recipe) has no staged-proof edge at all.
- C report §5 admits “New files pending from L/H report `NEEDS_L/H`, not false PASS (all 50 now present)”. Presence in shared copy is not import-closure proof; no `python -c` AST + `git grep` enumeration vs `contract_files` audit reproduces the 50-set (required by selection §3 + resolution §4).
- Impact: `CODE_DEPS_SHAPE`/`TOOL_DRIFT` either trips on healthy old staged proof (if 50 enforced) or silently omits a real dynamic edge (if 37 kept but materialize P2V edge unlisted). Must return actual top/dynamic/new-closure enumeration with per-function edges, no false `0 missing` claim. Do not silently keep 50 or 37 without that proof.

### 3.8 Canonical-writer refusal placement correct but swallowable; interactive alias laundering

- R1 `scripts/survey_weekly_mechanical_refresh_v2.py:898` calls `_require_canonical_mode_for_r1` after State load (`896`) and before HEAD/profile/guard creation (`899–926`) — placement satisfies “refuse BEFORE destructive action/output/guard”. But helper `823–846` swallows `ImportError`/`Exception` to canonical-only (`836,839–840`), so drifted selection proceeds to guard creation.
- Interactive `scripts/run_semantic_publication_v2_interactive.py:51` calls before delete (`80–87`) — placement correct — but helper `30–32` swallows selection errors and outer `54–55` swallows all non-`SystemExit` errors to proceed. `_safe_owned:17–20` does `path.resolve()` then `relative_to` with no ancestor `lstat` walk; later `is_symlink()` on resolved owned paths (`82–85`) cannot see alias parents. Deletion via alias therefore unlinks canonical bytes through an aliased parent.
- Quality `scripts/survey_semantic_quality_v2.py:196` calls before output (`199–210`) — placement correct — but helper `180–181` swallows.
- Impact: “refuse BEFORE delete/guard” holds on happy path only; corrupted selection bypasses refusal and reaches delete/guard/temp creation. Must propagate selection errors (fail-closed) and use raw-first ancestor checks before resolve (as P1 `_Collector` already does).

## 4. Schemas — one pass, one correction

- `schemas/editorial-publication-set-v2.schema.json:7–68` exactly matches contract §4.2 top keys + 15-role table with `file_ref` values, `additionalProperties:false` throughout — **pass**, no change.
- `schemas/publication-surface-revalidation.schema.json:5–8,96–244` correctly refactors to `oneOf [legacy, editorial]`, branch1 preserves actual 14 required keys + `additionalProperties:false` + `$defs` verbatim vs original `1–161` (no top-level required leak, `supersedes` common edge both branches, `canonical_anchor/before_state_ref/before_active_digest/before_candidate_ref/set_ref` new in branch2 only) — **pass on shape**, subject to §1–§2 runtime enforcement gaps above (schema alone does not prove retained-COPY/digest/anchor checks).
- No `scripts/*.py` or config-self added to `contract_files.pipeline` per C report claim (62→67 with only 5 new semantic schemas) — **registry direction correct** per map-resolution §3, but exact 67-list vs actual `config/survey-production-v2.json` bytes not re-audited here; final-code AST + `git grep` closure vs `contract_files` audit must still reproduce Weekly 8 / Longform 14-or-27 / P3S 37-or-50 / editorial 12 sets exactly (contradiction in §3.7 blocks sign-off until resolved; do not claim `unchanged8/14/37/new12` or `22/27/50` without that proof).

## 5. Required strictness gaps shared by L/C (blocking)

- **Exact types before reads**: L `_check_file_ref/_check_authority_ref` enforce `{"path","sha256"[,"byte_count"]}` exact sets + lowercase hex length + `byte_count>=1` before hashing — correct pattern. But every `core.load_json` / `schema_gate.load_and_validate_json` caller then trusts `record.get(...)` without re-checking exact required sets for `proposal.basis.state_ref`, `retention.rows[]`, `staged.proposal_ref/scope_review_ref/retention_manifest_ref`, `checkpoint.artifacts[]` before use. Missing-field `None` flows into `_repo_file(None)` → `repo_local_path` `TypeError` → `PublicationSetError` (fail-closed by accident, not by explicit shape refusal with stable code). Must check exact shapes before file reads per contract scopes.
- **Raw lexical no-alias/FIFO**: only P1 `_Collector` + retention `_Session` + human-gate `_raw_repo_file` implement raw-first ancestor `lstat` walks. L `_repo_file`, agent `_revalidation_row_path`/`_authority`/`_rel`, stage `_safe_file`/`_authority_ref_path`, production/freeze/orchestrator resolvers all use `core.repo_local_path` (`resolve()` first) + `is_symlink()` after. Must reuse established raw-first discipline with bounded regular-file reads + ownership where implemented, per root R1 §H4, not resolve-then-check.

## 6. H boundary (not reviewed; interface needs only)

- P1 `_dispatch_generated_receipt:83` raises `EDITORIAL_RECEIPT_PENDING` when `_edpub is None`; C report §5 notes H `validate_editorial_receipt` appeared mid-task with `EDITORIAL_RECEIPT_PENDING` fallback. No H correctness finding here. Lead must confirm receipt-kind header (`EDITORIAL_PUBLICATION_SOURCE_V1`) + scope-review binding + `main→receipt.primary` mapping once H2 lands; C must not invent a parallel receipt validator.
- Weekly `8→22` / Longform `14→27` closure bumps reported in H report are **out of scope** here and contradict map-resolution frozen `8→8`/`14→14`. Do not resolve here; root must decide whether editorial receipt gets its own 12-closure (resolution §4) or extends initial closures (selection §3 + H report). L/C review blocks on either until the chosen set is AST-proven.

## 7. Cheap tests are not behavioral integration

- `tests/test_survey_publication_set_v2.py` 10/10 (group-l test report) covers `derive_anchor_empty`, `normalize_rejects_unknown`, `parse_sequence`, `before_digest_deterministic`, `before_digest_rejects_malformed`, `legacy_schema_validates_old`, `revalidation_has_two_branches`, `seal_schema_requires_exact_15`, `seal_top_keys_exact`, `seal_self_hash`. No test exercises `resolve_publication_selection` live/drift/legacy-prefix/editorial-active, `validate_activation_record` retained-COPY/digest cross-binding, `_canonical7_from_validation` post-R1 staleness, or alias/duplicate-key refusal.
- `tests/test_group_c_editorial_consumers_v2.py` 5/5 (C report §4) covers `config_contract_files_only_five_new`, `p3s_exact50`, `group_c_only_frozen_apis`, `refusal_helpers_present`, `resolvers_present`. Presence/shape only; no test proves normal Preview/Freeze/Release in both modes, second pre-Preview correction, `R1×2→correction` cumulative anchor, active-vs-historical readback, or any §9 negative on public callers (wrong seal/manuscript/Candidate, old canonical Candidate after activation, inert set not adopted, research change, equal-SHA different path, stale/failed/missing reviews, build/drift, seal role errors, anchor/sequence/cycle/depth, State/predecessor drift, approved/foreign Candidate, canonical writer after activation, every record/State write/close/late-readback failure with observed delta + resume/healthy control).
- Both reports correctly withhold integration claims pending combined freeze/root review. Their “PASS” wording must not be quoted as operation proof.

## 8. Precise return

All items in §§1–3 + §5 are **CHANGES_REQUIRED** before lead integration or any long authority/build run. Prioritize in this order:

1. Fail-open fallbacks (§3.1, plus R1/wrapper/quality/P1/P2V swallows) — invalid pointers currently become canonical; every §9 negative on public callers is unproven until these propagate.
2. P1 versioned shape (`§3.5` shape, 3-vs-4 keys) + L canonical7 staleness (§1.1) + agent checkpoint without revalidation (§2.2) — repeat + `R1×2→correction` path dead on arrival.
3. Digest exact-seven (§1.2), legacy live checks (§1.3), retained-Profile + before-Candidate cross-binding (§1.6), digest fill (§1.7), seal trio/build/Gate/review bindings (§1.8), editorial chain completeness (§2.1), cycle/depth (§2.3), stage seven projection (§2.4 + §3.3).
4. Single resolver vs duplicates (§3.2), export malformed branch (§3.4), P2V caller token removal (§3.6), P3S 37-vs-50 proof (§3.7), alias/duplicate-key discipline (§1.5 + §5).

Do not author code or alternative design in response. Do not re-review H files. Preserve this report’s read scope; no whole-audit, implementation-acceptance, or production-adoption claim is made. Await H2 correction + L/C revision, then combined-code root review before targeted real execution.

