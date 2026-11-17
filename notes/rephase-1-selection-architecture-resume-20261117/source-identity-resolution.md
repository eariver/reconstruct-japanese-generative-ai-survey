# Source identity resolution — independent read-only Git proof 20261117

Role: fresh independent read-only Git/source identity investigator, not prior author/operator. No prior implementation/test/runtime authorship reused as authority.

Mandatory: `notes/rephase-1-selection-architecture-resume-20261117/astra-operation-resolution.md` FULL §5. No ref/source/State/config writes, no Git fetch/lazy, no hypothetical typo acceptance, no fixes/rerun/commit.

Scope DBs ONLY (explicit cwd, `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0`, cleaned `GIT_DIR/WORK_TREE/INDEX_FILE`, `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`):

- `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work` (selected real)
- `.rephase-1-editorial-runtime/selection-scaling-implementation-20261116T004649Z/candidate-work` (implementation)
- `.rephase-1-editorial-runtime/regression-supplement-20261116T141000Z/final-work` (regression final-work)

No broad DB search, no reconstruct Git/status/log/HEAD/Commit readback, no network/subagents/import/tests/runtime. Stdlib `hashlib` recompute allowed. `git cat-file commit/body size` then `sha1("commit <size>\\0"+raw)` vs OID.

## 1. Question

Expected documentary: `3231a0c280287411513bba359f4d3d2b6703f591` (f591)
Actual `.git/HEAD`: `3231a0c280287411513bba359f4d3d2b6703d591` (d591)
Root direct read confirmed d591. Operator prefix-relaxed full gate proceeded without root resolution — not authorized. SP exit2 35.004s / W34 exit2 180.013s, both `stage-checkpoint-v2.schema.json: 'from_state' is a required property`, reports absent, State/checkpoint/guard/outputs unchanged per `execution-20261117T005500Z-SP/W34/README.md` + `stderr.txt`. Not authorized fix; no retry here.

## 2. True object proof (all 3 DBs identical)

`.git/HEAD` raw (Read, no Git):

- real: `3231a0c280287411513bba359f4d3d2b6703d591`
- implementation: same d591
- final-work: same d591

`git rev-parse HEAD` → d591 in all 3, exit 0.
`git rev-parse HEAD^{tree} HEAD^` → `ff01b73e6012fd4519fdfb3807186753ff330367` + `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` in all 3, exit 0. Tree ff01 / parent ae0 TRUE as documented.

`git cat-file -e`:

- f591 → exit 1 in all 3 (missing/unsupported, no object)
- d591 → exit 0 in all 3 (exists)
- parent ae0 → exit 0, tree ff01 → exit 0 (checked impl + final-work; real rev-parse proves same)

`git log --oneline -1 --decorate=no` (all 3):

- `3231a0c Bounded Selection scaling repair: fail-closed exhaustive pins + COPY root + owned/return gates + genuine PREARCH oracles (4 modules + focused test)`

`git cat-file -p d591` (real):

```
tree ff01b73e6012fd4519fdfb3807186753ff330367
parent ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56
author Synthetic selection-scaling-impl-1085 <selection-scaling-impl-1085@example.invalid> 1794795519 +0900
committer Synthetic selection-scaling-impl-1085 <selection-scaling-impl-1085@example.invalid> 1794795519 +0900

Bounded Selection scaling repair: fail-closed exhaustive pins + COPY root + owned/return gates + genuine PREARCH oracles (4 modules + focused test)
```

`git cat-file -s d591` → `462`, raw_len `462` (all 3).

Stdlib recompute `sha1("commit 462\\0"+raw)`:

- real: `3231a0c280287411513bba359f4d3d2b6703d591` match True
- implementation: same match True
- final-work: same match True

`git cat-file -t d591` → `commit`.
`git remote -v` (all 3) → `origin https://invalid.invalid/inert.git (fetch/push)` only; no fetch performed, inert preserved, no config mutation.

Conclusion: ONE commit only, d591 genuine. f591 never existed as object in checked DBs. No ref drift evidenced (HEAD already d591, no second commit, no remote).

## 3. 774 delivery vs worktree vs commit-tree

Manifest: `notes/rephase-1-selection-scaling-repair-20261116/source-packaging/final-20261116T031000Z/complete-selection-scaling-manifest.json` `0dc361cb8284f3465243120b7cea8e20476c3fbe81d90a71ce3028dd43eed150`/187361B, intended 774. Patch `76ac1318cd58311a5a7c0d924ee26b2bdff68dc815e75014a1aacd517e51fd6b`/5691014B, base 409 `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`.

Worktree byte equality (cited, not re-hashed here): `entry-binding-r2.md` fresh stdlib 774/774 PASS, 0 missing/mismatch, bytes+SHA256+physical mode vs manifest. That proves worktree bytes equal delivery, NOT commit identity.

