# LF-2I independent final resolution (correction3, P1–P3) — BOUNDED_PASS

2026-10-10. Same fresh author-independent reviewer (C1 author, correction2
resolver). Read-only review; no full-suite rerun, no code/source edits, no
network/commits/subagents, no protected-DB writes. No disposable probe was
needed: P1–P3 are decided from saved source lines, packet manifests, and raw
logs, with on-disk identity re-observed read-only. Prior reports
(correction `independent-implementation-review.md`, correction2
`independent-final-resolution.md`) are preserved untouched; their overclaims
are corrected explicitly in §5 below, not rewritten.

## 1. Basis (exact final pins)

- Source `/tmp/opencode/jgas-lf2-design-20261009T113013Z`, HEAD
  `409b292756dd1277b9dfae87679934c0d2ce251c` (unchanged, no commits),
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`; status exactly 2M+7A
  source entries plus `__pycache__` side effects (listed separately, never
  claimed untouched).
- Changed this round only (same publisher+test budget):
  publisher `4d235a388955dcedd34d6a7dc5ac7761f9fc91de8bc723eb11f68cec6a229195`
  (was `71ef7b…`), integration test
  `4a03b564f8fa4dd39f2b48766ddb7612cf2d8d4dacdcc42ac39f637d2bca11a4`
  (was `61a3491a…`), both mode 664 (direct `sha256sum` re-verified).
- Unchanged 7 pins: derivation `c09c55…41149`, helper `d480e1…97d3c2`,
  gate runtime `e73058…bbe4`, gate schema `fe4a96…13322c`, receipt schema
  `4dadf8…3e8ca`, reader schema `7bae9d…d0643`, LF-1 test `ce6874…f913`.
- Governing: selected contract `4795a586…` + F1–F3, DM-021 disposition
  (initial + healthy readback only), root `astra-review-r3.md` (P1–P3).
  Prior 44- and 42-method results are superseded history; the only claim
  here is the new **43-test** run — no original-base/old-test/runtime
  transfer.

## 2. P1–P3 source fixes verified (actual on-disk code)

- **P1 PASS — `_safe` BEFORE any byte capture.** `_capture_lexical_bytes`
  is deleted (no references remain in the publisher). `main()` now calls
  raw-first `_safe(root, args.state/input, …)` BEFORE ANY content read
  (281-284), then captures bytes from the validated paths (286-287) with
  the post-derivation stability checks retained. Pre-validation capture
  means before semantic validation, never before path safety — the old
  alias-following read is gone. Proven by the new FIFO no-read probe
  `test_alias_outside_sentinel_never_opened`: State-leaf and input-parent
  aliases to outside FIFOs refuse via containment in a daemon thread with a
  join timeout (any open-for-read would block and fail the test); both
  refused promptly with full-snapshot equality and cleanup-only FIFO
  handling. Type/identity proof, correctly limited (see §6).
- **P2 PASS — snapshot uses the exact named context ref.** `_snapshot_inputs`
  selects the exact named `drafting-archive` row from
  `context["authored_refs"]`, runs that ref path through strict `_safe`
  directly (never `_rel`-resolve-first), and compares file SHA against the
  recorded ref hash (165-176); the snapshot stores the ref's path+hash
  (183-184), not a freshly adopted hash. New seam (h) drifts the archive
  immediately after real `load_derivation` returns but before
  `_snapshot_inputs` and proves refusal pre-mkdir/pre-write with an
  injected-archive-only delta. Existing later-window seams (c)/(e) preserved.
- **P3 PASS — recheck runs the ACTUAL control predicate.** Every
  `_recheck_snapshot` re-runs `generated.verify_tool_basis` with the
  validated recorded commit/closure (229-233), replacing the 14-file
  equality: config or any tracked control helper drift (not just the 14
  closure files) refuses at each window. Seams (i)/(j) mutate the unlisted
  tracked helper `scripts/survey_stage_validation_v2.py` (under the
  `scripts` control root, outside `CURRENT_CLOSURE`) after initial
  verification / during the final write and prove pre-write refusal with no
  outputs and pre-receipt refusal with the retained set and no receipt. No
  Core-change renewal or hash absorption.

## 3. Seams, suite, proofs, apply (actual packet evidence)

- Seams (a)–(g) retained and green; new (h)/(i)/(j) + FIFO sentinel test
  bring the integration module to 13 methods. `run.log`: **43 tests OK in
  1822.421s** (13 LF-2I + Gate module + 3 LF-1 loader controls), exit 0, no
  timeout, Python 3.14.4, `optimize 0`. `manifest.json`: proofs/pre/post/
  apply all PASS, child exit 0, forced git env
  (`GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`)
  for runner git + children, per-phase override rejection (all empty/0).
- `proofs.log`: same-guard A/B/C on NEW full disposable composites —
  A pre-guard rc 1 with child never launched, B exit-7 observed, C child0 +
  drift → post-guard rc 1. Numeric codes, exclusive log, no candidate canary.
- E3: exact SAVED `complete-overlay.patch` (M diff + clean `new file mode`
  diffs) applied as saved (`--check` exit 0, apply exit 0, per-file cleanly)
  to NEW `cp -a` byte-copy
  `/tmp/opencode/jgas-lf2i-409bytecopy-20261010T033640Z` (correction2's copy
  preserved): pre HEAD-409 clean/inert/no-alternates with 0 shared object
  inodes; post HEAD-409, status exactly 2M+7A, all-9 bytes + physical modes
  match, `ls-files -s` logical modes recorded.
- FROZEN/RELEASED healthy readback and both same-issue manuscript
  stage-Gate backstops retained green; no `EXCEPTION_*` /
  `REVIEWED_EDITORIAL_CORRECTION` paths (grep-clean); `config/*.json`
  untouched. The runner is exact-run evidence, NOT a certified general safe
  rerunner — no such certification is granted.

## 4. Evidence erratum (non-blocking, must be annotated)

`preserved-9-manifest.json` in THIS packet lists stale hashes for exactly 2
of 9 entries: publisher `1020e4…` and integration test `16864f…` (correction1
finals). The actual `preserved-9/` files on disk hash correctly to the
correction2 finals (`71ef7b…`, `61a3491a…`; other 7 entries match the
manifest). Provenance is intact via direct file hashing, but the manifest
must be annotated/corrected to `71ef7b976684e0f88407c24ba3ed8d6f51135be2b7a048b2655dd5b777ef5b40`
and `61a3491a572f113e6b2c94b897e5dde2ac234290c4925ceb1c1f0e52ebdd6ad9`
(or the two entries marked superseded) — it must not be read as claiming the
pre-edit state was correction1. This does not affect any source/test/runner/
apply guarantee and does not block the component verdict.

## 5. Explicit correction of my prior PASS claims

- **P1 claim corrected.** My correction1 review marked R2 PASS (bounded)
  while the caller passed a `_rel`-resolved publication path (aliases
  resolved away before the strict check) and captures read through aliases
  before `_safe`. Root R2/S2 + R3/P1 proved the overclaim. Now: safe-first
  ordering + raw lexical pub path + FIFO never-opened proof.
- **P2/snapshot claim corrected.** My correction2 resolution accepted the
  snapshot as complete, but it still adopted a fresh archive hash rather
  than comparing the exact named `drafting-archive` context ref whose bytes
  the derivation validated. Now: ref path+hash compared under strict
  containment with post-derive seam (h).
- **Runner/apply history.** My correction1 acceptance of logic-only proofs
  and 2-file construction was already superseded by correction2's real
  guard proofs + saved-patch byte-copy apply (re-run here with new pins);
  no prior-suite PASS was or is transferred.

## 6. Annotation: "no fixture-DB writes" + proof limits

The qualification's "no … fixture-DB writes" means **no writes to protected
original DBs** — reconstruct DB, ORIG409 (re-observed HEAD 409 clean),
design DB (no new commits/branches; 2M+7A + caches only), original/LF1/
verify copies. It does NOT mean no fixtures were created: isolated temp
fixture DBs (test setUp), disposable proof composites, and the `cp -a`
byte-copy are created by design under `/tmp/opencode` and are the
independence mechanism itself. New FIFO/seam proofs are type/identity
no-bypass/drift proofs; synthetic review/PDF/Human rows remain explicitly
type/identity fixtures — no genuine semantic/visual sufficiency, build
transfer, all-profile, or savings claim follows.

## Verdict

**BOUNDED_PASS** for the whole initial LF-2I component scope at the §1
hashes: C1 + root R1–R3 (incl. P1–P3) resolved with seams (a)–(j) + FIFO
probe, 43-test exact-pin evidence, same-guard proofs, and saved-patch
replay onto an independent ORIGINAL409 copy — subject only to the §4
manifest annotation. No full-publication, canonical-audit, adoption, or
rerunner certification is granted.

## Current limitations / next stop

- Source component remains an uncommitted 2M+7A overlay + caches, NOT a new
  HEAD; any candidate commit needs explicit authorization with fresh
  identity-bound acceptance. Whole candidate NOT_READY; step4/B3 OPEN;
  canonical audit unstarted.
- Next stop: root final code/oracle/evidence review of correction3, then the
  Human Commit Point. No automatic next unit; ordinary reconstruct
  Commit/Push remains Human-owned.

*Reviewer independence:* fresh scope, no authorship of candidate code/tests/
harness, no relabelling of Worker output; exact hashes above are the basis.
