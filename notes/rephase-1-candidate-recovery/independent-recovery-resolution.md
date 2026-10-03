# Independent recovery resolution — documentary corrections at 0456Z

Date: 2026-10-03 (after correction packet `m3-20261003T0445Z/corrections-20261003T0456Z`,
prior independent review `notes/rephase-1-candidate-recovery/independent-recovery-review.md`
verdict CHANGES_REQUIRED remains preserved).
Role: same fresh author-independent reviewer, recovery unit ONLY. Did not author
scripts/tests/candidate/design/corrections. No agents, no root edits, no tests,
diagnostics, recovery, candidate, archive, or source changes. Documentary check only:
read `README.md`, `corrections.md`, `recovery-manifest.json`, `commit-body.txt` +
`.exit.txt`/`.stderr.txt`; resolved against source/raw already reviewed in the
prior pass (no re-run, no fixture/network operations).

## 1. Packet completeness (documentary only)

- `corrections-20261003T0456Z/` holds exactly: `README.md`, `corrections.md`,
  `recovery-manifest.json`, `commit-body.txt`, `commit-body.exit.txt` (single `0`),
  `commit-body.stderr.txt` (empty). No harness/source/archive rewrites.
- `README.md` correctly scopes authority (prior independent review), lists R1–R6,
  declares `recovery-manifest.json` the unambiguous final readable manifest while
  retaining older `../manifest.json` (m3) and `../manifest.pretty.json` (m2 view)
  unchanged. No original claimed edited; nothing observed contradicts this.
- `commit-body.txt` (8 lines: head `b40de60`, parent `774dd39a`, author/committer,
  date `Sat Oct 3 13:36:48 2026 +0900`, subject, body `New honest identity directly
  on real 774dd39a... Not restored 481dec0/e4 ancestry. No Freeze code changes.`)
  matches live identity already verified. `.exit 0` + empty `.stderr` support
  read-only `git log` provenance. R5 correction (supplement C4 phrase
  "commit body in 17 stdout" inaccurate; `17-commit.stdout.txt` holds
  subject+stat only) is accurate.

## 2. R1–R6 resolution against already-reviewed source/raw

- **R1 Git classification — RESOLVED.** Retraction of report §1
  "methods 1/2/3/5 use no Git" replaced with exact call sites:
  t2/t3 `ROOT = Path(".").resolve()` (`test_survey_freeze_stage_boundary_v2.py:22,39`)
  → `survey_stage_validation_v2.py:624 repository_commit_sha` + agent-control
  `761/797/1290/1345/2016` (matches prior grep); selected t4 real CLI only,
  gate module has no git usage, `git ls-files` lives only in unselected weekly
  helper (matches prior reads of gate CLI + gate fixture `setUp` temp-dir root);
  t1 pure dict helpers (profiled-freeze module has no git/subprocess per prior
  grep) and t5 temp-dir + publication module with no git (prior grep no files
  found) correctly stated as no-Git. Manifest `five_methods[].git_binding` mirrors
  this per-method. No overclaim; t2/t3 correction strengthens Git-aware proof.
- **R2 suite guards — RESOLVED.** `run_five.py:101-115` before/after whole suite
  only, raw only `guards-before/after.txt` (+ identity pair, all
  `head=b40de60 tree=6570324 parent=774dd39a tracked_diff_exit=0`,
  `?? scripts/__pycache__/ only`), per-method logs carry no embedded HEAD/hash
  headers — manifest `suite_guards` states exactly this binding basis (runner cwd
  + suite guards + sources + no-change evidence). Accurate, no stronger pinning
  invented.
- **R3 restore wrapper unsafe — RESOLVED.** `set -u` only, no `-e`/`pipefail`,
  tar exits echoed not asserted, `| tee` masks inner failures, no hash gate,
  explicit **DO NOT RERUN** as general tool; restored success proven by manual
  correction (empty-remnant `rmdir`) + independent checks (identity/tree/parent,
  `ls-tree` identity, inventories, 0 shared inodes, no alternates, inert origin,
  restored positive PASS) — not by script exit. Manifest `script_rerun_caveat`
  + `restoration.script: evidence-only` matches. Correctly separates artifact
  success from wrapper exit.
