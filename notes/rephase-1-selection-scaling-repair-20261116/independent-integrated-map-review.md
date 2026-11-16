# Independent integrated map review — bounded Selection scaling repair

Status: AUTHOR-INDEPENDENT SCOPED REVIEW, MAP-ONLY. No code authorized.
Verdict: **CHANGES_REQUIRED** — combined map not implementation-ready. No GO.

## 1. Method and bounds

- Read ONLY: `astra-repair-resolution.md` FULL §§1–6 (root overrides all earlier errors), `integration-map-final.md` as OVERRIDDEN by root §6, `transitive-dependency-inventory.md`, `current-source-closure-map.md` + machine JSONs, plus active source worktree via Read/Grep.
- Earlier `integration-map.md` / `integration-map-r2.md` / `independent-map-review*.md` / `predicate-reuse-resolution-r3.md` treated as rejected history, not instructions. Not used as authority.
- Source: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` recorded HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` parent `cc1c7fd1…` tree `ec11cf6c…` (head not re-verified with Git here). Final773 manifest `a7e40c47…`/202833B BASE `409b292`, final141 DIRECT409 patch `171812f6…` unchanged per packet README.
- NO code/Git/runtime/imports/tests/fixtures/network/active/shadow/proof writes/subagents/reconstruct readback in this review. No new source certification. Standard-library parse/hash not invoked; recorded hashes quoted, not re-certified.

## 2. Combined authority under review

Author proposal (not approved):
- `notes/rephase-1-selection-scaling-repair-20261116/integration-map-final.md` + `integration-map-final-machine.json` (MAP-ONLY, 108 lines, status MAP-ONLY awaiting root+independent confirmation)
- Supporting (accepted as analysis, not runtime proof):
  - `transitive-dependency-inventory.md` + machine (source-read-only, §§1–8)
  - `current-source-closure-map.md` + machine (source observation only, 70/73/36/41/76 counts)
- Root authority (overrides proposal on conflict):
  - `astra-repair-resolution.md` §§1–6, especially §6.1–§6.4 literal corrections

No implementation dispatch has occurred. No code until explicit root dispatch after this review is resolved.

## 3. Source-grounded confirmations (what the combined map gets right)

Verified by direct Read in active worktree (line numbers are worktree observations):

