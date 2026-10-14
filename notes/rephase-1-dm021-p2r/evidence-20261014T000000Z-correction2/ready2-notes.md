# Ready2 notes (root readback: post-verify byte gap + runner cache hole)

2026-10-14. Last targeted draft review before long run/proof. Shipping
source changed (new pins below); P1 unchanged; no test execution, no
proof execution, no `-O`, no commits/branches/network/adoption. Prior
DRAFT/READY files preserved untouched (v7 DRAFT + v7 READY remain as
review history; only the proof READY's static-manifest filename was
synced per instruction).

## 1. Shipping gap fix (module)

Post-verify fresh `Session` compared retained file SETS and inode
identities but not byte hashes against capture-original measurements: a
same-inode in-place COPY/manifest edit after `verify_retention` returned
would re-snapshot as new bytes and compare to itself via `reverify`,
allowing false `CAPTURED`. Fix placed BEFORE the ownership
checks/`reverify` in the post block: every COPY `inv_files3`/`_inv_sizes3`
entry must equal its original plan row `sha256`/`byte_count`, and the
manifest entry must equal `manifest_sha`/`len(manifest_bytes)`
(`FINALIZATION_REFUSED`/`INDETERMINATE_INVOCATION`). The existing final
standalone verifier is unaffected (same-`Session` pins already bind
bytes there); only the new-`Session` capture boundary changed.

## 2. New oracle test

`test_capture_postverify_inplace_edit_refuses` wraps the REAL
`verify_retention` (call through, assert it returned VERIFIED, then
mutate, return its result): one owned COPY file rewritten in place
(truncating `write_bytes` = same inode, one flipped middle byte = same
size, different sha — defeating size/shape/identity checks), then the
capture must refuse `FINALIZATION_REFUSED`/`INDETERMINATE_INVOCATION`.
Immediate assertions: live originals unchanged (victim site excluded as
the injected owned-subtree mutation), additions owned-prefix-only,
partial preserved, retry refuses, bytes restored afterwards.

## 3. New source pins

- module `3833b14a281ab82999410d91361d5aace3c77015484e621c62077e480b73f5b2`,
  122231 bytes, `0o664`, 2080 lines.
- test `36814fe5424c09cd3a61957b2df880eb28284978fa272c8593937993247166bf`,
  92794 bytes, `0o664`, 1802 lines, 25 methods (24 + inplace oracle).
- schema unchanged `347e5499259a…`.
- `expected16-correction2b.json` (NEW; used manifests never overwritten).
  Re-verified byte-identical to current files after writing.

## 4. Runner refinement → `run_p2r_correction_v7.py.READY` preserved, `run_p2r_correction_v8.py.READY` NEW

- `cache-inventory-static.json` (NEW): 84 files with sha/size/mode, every
  entry verified regular non-symlink at authoring; live status audited at
  the same time: 100 rows = exactly 16 source + 84 cache, ZERO other
  extras. Residue preserved, nothing cleaned.
- v8 guard compares the EXACT full status (16 + preknown, len/set/dup)
  pre AND post with pre==post required; raw full status recorded both
  sides; no substring/wildcard classification anywhere in v8.
- Child env: `PYTHONPYCACHEPREFIX=/tmp/opencode/jgas-p2r-nocache-20261014T000000Z`
  (verified absent at authoring; v8 refuses if present at launch) plus
  `PYTHONDONTWRITEBYTECODE=1`; stale in-tree `.pyc` are therefore neither
  executed nor rewritten.
- Only the 5 forced keys are persisted
  (`GIT_NO_LAZY_FETCH`, `GIT_OPTIONAL_LOCKS`, `GIT_ALLOW_PROTOCOL`,
  `PYTHONDONTWRITEBYTECODE`, `PYTHONPYCACHEPREFIX`) plus a redaction
  count for the rest (no values, no names, no full env dump).
- All v7.READY guards otherwise kept (exact status/inherited13/held
  handles/exact safe.directory/immutable stages/killpg/`-u`/precedence).

## 5. Proof READY sync

`proof_apply16_v3.py.READY` now loads `expected16-correction2b.json`
(load line + docstring; all other E2 fixes unchanged). No other proof
changes; v3 patch + hash manifest still to be generated post-ack.

## 6. Checks executed (cheap only, exact commands)

- `python3 -c "import ast; ast.parse(...)"` on module, test, v8.READY,
  proof.READY — all `AST_OK`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -c "import unittest; ...
  loadTestsFromName('tests.test_survey_editorial_retention_v2')"` in the
  candidate — 25 methods collected incl.
  `test_capture_postverify_inplace_edit_refuses`; zero cache writes.
- Read-only status/pin/cache-attribute observations only. One collection
  probe earlier ran with the wrong cwd in a prior unit (recorded in
  correction2-notes); not repeated here.

## 7. Return for root ack (NO long run/proof until ack)

- Changed source: module `3833b14a…`, test `36814fe5…` (paths as before
  under `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60/`).
- Last READY: `evidence-20261014T000000Z-correction2/run_p2r_correction_v8.py.READY`.
- Proof READY (synced): `evidence-20261014T000000Z-correction2/proof_apply16_v3.py.READY`.
- Static manifests: `expected16-correction2b.json` (v8 + proof),
  `inherited13-static-freeze.json` (unchanged, P1-authoritative),
  `cache-inventory-static.json` (NEW, v8 preknown residue).