- **R4 preservation gaps — RESOLVED as disclosure, does not undermine proof.**
  Newly disclosed, each checked:
  - first tar stderr overwritten (verified `raw/archive-tar.stderr.txt` now 0
    bytes): final archive proof rests on live sha/bytes, authoritative listing,
    760 members, deterministic flags, and byte-identical inventories — not on the
    lost first stream. Loss limits failure archaeology only.
  - first member-list/sources regenerated in place (`archive-members.txt`,
    `archive-sources0.bin`): authoritative versions retained and match tar
    listing (prior live 760 = 74+686 verified). Defective versions unneeded for
    final proof.
  - `restore.sh` v1 source overwritten by v2 (v1 run outputs
    `restore-script.log`/`restore-listing.txt`/`restore-extract.*` survive; v2
    count bug preserved in `raw/restore2/`): v1 was failed layout assumption
    with no fixture impact (self-cleaned empty dest). Final proof uses corrected
    recursive count + manual completion, not v1 source.
  - two empty-dir `rmdir`s + `stage.tar` removal (15.8M, hash preserved in
    `raw/archive-stage.tar.sha256`, verified content `66db2f54...`) with observed
    output only: empty-dir removals are low-risk; stage-tar hash preserves chain
    of custody; final 686 + `.git` verified in place.
  - m2 `TGT`/`<message>` abbreviations retained, no invented transcript.
  "All failures fully preserved" is correctly retracted; exact gaps enumerated,
  nothing invented. Bounded partial-DB proof stands.
- **R5 commit body — RESOLVED** (see §1).
- **R6 delete scope — RESOLVED.** No blanket delete permission; only empty
  pre-restore dest, empty post-restore remnant, superseded `stage.tar`
  (hash-first) listed; `__pycache__` explicitly not removed. Minimal and bounded.

## 3. Final manifest accuracy

`recovery-manifest.json` verified as accurate final scope: exact
head/tree/parent/branch/author/date/subject/body (+ body source note),
delta `A11+M21 TREEDIFF_MATCH`, Freeze-9 pointer, fixture/restore/venv paths
with pins, 5 methods with exits/times/subcases/raw paths and per-method
`git_binding` as in R1, `suite_guards` as in R2, source + restored probes with
raw paths (positive rows=8, exact negative message, source sha256 == row 1 +
blob `6d14009`), archive SHA/bytes/members/layout/determinism/object counts
(28626/2317 = 2+1608+707 /26309; 32152/686/0) + shallow/single-ref/sparse cone +
  listing paths, restoration identity/inventories/index-note/sharing/script
  pointer, `script_rerun_caveat`, `failures_preserved` (5 items incl. overwrites),
  `limitations` (partial DB, content-not-closure, 41 R1 blobs, synthetic-fixture
  bounds, no ancestry/PASS/whole-readiness/Freeze/audit/platform claims,
  index-mtime note), and `correction_links`. Every claim resolves to a cited raw
  path already reviewed. No source/archive change introduced.

## Verdict: BOUNDED_PASS for recovery ONLY

All prior CHANGES_REQUIRED items are resolved by documentary correction; no
retest, new candidate, or archive rebuild is needed or was performed.
Recovery acceptance is code-free and bounded: genuine baseline child `b40de60`,
32-path content equality at tree `6570324`, 9 Freeze unchanged, isolated DBs,
5-method + positive/negative closure + restored-positive evidence, and portable
partial archive with offline restore proof — subject to stated partial-DB,
synthetic-fixture, and evidence-only-harness limits.

Explicitly NOT certified: safe reusable `restore.sh` (or any saved harness) as a
general tool; full-history/asset restoration (26309 promisor-missing blobs +
non-baseline ancestry unavailable offline); old-481/e4 ancestry or PASS transfer;
whole readiness; Freeze implementation; seven-point audit; platform or
real-publication claims. Original CHANGES_REQUIRED review remains preserved;
this file is the scoped resolution only. Next: Astra closeout + Human Commit Point.
