# Versioned-renewal implementation — AUTHOR-side recovery/status 2026-10-25 (NOT independent acceptance)

FRESH replacement status task. No source/test/build/fixture/commit work in THIS phase.
Read-only `ps`/`git`/`ls`/`stat`/`sha256sum`/stdlib-`json`+`hashlib` only. Project
validators NEVER imported/called (would execute untested code). No old-runner exec,
no network, no Git mutation, no `AGENTS.md`/source edits, no other-proc stop.

Root context read (not re-verified here): `AGENTS.md` Re:Phase-1 entry,
`outputs/rephase-1-versioned-renewal-precode-assessment.md`, packet
`notes/rephase-1-versioned-renewal-precode/README.md`, mandatory
`astra-precode-gate-resolution.md` incl. §6 (schema-pointer `""` erratum, strict LIVE
`agent.validate_agent_state` retained, no `Path(".")` repair), full SHA
`7d7d5a45…`, `independent-readiness-review.md` final-binding items. This file does
NOT replace those gates and claims NO HumanCommitPoint / NO independent PASS.

## 1. User-facing stopped state vs last success vs unverified diff

- **Stopped state (corroborated, no inference of cause):** `ps -u eariver` shows NO
  renewal/`python3 unittest`/TeX build child. Only system daemons + `agy`, `dbus`,
  `opencode web --hostname 0.0.0.0 --port 4096` PID 1771, `pipewire/*`, plus this
  status shell itself. 1771 is the live OpenCode server with an unrelated
  other-session process not owned here — **DO NOT kill**. No live owned renewal
  worker exists to stop; duplicate-execution risk is currently none.
  `GET /session/status` returned 401 earlier per task brief: no authenticated
  session status available; no credentials/config/network sought here.
  Previous HIGH session `ses_e93e31774ffeKdQEC2frddlLn9` returned EMPTY then
  `resumeTask` cancelled (session-layer signal only, not execution proof). The
  earlier `H provider error` was a different gap, NOT the current cause. Root does
  NOT infer cause; any “provider limit” label below is **hypothesis only, not fact**.
- **Last worklog-verified success (TURN3 checkpoint, 2026-10-24 16:55 JST):**
  `phase-high/20261024T130000Z/worklog.md` (335 lines, 20875 B,
  mtime 2026-10-24 16:55:35+0900) TURN3 §§3.1–3.5 records HIGH
  `1ee7066e04a581f407066bc9e02b84d322864d5f20e3d29a8252210dacf031d9`
  (reported 3048 lines; FILE-everywhere + targets-split + companions-direct +
  T2/T3 tidies present). Run34 `run34-20261025T033000Z/commands.log`
  (14170 B, mtime 16:51:22) + 20 `*-exit.txt` **all `0`** (1 B each), weekly
  `activate-u2-weekly-stdout.txt` + longform `activate-u2-longform-stdout.txt`
  both `{"status":"ACTIVATED",…,"observed":"new"}`, history both
  `{"chain_length":3,"n_bindings":31}`. High22 weekly `T1 d685950 → U1 r2 →
  T2 614c658 → U2 r3`, longform `T1 3b0c168 → U1 → T2 4a69c2e → U2 r3`,
  old E uncommitted, no C1 FILE-era activated, no U3; C1 SELF-era finalize is
  history-only (never retrofitted). FileREF rule is FILE SHA everywhere EXCEPT
  proof `basis_ref` SELF digest named internal; root-rejected H-weakening to SELF
  stands; H companions record-bound correct, no new sidecar.
- **Unverified current diff (DO NOT resume from it blindly):** workdir HIGH is now
  `1620b92c482a5c0c731b27ce7bf27a4eac59c45817da0910b6a7cf4c7a0ba8a2`
  (174208 B, 3045 lines, mtime 2026-10-24 17:23:28+0900) — hash-mismatched vs
  TURN3 `1ee…` AND vs fixture-T2 `f6a61245…` (174426 B, 3049 lines). Bytes of
  `1ee…` were never saved, so only hash-mismatch is provable, not a line diff.
  `H 7e04c7fa…` (201933 B, mtime 16:04:27) and `S d5472266…` (112329 B, mtime
  15:51:46) match TURN3 and are unchanged; `test_high 89d72f90…` (9725 B, mtime
  14:36:54) unchanged. Later run dirs `run35…run61` (mtimes 17:01 → 2026-10-25
  02:02) and fixtures `high23/high24` exist beyond the TURN3 log and are
  **unlogged/unverified** for resume (see §5). Log-tag timestamps
  (`runNN-YYYYMMDDTHHMMSSZ`) are NOT assumed to be wallclock; only file `mtime`
  cited above is wallclock evidence.

