# Versioned-renewal evidence reconciliation — READ-ONLY (run35–61 + high23/24 to actual latest bound milestone)

2026-10-25. READ-ONLY Co-Worker reconciliation. Human HEAD `f84fcf5` clean at start (per task brief).
STOP-CAUSE investigation explicitly NOT needed and NOT performed. No cause/API credential lookup.

No project imports/tests/build/source changes/Git mutation/network/old-runner exec/repair/rerun in this round.
Source FROZEN: no authors writing during this read-only round. Candidate/workdir HIGH/H/S/test pins below
are observed current bytes only, not re-authored here.

## 0. Authority and method (FILE-ref ONLY)

Read (not re-verified beyond cited bytes):

- `AGENTS.md` Re:Phase-1 entry — CURRENT 2026-10-24 versioned same-reader renewal PRE_CODE_READY,
  contract `478f0051` incl §11 unchanged, integrated R3 WITH R4/R5/R6 deltas AS OVERRIDDEN BY ROOT.
- `outputs/rephase-1-versioned-renewal-precode-assessment.md` (§5 required successor scope).
- Packet `notes/rephase-1-versioned-renewal-precode/README.md`.
- Mandatory `notes/rephase-1-versioned-renewal-precode/astra-precode-gate-resolution.md` INCLUDING §6:
  `observedSourceBinding.schema_pointer` is string allowing empty string; whole-doc pointer is `""`
  (not `"/"`; `/properties/editorial_correction_scope` is inventory only); strict LIVE public
  `agent.validate_agent_state` retained on canonical path + exact prePreview/Exception window;
  `production.verify_state_basis` is different globally current-pinned API, not a substitute;
  no Screening `Path(".")` repair. Full SHA `7d7d5a4552eb7a1abcbafa79d8f358ff10ec96e885b55f09f271766b136cab57`.
- `notes/rephase-1-versioned-renewal-precode/independent-readiness-review.md`
  Final-binding ROOT resolution review + Final-binding pointer-erratum confirmation.
- `notes/rephase-1-versioned-renewal-implementation/recovery-status-20261025.md` INCLUDING ROOT §7
  + `recovery-status-20261025.data.json` (FILE-ref ONLY).
- `notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z/worklog.md`
  TURN1–TURN3 (335 lines; TURN3 §§3.1–3.5 is last worklog-verified checkpoint, NOT latest activity).
- Phase run dirs `run35-20261025T033000Z` … `run61-20261025T110000Z` + fixtures `high23`/`high24`
  (listed in §3–§5). This reconciliation binds the LATER unreviewed/unbound evidence to the actual
  latest milestone; per ROOT §7 it is **unreviewed/unbound in TURN3, NOT established unexecuted**.
  Workdir hash difference is NOT a reason to revert or to rerun all later positives.

Method in this round (only): `Read` + read-only `bash` (`ps`/`git rev-parse/log/show/status`/
`ls`/`stat`/`sha256sum`) + `python3 -c` with stdlib `os/json/hashlib/subprocess(git only)`.
Project validators NEVER imported/called. No `python -m unittest`, no TeX, no fixture scripts executed.
`commands.log`/`*-exit.txt`/`*-stdout.txt`/`*-stderr.txt`/`overlay-*.txt`/`head-*-stdout.txt`/
`addlist-*.txt`/`ancestor-*-stdout.txt` read as bytes. Fixture `HEAD`/tree/tool-source blobs via
`git show HEAD:<path> | sha256sum` + `hashlib`. State/record/set/Candidate/proof via stdlib `json.load`
+ `hashlib.sha256` on FILE bytes. Log-tag timestamps (`runNN-…T…Z`) are NOT wallclock; only file
`mtime` is wallclock where cited. All cross-document `{path,sha256}` refs below are FILE-BYTE SHA256,
including `proof.basis_ref`. SELF digests appear only in an artifact's explicitly named internal digest
field (no cross-document SELF ref; root-rejected H-weakening stands).

No rerun of any completed case. No repair of any artifact. No new fixture commits. No cleanup
(`__pycache__` residue preserved per status unit). Whole unit NOT_READY; NO CommitPoint; NO independent PASS.

## 1. Correct candidate + current source pins (read-only)

- Reconstruct repo: `HEAD f84fcf5`, `git status --porcelain` clean at task start (no output; verified
  in this round). No ordinary candidate/reconstruct commits.
- Correct writable candidate (read-only here):
  `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
  `HEAD 409b292756dd1277b9dfae87679934c0d2ce251c` (actual409, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`),
  `M=39 U=42 total=81` (index: 39 modified tracked; 42 untracked new: 14 schemas [4 versioned-renewal
  +10 other] +12 scripts [3 versioned-renewal +9 other] +16 tests incl `test_versioned_renewal_high_phase.py`).
  Rejected M1 `.../versioned-renewal-impl-.../candidate-work` (fake root `a8890d4`) preserved, NOT used.
