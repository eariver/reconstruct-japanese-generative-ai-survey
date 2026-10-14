# P2R PhaseA evidence — 20261013T122831Z

Read-only candidate investigation, docs/evidence only. No copy/source/schema/test/fixture/runtime changes. No imports, no tests, no restoration, no network, no fetch, no index/ref/commit mutations.

## Method

- CWD for candidate checks: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
- Sanitized routing every Git command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_OBJECT_DIRECTORY -u GIT_ALTERNATE_OBJECT_DIRECTORIES -u GIT_COMMON_DIR GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file` (+ `NO_LAZY_FETCH=1 OPTIONAL_LOCKS=0 ALLOW_PROTOCOL=file` where set). No `add -N`, no `add`, no `commit`, no `fetch`.
- 13-path hashes via read-only `python3` hashlib + `stat` mode/bytes (no imports of candidate code).
- No old scripts rerun; no new script file created this unit (direct commands only, outputs transcribed to `raw-*` without overwrite of historical evidence).
- Reconstruct checks in `/home/eariver/git/reconstruct-japanese-generative-ai-survey` with same sanitization; `task.md` untracked is Human-provided input, not a modification.

## Verdict vs final P1 freeze

- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`: match `notes/rephase-1-dm021-p1/evidence-20261012T072355Z-correction4/freeze-pre.json` and `freeze-post.json`.
- `status --porcelain=v1 -uall`: exactly 3M + 10A = 13 rows, byte-identical order/content to freeze files (see `raw-candidate-status.txt`). `diff --name-only`: exactly the 3M paths.
- All 13 SHA256/mode/bytes: exact match to `freeze-post.json` (see `raw-candidate-13hashes.txt`). P1 pins preserved: module `5d2fde45…`, schema `5623c0d9…`, review-schema `e8598239…`, test `f581fad0…`.
- P2R budget 3A absent: `scripts/survey_editorial_retention_v2.py`, `schemas/editorial-retention-manifest-v2.schema.json`, `tests/test_survey_editorial_retention_v2.py` all absent (`rc=2`, grep rc=1). No collision, no hidden modification.
- Detached HEAD (branch output empty), `.git/HEAD` = `409b…`, no `FETCH_HEAD`, `shallow` present (partial DB persists), `index` present. Origin inert `https://example.invalid/rephase-candidate-recovery.git`. No fetch performed.
- Reconstruct HEAD `a45e1bfea675b496b44b01f50460d1458675c840`, status only `?? notes/rephase-1-dm021-p2r/task.md` (+ this new evidence dir untracked by design). No tracked modifications.
- Contract SHA `194fd7dea0bfef7e9605fc7ed34a2e90a7f0ab63428333c1dec48b605949370e` (18120B) and P1 complete patch SHA `85e9d9ab3c972a786afb1cf2f941bf4dbcfd4980f2e63d0ad9cf6df3cb55963c` (604448B) verified read-only.
- Runtime observed (version probes only): `Python 3.14.4`, `git version 2.53.0` — same major versions as P1 final evidence; no import/test execution in PhaseA. Existing partial/shallow DB, missing-26309-blobs, and unbundled-runtime limits persist as prior observations, not re-proven here.

## Raw paths

`raw-candidate-head.txt`, `raw-candidate-tree.txt`, `raw-candidate-status.txt`, `raw-candidate-diff-name-only.txt`, `raw-candidate-13hashes.txt`, `raw-candidate-p2r-absence.txt`, `raw-candidate-git-config-remote.txt`, `raw-candidate-git-entries-runtime.txt`, `raw-reconstruct-head-status.txt`, `raw-contract-p1-sha.txt`.

No failures this unit; every executed command `rc=0` except intentional absence probes (`rc=2`/`rc=1`).
