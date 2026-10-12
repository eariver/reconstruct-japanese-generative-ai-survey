# DM021-P1 independent closeout supplement (scoped, read-only)

2026-10-12. Author-independent scoped closeout reviewer; continues the prior
final correction4 review (`independent-final-resolution.md`, SHA
`78c3c9da...`). Read that resolution plus `evidence-qualification.md`,
`astra-closeout-resolution.md`, and `closeout-20261012T121721Z/
{verify_current.py, verify-current.raw.log, verify-current.json}`. No source/
schema/test changes, no tests, no old-script execution, no network, no DB/
index writes, no commit, no broader audit. All statements below are
read-observed at review time.

## 1. Mandatory erratum adopted: historical `add -N` disclosure

Root erratum (`astra-closeout-resolution.md` item 3) is ADOPTED as mandatory
and binding on this closeout:

- `evidence-qualification.md:57-60` wording — "Prior `add -N` + reset occurred
  ONLY in disposable gen/verify copies ... ACTIVE `diff --cached` is currently
  empty" — is TOO BROAD and historically FALSE.
- Actual history: the FIRST correction generator
  (`evidence-20261011T235631Z-correction/gen_correction_patch.py`, docstring
  "Uses `git add -N`" + "Read-only to active repo except transient `git add -N`",
  `REPO`=ACTIVE candidate path, `run_git("add","-N",*NEW)` + `run_git("reset",
  "HEAD",--,*NEW)`) transiently used `git add -N` in the ACTIVE candidate index
  and then reset it. That avoidable index mutation (intent entries, no commit,
  worktree untouched) is preserved/disclosed in that packet's report and in the
  prior independent review (§7/§8(ii)), which correctly recorded "transient
  `add -N` in active ... reverted ... do not repeat."
- Later generators, including final correction4 (`gen_correction_patch.py`
  copy-based: byte-copy ACTIVE to `R3-gen`/`R4-gen` temp, `add -N`+`diff` THERE,
  patch copied out, temp deleted), use disposable copies only; current ACTIVE
  `diff --cached --name-only` is empty (re-observed here via
  `verify-current.json`: `active_cached_empty=true`, `cached=""`, HEAD actual409).
  No candidate commit/branch resulted from any of these.
- Do NOT reinterpret current index emptiness as proof the earlier active-index
  mutation never occurred. Future patch generation must stay copy-based. This
  erratum does not alter bytes/pins; it corrects the historical record only.

## 2. Current evidence versus historical/continuous-proof limits

- Filtered `named_status` vs FULL raw: `run_final.py:100-108` FILTERS status to
  the 13 expected rows (`for line ... for exp ... if line==exp: keep`) and does
  NOT reject unrelated rows — extra rows would be silently ignored (code fact,
  stated in closeout log lines 6-10). The bound for THIS run comes from
  elsewhere: saved `freeze-pre.json == freeze-post.json` FULL (verified
  `pre==post`, `saved_pre_status_is_exact13_full_raw=true`), and closeout
  `verify-current.json` compares FULL raw CURRENT active/copy status (673 bytes,
  exact 13) to saved freeze-pre (`active_status_full_eq_freeze_pre=true`,
  `copy_status_full_eq_freeze_pre=true`). A closed unexpected-delta reject
  predicate is NOT certified; only full-raw equality at these pins is verified.
- Capture-at-run pins: `freeze-pre/post` 13 hashes/modes/bytes are capture-at-run
  (pre vs post at run time), not independent static preknown hashes. CURRENT
  active/copy 13 == freeze-pre (`active_13_eq_freeze_pre=true`,
  `copy_13_eq_freeze_pre=true`, all `0o664`, patch `85e9d9ab...` 604448B/13
  diffs) proves no drift SINCE the run; it is not retroactive per-run proof and
  not a static baseline certificate.
- Whole-`.git` separation vs HEAD-inode-only: original `proof_apply.py`
  object-separation compared ONLY `.git/HEAD` inode (lines 69-74 equivalent) —
  narrow and insufficient for full separation (stated in closeout log + root
  item 2; prior evidence keeps that narrow scope, not repaired retroactively).
  Current closeout walks the ENTIRE `.git` read-only (`lstat`, no follow):
  ACTIVE 134 files / COPY 134 / workspace 1075; 0 symlinks in ACTIVE/COPY;
  0 `nlink>1` in ACTIVE/COPY; shared `(dev,ino)` counts 0/0/0 across all three
  pairwise; no alternates; inert remotes (`example.invalid`); index empty;
  HEAD inodes differ (prior narrow check now subsumed). This proves CURRENT
  separation/equality at observation (`verdict=CLOSEOUT_CURRENT_MATCH`,
  `errors=[]`), not retroactive copy-time or continuous no-drift proof:
  repeated equal snapshots cannot exclude an intervening change restored before
  observation. Workspace HEAD `ab17af4...` distinct; workspace status only
  `?? notes/rephase-1-dm021-p1/` (this evidence itself).

## 3. Component verdict standing

The bounded correction4 component verdict (BOUNDED_PASS, D1+E1 at module
`5d2fde45`/test `f581fad0`/schema `5623c0d9`/pre-TeX `e8598239`, 36/3308.284s +
AS-SAVED apply proof) CAN STAND **if and only if** taken together with the
mandatory erratum (§1) and the limitations in §2 plus all prior scope limits
(read-only preparatory `REVIEW_REQUIRED/REVIEW_BOUND_PROPOSAL` only; retention
plan != retained bytes; whole NOT_READY, DM021 OPEN; no adoption/retention/
publication proof; old runs keep own scope, no count transfer). No additional
source/schema/test change is required by this closeout.

