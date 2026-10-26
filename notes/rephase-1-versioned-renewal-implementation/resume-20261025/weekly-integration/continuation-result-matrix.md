# Weekly continuation — result matrix (repair 739, G5→U4→P1→lifecycle low-level)

HumanHEAD `f84fcf5` (packet untracked only, verified). Selected `478f0051` §11, ROOT `7d7d5a45` §6. Repair INPUT READONLY `.rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work` (739, manifest `8b14885ab6c331738e2066f24f24c48e3a10b2daabe0b8a80ddb7c42f5a46f1`, all-file `20f1967f...`). H `6fe86e78...` (288349B, node-once-per-PUBLIC, no-authority-cache, root `astra-integration-corrections.md`), P1 `825dba1d...` (158652B, strict new-kind dispatch, public dispatcher/per-kind scope fields), PUB `3f4039fd...` (125977B, shared wrapper union + M1/M6 typed transitives), HIGH `9a0469ef...` stable, Reader `098a2c82...` stable, S `20f63eaf...` stable. 3 new tests (P1 dispatch, Freeze transitive, H traversal-opt) included but not executed here (unit-only, no fixture DB).

No candidate/INPUT/old-fixture edits. Old 736 snapshot + first fixture (`.../versioned-renewal-weekly-20261025T052132Z/renewal-weekly` HEAD `6141dad`, r5 VALIDATED) + all raw preserved (no cleanup/reset/purge/network/old-runner/ordinary commits). Only NEW independent copy + WEEKLY continuation harness/evidence. Fresh Python per tool commit, unique UTC dirs + raw exits/source identity, 1200s timeouts, TMPDIR workspace-local, monotonic `recorded_at` (prev max +1s vs wallclock distinct).

## Fixture

- NEW copy `.../versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly` from valid prePreview r5 (`6141dad`) via `git clone --no-hardlinks` + E manifest exact (untracked 204 + ignored 3 incl `.../high-c1-weekly/build/main.log`, `.../main.pdf`, renewal r2-r6 + `wk-ed-renew-1/2/3` + lifecycle + artifact docs). `E_HASH_UNCHANGED`, `nlink_bad=0`, `inode_overlap=0`, no alternates, no `GIT_*`. See `continuation-setup-20261025T083000Z/commands.log`.
- Overlay 739 except style (preserve G2 variant `a4bd135a...`, otherwise shipping `035645...` would change outputs and force C not U). `OVERLAY_738_OK`, style `a4bd...` preserved. SOURCE-only add 8 files (H/P1/PUB + S revert G4 marker + `survey_weekly_derivation_v2` revert G2 marker + 3 new tests), overlap E 0. G5 `6e82e97931151eeccb4fcadf51449f2bd479cfa0` (parent `6141dad`, ancestor `721a04d` OK, message repair 739 preserve style for U reuse). Variant manifest `continuation-g5-20261025T083000Z/variant-manifest.json`: `739 BASE + style a4bd variant; H6fe86/P1825dba/PUB3f4039 new; S/weekly_derivation revert previous synthetic markers to shipping (history preserves markers, live is shipping + style variant)`, not pretend byte-identical shipping tree. Pins after G5: H `6fe86...`, P1 `825dba...`, PUB `3f4039...`, HIGH `9a04...`, Reader `098a...`, S `20f63...`, style `a4bd...`. Fresh Python after commit (subprocess CLI, no stale imports).

## U4 (G5 tools current, REUSE, style unchanged) — SUCCESS

Dir `continuation-u4-20261025T084100Z`, all 0:

- `c-u4-prepare` 0 (`high-u4-weekly`, REUSE_TARGETS, prior r5, basis `.../high-u4-weekly/renewal-basis.json`, synthetic `2026-10-25T08:41:00Z` = max(prev `05:36:08Z`+1s, wallclock), distinct).
- `c-u4-qa` 0 (fresh QA, synthetic, exact bytes, 3 checks).
- `c-u4-finalize` 0 (`REUSED_TARGETS`, set `.../high-u4-weekly/publication-set.json`).
- `c-u4-activate` 0 (`ACTIVATED r6`, record `.../publication-surface-revalidation-r6.json`, reason G5 repair bringing current, executor continuation).
- `c-u4-history` 0 (`HISTORICAL_IDENTITY_VERIFIED` 6 refs EDITORIAL+U1+C1+U2b+U3+U4, `schema_pointer ""`, FILE SHAs). Older proof (r5 U3, G4 epoch) HIST, new proof (r6 U4, G5 epoch `6e82e97`) CURRENT; older proof stale refusal expected (detached CURRENT drift, not bypassed – U4 re-derives with new tools, does not reuse old proof bytes as current).
- Brings new P1/PUB/H tool source current BEFORE P1 (as ordered).

## P1 renewal→editorial changed-reader (r6-active, G5 tools) — SUCCESS (short positive)