- C1 — Discovery Raw independent of supplement: `survey_discovery_v2._normalize_record` 121–127 unconditionally reads/hashes every `source.raw_paths` via `_safe_repo_file` + `sha256_file` + `stat().st_size`. `survey_evidence_v2._resolve_phase_supplement_context` 322–330 returns legitimate empty context (`manifest_ref None`, empties) when `authority_supplement` absent. Empty supplement says nothing about Discovery/X/root Raw. Map §0 retraction + inventory §1 correct. R2 §R4(d) correctly retracted.
- C2 — Historical wrapper preserved exactly: `survey_agent_tool_v2._historical_state_basis_wrapper` 53–98 only tolerates `state_sha256` drift after sibling `screening-accepted.json`/`evidence-accepted.json` is_file/no-symlink (71–73) AND `sha256_file(package)==acceptance.package_sha256` (75–76), then in-memory `adjusted.basis.state_sha256=sha256_file(state_path)` 92–95 + `original(...,adjusted,...)` 96. No second wrapper in runner/freshness. Map §§1/5 + inventory preserve this. Proposal to demand stored SHA==LIVE correctly withdrawn.
- C3 — Proof/decision bytes not opened by existing readback: inventory §3.2/§4.2/§7 correctly observes SHA-only cross-bind (`resolve` 1181–1201, checker 3891–3920 shape only). Map §0/§4 new SizedRef rehash as bounded integrity binding (not old-behavior claim) is the correct scope. No new schema/family claimed for this.
- C4 — No Session files: inventory §3.5/§8 correctly narrows “session-root” to in-memory `root_records`/`root_path` for content cores. Map §0 retraction correct.
- C5 — Existing content cores exist for 0AG path: `survey_architecture_v2_base._load_upstream_content` 85–152 (expectations + root_records/root_path, no `implementation_sha`), `_derive_matrix_rows_content` 183–276 (P retained `sha256_file+load_json` per card/view 213–218), `screening._validate_screening_package_basis_content` 1281–1319 (path-identity 1304–1305) vs LIVE `validate_package_basis` 1322–1338 (SHA+`verify_state_basis` 1332–1338), `evidence._validate_evidence_package_basis_content` 1144–1200 (path-identity 1168–1169) vs LIVE 1203–1251 (SHA+verify 1219–1223). Map §5 EU/summary via content cores is source-plausible.
- C6 — Runner/LOW/BASE/attention registries: runner 20–28 imports `agent,agent_tool,architecture(wrapper),discovery,core,low,review_attention,schema_gate,screening`, NO `base` (new edge runner→`base` is real delta); LOW 40–49 top-only `core` shape-only + `schema_gate` + stdlib (B1 leaf preserved, function-local `evidence/completeness` at 459–460 pattern); BASE 15–17 already imports `completeness,evidence,core`. LOW historical7 `low:587–599` (2 modules+5 schemas), `$id`s 601–607, Contract8 recompute 762–798. Closure-map 70/73, 36/41, 76-no-scripts, LOW/base/attention in replay rows, runner absent row but `implementation_control_roots: scripts` bound, no membership expansion for existing 4-file edits — accepted as supporting observation, consistent with reads above.
- C7 — Quantitative correctly qualified: map §1/§9 states 21AG (3+2+1+6 + package-once 3+6) as source/call-graph estimate only, not affordability proof; actual W34-409/SP-160 7-run decides; wall/CPU/rchar to be recorded honestly. Compliant with root §5/§6 (no 250–400s/fits1200 claim, no speedup assumed).
- C8 — Epoch/continuation correctly bounded: map §§7–8 requires new independent byte-copy, meaningful source-only commit in NEW independent DB after root authorization, `verify_current_stage_basis` 42–50 (`implementation_sha==repository_commit_sha` HEAD-only + `validate_agent_state`) under original override 121–143 at run 309–313/432–436 only, no State/Profile hand-repin, no old-implementation override, no fresh-init fixture standing in for saved-State continuation (old init `48082…` history remains). Correct per root §§2/6.3 and F5 qualification.
- C9 — Standalone/LEGACY/completion preserved: map retains public standalone API, LEGACY same-triplet canonical branch (`_dm022_pinned_family` 50–67, `_dm022_resolve_ledger_completeness` 70–98), LOW `_verify_completion_full` 996–1125 with 2× adopted-graph + `lstat_slot` tolerance 1102–1124, no global atomicity/cleanup/rollback claim. Correct per root.

## 4. Load-bearing deviations — CHANGES_REQUIRED (must return to root/author, not invent at implementation)

### F1 — Literal signatures violate root §6.2 (blocking)

Root §6.2 requires:
- `base._validate_candidate_matrix_against_upstream(repo_root, matrix, upstream, profile_path, completeness_path, ledger_path, evidence_path, views_path) -> list[str]` (repo_root FIRST)
- `base._summarize_review_contents(repo_root, upstream, matrix, selection, architecture, profile_path, completeness_path, ledger_path, matrix_path, selection_path, architecture_path, errors) -> dict` (full paths+errors, not 4-dict)

Map §3 + machine `handle` propose:
- `..._against_upstream(matrix, upstream, profile_path, ...)` — missing `repo_root`
- `_summarize_review_contents(upstream, matrix, selection, architecture) -> tuple[dict,dict]` — insufficient 4-dict, wrong return, omits repo_root/paths/errors

Source ground: existing `validate_candidate_matrix(matrix,*args)` 388–397 re-derives via `derive_candidate_matrix(*args)` (which takes `repo_root` first 356–365); existing `build_..._summary` 852–1044 takes `repo_root` + 11 paths + `implementation_sha`. A 4-dict summary cannot bind matrix/selection/architecture file bytes, bases, or accumulated errors. Implementation with map signatures would not satisfy root. **Correct to root literals before code.**

