# Correction packet — recovery review CHANGES_REQUIRED (documentary only)

Worker-packet entry. No root `AGENTS.md`/handoff/assessment edits are made by
this packet; no tests, diagnostics, recovery, candidate, or archive changes.

- Authority: `../independent-recovery-review.md` (fresh independent reviewer,
  verdict CHANGES_REQUIRED, correction-only, no retest).
- `corrections.md` — R1–R6: retracted Git classification with exact function
  paths/lines (t2/t3 indirect Git via `repository_commit_sha`; selected t4 no
  index binding; t1/t5 no Git), suite-level (not per-method) guards and raw-log
  binding limits, `restore.sh` evidence-only status with explicit DO NOT RERUN,
  true preservation gaps (overwritten tar stderr/member lists, v1 script
  source, unrecorded rmdirs), commit-body clarification, no delete authorization.
- `recovery-manifest.json` — final readable manifest: exact candidate/parent/
  tree, fixture/restore/venv paths, 5 methods + subcases with exits and raw
  paths, source-probe + restored-probe raw paths, archive SHA/bytes/members/
  object counts/shallow+ref limits, script-rerun caveat, failures/limitations/
  correction links. The older `../manifest.json` (m3 results) and
  `../manifest.pretty.json` (m2 view) are retained unchanged; this file is the
  unambiguous final one.
- `commit-body.txt` (+`.exit/.stderr`) — read-only commit-object inspection
  supporting the R5 clarification.

For the scoped resolution reviewer: verify each R-item against its cited
source/raw path; confirm no original was edited (m2/m3 report/manifest/raw/
harness bytes intact); confirm the manifest's every claim resolves to a cited
raw path. Then Astra closeout + Human Commit Point.