- Candidate pins (stdlib `hashlib`; mtimes JST wallclock):
  - HIGH `scripts/survey_versioned_renewal_v2.py` `1620b92c482a5c0c731b27ce7bf27a4eac59c45817da0910b6a7cf4c7a0ba8a2`
    174208 B, 3045 lines, mtime `2026-10-24 17:23:28+0900`.
  - H `scripts/survey_versioned_renewal_history_v2.py` `7e04c7fa…` 201933 B, mtime `16:04:27`.
  - S `scripts/survey_versioned_renewal_source_v2.py` `d5472266…` 112329 B, mtime `15:51:46`.
  - `tests/test_versioned_renewal_high_phase.py` `89d72f90…` 9725 B, mtime `14:36:54` (per data.json).
  - Schemas: basis-v2 `76f77ee5…` 8322 B; publication-set-v2 `a7594e63…` 3266 B;
    source-manifest-v2 `9d58894e…` 11138 B; source-proof-v2 `4c6413ea…` 7222 B.
- Divergence (hash-mismatch only, no line diff provable):
  - TURN3-verified HIGH `1ee7066e04a581f407066bc9e02b84d322864d5f20e3d29a8252210dacf031d9`
    3048 lines (reported; bytes never saved, so only mismatch provable).
  - Fixture-T2 HIGH `f6a612451453b504155741df1f258eecc13345a3f822ded531c6183b0f99233d`
    174426 B, 3049 lines (both high22 routes at T2 commits).
  - Workdir HIGH `1620b92…` 174208 B, 3045 lines (current; see §2 = high24 G2+ epoch).
  - `1ee…` matches neither `f6a6…` nor `1620…`; per ROOT §7 do NOT revert workdir on this basis.

## 2. Fixture source epochs (actual per-run binding, not assumed current)

Base retained in all fixtures: `721a04d` (SOURCE R7b TEST-ONLY, 721 files) with ancestors
`00397c3` (R7 strict), `ce90246` (R6 strict), etc. Old E uncommitted (`?? architecture-*/raw/selection-*/
sources/surveys/views-*/draft-package*`); tracked clean; inert `example.invalid` origins.
`status --porcelain` in high22/high24 shows only those `??` (tracked clean).

- high22 `versioned-renewal-high22-20261025T030000Z/` (TURN3 checkpoint fixtures):
  weekly `HEAD 614c658ffca238fd24da9914ee99fe90b62ca799` (T2 maintenance, parent `d685950`
  weekly tool-source before authorities); longform `HEAD 4a69c2ecaa0a55b43ae7025613240728e3a696`
  (parent `3b0c168`); HIGH bytes at T2 commits `f6a61245…` both routes (174426 B).
  Tool-epoch HIGH at T1: `2e40fcbba66e…` 171070 B (weekly `d685950`; longform analogous).
  Renewals present: `high-c1-*`, `high-u1-*`, `high-u2-*` both routes. No U3. Active records
  weekly `r1–r3`, longform `r1–r3` (see §4). States VALIDATED_DRAFT, checkpoints null.
- high23 `versioned-renewal-high23-20261025T040000Z/renewal-weekly`:
  `HEAD 721a04d` only (weekly-only; `git log` shows no HIGH TEST-ONLY commits). Clone-base only;
  no HIGH commits observed; no renewal-dirs inventoried here. NOT a runnable renewal starting point.
  No run35–61 `commands.log` references high23 as execution root (all later runs reference
  high22 or high24 paths).
- high24 `versioned-renewal-high24-20261025T040000Z/` (actual latest bound milestone):
  weekly `HEAD 50b03a64627a8bbcc725c7fcbebc3d30dce84c9b` (G6 P1-receipt `authoring_refs` key),
  chain `721a04d → 3d456e5 G1 base → c3a96f0 G2 (E5 loop tidy) → a858237 G3 (F3 tidy) →
  9343b94 G4 (P1 proof context) → 053515d G5 (P1 routing) → 50b03a6 G6`;
  longform `HEAD dbdaf611206050dbc98e7973787ab77076cc4c73` (G3LF P1 integration + current HIGH),
  chain `721a04d → 26c403f G1 base → 140780f G2 → dbdaf61 G3LF`.
  Observed `HEAD^{tree}` both routes `1b54f7f64fcf8541eaddba4cbef9034f8501bbf6` (same tracked tree
  at HEAD; different commits, same tree — recorded as observed, not load-bearing).
  Tool-source HIGH blobs (`git show <commit>:scripts/survey_versioned_renewal_v2.py | sha256sum`):
  G1 base (weekly `3d456e5`, longform `26c403f`) = `37d675619129…` 174245 B;
  G2+ (weekly `c3a96f0/a858237/9343b94/053515d/50b03a6`, longform `140780f/dbdaf61`)
  = `1620b92c482a…` 174208 B, 3045 lines = candidate-work HIGH. Thus candidate-work HIGH is the
  high24 G2+ epoch, not high22 T2 nor TURN3 `1ee…`. `overlay-g1/g2/g3/g4/g5/g6/g3lf-*.txt`
  all `mismatches=[]`; `head-*-pre/post-stdout.txt` pin the exact G-transitions
  (e.g. g1 pre `721a04d` → post `3d456e5`/`26c403f`; g4 pre `a858237` → post `9343b94`; etc.).
- Provenance rule for resume (per root map, restated, not re-proved here): U targets come from
  immediate selected predecessor; stored manuscript/build proof may be older typed-lineage ancestor
  (NOT forced latest proof). Historical tool-epoch rows are owner/path-specific and verified at
  recorded commits; E evidence is live/COPY, NOT required at tool commit. Detached proof checks
  CURRENT tools on EVERY readback.