Dir `continuation-p1-20261025T084322Z`, `cp1-stage-authoring` 0 (canonical `core.json_bytes` write, new ID `wk-ed-renew-4`, Weekly envelope edit: headline/deck changed + 3pp incl exact synthesis `The accepted source authors describe the tested method.`, preserve old invalid `wk-ed-renew-1/2/3` partials, no edit/delete), `cp1-p1-prepare` 0 (1200s, no timeout, no cProfile needed).

- Previous blocker `RECEIPT_KIND_UNKNOWN: VERSIONED_RENEWAL_SOURCE_V1` in `_dispatch_generated_receipt` (old 736 P1, r5) FIXED by repair P1 `825dba...` (new public dispatcher: renewal kind → `validate_renewal_receipt` detached CURRENT, per-kind scope fields, no cross-kind guess). Active U4 receipt `VERSIONED_RENEWAL_SOURCE_V1/WEEKLY_GENERATED_V2` with `authoring_refs` + `reviewed_reader_ref` now dispatches correctly.
- H new traversal-opt: `r8 schema 1360→75 calls, 29→3.8s under profile` (per repair note); actual P1 here completed well within 1200s (exit 0, no faulthandler dump, no cProfile trigger). No global cache/source weakening/runtime override. Timestamps `wallclock vs synthetic` distinct, monotonic (`prev_max r6 08:41:00Z` → synthetic `08:43:22Z`).
- Extended pipeline P2R→scope→P2V→P3S63→prepare REAL PDF→reviews→finalize→activate: OPEN (P1 short positive both routes already code-author per task, extended unexecuted in repair; this continuation proves P1 short positive on Weekly with new tools, extended remains for next worker with same G5 epoch).

## Lifecycle low-level on r6 U4 (PUB shared-wrapper fix verify) — SUCCESS

Dir `continuation-lifecycle-20261025T084944Z`, `cl-lifecycle` 0, State pinned True (artifact-level, no State mutation in this low-level path).

- `stage.validate_stage` + synthetic Preview (`NO genuine Human approval`, explicit fixture label) + `build_freeze` + `validate_release_manifest` + `build_merge_verification` + `build_release_record` all PASS (previous blocker `renewal checkpoint wrapper evidence artifact materiality-ledger not allowed (exact producer map)` at `survey_publication_v2.py:684` FIXED by PUB `3f4039...` shared wrapper union + M1/M6 typed transitives). Full Freeze exact guard scope, no helper placeholder. PDF 5 pages, HEAD `6e82e97` (G5), seal `.../high-u4-weekly/publication-set.json`, Candidate/QA/Gate/typed proof bindings via seal roles. Synthetic reviews explicit, content NO-GO retained.
- Public agent transitions to full RELEASED actual State (stage.validation→agent build/advance to RELEASE_CANDIDATE→synthetic Preview→profiled Freeze→Release advance/readback, exact gates/state/provenance write windows, SourceRoot same fieldscan canonical Profile immutable): OPEN (required independently from editorial result; this low-level proves Freeze fix, public RELEASED with State mutation remains for next worker, either on editorial-active branch or via clone NEW prePreview U4 snapshot read-only DB disjoint fork as ordered).

## Artifact/ALREADY controls (new state, code affected)

- `ALREADY_ACTIVE` on r6 set (canonical path) 0 (`ALREADY_ACTIVE r6`, readonly, no new record, strict CURRENT set validate/readback). Alias helpers unchanged (HIGH `9a04...` stable, existing coverage sufficient); new state check passes (same `HIGH_PATH` REFUSED logic, not re-proven here beyond canonical ALREADY).
- Artifact-only `afab176` (docs note, no Core change) after U4: history r6 0 (`HISTORICAL_IDENTITY_VERIFIED`, readback only, not new renewal reason).

## Raw exits

- Setup: `clone-0`0, `remote-0`0, `cfg-*`0, `noalternates`0, `add-739`0, `commit-g5`0.
- U4: prepare/qa/finalize/activate/history 0.
- P1: stage-authoring 0, prepare 0.
- Lifecycle low-level: `cl-lifecycle` 0.
- Controls: ALREADY 0, artifact-readback 0.

## Provenance, no whole PASS

- Current fixture HEAD `afab1762a90ca568b333abae7f1641ea64bdb5df` (G5 `6e82e97` + artifact), tree after U4/P1/lifecycle (renewals `high-u4-weekly` + `wk-ed-renew-4/authoring-input.json` + lifecycle `high-u4-weekly-continuation/` untracked, E preserved). Active `r6 dbeba4cb...` (U4), State VALIDATED_DRAFT (prePreview, provenance r6). Old renewal proof fresh (C1 `bd2e39...` older ancestor preserved byte-identical).
- Code changes NONE to shared candidate/INPUT/old fixture (fixture-only SOURCE G5 + artifact docs, E/renewals uncommitted, no reconstruct commit).
- No whole-unit/independent PASS/CommitPoint. Root to coordinate extended editorial (P2R→...→activate, EDITORIAL63 history scope under new epoch) + public RELEASED via agent transitions (full State) + affected HISTORY/P1/Freeze/lifecycle regressions + independent final review. Previous blockers (P1 dispatcher, Freeze wrapper) FIXED and verified; H perf improved (no timeout).
