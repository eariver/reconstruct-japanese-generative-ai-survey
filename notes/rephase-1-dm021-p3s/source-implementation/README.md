# DM021-P3S source implementation packet (Co-Worker A)

2026-10-17 UTC. Implements ONLY the selected 3A in a NEW independent
candidate copy; no verification-tools writes (Co-Worker B scope), no
candidate commit/branch/network, no fixture/test execution yet. Root selects
smoke/affected/full checks after this source + draft review.

## 1. Identity

- Source (preserved, untouched): `/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60`
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` (detached), tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, 102 status rows (3M+15A+84pyc),
  static18 18/18 MATCH, 84 pyc census-only. P2V apply copy
  `/tmp/opencode/jgas-dm021p2v-preserved-proof-20261015T171102Z/TB1proof-clean409-copy`
  and all P2R/P2V active/proof copies preserved (no writes there).
- New implementation copy: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
  (`cp -a` whole worktree incl. `.git`; see `preparation-raw.md`).
- Reconstruct HEAD at implementation: `6dcbb89...` (see `reconstruct-head.txt`;
  only `notes/rephase-1-dm021-p3s/**` untracked, incl. B's
  `verification-tools/` which A never touched).

## 2. Implemented 3A (in the NEW copy only)

| # | Path | Bytes | Mode | SHA256[:16] | Role |
|---|---|---|---|---|---|
| A1 | `scripts/survey_editorial_staged_source_v2.py` | 77172 | 0o664 | `49a5564371ae57c2` | `materialize_staged_source` (lazy-P2V writer) + `verify_staged_source` (standalone replay) + `_SessionScopeReader.safe(value,label)` + S2 `37/route` + canonical manifest/digest + exclusive dirfd ownership + primary/secondary close handling |
| A2 | `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258` | strict `EDITORIAL_STAGED_SOURCE_V1`/`STAGED_ONLY`/`2.0-rc1`, 17 top-level required incl. strict 8-key `contract_identity`, sized output/style refs, `producer_head`, `manifest_digest` |
| A3 | `tests/test_survey_editorial_staged_source_v2.py` | 40738 | 0o664 | `92fcc964838991e8` | 16 behavioral methods O1–O14 + R1; real P1/P2R/P2V seams; UNTRACKED_P3S_SOURCES 18 entries (15 inherited + new3); fresh-subprocess R1; immediate no-write + exact owned-delta assertions |

- Inherited 18: byte-identical (18/18 vs `expected18-source-correction-v5.json`).
- Future composite: 21 source (3M+18A) + 84 caches = 105 status rows; tracked
  diff vs HEAD is exactly the inherited P2V 3M overlay (182 +++/10 ---).
- Runtime/test posture: cheap `ast.parse` + `jsonschema.check_schema` only
  (`PYTHONDONTWRITEBYTECODE=1`, stdlib/third-party imports only, cwd inside
  the copy but no candidate-module imports); cache count unchanged 84 before
  and after; no historical scripts run; no fixture/test/PDF production.

## 3. Selection compliance notes (for root readback)

- S2: shared 27 `.py` sorted + 5 shared schemas sorted; per-route 37 unique
  (`_route_code_deps` asserts size 37, manifest order enforced sorted);
  proposal+retention schemas included (F2 fix); new test excluded from runtime
  pins; P2V module pinned writer-side only via lazy import.
- Writer W3 decided: P2V `measured.proposed_reader_sha256` + independently
  pinned staged reader validated by route canonicalizer + actual renderers;
  no private `_pipeline_data`, no public P1 after retention.
- Config/KEEP: no blanket exclusion — retained KEEP rows (incl. config/tool
  when present) enforced through called P2R + independent typed re-reads;
  live config/HEAD never used by the verifier; no `HEAD == producer_HEAD`.
- Ownership: exclusive dirfd `mkdir` + entry/fd fstat identity before writes;
  files `O_CREAT|O_EXCL|O_NOFOLLOW` + fstat + entry bind before bytes;
  manifest LAST + readback; `INDETERMINATE_INVOCATION` distinct from
  `INCOMPLETE`; primary survives secondary closes (manual attach, never via
  P2R's `RetentionError`-assumption path).
- Oracle distinctions kept: O10 same-inode edit vs new-inode same-byte swap;
  O6a TOOL_DRIFT reaching the check vs O6b honest earlier KEEP preemption;
  O4 conditional live-State replay-positive/materializer-negative; O13
  immediate fault-present no-write (not post-repair equality).
- Known non-claims: no execution yet (16 methods unaudited at runtime);
  `_check_runtime_binding` is a tripwire, not hotpatch proof; no
  crash-atomicity/power-loss/replica claims; no adoption/production.

## 4. Packet files

- `reconstruct-head.txt`, `reconstruct-status.txt`: reconstruct HEAD + status
  at implementation time.
- `preparation-raw.md`: every preparation command + direct raw outputs
  (pre-copy identity, copy, post-copy isolation, post-implementation static
  checks, diff, cache-effect evidence).
- `coverage-matrix.md`: O# → test method → seams → expected; static file
  inventory; deferred-runner note (B scope, non-overlapping).