## 2. Repo + candidate identity (read-only)

- Reconstruct repo: `HEAD c5b0d7cff9f978a2823f9a9e00ae1e0f9d5b3e1f`, branch `main`,
  `git status --porcelain` = only `?? notes/rephase-1-versioned-renewal-implementation/`
  (this status unit). No ordinary candidate/reconstruct commits.
- Correct writable candidate:
  `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
  `HEAD 409b292756dd1277b9dfae87679934c0d2ce251c` (actual409/tree `8ce36998`),
  `M=39 U=42 total=81`, index clean for tracked (`diff --cached` not re-run here;
  TURN3 recorded clean). `M` = 35 consumer/schema/config overlap + 4 workflow/style
  (list in data.json; `git diff --stat` 39 files, 4632+/606-). `U` = 4
  `versioned-renewal-*.schema.json` + 10 other new schemas + 3
  `survey_versioned_renewal_{history,source,v2}.py` + 9 other new scripts + 16 new
  tests incl. `test_versioned_renewal_high_phase.py`. Rejected M1
  `.../versioned-renewal-impl-.../candidate-work` (fake root `a8890d4`) preserved,
  NOT used.
- Candidate HIGH/S/H pins (stdlib `hashlib`, no validator import):
  HIGH `1620b92c…` 174208 B; H `7e04c7fa…` 201933 B; S `d5472266…` 112329 B;
  `schemas/versioned-renewal-basis-v2.schema.json 76f77ee5…` 8322 B;
  `-publication-set-v2  a7594e63…` 3266 B;
  `-source-manifest-v2 9d58894e…` 11138 B;
  `-source-proof-v2 4c6413ea…` 7222 B. Full lists in `recovery-status-20261025.data.json`.

## 3. Run34 exact evidence (last TURN3-verified success)

- All 20 `*-exit.txt` in `run34-20261025T033000Z/` are `0` (weekly+longform
  prepare/finalize/activate/history/qa/status/head/add/commit). File mtimes cluster
  16:39–16:51 JST (log-tag `20261025T033000Z` ignored for wallclock).
- `activate-u2-weekly-stdout.txt`:
  `ACTIVATED / sources/2026-W37/production-state.json /
  .../wk-boot-1/renewals/high-u2-weekly/publication-set.json`; longform analogous
  under `sources/SP001/.../lf-boot-1/renewals/high-u2-longform/`. `stderr` empty.
- `history-u2-{weekly,longform}-stdout.txt`: both `chain_length 3, n_bindings 31`.
- `commands.log` shows the exact T2-maintenance commit + prepare/finalize/activate/
  history chain for both routes, each `exit=0`. No rerun performed here.

## 4. Exact high22 fixture checkpoint (stdlib JSON only, no `agent` validators)

- Parents: `.rephase-1-editorial-runtime/versioned-renewal-high22-20261025T030000Z/`
  `renewal-weekly HEAD 614c658ffca238fd24da9914ee99fe90b62ca799`
  (`T2 maintenance, dead-assignment tidy, behavior-neutral, trio untouched`),
  parent `d685950` (weekly tool-source before authorities); `renewal-longform HEAD
  4a69c2ecaa0a55b43ae7025613240728e3a696`, parent `3b0c168`; both retain old
  `721a04d` ancestor, old E uncommitted (`?? sources/ surveys/ views-*/ raw/
  architecture-*.json …`), inert `example.invalid` origins, `status` shows only
  those `??` (tracked clean). Tool-epoch HIGH bytes at T2 commits:
  `f6a612451453b504155741df1f258eecc13345a3f822ded531c6183b0f99233d` both routes
  (differs from workdir `1620…`; see §5). Inode-disjointness claimed in TURN3 is
  preserved as history, NOT recertified here (no new inode guard run).
- States: weekly `sources/2026-W37/production-state.json` 5965 B
  `2f2d5686f7a9537c1a9cf21fd728e7c655fbf6a30e8ac2c44ead5a900c0e180b`,
  `lifecycle_state VALIDATED_DRAFT`; longform `sources/SP001/production-state.json`
  5926 B `f4f680572d0c943bc81a196f766fda1df080cc0dc699b5a91cfd7f3a71e28821`,
  same lifecycle. `checkpoints` is null in these fixture States (no named-pointer
  inference made here).
- Renewal dirs present: `high-c1-*`, `high-u1-*`, `high-u2-*` both routes.
  U2 set/proof/Candidate/basis (weekly): set 5320 B
  `c850d33e764a264fb225f238499f01290184bb9ed075377cae59b91447c49f79`,
  Candidate 2038 B `c0758f9a…`, basis 41342 B `08c64909…`, proof 31254 B `0a6fb0c2…`;
  longform set 5277 B `86ddcd63…`, Candidate 2019 B `875bc118…`. Active records:
  weekly `.../publication-surface-revalidation-r3.json` 3562 B `7a059cc9…`,
  longform 3539 B `4d4acd9d…`. QA/quality, `build-record.json`,
  `reader-surface-gate-v2.json`, `validated-source-manifest.json` present under
  each `high-u2-*` (directory listing in data.json; content NOT validated here).
- Provenance rule for resume: U targets come from immediate selected predecessor;
  stored manuscript/build proof may be older typed-lineage ancestor (NOT forced to
  latest proof). Historical tool-epoch rows are owner/path-specific and verified at
  recorded commits; E evidence is live/COPY, NOT required at tool commit. Detached
  proof checks CURRENT tools on EVERY readback (per root map).

## 5. Unexecuted / unverified after `1ee…` (explicit)

- Workdir HIGH `1620…` (mtime 17:23:28) postdates worklog (16:55:35) and run34
  (16:51:22) and mismatches both `1ee…` (TURN3 verified) and fixture-T2 `f6a6…`.
  Line counts 3048 → 3049 (T2) → 3045 (workdir) suggest post-T2 edits; bytes of
  `1ee…` absent so no authoritative diff. **Treat workdir HIGH as UNEXECUTED.**
- Unlogged run evidence after TURN3 (all wallclock by `mtime`, tags ignored):
  `run35` (17:01, C1-targets `exit 1` both routes = expected `RENDER` refusal, not
  a defect proof here); `run36-g1` (17:23, 48 exits all `0`, C1
  prepare/targets/finalize/activate/history green both routes, history shows 3
  refs `EDITORIAL+U1+C1`); `run36-g2/g3`, `run38–61` (mtimes to 02:02 Oct25, many
  all-`0`, plus `run37` lifecycle `exit 1`, `run39` 1 lifecycle `1`, `run43/45/47/49`
  `ed-probe exit 1`, `run55 u3-activate exit 2`). None are in TURN3 worklog; **none
  are adopted as last success** — they are unverified current diff requiring
  root-directed re-verification before any resume decision.
- Newer fixtures `high23` (weekly-only, `HEAD 721a04d`, no HIGH commits — clone
  base only) and `high24` (weekly `HEAD 50b03a6 G6 P1-receipt authoring_refs`,
  longform `HEAD dbdaf61 G3LF P1-integration + current HIGH`, full G1–G6/G1–G3LF
  chains in `git log`) postdate high22 T2. They are NOT the TURN3 checkpoint and
  are NOT verified here.
- Consumer/schema deltas in workdir (`M=39`, `U=42`) vs `409b292` are exactly the
  HIGH+consumer operation scope; fixed-3-new-modules / 4-new-schemas /
  5-existing-schema-branch and replay `63/route`, `66 union`, pipeline `67→71`
  counts are map memberships (per root), NOT measured successor source. Existing
  `R1`/canonical after versioned refusal retained. Any map contradiction returns
  to Astra before broadening.
- Preserved non-cleanups: `__pycache__`/`*.pyc` cleanups happened (root-unauthorized);
  NO further cleanup performed here — preserve everything including residue.
  All 22 `versioned-renewal-high[2-22]*` + base `high-*` parents and 34+ run dirs
  observed present; historical `rm -rf <next-name>` were no-ops; the earlier
  “failed parents removed” claim was withdrawn in TURN3. Do NOT recertify the
  no-op claim without data.
- No `C1 FILE-era` activation accepted at TURN3; no `U3`; `C→U→U`,
  renewal→editorial, normal direct Candidate/Preview/Freeze/Release, explicit
  failure/resume, affected regressions, and independent final implementation review
  are all OPEN and delegated to root next. Detached helper-only completion is NOT
  accepted; both routes + genuine changed-tool epochs in isolated synthetic
  fixtures + repeat `C→U→U` + renewal→editorial + normal lifecycle + failure/resume
  are required scope per assessment §5.

## 6. Scope, limits, and next safe resume plan (status only)

- **Conclusions (bounded):** (a) No live renewal work to interrupt; root
  02:21:52+09 observation corroborated. (b) TURN3 checkpoint (`1ee…` + run34) is
  the ONLY verified resume base; workdir `1620…` + runs 35–61 + high23/24 are
  unverified diff. (c) High22 U2-active fixtures (HEADs/pins/hashes above) are
  intact with old E uncommitted; no candidate/reconstruct commits leaked.
- **NOT concluded:** cause of CoWorker stop (EMPTY return + `resumeTask cancelled`
  are session signals; provider-limit is hypothesis-only); semantic quality of any
  edition (Production semantic NO-GO retained); whole `NOT_READY`/step4B3/audit/
  `DM021+022` closure; representative-quality/Profile/adoption/savings.
- **Safe resume (for root to delegate, NOT executed here):** (1) Re-pin workdir
  `1620…` vs `1ee…`/`f6a6…` + schemas/consumers via read-only hash/diff; decide
  keep vs revert BEFORE any execution. (2) Re-verify high22 U2 States/sets/
  Candidates/proofs with CURRENT tools on EVERY readback (detached check), then
  (3) execute ONLY the root-ordered remainder: C FILE-era redo both routes,
  repeat incl. `C→U→U`, renewal→editorial, normal direct lifecycle, ALREADY_ACTIVE/
  resume oracles, affected regressions, final independent review. No repeat of
  completed run34 U2 positives except as explicitly ordered repeat-chain with fresh
  epochs. No fixture/evidence mutation in status phase (obeyed).
- Evidence: this file + `recovery-status-20261025.data.json` (hashes/paths/mtimes/
  exit tallies). No HumanCommitPoint claimed; ordinary Commit/Push Human-owned.

## 7. Astra status-review corrections (binding over earlier recovery wording)

This status inspection confirms no renewal execution child at inspection time, not the cause of the task cancellation or the internal model-request state. OpenCode itself remains running; the unauthenticated local status request returned401. Do not stop unrelated sessions or infer a provider failure from the empty/cancelled task response alone.

Two statements above require correction before resume:

1. §1's `FILE SHA everywhere EXCEPT proof basis_ref SELF` is incorrect. **Every cross-document `{path,sha256}` ref, including `proof.basis_ref`, is FILE-BYTE SHA256.** SELF digests appear only in the artifact's explicitly named internal digest field. This was the root decision implemented by S and HIGH; the exception proposal in the earlier HIGH mismatch document remains rejected.
2. Later source/run evidence is **unreviewed/unbound in the TURN3 summary**, not established to be unexecuted. The run35–61 artifacts, including run36's zero exits, show later activity requiring inspection. Workdir hash difference from TURN3 is not a reason to revert it or rerun all later positives. First correlate the later run commands/exits, fixture commits, exact source bytes and current States. Preserve all snapshots/partials. Determine the actual latest successful boundary and only then resume the still-unexecuted or failed obligations. Do not revalidate high22 with different current tools and expect its earlier current-eligibility result to transfer automatically.

At root's status inspection the last newly discovered evidence mtime was approximately 2026-10-25 02:02 JST, whereas the worklog's TURN3 entry stopped at 2026-10-24 16:55 JST. Thus the worklog had lagged subsequent activity; this was not evidence that no work occurred after run34. No runtime tests, source edits, artifact repairs or new candidate commits were performed during this status inspection. Whole implementation remains incomplete; this is **not** a Human Commit Point or implementation acceptance.