## 3. Run35–61 exact evidence (per-dir FILE reads; no rerun)

Legend: SUCCESS = `*-exit.txt` `0` (+ stdout `ACTIVATED`/`VALID`/expected JSON where applicable).
SUCCESS_RAW_MISSING_EXIT = stdout shows success (`ACTIVATED`/`ALREADY_ACTIVE`/`RC= 0`/`RC-SET= 0`/
`approval/candidate/merge/release OK`) but corresponding `*-exit.txt` absent (raw gap, NOT code acceptance).
FAIL = non-zero exit or traceback refusal or `Timeout (0:03:00)!` stacks. ATTEMPTED_NO_EVIDENCE =
dir exists but `commands.log` 0 B and no exit/stdout (no outcome). SKIP = phase not attempted in that dir.
`commands.log` tags are NOT wallclock; mtimes `run35 17:01:52 → run61` (Oct24 17:01 → Oct25 02:02 per status unit)
are wallclock only. Tool-epoch binding per run from `commands.log` cwd + traceback paths + `head-*` pins.

- `run34-20261025T033000Z` (TURN3 baseline, reference only): 20 `*-exit.txt` all `0`; weekly+longform
  `activate-u2-*-stdout.txt` `ACTIVATED … high-u2-*/publication-set.json observed new`; history both
  `chain_length 3 n_bindings 31` (per recovery-status). Fixture high22 T2 (`f6a61245`).
  SUCCESS (TURN3-verified; ONLY verified resume base per status unit, now superseded as latest bound
  per ROOT §7 — preserve, do not rerun except as explicitly ordered repeat-chain).
- `run35-20261025T033000Z` (high22; 4 exits): `c1-prepare-weekly/longform-exit.txt` `0` SUCCESS
  (RENDER_TARGETS prepare); `c1-targets-weekly/longform-exit.txt` `1` FAIL (expected RENDER refusal;
  `*-stderr.txt` traceback `prepare_renewal_targets … :1119` on high22 paths). No finalize/activate/
  history in dir → SKIP. Verdict: C1-targets FAIL as oracle (not defect proof here).
- `run36-20261025T040000Z-g1` (high24 G1 base; 48 exits all `0`): clone from
  `versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly`, `head-*-pre 721a04d` →
  `head-g1-post-weekly 3d456e5 / longform 26c403f`, HIGH `37d67561…`. U1 prepare/finalize/activate/
  history/qa both routes SUCCESS (`g1-u1-*-activate-stdout.txt` `ACTIVATED r2 observed new`;
  history 2 refs `EDITORIAL+U1`). C1 prepare/targets/finalize/reviews-qa/activate/history both routes
  SUCCESS (`g1-c1-*-activate-stdout.txt` `ACTIVATED r3 observed new`; history 3 refs
  `EDITORIAL+U1+C1` with FILE `source_ref {path,sha256}` + `schema_pointer ""`). C1 FILE-era redo
  SUCCESS both routes at G1 (supersedes high21 SELF-era C1 history-only; SELF-era finalize never
  retrofitted, preserved as history).
- `run36-20261025T040000Z-g2` (high24 G2; weekly 8 exits all `0`; longform exits partial):
  weekly U2 prepare/finalize/activate/history/qa SUCCESS (`g2-u2-weekly-activate-stdout.txt`
  `ACTIVATED r4`; history 4 refs `EDITORIAL+U1+C1+U2`). Longform U2 finalize/prepare/qa `exit 0`
  SUCCESS; `g2-u2-longform-activate-stdout.txt` `ACTIVATED r4 observed new RC= 0` + history 4 refs
  (`EDITORIAL+U1+C1+U2`) but corresponding `*-exit.txt` ABSENT → SUCCESS_RAW_MISSING_EXIT (raw gap).
  Tool epoch G2 (`c3a96f0` weekly / analogous longform; HIGH `1620b92…`). Verdict: U2 SUCCESS both
  routes (weekly exit-proved, longform raw-only); demonstrates `C1(r3)→U2(r4)`.
- `run36-20261025T040000Z-g3` (high24 G3 weekly-only; 11 exits all `0`): U3 weekly prepare/finalize/
  activate/history/qa SUCCESS (`g3-u3-weekly-activate-stdout.txt` `ACTIVATED r5`; history 5 refs
  `EDITORIAL+U1+C1+U2+U3`). Tool epoch `a858237` (HIGH `1620b92…`). Longform not in dir → SKIP.
  Verdict: weekly `C1→U2→U3` (`C→U→U`) SUCCESS raw+exit; longform `C→U→U` NOT shown here (see run55).
- `run37-20261025T043000Z` (high24; 2 exits): `lifecycle-weekly/longform-exit.txt` `1` FAIL both.
  `lifecycle-weekly-stderr.txt` `StageValidationError: … versioned activation seal invalid …
  doubled `.rephase-1-editorial-runtime/…/renewal-weekly/.rephase-1-editorial-runtime/…` prefix
  (U3+U2 seals)`; longform analogous (U2+C1 seals). Normal lifecycle FAIL (doubled-path artifact
  in one-off check; harnesses pass absolute roots per TURN3 §3.3 — recorded, not repaired here).