Commit-tree identity (this unit, real DB):

- `git ls-tree -r HEAD --name-only | wc -l` → `32241` (full tree, not scoped 774)
- manifest 774 paths in tree: missing 0
- `git_mode` mismatch: 0
- blob `sha256(raw)` vs manifest `sha256`: mismatch 0 (full 774)
- 5 pins: `10126da7…/7796`, `b3cd4a95…/51050`, `fd788b74…/309483`, `b16c4759…/50865`, `a21f5949…/49973` all True, blobs `dc7a1829…/969f82ca…/dcf9a03b…/bc1f1abe…/6b6a922b…`, modes `100644`

Distinction preserved: worktree 774/774 does not imply commit exists; tree 774/774 + recomputed d591 + parent/tree binds delivery bytes to true commit ff01/ae0/d591.

Source-only: did not read missing 26309/bulk31466/runtime/TeX/unrelated blobs.

## 4. Retrospective bounds, earliest log, preservation

Prior f591 strings are documentary wrong, preserved unrewritten:

- `real-rehearsal-20261116T022222Z/README.md` §5 + `machine.json` §source_commit/real_copy: f591, parent ae0, tree ff01, 5 files 2538+/99-, exit 0. `source-commit-stdout.txt` only short `3231a0c`, no full OID; full f591 transcription has no raw backing in that packet.
- `source-packaging/final-20261116T031000Z/packaging-report.md` §1 + `machine.json` §source_3231: f591.
- `astra-closeout-resolution.md` §2 + §4, `final-implementation-review.md` §2: f591 recorded-only.
- `continuation-observation.md` §1 + `entry-binding-r2-machine.json` §selected: f591 recorded-only (superseded by R2 for bytes, not for commit cert).
- `current-proof-20261116T030000Z/machine.json` §source_3231: f591 (pins only, see §5).
- `regression-supplement-20261116T141000Z/report.md` §Errata + `machine.json` §raw_head_note: `raw/final-adapted-head.txt` `3231a0c…d591` preserved, then mislabelled “WRONG single-char d vs f”; actual recorded source commit claimed f591 “no Git readback requested”.

Earliest durable d591: `regression-supplement-20261116T141000Z/raw/final-adapted-head.txt` (`3231a0c280287411513bba359f4d3d2b6703d591`). At creation it was stored raw and explicitly preserved, not rewritten. Its contemporaneous prose misjudged it as typo; current object proof shows raw was true. Earlier full f591 records have no object backing (`cat-file -e` exit 1). Cause of transcription (single-char f/d) UNKNOWN where history insufficient; no drift/second-commit/remote evidence asserted, no hypothetical typo acceptance as proof (proof is object existence + recompute, not prefix/worktree match).

Preservation: all prior files untouched; this resolution adds corrigendum only, does not rewrite raw, manifest, patch, State, or HEAD.

## 5. Scope: CURRENT ca8, pack/base

CURRENT fixture `ca8a978a0f6ceaa5a386b34f9725b889499a9aab` (`current-proof-20261116T030000Z/README.md` + `machine.json`): NEW synthetic Weekly fixture, bootstrap `versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly`, overlay current774 4 mods, `fixture774-pins.json` 4/4 OK, `loaded-files.json` from fixture, `CURRENT_PROOF_VALID`, LOW `fd788b74…` drift refusal + restore, runner `b16c4759…` control-root refusal + restore, closure 70, no reseal. Code bytes identical to §3 tree blobs; commit-string typo does not change blob SHAs. Independent source proof unchanged; no re-proof needed for identity typo.

Pack: base 409/tree 8ce, DIRECT409 patch 76ac…/5691014B, manifest 0dc3…/187361B file bindings correct (0 mismatch). Only `manifest.source_identity.author_head` = f591 metadata wrong. Do NOT mutate frozen manifest/patch. Corrigendum binds to artifact SHAs (`0dc361cb…`, `76ac1318…`), not republish.

## 6. Corrigendum (no republish)

- True source: d591 / ae0 / ff01, recomputed match True, 774/774 tree-bound.
- All prior f591: superseded documentary transcription, preserved as history.
- Future refs must cite d591 with this resolution + manifest/patch SHAs; frozen `0dc3…`/`76ac…` remain authority for bytes.
- If manifest metadata ever re-emitted, emit new artifact with new SHA; never edit `0dc3…` in place.

## 7. Limits

Read-only Git only in 3 named DBs, no reconstruct Human-repo action, no execution, no State/HEAD/config mutation, no fetch, no broad search. Mechanical SP/W34 schema refusal remains open per §5 dispatch; substantive R2 reviews remain bounded editorial, not advance authority. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN.

Files by this unit only: `source-identity-resolution.md`, `source-identity-resolution-machine.json`, `source-identity-raw-20261117T060000Z/` transcripts. No other writes.