Actual blockers: NONE. No file/hash/mode/status/index/alternates/remote/
separation mismatch was observed; `verify-current.json` reports zero errors and
`CLOSEOUT_CURRENT_MATCH`. Any future claim beyond current-state equality at
these pins (continuous no-drift, closed reject predicate, retroactive per-run
certification, generic safe-rerunner) would need new evidence and is NOT made
here.

Prior records preserved unmodified; this supplement adds only this file. Stop
at Human Commit Point; Commit/Push Human-owned.

## 4. Reviewer erratum (evidence precision; earlier wording preserved)

Lines 55-56 phrase "proves no drift SINCE the run" is imprecise and is
corrected here without altering the earlier text: observed equality proves
byte/mode/status match AT the recorded observations only (freeze pre/post at
run time; CURRENT active/copy at closeout observation). It cannot prove
continuous no-drift between observations and cannot exclude an intervening
change-and-restore that returns identical bytes before the next observation.
This matches §2 lines 67-69 and the root limitation. Verdict in §3 is UNCHANGED
(BOUNDED_PASS with mandatory erratum §1 + limitations §2).

## 5. Final closeout 170955Z review (current observation only; NOT verifier certification)

Read `closeout-20261012T170955Z-final/{verify_final.py, closeout-note.md,
verify-final-20261012T170955Z-corrected.raw.log/.json}` plus the preserved
initial pair (`verify-final-20261012T170955Z.raw.log/.json`, exit-30 parser
failure). No scripts run, no source/test touched. This section is current-
observation review only; it does not certify the verifier itself.

- Prior walker/remote gaps closed as current checks: `verify_final.py`
  `walk_git_strict` lstats EVERY `.git` entry INCLUDING directories via
  `os.scandir` (any traversal/stat error, symlink, non-regular non-dir, or
  `nlink!=1` recorded as error — no silent `continue`); observed active/copy
  229 entries (95 dirs + 134 files), workspace 1341 (266 + 1075), 0 symlinks /
  0 nlink_bad / 0 stat_errors everywhere; cross-repo `(dev,ino)` sharing 0/0/0.
  Remote/pushurl/rewrite allowlist is exact on repo-local origins
  (`file:.git/config*`): single `remote.origin.url` equal to the expected URL,
  no `pushurl`, no `url.*.insteadOf/pushInsteadOf`, no `include.*`, no proxy
  keys, no extra remotes, effective `remote -v (push)` token equality.
  Observed: active/copy `remote_exact=true`, workspace `remote_exact=true`
  (github URL), `errors=[]`, `verdict=FINAL_CURRENT_MATCH`.
- Residuals explicitly dispositioned (documentation/runner scope, NOT blockers
  at these pins): (a) config helper evaluates repo-local origins only; global
  effective records (credential/user keys in saved config) are recorded
  informational and can never satisfy the allowlist — a global `url.insteadOf`
  style rewrite would not be evaluated, so NO generic inert-remote
  certification is claimed; observed repo-local keys show no rewrites at these
  pins. (b) rewrite-key match uses camel-case suffixes (`.insteadOf`/
  `.pushInsteadOf`); a normalized/lowercased rewrite key form could miss —
  noted as matcher limitation, no such keys observed. (c) effective-push helper
  count/token predicate is imperfect (length-then-token double structure);
  observed single push line with exact token equality, but no general push-
  parsing certification. (d) lowercase `ls-files -v` tags are assume-unchanged/
  skip-worktree markers, NOT intent-to-add; the "index-empty" claim herein means
  no staged/intent delta (cached empty + zero staged index-column rows + zero
  lowercase tags — all observed empty), NOT a literal empty Git index; it is
  supported by the actual FULL exact status (673B exact13) + cached evidence in
  `verify-final-*-corrected.json`, not by assertion alone.
- Script-fix transparency: the first run in this directory failed ONLY on the
  `parse_config_exact` tab/whitespace split bug (initial JSON:
  `FINAL_MISMATCH` with `remote.origin.url ... []` for all three repos; source
  identity/isolation lines passed). The buggy pair is PRESERVED as defect
  evidence. The parser was fixed (first-`=` split, repo-local scope) and the
  corrected run wrote NEW exclusive outputs without overwriting. The ORIGINAL
  pre-fix `verify_final.py` script bytes do NOT exist as a separate preserved
  file (only the fixed `verify_final.py` is present); this is stated as fact —
  no reconstruction attempted.
- Saved config/remote/status evidence read: active/copy FULL raw status == 
  freeze-pre exact13, cached empty, staged rows `[]`, `ls_v` lowercase `[]`,
  alternates absent, inert exact remotes, all13 sha/mode/bytes == freeze-pre,
  patch `85e9d9ab...` 604448B/13 diffs, contract `07e89990...` — all true in
  the corrected JSON. Actual blocker vs scope: NO blocker observed; residuals
  above are verifier/documentation limits, not source failures. Any claim
  beyond current-state equality at these pins (continuous no-drift, closed
  future predicate, retroactive certification) needs new evidence and is NOT
  made here. Component verdict (§3, as errata-corrected §4) stands UNCHANGED.
