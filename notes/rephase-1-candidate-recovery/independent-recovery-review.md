# Independent recovery review — fixed-baseline candidate recovery ONLY

Actual clock: 2026-10-03T04:54:20Z / 13:54:20+09:00 (verification window ~04:50–04:54Z).
Role: fresh author-independent reviewer for recovery unit ONLY. Did not author
recovery scripts/tests/candidate/design. No agents spawned. No edits to
root/worker/candidate/old logs/packets.

Boundaries observed: read AGENTS.md + `notes/rephase-1-candidate-recovery/task.md`,
`method-decision.md`, `verification-decision.md`, `preflight.md`.
Inspection was read-only under `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
GIT_ALLOW_PROTOCOL=file`, no `GIT_*` root/object overrides present at start
(verified `env | grep ^GIT_` empty). NO tests/imported-source execution, network,
checkout, Git config/ref mutation, recovery/fixture writes. Only hash/tar
read-only integrity/list/content inspections and read-only Git
`rev-parse/log/ls-tree/diff/remote` + file reads. Did not extract archive into
git/workspace, did not execute `run_five.py`/`run_closure.py`/`restore.sh`/
`restore_check.py`. Reconstruct HEAD at review: `fe17541` (matches expected).

## 1. Verified pins (live read-only + packet binding)

- Candidate: `/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z`
  - `rev-parse HEAD` = `b40de600e9ed1f80cb278213ccf17aa5f3cd9de3` (matches m2
    `raw/18-head.stdout.txt`, m3 `raw/five/guards-before.txt`,
    `raw/closure/closure-*.txt`).
  - `rev-parse HEAD^{tree}` = `657032438c6ed8b1c055d5a120b67b4b261a5092`
    (matches m2 `raw/18-tree.stdout.txt`, expected historical assembled tree;
    content equality only).
  - `log --format=%P -1` direct parent = `774dd39a951c9ac3818e83dfffd4c7666efb0a20`
    (real fixed baseline). Second log line shows baseline's own merge message;
    shallow log shows baseline only (m2 `raw/08-log.stdout.txt` one line).
  - `.git/shallow` contains only `774dd39a...` (live `cat`). Branch live
    `codex/rephase-candidate-recovery`. Remote live inert only:
    `origin https://example.invalid/rephase-candidate-recovery.git`.
- Restored: `/tmp/opencode/jgas-recovery-restore-20261003T0445Z`
  - Live `HEAD`/`HEAD^{tree}`/parent identical to candidate (verified).
  - Live `remote -v` inert only. Live `ls-tree -r HEAD` byte-identical to
    candidate (`diff <(ls-tree) <(ls-tree)` → `LSTREE_IDENTICAL`, both 32152
    entries).
- Archive: `notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz`
  - Live `ls -l` 5,152,199 bytes; live `sha256sum` =
    `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c`,
    matches `.sha256` file. Live `tar -tzf | wc -l` = 760; split 74
    `candidate-partial-b40de60/.git/` + 686 worktree (matches report/manifest).
  - No absolute/`..` members (live `grep -E "^/"` 0, `grep -F ".."` 0),
    no `FETCH_HEAD` in listing, no `pycache`/`venv` in listing, deterministic
    `archive-listing.txt` shows `0/0`, mtime `2026-10-03 00:00`, no symlinks
    (`->` none in spot check; `tar -tzvf | grep "->"` empty).

## 2. Genuine baseline/shallow relation + exact tree

- Shallow single-commit history with promisor `blob:none`: genuine fixed-baseline
  fetch feasible per m2 `raw/04-fetch.*` (exit 0). Shallow boundary
  `[774dd39a...]`, sparse cone `.github config docs schemas scripts tests
  templates specials` retained (live `.git/info/sparse-checkout` + m2
  `raw/21-isolation.stdout.txt`). Parents named by baseline commit object are
  NOT locally available (log shows baseline only) — disclosed, not healed.
- New HEAD is honest new identity directly on real `774dd39a`, NOT restored
  `481dec0`/e4 ancestry. Tree `6570324...` equality is source-content equality
  to historical assembled tree, not history/asset closure, not old PASS transfer.
  No whole readiness claimed here.

## 3. 32-path modes/blobs, no unrelated delta, 9 Freeze unchanged

- Live `diff --name-status 774dd39a b40de60` sorted = exactly A11+M21 = 32 paths
  in report/manifest/m2 `raw/19-treediff.stdout.txt` order (verified live count
  32). `diff --stat` tail `32 files changed, 9323 insertions(+), 1446
  deletions(-)` matches commit message/manifest.