- `run38-20261025T043000Z`: `commands.log` 0 B only; no exits/stdout → ATTEMPTED_NO_EVIDENCE, all SKIP.
- `run39-20261025T050000Z` (high24; 2 exits): weekly `exit 1` FAIL (`refusing to overwrite stage
  validation report …/lifecycle-stage-high-u3-weekly.json`); longform `exit 0` SUCCESS
  (`lifecycle-longform-stdout.txt` stage/approval/freeze/manifest/merge/release for
  `high-u2-longform`). Verdict: normal direct lifecycle longform-U2 SUCCESS; weekly overwrite
  guard FAIL (not defect proof).
- `run40-20261025T053000Z`: `commands.log` 0 B only → ATTEMPTED_NO_EVIDENCE, all SKIP.
- `run41-20261025T060000Z` (1 exit): `lifecycle-weekly-exit.txt` `0` SUCCESS
  (`lifecycle-weekly-stdout.txt` stage/approval/freeze/manifest/merge/release for
  `high-u3-weekly-b` distinct `-b` variant). Normal lifecycle weekly-variant SUCCESS.
- `run42-20261025T060000Z` (1 exit): `ed-probe-exit.txt` `0` SUCCESS_AS_REFUSAL
  (`ed-probe-stdout.txt` `REFUSED_TARGET_EXISTS …/ed-renew-1/authoring-input.json`).
  Renewal→editorial probe refused before pipeline (guard oracle).
- `run43-20261025T063000Z` (1 exit): `ed-probe-exit.txt` `1` FAIL
  (`ValueError: renewed manuscript requires explicit renewal proof context` at
  `survey_reader_publication_v2.py:388` via `survey_editorial_correction_proposal_v2.py:1630`
  `_pipeline_data`). Renewal→editorial FAIL (missing proof context).
- `run44-20261025T063000Z` (high24 G4; 6 exits all `0`): `head-g4-pre a858237 → post 9343b94`
  (`HIGH phase TEST-ONLY: G4 epoch (P1 renewal proof context…)`), `overlay-g4 mismatches=[]`.
  Fixture-maintenance only; no U/C lifecycle in dir → renewal ops SKIP.
- `run45-20261025T063000Z` (1 exit): `ed-probe-exit.txt` `1` FAIL
  (`RenewalSourceError: BASIS_CURRENT_TOOL_DRIFT: proof closure drift:
  scripts/survey_editorial_correction_proposal_v2.py` at `survey_versioned_renewal_source_v2.py:1275`).
  Renewal→editorial FAIL (detached CURRENT-tool check firing, per root map).
- `run46-20261025T063000Z` (no exits; 10 stdout/stderr): `u3b-*` weekly prepare/finalize/qa/history
  stdout present; `u3b-activate-stdout.txt` `ACTIVATED r6 … high-u3b-weekly/publication-set.json`
  (no `*-exit.txt`, no `RC=` line in file) → SUCCESS_RAW_MISSING_EXIT. Weekly repeat U3b SUCCESS raw.
- `run47-20261025T064000Z` (1 exit): `ed-probe-exit.txt` `1` FAIL
  (`ProposalError: RECEIPT_REF_SHAPE … StopIteration` for `publication-semantic-input` at
  `survey_editorial_correction_proposal_v2.py:1709-1714`). Renewal→editorial FAIL.
- `run48-20261025T070000Z` (high24 G5; 6 fixture exits all `0` + 10 `u3c-*` stdout/stderr, no `u3c` exits):
  `head-g5-pre 9343b94 → post 053515d` (G5 P1 routing), `overlay-g5 mismatches=[]`;
  `u3c-activate-stdout.txt` `ACTIVATED r7 … high-u3c-weekly/publication-set.json RC= 0`,
  `u3c-activate-stderr.txt` empty → SUCCESS_RAW_MISSING_EXIT. Weekly repeat U3c SUCCESS raw.
- `run49-20261025T071000Z` (1 exit): `ed-probe-exit.txt` `1` FAIL
  (`ProposalError: RECEIPT_REF_SHAPE: renewal receipt lacks routing refs` at `_pipeline_data:1709`).
  Renewal→editorial FAIL.
- `run50-20261025T073000Z` (no exits; `battery-stdout.txt` 19608 B, `battery-stderr.txt` 0 B):
  `SET_VALID true` + `RECEIPT_VALID true` for `high-u3c-weekly` (`proof_ref FILE
  e79756390b88…`; `renewal_basis_ref FILE 7ffd22d15ee6…`; `authoring_refs`/`accepted_refs`
  FILE SHAs; `RC-SET= 0` embedded) → SUCCESS_RAW_MISSING_EXIT. Set/receipt/current-readback
  for U3c SUCCESS raw (not activation).
- `run51-20261025T073000Z` (high24 G6; 6 fixture exits all `0` + 10 `u3d-*` stdout/stderr, no `u3d` exits):
  `head-g6-pre 053515d → post 50b03a6` (G6 P1 `authoring_refs` key), `overlay-g6 mismatches=[]`;
  `u3d-activate-stdout.txt` `ACTIVATED r8 … high-u3d-weekly/publication-set.json RC= 0`
  → SUCCESS_RAW_MISSING_EXIT. Weekly repeat U3d SUCCESS raw (latest weekly activation; history
  r8 verified in run56).
