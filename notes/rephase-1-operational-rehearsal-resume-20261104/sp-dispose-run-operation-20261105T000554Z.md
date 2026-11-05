# SP r2 dispose + normal retry — single authorized operation report

Authority: `astra-resume-resolution.md` §6 FULL (one invocation only).
Tool `sp-operator-dispose-run-r2-20261104.py` 46350B `2044257f…`,
launcher 3020B `b60d2cad…`, READY 12270B `c7cd05a8…`,
manifest 395713B `6507804d…`, helper 42142B `2c6f1aeb…` — all verified programmatic before launch.

## Invocation (once, no duplicate/rerun)

- `RET=notes/rephase-1-operational-rehearsal-resume-20261104/retention-SP-dispose-20261105T000554Z` (new, exclusive, directly under packet; no prior `retention-SP-dispose-*` or `dispose-run-r2-*` existed)
- READY `retention-SP-20261104T162747Z/READY.json`, manifest `sp-prepare-expected-manifest-r6-20261104.json`
- cwd `/home/eariver/git/reconstruct-japanese-generative-ai-survey`, UTC 2026-11-05T00:05:54Z→00:06:21Z, parent PID 4151751
- env: no `GIT_DIR/WORK_TREE/INDEX_FILE/OBJECT_DIRECTORY`; `HOME=/home/eariver`; launcher exports `PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0`; no network/Production/reconstruct Git; e84 isolated Git only via tool
- run bundle `dispose-run-r2-20261105T000554Z-4151755`: `launcher.json` (argv/cwd/python/env/UTC), `raw/tool.stdout.txt` 271B, `raw/tool.stderr.txt` 0B, `raw/tool.exit.txt` `0`
- launcher exit 0, tool exit 0. No edits/fixes/reruns after.

## Result — record normal-run vs wrapper postchecks separately

- Normal run (existing API once): `evidence_result_count=160`, `completeness_status=LIMITED`
- Wrapper postchecks: `post-run-verify pass`, exit 0 (not mechanical PASS claim)
- New Evidence `df6711954d6ee37f0489c6f87e8d072511af26168adb033b0f327d1165faf0ac`: accepted 49237B `d6426426…`, package copy 50279B `4f6b9bda…`, archived input 355386B `0ee3187e…` == staged, audit binds NEW archived path + staged bytes, 160 tasks/results; new Views `2ad42d4d…`: 64222B `e439db85…`, 160 views; discovery 165 nonempty; ledger 66850B `253cb2ea…` rows 165; completeness 33683B `18a05292…` 15 obligations LIMITED
- Tree: SP 1056 files / 37 dirs (571 pre + 485 new files + 5 new dirs); umask `0o2` → `0o664`, no chmod of products

## Preservation

- Backups exact O_EXCL 0o664 nlink1: ledger 66865B `ee13b8ee…`, completeness 32511B `c60a9624…`, State SHA `4865998b…`; manifest 1315B `490ce0aa…`
- Unchanged: State `4865998b…` CAND, Profile `aff05fd5…`, old accepted `9c254319…/34f81e56…/890a4323…/7a205de1…`, W34 preflight input `1ea56297…` + W34 State/ledger/completeness; no W34 run; no State/CP/Human/source change
- Deviations preserved, no false claim: old v1 wrapper altered (now 44098B `546f7174…`, not `d591e5d4…`); old helper 20/20 stale exit1 not exit0; single run only, no restore/cleanup
- Records: `DISPOSE_RUN.json` 9244B `cf26a23c…`, `journal.json` 2552B `f482d1cf…` in NEW retention. Full hashes in `sp-dispose-run-artifact-manifest-20261105T000554Z.json`.

## Next review needed

Independent Evidence re-review of NEW `df671195/2ad42d4d` sets + new ledger/completeness (mechanical success ≠ CHANGES_REQUIRED clearance); then Selection/Architecture; audit/adoption/savings OPEN. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN. Human Commit Point — stop.