- Sample live `ls-tree HEAD` R1 postimages match manifest:
  `survey_agent_control_v2.py d11febc...`,
  `survey_reader_surface_gate_v2.py 89b5b85...`,
  `survey_weekly_derivation_v2.py 6d14009...` (all `100644`).
  Full 32 identities in m2 `raw/20-identities.stdout.txt` match
  `manifest.pretty.json:final_32_identities`.
- 9 Freeze paths: live `diff 774dd39a b40de60 -- <9 paths>` empty, exit 0.
  Unchanged bindings match manifest (e.g. `survey_profiled_freeze_v2.py
  27e5bcb1...`, workflow `de6531d7...`, 4 schemas, 2 tests). No unrelated
  tree-reference delta beyond approved 32 (report `TREEDIFF_MATCH`; live
  `ls-tree -r HEAD` 32152 entries corroborates e4 32149+3).

## 4. Physical DB isolation, credentials, shared objects, remotes

- Candidate live `.git`: real directory, no `objects/info/alternates`, no
  `.git/commondir`, no symlinks under `.git` (`find -type l` empty), inert
  origin only, `config` holds only core/sparse/inert-origin (read live).
  `FETCH_HEAD` present live (names real acquisition URL) — correctly EXCLUDED
  from archive; content preserved in m2 `raw/04-fetch.*` per report.
- Restored live `.git/config` inert only, no alternates, no symlinks observed.
- No credential patterns in either `.git/config` (live `grep -ri
  password|token|secret|ghp_` empty); no `github.com` in restored/candidate
  configs (live `grep github.com` empty). Packet `supplement.md:C5` redaction
  note for `m2/raw/00-env-sort.txt` (`OPENCODE_SERVER_PASSWORD=<redacted>`)
  is accurate — that file is not pristine transcript, must not be cited as one.
- No shared objects/hardlinks: sample live `stat -c "%d %i"` shows same device
  (45) but distinct inodes (`HEAD` 4613 vs 12268; `survey_weekly_derivation_v2.py`
  5407 vs 12858). Packet `verify-orig-inodes.txt` (782 lines, orig range) vs
  `verify-new-inodes.txt` (760 lines, new range 12267–13108) are disjoint ranges,
  consistent with no inode sharing. Sample worktree bytes identical:
  `survey_weekly_derivation_v2.py sha256 1cb1f705...` both sides;
  `survey_profiled_freeze_v2.py 6a6a2cd6...` both sides (matches closure row 1
  sha256 in `raw/closure/closure-source.txt` + blob `6d14009...`).
- `.git/index` difference (excluded FETCH_HEAD + index stat-refresh) is the only
  object-store delta claimed; packet `verify-lstree.txt` (full 32152-row
  `ls-tree`) + `verify-objstore.txt` (74 object/config/log/shallow rows) support
  content-identical claim via `ls-files -s` + clean diff both sides
  (`verify-orig-stage.txt` vs `verify-new-stage.txt` present; live `ls-tree`
  identical corroborates). Read-only git may refresh index mtimes — disclosed,
  bytes unaffected.

## 5. Test scope/oracles/log binding and failures (5 methods)

Runner source read (`run_five.py`): 5 literal unittest argv, `FIXTURE`,
`EXP_HEAD/TREE/PARENT`, `VENV_PY` pins embedded; `SCRUB` Git overrides removed,
allow-listed env only (`GIT_NO_LAZY_FETCH`, `GIT_ALLOW_PROTOCOL`,
`PYTHONDONTWRITEBYTECODE`); `check_identity` asserts head/tree/parent +
`diff --quiet HEAD` exit 0. Raw binding verified:

- `raw/five-runner.stdout.txt` `methods=5 failures=[]`; `raw/five/summary.txt`
  same; per-method `*.argv.txt` literal, `*.exit.txt` 0, `*.stdout.txt` empty
  (expected — unittest verbose goes to stderr), `*.stderr.txt` each `... ok`,
  `Ran 1 test`, `OK` with times 0.000 / 11.754 / 22.728 / 0.909 / 2.443 matching
  report table. Subcases (t3 3/3 missing/extra/wrong-visual; t4 3 path/cwd) are
  in-method `subTest`, not separate methods — report wording accurate.
- Oracles are real validators/type/identity/flow checks on synthetic fixtures in
  `tempfile` sandboxes; synthetic reviews/checkpoints/PDFs are not editorial /
  visual / Human-approval evidence; workflow text assertions are source-text
  checks; no DM-repair tests selected — all disclosed in report §1.