- `run52-20261025T074000Z` / `run53-20261025T080000Z`: `commands.log` 0 B only
  → ATTEMPTED_NO_EVIDENCE, all SKIP.
- `run54-20261025T090000Z` (`commands.log` 0 B + `ed-probe-stacks.txt` 31084 B):
  `Timeout (0:03:00)!` in `survey_versioned_renewal_history_v2.py:450 _git_run` via
  `_git_commit_exists/_git_tree_mode/_git_show_blob/_git_blob_sha` → `_check_observed_binding_row_structural:856`
  → `_verify_versioned_ancestor` → `verify_versioned_history` → `survey_publication_set_v2`
  → `survey_agent_control_v2` → `survey_editorial_correction_proposal_v2 prepare_proposal`
  → FAIL_TIMEOUT. Renewal→editorial probe timeout (stacks only, no exit).
- `run55-20261025T100000Z` (high24 G3LF longform; 10 exits: 6 fixture `0`, `u3-prepare/qa/finalize 0`,
  `u3-activate 2`): fixture `head-g3lf-pre 140780f → post dbdaf61` (G3LF P1 integration + current HIGH),
  `overlay-g3lf mismatches=[]`; `u3-prepare-exit.txt 0` SUCCESS; `u3-qa-exit.txt 0` SUCCESS;
  `u3-finalize-stdout.txt` `REUSED_TARGETS` (+ set/proof/receipt/build/bundle/gate/candidate paths)
  `exit 0` SUCCESS (U3 longform generation); `u3-activate-exit.txt 2` FAIL with
  `u3-activate-stderr.txt {"phase":"ACTIVATE","code":"SEAL_BIND","disposition":"PRESERVED_INCOMPLETE",
  "detail":"low activation-record validation failed: versioned activation history invalid:
  HISTORY_ANCESTOR: history chain chronology must be nondecreasing"}` (no overwrite; preserved
  incomplete). No `u3-history-*` in dir → history SKIP. Verdict: longform U3 prepare/finalize SUCCESS,
  activate FAIL (refusal). This is the run55 u3 refusal: distinguish precisely from later weekly
  repairs — weekly `u3b (run46 r6) / u3c (run48 r7) / u3d (run51 r8)` ACTIVATED are WEEKLY-route
  repairs and do NOT repair longform U3; longform U3 remains FAIL with no longform repair in evidence.
- `run56-20261025T080000Z` (no exits; 4 files): `already-active-stdout.txt`
  `ALREADY_ACTIVE … publication-surface-revalidation-r8.json observed new RC= 0` + empty stderr
  → SUCCESS_RAW_MISSING_EXIT (ALREADY_ACTIVE/resume oracle weekly r8);
  `r8-history-stdout.txt` `HISTORICAL_IDENTITY_VERIFIED true` 8 refs
  (`EDITORIAL 65246288… + VERSIONED 30951f21…(U1)+478c78eb…(C1)+948d6df4…(U2)+d0e578e1…(U3)+
  8c0b3709…(U3b)+06a5868c…(U3c)+f5edec99…(U3d)`) + `observed_source_bindings` FILE refs with
  `schema_pointer ""` → SUCCESS_RAW_MISSING_EXIT. Weekly `C→U→U` + repeat chain history SUCCESS raw.
- `run57-20261025T080000Z`: `commands.log` 0 B only → ATTEMPTED_NO_EVIDENCE, all SKIP.
- `run58-20261025T083000Z` (no exits; 2 files): `merge-release-stdout.txt`
  `approval OK; candidate_sha: 10d9bdac4173 HEAD: 50b03a64627a merge OK release OK` + empty stderr
  → SUCCESS_RAW_MISSING_EXIT. `candidate_sha 10d9bd…` = high-u3d-weekly candidate (cf §4
  `10d9bdac4173…`); `HEAD 50b03a6` = high24 weekly G6. Normal Release-path weekly SUCCESS raw.
- `run59-20261025T090000Z` (`commands.log` 0 B + `ed-probe-stacks.txt` 62686 B): `Timeout (0:03:00)!`
  (same history/git + `jsonschema` frames) → FAIL_TIMEOUT. Renewal→editorial probe timeout.
- `run60-20261025T100000Z` (1 exit): `status-g3lf-longform-exit.txt 0` SUCCESS (untracked `??`
  list only) + `addlist/overlay-g3lf` present. Fixture-status only; renewal ops SKIP.
- `run61-20261025T110000Z` (`commands.log` 0 B + `ed-probe-stacks.txt` 24982 B): `Timeout (0:03:00)!`
  → FAIL_TIMEOUT. Renewal→editorial probe timeout.

No run35–61 dir shows detached helper-only completion; both-routes + genuine changed-tool epochs
(G1 `37d67561…` vs G2+ `1620b92…` + high22 T1/T2 `2e40fc…/f6a61245…`) + isolated synthetic DBs
(no alternates/hardlinks per `work-*.txt`/`overlay` discipline) are present as raw evidence;
independent acceptance still required (§6).

## 4. Per-route matrix to latest bound milestone (actual source per run, not assumed current)

