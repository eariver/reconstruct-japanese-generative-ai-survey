# Baseline-control operation qualification (proof-copy test-file add/remove)

Preserves `baseline-control-original-final139-raw.txt` (42 lines, exit 1) and narrows prior blanket “saved proof untouched” statements (e.g. implementation `README.md` “Saved e84/proof untouched”; “old proof untouched” in `corrected-implementation-independent-review.md` §2 / `corrected-v2-independent-review.md` §2). No rerun, repair, cleanup, Git, readback, network, imports, tests, or subagents performed for this qualification; existing raw + tool history only.

## What the raw shows

- Traceback test path is the original saved snapshot: `.../evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60/tests/test_dm022_supplement_carry_v2.py` (lines 26, 29–34).
- That path currently globs absent (verified this turn). Do not infer its content from current absence.
- Content is bound by the raw itself plus tool history: raw header line 7 records `TEST_SHA256: 5d5d3aadec70bc5d5c22fdec3e3c65d4f38d73aa995d326d8927fb8f73e26f00`, and tool history shows the same hash from `sha256sum` immediately after the copy into proof-copy. That hash is the focused test file as it existed at control time (PID 676052, START 20261107T031146Z, exit 1). The current workcopy focused file differs (`a8aaafe3…`, 17 methods after later duplicate-test additions); do not present current workcopy content as the control file and do not reconstruct the removed file as original final139 content (it was never part of final139).

## Actual control procedure (tool history/raw only)

- In proof-copy workdir only: `cp <workcopy-test> tests/test_dm022_supplement_carry_v2.py` (new untracked path), `sha256sum` (test `5d5d3a…`; LOW `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b`; HIGH `388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c9f76b6f9efd4`), single-test run (`test_thematic_direct_novel_then_unchanged_carry`, expected `source_bindings must explicitly select task-bound sources` card-build refusal, not token), then `rm tests/test_dm022_supplement_carry_v2.py` with `ls` confirming absent and `sha256sum` confirming LOW/HIGH hashes unchanged.
- No other proof-copy writes are recorded in tool history for this control. Test execution used temp fixture dirs outside proof-copy; `PYTHONDONTWRITEBYTECODE=1` (no `__pycache__`); fixture Git DBs are per-test temp dirs, not proof-copy `.git`.

## Paths/bytes/modes/times changed

- Added then removed exactly one untracked path: `proof-copy/.../tests/test_dm022_supplement_carry_v2.py` (bytes = the `5d5d3a…` test file; mode not recorded in raw/tool history — not claimed).
- `tests/` directory entry changed by the add/remove; file/dir mtimes were not recorded — no values claimed.
- Tracked 771 files: no writes recorded for this control. LOW/HIGH bytes/hashes verified identical before/after in tool history (hashes above; sizes 218692B/92741B per prior manifest records). A full 771-entry manifest comparison was not re-run at control time — full re-verification is not claimed.
- Narrowed claim (replacing blanket “untouched”): old 771 tracked content preserved as far as verified (two runtime files before/after identical; no tracked-file writes in tool history). The proof-copy directory was temporarily modified (untracked add/remove), so blanket untouched is withdrawn.

## Authorization note

- The `cp` into the saved proof-copy snapshot was a procedural deviation: the bound control should have used an independent copy, not the saved snapshot. The subsequent `rm` restored the path to absent but does not erase the write history. Documented here; not repeated and not claimed as authorized saved-proof writes.

## First (unbound) control, for separation

- `baseline-control-raw.txt` ran in the workcopy candidate-work (not proof-copy) after `git checkout HEAD -- scripts/...` temporarily rewrote workcopy runtime files to original blobs, then `git apply` restored the fix (tool history). No proof-copy writes occurred in that control. Its raw lacks ARGV/env/PID/source pins; it is preserved as a historical exact-error observation only, not a source-bound control.

## Reads and unknowns

- Tool history shows reads of proof-copy files (`sha256sum`, `ls`, test-execution imports/reads). No claim is made about root readback activity beyond tool history/raw (unknown — not claimed as zero).

## Evidence loss

- None for the two baseline raws (both saved in packet). Control test-file bytes survive via raw header hash plus tool-history hash, not via the filesystem (absent by design after removal). This qualification does not reconstruct tool-history-only fixture failures noted elsewhere.