- Failures preserved, none hidden: m2 `raw/35-imports.stderr.txt`
  `ModuleNotFoundError: No module named 'scripts'` (scripts-dir probe-path
  error) + `35b-imports.stderr.txt` empty with `IMPORTS_OK` (repo-root correction);
  tar first-attempt stale-path bug + regenerated member list (archive now 760,
  exit 0); restore v1 subdir assumption + v2 count assertion with manual `rmdir`
  completion (see §7). `m2 "all exits 0"` covers acquisition/patch only per
  `supplement.md:C3` — accurate after correction.

## 6. Git-aware closure probe (actual)

`run_closure.py` read: Phase A `current_closure(root)` +
`_verify_head_bytes(root, EXACT_NEW_HEAD, closure)` must return cleanly; Phase B
in-memory deepcopy with one sha256 corrupted must raise exact
`ValueError("Weekly receipt current-tool closure drift: <name>")`, no file
mutations. Raw verified:

- `raw/closure-runner.stdout.txt`: `positive=PASS rows=8`, `negative
  message=Weekly receipt current-tool closure drift:
  scripts/survey_weekly_derivation_v2.py`, `negative=PASS exact drift message`.
- `raw/closure/closure-rows.txt`: 8 rows (5 scripts incl. 2 B-new, 2 schemas, 1
  style); `closure-source.txt`: module file sha256 `1cb1f705...` == row 1,
  git blob `6d14009...` (R1 postimage); `closure-positive.txt`/`closure-negative.txt`
  exact messages; `closure-identity-before/after` head/tree/parent pinned.
- Restored `raw/restore2/restore-check-*.txt`: `head/tree/parent` identical,
  `tracked_diff_exit=0`, `restored_positive=PASS rows=8`, worktree still clean.
  Only positive diagnostic run in restored copy (no 5-test repeat) — per decision,
  sufficient for offline-usable proof with existing pinned venv.

## 7. Restoration manual corrections; proven vs unsafe rerun