Tool-epoch key: H22-T2 `f6a61245…` (high22); G1 `37d67561…` (high24 G1); G2+ `1620b92…`
(high24 G2–G6/G2–G3LF = candidate-work HIGH). `E` = old uncommitted evidence (live/COPY, NOT required
at tool commit). FILE = FILE-BYTE SHA256 everywhere incl `proof.basis_ref`; named-internal SELF digest
only inside artifact field (see §1 rule).

| Requirement (assessment §5) | Weekly (high24 unless noted) | Longform (high24 unless noted) |
|---|---|---|
| Real R3-format bootstrap | g1 clone `bootstrap-weekly → high24/renewal-weekly`, `head-pre 721a04d → post 3d456e5`, `overlay mismatches=[]`, `addlist` 4 schemas+3 modules+consumers; high22 parent `ada39db/ea8203b` analogous (worklog §4). SUCCESS (exit-proved g1; history raw). | Same with `bootstrap-longform`, `post 26c403f`. SUCCESS (exit-proved g1). |
| U generation (real tool commit + source pin) | U1 (g1 G1 `37d675…`) SUCCESS exit; U2 (g2 G2 `1620b…`) SUCCESS exit (`ACTIVATED r4`); U3 (g3 G3 `1620b…`) SUCCESS exit (`ACTIVATED r5`); U3b/c/d (G4/G5/G6 `1620b…`) SUCCESS raw (`ACTIVATED r6/r7/r8`). Pins §5. | U1 (g1 G1) SUCCESS exit (`ACTIVATED r2`); U2 (g2 G2 `1620b…`) SUCCESS raw (`ACTIVATED r4`, exit missing); U3 (run55 G3LF `dbdaf61`, HIGH `1620b…`) prepare/finalize SUCCESS exit (`REUSED_TARGETS`), activate FAIL `exit 2`. Pins §5. |
| C generation (new trio/current proof/manuscript/build; receipt AFTER build; new postrender reviews) | C1 (g1 G1) SUCCESS exit (`ACTIVATED r3`; `g1-c1-*-targets/finalize/reviews-qa exit 0`; real TL PDFs per worklog Turn2 run29 history, not re-hashed here). Run35 C1-targets on high22 FAIL `exit 1` is earlier RENDER refusal oracle, superseded by g1 FILE-era C1 SUCCESS. | C1 (g1 G1) SUCCESS exit (`ACTIVATED r3`). Same run35 note applies (high22 `exit 1` superseded). |
| Activate / history / current readback | U1 r2 (2 refs), C1 r3 (3 refs), U2 r4 (4 refs), U3 r5 (5 refs) exit-proved; U3b r6/U3c r7/U3d r8 + r8 history 8 refs raw (`HISTORICAL_IDENTITY_VERIFIED true`, FILE bindings, `schema_pointer ""`). States `VALIDATED_DRAFT`, checkpoints null (no named-pointer inference). Detached CURRENT-tool check evidenced by run45 `BASIS_CURRENT_TOOL_DRIFT` refusal. | U1 r2 (2 refs) exit-proved; U2 r4 (4 refs) raw; C1 r3 (3 refs) exit-proved; U3 finalize raw, NO activated history (activate refused). States `VALIDATED_DRAFT`, checkpoints null. |
| `C→U→U` (typed lineage, not forced latest-proof equality) | `EDITORIAL(r1)→U1(r2)→C1(r3)→U2(r4)→U3(r5)→U3b(r6)→U3c(r7)→U3d(r8)` SUCCESS (exits to r5, raw to r8; r8 history 8 refs). U targets from immediate predecessor; stored proof may be older ancestor (per map). | `EDITORIAL(r1)→U1(r2)→C1(r3)→U2(r4)` SUCCESS (exits to r3, raw to r4); `→U3` FAIL at activate (run55 `exit 2`). Longform `C→U→U` incomplete (U3 not activated). |
| Renewal→editorial | Probes `run42 exit 0 REFUSED_TARGET_EXISTS` (guard oracle SUCCESS_AS_REFUSAL); `run43/45/47/49 exit 1` FAIL (proof-context / `BASIS_CURRENT_TOOL_DRIFT` / `RECEIPT_REF_SHAPE` ×2); `run54/59/61` FAIL_TIMEOUT (history/git stacks). NO successful renewal→editorial proposal in evidence. OPEN. | No longform renewal→editorial success in evidence. OPEN (same probe class ran on weekly root; longform route not separately probed to success). |
| Normal direct Candidate/Preview/Freeze/Release | `run41 exit 0` SUCCESS (`lifecycle-stage-high-u3-weekly-b` + approval/freeze/manifest/merge/release); `run58` SUCCESS raw (`approval OK candidate 10d9bd… HEAD 50b03a6 merge/release OK` on U3d); `run39` weekly FAIL (overwrite guard) vs longform SUCCESS (U2 lifecycle). `run37` FAIL both (doubled-path seal). Partial coverage only. | `run39 exit 0` SUCCESS (U2 lifecycle set); `run37` FAIL (doubled-path seal). No U3 lifecycle (blocked by activation refusal). Partial only. |
| `ALREADY_ACTIVE` / resume / fault controls | `run56` SUCCESS raw (`ALREADY_ACTIVE r8`; `r8-history` 8 refs). `run35 exit 1` RENDER refusal oracle; `run37/39` lifecycle refusals; `run42` `REFUSED_TARGET_EXISTS`; `run55 exit 2 PRESERVED_INCOMPLETE` (no rollback/adoption/deletion). Explicit resume/IO/close/fsync/replace/postread/foreign-inode/32/33/cycle/anchor oracles from worklog Turn2 run30 + §5 R1×2 anchor NOT re-executed here — OPEN for affected scope. | No longform `ALREADY_ACTIVE` success in evidence (U3 not activated, so no U3 `ALREADY_ACTIVE`). Fault controls as left (same `exit 2` is longform U3 refusal itself). Resume/IO/close etc. OPEN. |
| Affected regressions / independent final review | `run50` SUCCESS raw (`SET_VALID`+`RECEIPT_VALID` U3c) is narrow set/receipt check only. Full affected regressions (original routes/R1 slow incl R1×2 anchor/DM004 `7/7` + publication/quality/gate/stage + pubset/revalidation/freeze + staged EDQUOT) NOT in run35–61; preserved from Turn2 history only, not transferred. Independent final implementation review NOT performed. OPEN. | Same: no longform regression suite in run35–61; independent review OPEN. |