### F2 — Ownership/lifetime/order violates root §6.1 (blocking)

Root §6.1 orders: capture read-set → original full validation → recheck original set → construct checked runner context; LOW read-set is DATA only (no authority); runner-private factory owns validation+context; context/upstream runner-local, LOW never owns `upstream`; exact split:
`LOW:_capture_selection_read_set`, `LOW:_recheck_selection_read_set`, `runner:_prepare_checked_selection`, `runner:_check_selection_boundary`; public functions take no checked bundle/skip flag.

Map §3 proposes different ownership/names:
- `low._get_selection_authority_bundle` + `_SelectionAuthorityBundle` holding `upstream: MappingProxyType|None` (LOW owns upstream — directly contradicts “LOW never owns architecture upstream”)
- `low._assert_selection_authority_fresh` + `low._bundle_upstream_paths` (LOW-owned freshness/bundle, not runner `_prepare/_check`)
- Construction order “pre-capture → full 21AG → seal” omits explicit post-validation full read-set recheck before sealing (freshness §6 is post-seal, not the required pre-seal recheck)
- `base._build_architecture_review_summary_with_upstream(...,implementation_sha,upstream)` carries `implementation_sha` alongside held upstream, implying LIVE re-entry instead of pure 0AG content use

Source ground: LOW header 9–35 forbids caller-dict authority, HIGH-only writes, PATHS-only public entries; runner 243–313 owns sequencing. LOW holding upstream would place architecture responsibility in historian, which root §2 explicitly forbids. **Rename/rescope to root split; move upstream holder runner-local; insert recheck between initial validation and seal; drop `implementation_sha` from with-upstream path (use held upstream + paths only).**

### F3 — Changed-paths omits attention file; internal inconsistency (blocking)

Root §6.3 requires extracting existing attention payload construction+validation into a private pure payload helper in `survey_review_attention_v2.py`, used by both unchanged public builder and writer, and mapping/testing that additional file/import/closure consequence.

Map §7 describes the extraction (correctly: `build_attention` 32–143 returns Path, basis SHAs 119–126, limit/count/truncation 127–139, `validate_attention` 146–159 rehashes 3 paths) but §2 “Changed paths (existing files only)” lists only 3 files (runner, LOW, BASE) and machine `changed_paths_existing_only` lists 3. Attention file absent. §7 says “Map/test that additional file/import/closure consequence” yet §2 does not.

Source ground: `survey_review_attention_v2.py` is already G76 replay member (closure-map), so no membership expansion, but file edit + import/closure delta must be listed. **Add 4th path `scripts/survey_review_attention_v2.py` (private pure helper, no second algorithm/new module) to changed-paths, imports, and closure/G76 impact; or explicitly scope it out with root approval — do not leave §§2/7 inconsistent.**

### F4 — Healthy no-supplement vs supplemented→null downgrade conflated (blocking)

Root §6.4: healthy no-supplement is valid (`_resolve_phase_supplement_context` returns empty context); generic “None+None refusal” withdrawn; test legal no-supplement separately from explicit supplemented→null downgrade refusal.

Map §8 oracle states “No-supp/LEGACY … — no-supplement `None+None` refusal (`evidence:300–330,1194–1198`)” without the separation. Source ground: 300–330 empty context is legitimate (C1 above); card-level `requires-context` refusal when IO actually needed is a different gate. Map retains withdrawn generic refusal. **Split oracles: (a) legal empty-supplement passes on synthetic fixture; (b) explicit supplemented→null downgrade (package previously bound supplement, now absent/null) refuses. Cite exact card predicate, not generic None+None.**

### F5 — Freshness/return and boundary checks need tightening (required, not generic precode)

