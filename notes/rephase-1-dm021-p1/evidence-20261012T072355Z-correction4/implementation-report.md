# DM021-P1 R4 correction implementation report (worker → root + independent D1/E1 resolution)

Source: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
(HEAD409b292/tree8ce, detached, no branch/commit/network/Production). 13 paths 3M10A,
same 3A1M; LF2I 9 + pre-TeX `e8598239` preserved. Correction3 module `69790944`/
test `84a6e4a11` + 36 PASS preserved in `preserve-prior/`. R4 edits module+test only
(schema `5623c0d9` unchanged).

## Final pins (freeze-pre==post, named-status)

HEAD409b292/tree8ce, 3M10A named exact. Module `5d2fde45` 110155B, test `f581fad0`
112708B, all 0o664. No other runtime/controller/reason/writer changes.

## D1 — Discovery x_source_intake/raw_refs + X-manifest locals (exact, typed)

Collector finds pinned `upstream:discovery-acceptance` nodes (checkpoint-bound, not
receipt-prefix iteration), then for each:

- Top-level `discovery_path/sha256` (raw JSONL, SHA; size from live for node) →
  `upstream:discovery-raw-jsonl` KEEP+frozen (edition-tree walk does not substitute;
  JSONL is inside source_root but still needs graph/frozen/retention membership).
- REQUIRED `x_source_intake{path,sha256}` (explicit local authority, never URL) →
  `upstream:x-source-intake` KEEP+frozen.
- X-manifest actually required locals via schema/validator conventions (typed, no new
  intake, no generic URL following): `production_profile{path,sha256}` →
  `upstream:x-production-profile` (research, frozen; unions with State profile if same
  path/sha); `runs[].task{path,sha256}` → `upstream:x-task:<run_id>` (research,
  frozen); `runs[].result.raw{path,sha256,byte_count}` → `upstream:x-raw:<run_id>`
  (research/raw, frozen, exact size bound `len==byte_count` in addition to SHA).
  Drive paths (`drive_task_path`, `drive_file_name`), policy/series literals stay
  provenance (never followed).
- `records[].raw_refs[]{path,sha256,byte_count}` (explicit, REQUIRED, minItems 1;
  outside edition roots possible, e.g. repo-root `raw/source.json` in fixtures) →
  `upstream:discovery-raw:<did>` KEEP+frozen, exact SHA+size bound.
  `source_locator` (URL string) deliberately NOT followed (provenance only).
  If validators do not require a metadata literal as live dep, it is not followed
  (only the two authority shapes above + JSONL path are collected; all have explicit
  SHA/size in schema).

Research/raw KEEP+frozen; no tool/prompt/control refs in these fixtures' manifests
(all X locals are research authority here) — distinction recorded, none omitted.
Missing/unclassified required local stops (`DISCOVERY_*`/`X_*`), never silently
excluded. Literal refs are actual `col.pinned` checked files (SHA+size), not
name-prefix claims.

Oracle `_assert_transitives_expected_set` extended (checkpoint API + independent
container maps, never P1 nodes/receipt list): expected Discovery JSONL/x-manifest/
profile/tasks/raws/raw_refs derived in TEST via independent `core.load_json` of
actual acceptance/manifest (explicit fields, never URLs), asserted KEEP+frozen/
retention with sizes; wrappers operational excluded; pub/QA/State/receipt/candidate
excluded. Stale completeness sibling still proven NOT adopted.

Seam `d1-outside-raw-scope` (same drift fixture, no new build): independently resolves
discovery acceptance (agent API, not P1 graph), selects raw with path outside
`source_root`/`survey_root` (repo-root `raw/source.json`, proves tree-walk
insufficient), records clean-vs-mutated injected-only delta (ONLY raw differs),
validates WITH scope → refuses (`DERIVATION_REFUSED` early via discovery validator
or `DISCOVERY_RAW`/size/recheck late — all fail-closed), then proves mutated-vs-post
identical (no P1 writes beyond injected), HEAD/status unchanged beyond injected,
explicit restore (no cleanup masking).

## E1 — NEW exclusive runner (code facts fixed, prior qualified)

`run_final.py` (not old `run_correction.py`): rejects `GIT_*`/`PYTHONPATH`/`PYTHONHOME`/
`optimize!=0` BEFORE any candidate Git calls; parent freeze Git uses sanitized
forced `GIT_NO_LAZY_FETCH=1/GIT_OPTIONAL_LOCKS=0/GIT_ALLOW_PROTOCOL=file` with
every rc checked (no silent empty head/tree/status); exclusive `open(x)`/O_EXCL for
every log (no existence-then-`w` race); records argv/cwd/interpreter/env +
forced Git; compares all13 hashes/modes/named-status (13 rows only, caches ignored
for status)/base pre AND finally-post (explicit-raise, not asserts); preserves
timeout partials (5400s timeout, prior 3255s measured); NEVER deletes/repairs
source/cache before comparison; records caches separately (`caches-post.json`,
here `{}` with `PYTHONDONTWRITEBYTECODE=1`, no caches — recorded, not deleted).
Prior exact-run evidence preserved/qualified (not called certified fail-closed).

## Tests

**36/36 OK in 3308.284s, exit 0, pre/post files/head/named-status identical.**
Python 3.14.4/jsonschema 4.23.0/pypdf 6.16.2/git 2.53.0. Gate 27/27, P1 9/9 (C1+R3
oracles both routes, D1 oracle+seam, R1×2, ordinary compat). Old36 stays its scope
(no transfer). Two R4 attempts failed (D1 regex too strict, accepted DERIVATION early;
D1 delta assertion counted injected in pre) preserved in `attempt-1-d1-regex/` +
`attempt-2-d1-delta/` with analyses.

## Patch/proof (copy, no index writes)

`gen_correction_patch.py` byte-copies ACTIVE to `/tmp/.../R4-gen-...`, `add -N`+`diff`
THERE (disposable index), copies patch out, deletes copy — ACTIVE
`diff --cached --name-only` empty (verified). Patch 604448B
`85e9d9ab3c972a786afb1cf2f941bf4dbcfd4980f2e63d0ad9cf6df3cb55963c`, 13 diffs,
base HEAD409/tree8ce. `proof_apply.py` byte-copies ACTIVE to `/tmp/.../R4-verify-...`
(inert origin, no alternates, inode separation), reverts ONLY 13 in COPY to clean409,
`apply --check`+`apply` AS SAVED exit 0, all13 hashes/modes/status/base equal.
No commits/branches/network/subagents/protected edits.

STOP for root + independent D1/E1 resolution with actual source/log citations.
Whole NOT_READY, DM021 OPEN. Commit/Push Human-owned. No full closure claimed if
transitive missing (none; views present via checkpoint in both fixtures, included).