All SUCCESS above are RAW command/exit/stdout artifacts read via stdlib; NONE is code independent acceptance.
No stale SELF-era positive is claimed: high21 SELF-era C1 finalize is history-only (never activated,
never retrofitted); all `proof.basis_ref` values checked here are FILE SHAs matching basis FILE bytes
(examples weekly C1 `12becfb456ec…`, U1 `05592e61b6db…`, U2 `5d0c717130e5…`, U3 `c27cc385dfdd…`,
U3b `e8c160df1c73…`, U3c `7ffd22d15ee6…`, U3d `8f8428584699…`; longform C1 `ded814b25aed…`,
U1 `343ee8974bb0…`, U2 `aa86aa2f14f9…`, U3 `1630d6db47a8…`).

## 5. Exact latest fixtures + State/record/set/Candidate/proof (stdlib only)

- high24 weekly (`HEAD 50b03a6`, tree `1b54f7f6…` observed): State
  `sources/2026-W37/production-state.json` 5965 B `7fd02fcb5d43…` `VALIDATED_DRAFT`, checkpoints null,
  `selected_record`/`selected_set` null (no selection inference here). Renewals
  `high-c1-weekly/high-u1-weekly/high-u2-weekly/high-u3-weekly/high-u3b-weekly/high-u3c-weekly/
  high-u3d-weekly`. Active records `r1 65246288…(EDITORIAL) / r2 30951f21…(U1) / r3 478c78eb…(C1) /
  r4 948d6df4…(U2) / r5 d0e578e1…(U3) / r6 8c0b3709…(U3b) / r7 06a5868c…(U3c) / r8 f5edec99…(U3d)`
  (record `sha256` = set FILE per history `record_sha`; full per-record sizes/hashes in run dirs +
  fixture `publication-surface-revalidation-r*.json`). Latest U3d set 5488 B `e643c8fa988b…`,
  Candidate 2128 B `10d9bdac4173…`, basis 69684 B `8f8428584699…`, proof 59385 B `ecd4a5cd555c…`
  with `proof.basis_ref FILE 8f8428…` = basis FILE. QA `reader-surface-gate-v2.json` 5951 B,
  `validated-source-manifest.json` 20005 B, `build-record.json` 2205 B, bundle 2622 B (per §3 `ls`).
- high24 longform (`HEAD dbdaf61`, tree `1b54f7f6…` observed): State
  `sources/SP001/production-state.json` 5926 B `17b7aee049e6…` `VALIDATED_DRAFT`, checkpoints null,
  selection null. Renewals `high-c1-longform/high-u1-longform/high-u2-longform/high-u3-longform`
  (U3 finalized `REUSED_TARGETS` but NOT activated). Active records
  `r1 2bd14fc72…(EDITORIAL) / r2 fae26722…(U1) / r3 3e3b72cc…(C1) / r4 610ae01859…(U2) /
  r5 99554deb…` (r5 present as file but U3 activate refused; r5 is NOT an activated U3 binding —
  do not cite as U3-active). Latest activated = r4 U2 (set 5455 B `d10327c28769…`, Candidate 2117 B
  `0a58b0126ed…`, basis 47551 B `aa86aa2f14f9…`, proof 37332 B `172e3b2a01c3…`, `proof.basis_ref FILE
  aa86aa…`). U3-finalized set 5455 B `d797de830879…`, Candidate 2117 B `ec9202773b7a…`,
  basis 53024 B `1630d6db47a8…`, proof 42805 B `f09cfa9a2905…` (`proof.basis_ref FILE 1630d6…`).
- high22 preserved (TURN3 checkpoint, NOT latest): weekly State 5965 B `2f2d5686…`, longform 5926 B
  `f4f68057…`, both `VALIDATED_DRAFT`; U2 sets/proofs/Candidates/basis + active `r3` records per
  recovery-status §4 (weekly set 5320 B `c850d33e…`, Candidate 2038 B `c0758f9a…`, basis 41342 B
  `08c64909…`, proof 31254 B `0a6fb0c2…`; longform set 5277 B `86ddcd63…`, Candidate 2019 B `875bc118…`).
  Do NOT revalidate high22 with different current (G2+) tools expecting transfer (ROOT §7).