Map §6 freshness (`_assert_..._fresh` via existing primitives + FULL own-epoch 639–799 every gate) and §7 writes/return (sites 316→319/362→365/427→430/440→443/444→447–448/451→454/456→459–471, preflight 101–114/304, `exists/is_symlink` refuse, `lstat_slot` tolerance, outer return 472–481 re-binds 7 rels+SHAs after final freshness) are directionally right and source-plausible (runner return 472–481 currently returns rels/counts only, no SHA re-hash — inventory §3.8; audit 459–471 binds archive+5 outputs, not itself).

Remaining gaps before GO:
- State explicitly: preflight7-absent runs once; later boundaries require owned-outputs equal producer expected serialized bytes and not-yet-written slots absent (do not re-run 7-absent after first write); completion 7-slot tolerance stays separate; no adopted conflicting output. Map §7 states this but must tie each of the 7 writes to expected-bytes source (matrix/selection/architecture/review/attention/input-archive/audit) with existing serialization helpers named.
- At mutation seams inspect immediate refusal/no-next-write, not merely post-restore equality (root §6.3). Map §8 “mutate → gate refuses, no write” is correct direction — retain and enforce per-seam (not equality-after-restore).
- Partial files remain on failure, no cleanup/retry/rollback; unknown State/guard refuses. Already stated — keep.
- Needed-blob fault ONLY on NEW disposable fixture copy with layout/retained-original control, never `b797…` (already absent/unrelated), never author/implementation/delivery DB; FULL own-epoch batch must refuse. Map §8 states this — keep verbatim at implementation.

### F6 — Test/oracle mapping mostly complete, two explicit gaps

Map §8 covers: full validity on new byte-copy (W34-409/SP-160 all-seven, 7/7 schemas, basis binds, READY, audit binds); late drift per byte (Raw/task/result/card/View/supplement/COPY/State/checkpoint/four-ref/guard/stale-slot) + unlink missing; outer-return/archive drift; nonreuse (fresh invocation, W34 bundle must not validate SP via `issue_id`/triplet ` _load_upstream_content` 108 + `require_same_triplet`); no-supp/LEGACY/history-current on synthetic fixtures; needed-blob disposable; no repeated expensive run for stability (two clean copies same-input 7-output `audit.json` SHA equality, inodes may differ per 1102–1124).

Gaps to close (no new generic cycle, just add):
- Explicit extra-file and symlink negatives via `_exact_regular_files` (screening 99–113, evidence 738–753: missing/extra/symlink/non-file all refuse). Map §2 cites exact-set but §8 oracles only list unlink. Add: extra file and symlink cases on NEW disposable fixtures.
- Explicit input/archive/audit/outer-return binding: mutate `input_path` bytes vs `archive_path`, mutate owned-output between last write and 472–481, mutate State/checkpoint/artifact at return. Partially stated — make per-site.
Helpers listed (runner, architecture, DM022 lifecycle/prearch, late-prepublish, normal-writer, evidence/completeness/active, B-side consumers, agent/tool, C-side, g71/g76 fixtures) are plausible; actual helper selection to be bound at implementation without changing oracle intent.

## 5. Closure and dependency disposition

- `transitive-dependency-inventory.md` accepted as supporting analysis (Discovery Raw, X manifest/tasks/Raws, package prompt/contracts, typed checkpoint artifacts/reports as consumed; proof/decision SizedRefs as new bounded binding, not old full verification; DATA-only fields §§4–7 preserved; no new module/schema/family/global-flag).
- `current-source-closure-map.md` accepted: pipeline 76 with 0 scripts, G76 70/route 73 union, Weekly 36 / Longform 41, DM022 source 7 unchanged (2+5), `_MAPPED_DM022_CODESET` exact, runner control-root bound (not row), no membership expansion for existing 4-file edits (runner→base import, attention private helper inside same file, LOW edit). New module or runner promotion into replay would be explicit expansion (37→38 py etc.) — not selected.
- Unresolved shape must return to root, not invent validators: manifest `profile_ref/discovery_ref/screening_ref` vs request refs, `record.profile` vs `request.profile_ref`, `candidate_outputs`/`proposed_artifacts`/`operation`/`producer_boundary`, retention-plan vs inventory path coincidence — all DATA-only in this path per inventory §§3–4. Preserve full predicates; disclose DATA-only; no second attention algorithm, no bespoke verifier, no global cache, no public skip/caller-dict.

