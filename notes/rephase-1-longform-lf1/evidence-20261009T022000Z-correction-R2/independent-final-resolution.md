# LF-1 independent final resolution — BOUNDED_PASS (scoped)

2026-10-09. Same author-independent reviewer as B1/B2. Resolves my B1/B2 and
root R2 items 1–7 against final packet `evidence-20261009T022000Z-correction-R2/`.
Read-only static review + read-only identity checks only. No candidate/source/
reconstruct edits, refs, network, or rerun (full 31-test run already evidenced
once; no repeat). No subagents, no code fixes.

## 1. Final identity (independently verified)

- Basis HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`; status exactly three `??`,
  zero tracked mods; remote inert `example.invalid`; source
  `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` HEAD 409, clean.
- Overlay: runtime `233e86557f1627203a4f1e4129c953bf34e1319bd8949b1d58b7d417b0744cf7`,
  schema `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643`,
  tests `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913`
  (all match packet manifest and post-apply hashes).
- Runtime CPython 3.14.4 (`/usr/bin/python3`), caller = reconstruct checkout;
  parent env has NO `GIT_*`/`PYTHONPATH`/`PYTHONHOME` overrides (verified live;
  log filtered-env correctly shows none in parent, child pins recorded).
  No old-3.12.14 transfer; no prior-hash transfer claimed.

## 2. Correction of my earlier runner PASS overclaim

My R1R6 review called `run-corrected.sh` a PASS guard. Retracted: per root R2.3
it only PRINTED post HEAD/tree/status/hashes, never compared them, exited
child-0 despite post drift, used existence-test + truncate (not exclusive
create), and `cd` under `set +e` could fail without stopping the child. That
script is superseded evidence only. The new `run_evidence.py` replaces it: one
shared `guard()` (HEAD/tree/exact-status/zero-tracked/3-hashes + inert-remote,
no-alternates, no-hardlinked-objects) asserted BEFORE the child and in a
`finally` AFTER it; exclusive `open(...,'x')`; exit 0 pass / 1 child-fail /
2 pre-refuse (no `CHILD_SPAWN`) / 3 postguard-fail even when child exits 0.

## 3. B1 / root R2.1 — schema dot: FIXED, proved end-to-end

Schema `citation_key` is now `^[A-Za-z][A-Za-z0-9:._-]*$`, identical to module
`_CITATION_KEY`; new `test_dotted_did_full_loader_schema_positive` runs dotted
DID `paper.v1-D001` through the REAL chain → projector → schema validation
(key `sp001paper.v1d001`). Helper-only gap closed. No writer/renderer
import or invocation (imports checked; writer name appears only in a
never-import docstring).

## 4. B2 / root R2.2 — full module on final hashes: PROVED

`run-full-module.log`: `31 tests, 2225.376s, OK` (bare OK = zero skips),
exit 0, pre/post guards asserted PASS on final pins. All 31 methods present in
the test file, including every B2 area (directive file+symlink, lifecycle,
no-write, path escapes, order, Unknown fallback, ambiguity + equal-timestamp
first-capture control, stable nonreader, membership/cardinality) plus 5 new R2
tests. Historical 5-method provenance regression stays separately bounded
(not rerun, not claimed fresh) — accepted.

## 5. Root R2.4–2.6 — substance checks (actual reads, not trust)

- Preflight: `_preflight_evidence_tree` is called FIRST in `_longform_records`,
  before `validate_evidence_acceptance`; stat-only (`_safe`, symlink/ancestor/
  non-regular checks, no content reads). Alias test swaps `results/` for an
  outside-malformed-sentinel alias and proves refusal `alias/symlink` BEFORE
  parsing, spies show real validator NEVER called and sentinel NEVER read +
  byte-unchanged, immediate `_snapshot` no-write equality, healthy control
  after disclosed repair. Real loader retains exact-set authority. FIXED.
- Table: 35 rows on ONE reused chain covering the listed missing fields
  (anchors, frontmatter heading/scope, narrative paragraph, timeline text,
  synthesis paragraph, note title, cross paragraph/Qwen/DeepSeek/Kimi,
  glance/comparison order reversals). Derived-value probes use spy-captured
  ordered/records from a loaded context and are labelled PURE throughout;
  HOLD pure-build vs upstream NEEDS_MORE BLOCKED are now correctly classified
  (prior "direct loader-level" wording retracted). Immutability test mutates a
  REAL returned surface and proves a second projection byte-identical with
  trusted constants unaffected. Equal-timestamp control proves first-capture
  `urldate 2026-08-22`; multi-DID-per-card honestly disclosed non-constructible.
  `bad_syn2` asserts the exact ValueError. FIXED with honest labels.
- Packaging: `verify-apply.log` uses a FRESH byte-copy
  `/tmp/opencode/jgas-lf1-verify-20261009T023000Z` (no reset of prior copies):
  HEAD/tree verified, clean, inert origin, no alternates, zero shared inodes,
  zero hardlinked objects; `apply --check`/`apply` exit 0; post-apply exactly
  three `??`, zero tracked mods, three SHA match. Partial-DB (26309 missing
  blobs) and unbundled-runtime limits disclosed; no full-history claim. PASS.

## 6. Runner residual qualifications (nonblocking for this exact run)

`run_evidence.py` is exact-run evidence, NOT generic safe tooling: (a) the
multilink `find` returncode is unchecked (empty stdout on failure would pass) —
observed run's DST is intact so the check executed; (b) `--proof-postdrift-file`
has no enforced distinct-DST guard — the observed proof DID use a disposable
`--dst` and shell log proves the candidate has no canary before/after
(lines 33–41), so the boundary held in fact but not by construction; (c) on
`TimeoutExpired` partial child output is discarded — no timeout occurred
(2225s < 3600s). Qualify, do not re-test.

## 7. Verdict and limits

**BOUNDED_PASS** for the LF-1 source-only component on exactly the pinned
3-file overlay over unchanged 409: schema dot e2e, full 31-method evidence,
pre/post asserted guards with three guard proofs, preflight/sentinel,
35-row/pure-vs-real/immutability/resolver evidence, and independent packaging
all verified. Limits: uncommitted overlay, NOT a new HEAD/commit; no
canonical/shipping/production PASS; whole candidate NOT_READY, step4/B3 OPEN,
canonical audit unstarted; no LF-2; no-write oracle is scoped fixture-tree +
Git plumbing (not full-filesystem); runner qualifications above apply to any
reuse. STOP at Human Commit Point.