- high23: weekly-only `HEAD 721a04d`, no HIGH commits, no renewal activation; NOT eligible.

CURRENT eligible runnable fixture starting point (read-only identification, NOT execution order):

- Weekly: high24 `renewal-weekly` at `HEAD 50b03a6` (HIGH `1620b92…` = workdir HIGH), latest activated
  `r8 (high-u3d-weekly)`, history 8 refs verified raw in run56. Eligible for root-ordered next:
  repeat/ALREADY_ACTIVE/resume oracles, renewal→editorial retry (after P1 receipt/routing gaps),
  normal lifecycle on activated U3d, affected regressions, independent review. Do NOT revert workdir
  HIGH (`1620b92…`) to `f6a61245…`/`1ee…`; do NOT rerun `run34/g1/g2/g3/u3b/c/d` positives except as
  explicitly ordered repeat-chain with fresh epochs.
- Longform: high24 `renewal-longform` at `HEAD dbdaf61` (HIGH `1620b92…`), latest activated `r4
  (high-u2-longform)`; `high-u3-longform` finalized (`REUSED_TARGETS`) but activate refused
  (`HISTORY_ANCESTOR` chronology). Eligible starting point is r4-active with U3-finalized pending;
  U3 activation must NOT be blind-retried — requires root-directed chronology/binding inspection
  (exact instant/ancestor predicates per astra §2 table) before any resume. Renewal→editorial,
  U3 lifecycle, `ALREADY_ACTIVE` on U3, and regressions remain OPEN on this route.

## 6. Remaining raw gaps (unfilled; do not fill by inference)

- Missing `*-exit.txt` where stdout shows success: g2 longform activate/history; `u3b/u3c/u3d`
  prepare/finalize/activate/history/qa; `run50 battery`; `run56 already-active/r8-history`;
  `run58 merge-release`. `RC= 0`/`RC-SET= 0`/JSON `ACTIVATED`/`ALREADY_ACTIVE` are embedded stdout
  only, not exit files.
- `commands.log` 0 B (no command evidence) for `run38/run40/run52/run53/run57`; `ed-probe-stacks.txt`
  only (no exit/stdout JSON) for `run54/run59/run61` timeouts.
- TURN3 HIGH `1ee…` bytes absent (hash-mismatch only, no diff).
- State `selected_record`/`selected_set` null in both high24 States despite `r1–r8`/`r1–r5` record
  files (selection binding requires root-directed re-verification with CURRENT tools on EVERY readback;
  detached check, not history check).
- No per-file SHA pinning here for all 39M+42U paths beyond HIGH/H/S/test + schemas + §5 renewal
  artifacts; closure `63/route`, `66 union`, pipeline `67→71` remain map memberships (per root),
  NOT measured successor source here. Existing R1/canonical after versioned refusal retained
  (no new R1×2 proof here). Full accepted-authority predicate equivalence, per-file pins, tripwire
  table, freeze-snapshot enumeration, build-record variant end-to-end with real disposable build/
  transfer remain OPEN.
- Affected regressions (original routes/R1 slow/DM004/publication/quality/gate/stage/pubset/
  revalidation/freeze/staged) and independent final implementation review remain OPEN.
- `high23` renewal-dirs not inventoried (clone-base only); `high24` inode-disjointness NOT recertified
  here (TURN3 claim preserved as history only).

## 7. Next independent test scope (for root to delegate; NOT executed here)

1. Re-pin workdir `1620b92…` (+ H/S/schemas/consumers) via read-only hash/diff; keep (do NOT revert
   to `1ee…`/`f6a61245…`); preserve all snapshots/partials including `run38/40/52/53/57` no-ops and
   timeout stacks.
2. Independent review of LATER raw positives (g1/g2/g3/U3b/c/d/battery/already-active/merge-release/
   lifecycle `-b`/U2-longform) with CURRENT tools on EVERY readback (detached proof check); do NOT
   assume high22 current-eligibility transfers to high24 epochs.
3. Root-ordered remainder ONLY: longform U3 chronology fix inspection (no blind retry of run55 `exit 2`);
   repeat incl `C→U→U` on longform to match weekly; renewal→editorial (P1 receipt/routing/proof-context
   gaps behind `run43/45/47/49` + timeouts `54/59/61`); normal direct Candidate/Preview/Freeze/Release
   with real PDF where C (weekly U3d + longform U2/U3 after activation); `ALREADY_ACTIVE`/resume oracles
   (weekly r8 done raw, longform pending); affected regressions + final independent implementation review.
   No detached helper-only completion; both routes + genuine changed-tool epochs in isolated synthetic
   fixtures + repeat `C→U→U` + renewal→editorial + normal lifecycle + failure/resume required per
   assessment §5. Any map contradiction returns to Astra before broadening.

Whole implementation remains incomplete; whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN;
Production semantic NO-GO on synthetic editions; fixture reviews are synthetic, never genuine approval.
This is NOT a Human Commit Point and NOT implementation acceptance. Ordinary Commit/Push Human-owned.

(End — read-only; no execution, no mutation, no rerun.)