## 6. What remains for GO (bounded, no generic precode cycle)

1. Correct F1 literals verbatim (repo_root first; full-paths+errors summary).
2. Rescope F2 to root split/names/lifetime; upstream runner-local; capture→validate→recheck→seal; public functions take no bundle/skip.
3. List attention file as 4th existing-file edit with import/closure delta (or root-approved scope-out).
4. Split no-supp valid vs downgrade refusal oracles with exact predicates.
5. Tighten F5 per-site expected-bytes + immediate-refusal semantics; keep disposable-only blob faults, partials remain, no auto-retry.
6. Add extra/symlink + per-site outer-return oracles (F6).

After (1)–(6) are re-mapped, independent scoped confirmation + explicit root dispatch are both required before any implementation. Implementation then on NEW independent copy with meaningful source commit (dirty oracles labelled dirty, clean re-run binds committed bytes), actual W34-409/SP-160 all-seven normal-writer completion, fresh CURRENT proof (`verify_renewal_source_proof` CURRENT_PROOF_VALID + SAME-proof drift refusal/restore), exact DIRECT409 `409b292`→new-HEAD patch + manifest + proof-copy `candidate-partial-b40de60` check0/apply0 all-paths×3, scoped689+new, missing26309/bulk31466/runtimeTeX nonbundled + whitespace diagnostics retained, wall/CPU/rchar honestly recorded. Genuine gaps (un-pinnable class, new schema/module/family/global-flag, supplement shape change, Profile P1–P4, DM022-HIGH/LOW residual, Thematic/Retrospective scope) return to root, no auto-broaden.

Quantitative 21AG remains source estimate, not affordability; real 409/160 oracle required. Exact function bodies need not be prewritten, but no load-bearing unknown may remain — F1–F4 are load-bearing and block GO.

No code until root dispatch. Ordinary Commit/Push Human-owned.

(End of review — MAP-ONLY, no implementation, no runtime proof.)

## 7. Correction addendum — combined binding authority reassessed (supersedes §4 blocking, no author rewrite required)

This addendum corrects the §4 verdict per clarification: ROOT §6 is literal implementation map and prevails over superseded author prose. Author old prose is preserved historically; ROOT prevails. Do not require author rewrite merely to repeat already-binding root corrections.

- Corrected verdict: **GO SCOPED WITH MANDATORY ROOT CONDITIONS** — combined `ROOT §6 + transitive-dependency-inventory + current-source-closure-map` is sufficient for bounded implementation after explicit root dispatch. Implementation behavior remains unproved until real W34-409/SP-160 oracles. No code authorized by this review alone.
- Combined binding (SHA256/size, stdlib hash, no fresh source certification):
  - `astra-repair-resolution.md` `6b17919202c42b12a89be8a4ff7f335629d99c11d7de5f66715f373cf1e4b632`/18843B — §§6.1–6.4 literal, prevails on all conflicts
  - `integration-map-final.md` `1570ed8cf9af896b2d86bd4c230df19eeba951f36ff5ed411c356873ecf8df3b`/21925B + machine/11799B — author proposal, §§0/2/3/8 superseded where conflicting, retained otherwise
  - `transitive-dependency-inventory.md` `72bc2a865fe56440b161ed35947571978cff2ca7c719a11d1f96751942b839b1`/37581B + machine/39669B — supporting analysis, not runtime proof
  - `current-source-closure-map.md` `14e88cf3ab2e187a8ed63346f4af3e1493072165d9fde41123e5c01847676c1b`/8385B + machine/10595B — source observation only

### Superseded author sections → corrected root conditions (ROOT prevails)

