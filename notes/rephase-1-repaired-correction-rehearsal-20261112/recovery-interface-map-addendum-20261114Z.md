# Recovery addendum 20261114Z — exact-blob + artifact-child plan (read-only)

Base: `recovery-interface-map.md` + `astra-operation-resolution.md` §12 + `profile-git-diagnosis-20261114Z/diagnostic-report.md` + `diagnostic-machine.json` (do NOT repeat 544-DB probe). No restore/commit/resume/writes/tests/imports/network/Production/reconstruct-Git. New file only.

## 1. Verified distinction (source + data)

- Missing is **object**, not OID/tree/header: `cc1c` tree correctly lists `sources/2026-W34/production-profile.json` → `155b78cfd588eb9300349e4568ee7065ae498477`; `cat-file --batch` returns `155b78cf… missing` (2 tokens → helper reports `batch header mismatch`). Diagnosis §1/§7, machine `needed_object_read.missing_objects[0]`, `present 84/1 missing`, batch exit 0. Helper `survey_research_authority_v2.py:739-740` wording defect only; refusal fail-closed correct.
- Exact candidate: `.rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/production-profile.json` → sha256 `a6e3eb3006dde95da008876486cbfc7fdce75f507f7efcd6b0fcaba5e154b21a`, 2371B, blob `155b78cf…`. Provenance `notes/rephase-1-contract/inputs.json` + `phase-4f/inputs.json` + `evidence.json` + `tree.json` + `material-sufficiency.md`. Read-only verified; not restored. Live copies (4 runtimes) are `c2990d4f…`/`2a8c3089…` — must NOT substitute.
- Live `2a8c3089…`/2371B differs ONLY two embedded hashes vs recorded (`e6ae2637…→3adfbda22131…`, `3a36dcea…→b5b955d524…`); names `WEEKLY`/`WEEKLY_MAGAZINE` identical. Diagnosis §4 + `expected-vs-live-w34-profile.diff.txt`; captured file read confirms old hashes, live file read confirms current hashes.
- `_verify_own_epoch_commit:639-799` docstring: proof against RECORDED objects only; never LIVE tools, never HEAD==recorded, never State recursion. `profile_rel` added to `needed` (`:668-695`), `ls-tree` 100644/blob required (`:696-714`), batch 3-token check (`:734-740`). Commit profile bytes used ONLY for `research_profile`/`publication_profile` names (`:773-784`); Contract8 recomputed from COMMIT `config/survey-production-v2.json` + contract files (`:762-793`, mirrors `core.contract_identity`), compared to `record.contract` + `pins.contract` (`:795-798`). No comparison of commit-profile sha to `request.profile_ref.sha256` (`2a8…`) or checkpoint `profile.sha256`.
- Request/profile actual bytes separately validated in `_verify_adopted_graph_full:802-993`: `request.profile_ref` shape + `_verify_sized_ref_bytes` (`:837-856`), `prof_abs` fed to `evidence/views/ledger/completeness` FULL validators (`:946-972`). So restoring baseline blob satisfies mechanical git precondition while adopted graph still validates live `2a8…` bytes. No code patch/waiver needed.

Therefore EXACT blob restoration changes **object DB only** (fill missing `155b78cf…`), no tree/head/liveProfile/State/guard change: tree already expects that OID; `cc1c/ed2dc4` unchanged; live `2a8…`, State `a858…`, guard `387ee54f…/a858…/73ab28ea…` untouched.

## 2. W34 normal resume after fill (not manual recovery)

- Current class `E` + guard held (State `a858…` == COPY-derived expected, guard present, checkpoint `73ab28ea…`, manifest `867eba96…`, work `cc1c/ed2dc4`). Diagnosis §7 + machine `normal_resume_predicates`.
- Normal owner path (requires NEW root dispatch, not this unit): single `resume_bound_attempt` (`survey_prearchitecture_acceptance_v2.py:1422`, `resume_revision:1518` identical) → recompute planned/expected from retained files → verify nonce/planned/before/expected + retention==manifest-7 → `write_checkpoint_as_planned` (idempotent) → `clear_remaining_exact_slots:1006` (7 absent → `absent_legitimate`) → `write_cleanup_completion:1063` → FULL (`:1102` → `:979` now passes) → `release_guard:1132` → `readback_revision:1523` via `resolve_research_authority`. No manual State rollback/guard-delete/pin-rewrite.
- Without fill, resume/readback/`ALREADY_ACTIVE`/new adopt at same commit all hit same missing blob (machine `normal_resume_predicates`, diagnosis §7). No success path without object or epoch change.

## 3. SP: absent tree, not missing blob

- `sources/SP-efficient-llm-2026/production-profile.json` absent from `cc1c/e84/480/b40` trees, index, `log --all` (0), 2523 untracked files. Prepared manifest pins `cc1c`, request/State bind `aff05fd5…`/13748B (`9251f487…`), c8 capture `22f2e822…`/`37be89b9…`. SP adopt would fail at `recorded-commit tree lacks required path` (`:709-711`) before batch. Diagnosis §8 + machine `sp_risk`. Object fill cannot cure; needs new source tree.

## 4. After-W34-guard artifact-only child (proposal for root, not executed)

- Precondition: W34 `RESUME_CLEARED` + completion + `release_guard` + verified `readback` at `cc1c` first. No epoch move before.
- Then root may authorize ONE isolated child commit (parent `cc1c`, inert origin, independent DB, no reconstruct writes): stage ONLY unchanged current profiles — W34 `2a8c3089…` (live) + SP `aff05fd5…` (live, 13748B). No State/records/R/manifests/source code/schemas/tests. Source 773 identical (`a7e40c47…`); new profile-data epoch explicit (new HEAD/tree).
- Effect: new tree contains SP path; SP prepares NEW request/revision (new ID, e.g. `sp-repaired-20261112-r2`) pinning new HEAD/tree + same `aff05…` profile_ref; existing `sp-repaired-20261112-r1` (`694f5e49…`, pins `cc1c`) preserved unadopted. No hand-rewrite of old `expected_head`. W34 new R not needed.
- Old W34 `cc1c` record still reads back: own-epoch pinned to `cc1c` objects (still reachable via parent), `_git_read`/`_verify_own_epoch_commit` never lock HEAD (`:639-653`, `:610-617`), `resolve` rechecks triplet→`73ab28ea…` not HEAD. No current-HEAD lock after guard release.

## 5. Verdict

**`BOUNDED_RECOVERY_PLAN_READY`** — conditional, not authorization:

1. Root accepts baseline-vs-live profile distinction (§1) and authorizes exact `155b78cf…` fill from verified 774 capture only (no live-blob substitute, no network).
2. Single W34 `resume_bound_attempt` + `readback` + independent verification, SP held, no Selection/Architecture.
3. Separate root dispatch for artifact-only child + SP new-request/new-R2 cycle; old W34 `cc1c` readback + old SP_R1 preservation verified; no B2/B4 source features, no code change, no waiver, no manual recovery.

Real blocker if (1) refused: remain `E`+guard `INDETERMINATE`, hold SP, return object/contract gap. No automatic restore/commit/resume performed here.