- `restore.sh` read: `set -u` ONLY — no `set -e`, no `set -o pipefail`, no
  `pipefail` check. `tar -tzf`/`tar -xzf` exits only echoed (`list-exit`,
  `extract-exit`), not aborting; `mv` results echoed, not asserted; final
  `} 2>&1 | tee "$RAW/script.log"` masks left-side failures (pipeline exit is
  `tee`'s without `pipefail`); `grep` 1-vs-0 handled via `test ! -s` but fragile.
  `worktree-entries-moved` counts top-level dirs (12), not files — original v2
  assertion `moved -eq 686` was wrong; current file asserts recursive
  `find ... -type f | wc -l -eq 686` (correct count) but `script.log` in packet
  still shows stale `worktree-entries-moved:12` → `WORKTREE_COUNT_MISMATCH`
  without `restored-worktree-files:` line, i.e. log from pre-fix script version.
  Final restore completed manually with recorded `rmdir` (remnant empty; 686
  files + `.git` verified in place). All v1/v2 raw kept.
- Proven: archive integrity (size/sha/members/layout), extracted `.git` + 686
  worktree bytes identical to candidate (live `ls-tree` identical, sample
  sha256 identical, 0 shared inodes, no alternates, inert origin), restored
  positive diagnostic PASS. Unsafe to rerun as general CLI: saved `restore.sh`
  must be treated as evidence-only, not safe rerun instructions; rerun without
  manual correction would still emit mismatch/fail masked by `tee`. Same for
  saved preparation harnesses (overwriting logs/warn-only risks per prior packets).

## 8. Root-flagged likely inaccuracies — independent check

All four CONFIRMED as inaccuracies in m3 report wording (not in underlying
artifact/test outcomes):

1. **Stage methods invoke Git indirectly through real recovered root — TRUE.**
   `grep` in candidate scripts: `survey_stage_validation_v2.py:624`
   `current_impl = core.repository_commit_sha(repo_root)` (→ `git rev-parse HEAD`
   subprocess); `survey_agent_control_v2.py:761,797,1290,1345,2016` same helper;
   `survey_weekly_derivation_v2.py:578-611` direct `git rev-parse/verify/commit`
   subprocesses. t2/t3 call `validate_stage`/`build_stage_checkpoint`/
   `advance_with_checkpoint`/`approve_publication_preview`/`build_freeze` with
   `ROOT = Path(".").resolve()` = recovered fixture CWD, so they DO exercise the
   recovered Git DB. m3 report §1 line "methods 1/2/3/5 use no Git subprocesses
   and no real Git repos" is therefore inaccurate for 2/3. Correction strengthens
   (not weakens) Git-aware proof for stage path.
2. **Direct-primary CLI selected method probably no Git index usage — TRUE.**
   `scripts/survey_reader_surface_gate_v2.py` has no `repository_commit_sha`/
   `subprocess`/`ls-files` (grep 1 false-positive comment only). Selected
   `test_direct_primary_cli_admission_absolute_relative_and_cwd` uses
   `_direct_fixture()` (temp dir via `test_survey_reader_surface_gate_v2`, not
   REPO) + `_run_cli` (`PYTHONPATH=REPO`, `cwd=root` or `cwd=REPO` for one
   subcase) against synthetic manifests; `git ls-files cwd=REPO` lives only in
   `_make_env_identity_weekly_fixture()` used by unselected
   `test_generated_weekly_cli_admission_and_readback`. m3 report §1 lines 37-39
   conflates module capability ("reads real recovered index for weekly variant")
   with selected-method execution. Selected t4 proves real CLI admission, not
   recovered-DB Git binding; Git binding for CLI path is covered only by closure
   diagnostic + unexecuted weekly helper, not by t4.
3. **Guards bracket entire 5-suite, not each method — TRUE.** `run_five.py:101-115`
   calls `check_identity("before")` once before loop and `check_identity("after")`
   once after; raw has only `guards-before.txt`/`guards-after.txt`
   (both `head=b40de60 tree=6570324 parent=774dd39a tracked_diff_exit=0 status:
   ?? scripts/__pycache__/ only`). Report phrase "guarded before/after every run"
   must be read as suite-level, not per-method. No evidence of intermediate
   mutation (before==after, temps auto-cleaned), but per-method bracketing was
   not performed.
4. **`restore.sh` lacks `set -e`/`pipefail`/checks, not safe general CLI — TRUE**
   (see §7). Must be labelled evidence-only; actual restored proof relies on
   manual corrections + independent verify files, not on clean single-script rerun.

Worker will add correction supplement, originals preserved — these items must be
addressed there, not by editing originals.

## 9. Limitations / non-transfer (exact)

- Partial DB + sparse worktree backup only: census `28,626 reachable — 2,317
  present (2 commits, 1,608 trees, 707 blobs; batch-check 0 missing among them),
  26,309 promisor-missing blobs`; worktree `32,152 tracked, 686 materialized, 0
  mismatches`. 41 R1 historical data blobs unverified; non-baseline ancestry
  unavailable offline. Tree equality ≠ asset closure.
- Synthetic fixtures prove type/identity/flow, not semantic/visual/Human
  authority; canonical test reaches synthetic Release record, not real Release;
  profiled identity method does not invoke Freeze builder.
- Source equality is NOT old-481/e4 ancestry or test PASS transfer; no whole
  readiness, no Freeze implementation approval, no seven-point audit,
  no platform/real-publication claims. Untracked `scripts/__pycache__/` observed,
  excluded from archive; venv/tooling (163M) excluded by design; read-only git
  may refresh index mtimes (bytes unaffected).

## Verdict: CHANGES_REQUIRED (correction-only, no retest)

Actual restored archive proof DOES support bounded recovery — candidate identity,
32-path/No-delta/9-Freeze, isolation, 5-method PASS binding, positive+negative
closure, offline restore identity/tree/bytes/no-sharing + restored positive
diagnostic are all verified against live paths and packet raw. No new candidate,
no test repeat, no Freeze work is required.

What blocks bounded completion now is documentation/script-labelling only:
worker correction supplement must (a) retract "1/2/3/5 no Git" for t2/t3 and
state indirect `repository_commit_sha` Git usage through recovered root; (b)
clarify selected t4 exercises real CLI but NOT recovered index (`git ls-files`
weekly path unexecuted; Git binding via closure diagnostic only); (c) clarify
guards are suite-level before/after, not per-method; (d) label saved
`restore.sh` (and preparation harnesses) as evidence-only, explicitly unsafe for
general rerun (`set -u` only, no `-e`/`pipefail`, `| tee` masks exit,
stale `script.log` vs current file, manual `rmdir`/file-count correction
required), stating what was actually proven (§7). Originals stay preserved.

Code-free recovery acceptance only. No Freeze implementation approval,
seven-point audit, or platform/real-publication claims. Next: worker supplement,
then Astra closeout + Human Commit Point. No repeat Summary fetch or cosmetic
rerun.