- F1 superseded: map §3 + machine `handle.shared_projection/against_upstream` (`(matrix,upstream,…)` / 4-dict `->tuple`) are superseded. Corrected binding is ROOT §6.2 literals: `base._validate_candidate_matrix_against_upstream(repo_root, matrix, upstream, profile_path, completeness_path, ledger_path, evidence_path, views_path)->list[str]`; `base._summarize_review_contents(repo_root, upstream, matrix, selection, architecture, profile_path, completeness_path, ledger_path, matrix_path, selection_path, architecture_path, errors)->dict`. Implementation shall use root literals.
- F2 superseded: map §3 `low._get_selection_authority_bundle` holding `upstream`, `low._assert…_fresh`/`_bundle_upstream_paths`, `base._build_…_with_upstream(…,implementation_sha,upstream)`, and “pre-capture→21AG→seal” without named recheck are superseded. Corrected binding is ROOT §6.1: `LOW:_capture_selection_read_set→_SelectionReadSet` DATA-only (no authority) + `LOW:_recheck_selection_read_set` + `runner:_prepare_checked_selection→_CheckedSelection` (owns validation+context, single `run()`) + `runner:_check_selection_boundary`; order capture→original full validation→recheck→sealed runner context; upstream runner-local, LOW never owns `upstream`; public functions take no bundle/skip; with-upstream path uses held upstream+paths only, no `implementation_sha` LIVE re-entry; original initial calls moved inside factory, not duplicated outside.
- F3 superseded: map §2 “Changed paths (existing files only)” 3-file list omitting attention is superseded. Corrected binding is ROOT §6.3+§6.4: 4th path `scripts/survey_review_attention_v2.py` private pure payload helper (existing construction+validation extracted, used by both unchanged public builder and writer; no second algorithm/new module) is explicitly required; map/test that file/import/closure consequence. Membership needs no expansion (already G76 replay member; runner remains non-row control-root `scripts` bound).
- F4 superseded: map §8 generic “None+None refusal” is superseded/withdrawn. Corrected binding is ROOT §6.4: healthy no-supplement valid (`_resolve_phase_supplement_context` empty context); test legal no-supplement separately from explicit supplemented→null downgrade refusal. Implementation oracles shall split accordingly with exact card predicates.

No load-bearing design gap remains in combined ROOT §6 + inventory + closure after above substitution. Exact function bodies need not be prewritten; no load-bearing unknown: all signatures/origins/traversals/closures/writes/oracles are bound by ROOT + C1–C9 above. Quantitative 21AG remains estimate only; real 409/160 decides.

### F5/F6 as mandatory implementation conditions (ROOT §6.3/§6.1, no generic precode)

- Expected-bytes binding: each of 7 writes compared to producer expected serialized bytes immediately + at later boundaries/outer return; not-yet-written slots absent (preflight7-absent once, not re-run after first write); completion 7-slot tolerance separate; no adopted conflicting output; partials remain, no cleanup/retry/rollback.
- Immediate refusal/no-next-write at mutation seams (not post-restore equality): first-write, late Raw/X/task/result/card/View/supplement/COPY/State/checkpoint/four-ref/guard/stale-slot, input-vs-archive, owned-output drift to return 472–481, State/checkpoint/artifact at return.
- Exact-set containment: missing/extra/symlink/non-file refuse via `_exact_regular_files` (screening 99–113, evidence 738–753) + ancestors/containment + parent closure; test extra-file + symlink negatives on NEW disposable fixtures (never author/implementation/delivery DB; never `b797…`).
- Needed-blob fault ONLY on NEW disposable copy with layout/retained-original control; FULL own-epoch batch 639–799 must refuse every gate; restore then re-verify.
- New independent byte-copy, meaningful source-only commit after explicit root dispatch; old init480 + EVIDENCE_REVIEWED history preserved; no State/Profile repin, no old-implementation override; `verify_current_stage_basis` under original override only at run 309–313/432–436; fresh CURRENT proof required; DIRECT409 patch+manifest+proof-copy, wall/CPU/rchar honestly recorded; genuine gaps return to root.

Implementation behavior unproved until oracles pass. No code until explicit root dispatch. Ordinary Commit/Push Human-owned.

(End of correction addendum — MAP-ONLY, combined ROOT-prevails GO SCOPED.)

