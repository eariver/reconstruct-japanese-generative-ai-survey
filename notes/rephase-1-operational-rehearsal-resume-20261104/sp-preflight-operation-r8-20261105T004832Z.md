# SP r8 input-only preparation — single authorized operation report

Authority: `astra-resume-resolution.md` §9 (one input-only preparation; no SP removal/retry).
Tool 16088B `200ed99c…`, launcher 2192B `c00e825c…`, manifest 608012B `6c61b254…`,
input 355643B `697a4ed0…`, helper 42142B `2c6f1aeb…` — verified programmatic pre-launch.

## Invocation (once)

- `RET=retention-SP-preflight-20261105T004832Z`, `ID=r8-D165fix-20261105T004832Z`
  (both new, exclusive; no prior same names). Direct packet child; parents clean.
- Env: no `GIT_*` overrides; `HOME=/home/eariver`; launcher exports
  `PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0`; no network/Production/reconstruct Git.
- First `./launcher` attempt exit 126 (non-executable mode from authoring Write,
  tool never invoked, no bundle/retention created); then single `bash launcher`
  invocation (same bytes, no edit) UTC 00:48:41→00:48:44Z, Python 3.14.4.
- Bundle `preflight-r8-20261105T004841Z-100097`: `launcher.json`, `raw/tool.stdout.txt`
  258B (`tasks 160/records 160`), `raw/tool.stderr.txt` 0B, `raw/tool.exit.txt` 0.
  Launcher exit 0. No edit/fix/rerun/removal/State advance.

## Result (READY, no semantic PASS inference)

- `READY.json` 6542B `7170c9a40b79435d99c2f8388ac6ecdbf96886a1da4c0667d1e89706871c9e41`,
  `journal.json` 597B `91a67877…`: stage `prepare-only`, phase1 pass →
  stage-1-input → package+validate-input (160/160) → finish-authority-phase pass.
- `new_input` `evidence/proposed-input/interactive-evidence-r8-D165fix-20261105T004832Z.json`
  355643B `697a4ed0…` 0o664 (verbatim r5); `new_supplement` retained `ffcd0a7e…`;
  `staged_raw` 17 retained; `package_json_sha` `4f6b9bda…`; pkg `pkg-r8-D165fix-20261105T004832Z`.

## Post-observation (active e84)

- SP tree 1057 files / 37 dirs (1056 + exact 1 NEW input, 0 missing/modified/deleted).
- Retained 17 Raw + supplement `ffcd0a7e…` unchanged; old accepted (`09f487ab…`,
  `50c919b9…`) + new accepted (`df671195…`/`2ad42d4d…`) + current canonical ledger
  `253cb2ea…` 66850B / completeness `18a05292…` 33683B + State `4865998b…` unchanged.
- W34 canonical Ledger/Completeness remain absent; backups in
  `retention-W34-dispose-20261105T003915Z/` untouched by this SP operation.

Next: separate r3 dispose+retry authorization with this READY + r7 manifest;
Selection/Architecture/audit/adoption OPEN. Human Commit Point — stop.
