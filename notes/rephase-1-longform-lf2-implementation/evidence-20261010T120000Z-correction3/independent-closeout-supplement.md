# LF-2I independent closeout supplement — BOUNDED_PASS retained

2026-10-10. Closeout-only supplement by the same author-independent reviewer
(C1 author; correction2/correction3 resolver). No code/test rerun, no network,
no subagents/probes/commits. Read-only review of root
`astra-closeout-qualification.md` and the targeted compat packet
`../evidence-20261010T035424Z-cli-compat/` (qualification, runner source,
manifest, raw logs). Prior reports preserved untouched; own overclaims
corrected in §3.

## 1. Preserved-manifest condition closes

My correction3 §4 erratum (stale `1020e4…`/`16864f…` in
`preserved-9-manifest.json`) is satisfied by root's annotation: the two
preserved flat files were directly re-hashed to correction2 finals
`71ef7b976684e0f88407c24ba3ed8d6f51135be2b7a048b2655dd5b777ef5b40` and
`61a3491a572f113e6b2c94b897e5dde2ac234290c4925ceb1c1f0e52ebdd6ad9`,
which supersede those manifest entries only; original metadata is preserved,
not overwritten. I adopt the annotated values. Final source
(publisher `4d235a38…`, test `4a03b564…`) was already correctly pinned in
`hash-manifest.json`; the stale preservation metadata never affected final
source/test/apply identity. No further action on this item.

## 2. Compat supplement: 2-method bounded evidence (accepted as limited)

- Exact binding: `tests/test_survey_gate_cli_persisted_review_v2.py`,
  `GateCliPersistedReviewV2Tests`,
  `test_generated_weekly_cli_admission_and_readback` (line 637: real
  accepted-chain → surface → persisted review → receipt → manuscript, CLI
  `scan-manuscript` with `--state`, single-new-file oracle, Gate route +
  receipt binding + `weekly.validate_receipt`) and
  `test_direct_primary_cli_admission_absolute_relative_and_cwd` (line 335:
  absolute + relative-cwd-root + relative-cwd-differs CLI admission, Gate
  route `DIRECT_PRIMARY`, no-write check).
- Identity: same correction3 final 9 hashes/modes pre AND finally-post
  (manifest `identity_pre`/`identity_post` overlay verified, HEAD/tree/parent
  `409b292…`/`8ce3699…`/`34f934e…` unchanged, status exactly 2M+7A plus
  separately listed caches). No source change, no 43-suite rerun, no old
  whole runner.
- Result: child exit 0, no timeout, `Ran 2 tests in 99.827s / OK`
  (`run.stderr.log`); stdout only real publisher prints (766 bytes).
  Forced no-network Git env for parent git + child, `TMPDIR=/tmp/opencode`,
  routing/optimize rejection via explicit raises (runner source verified:
  `raise RuntimeError`, no `assert`, no `--allow-empty`); `optimize 0`
  observed.
- Fixture scope: weekly path uses the module's own process-scoped-identity
  adapter (`GIT_AUTHOR/COMMITTER_*` env, no `git config user.*`, real
  git/validators, no success mocks); the inherited persistent-`git-config`
  `setUp` is documented as NOT invoked by these two methods. Direct path
  copies schemas/config only. Independent temp DBs under `/tmp/opencode`.
- Bound: this closes the identified missing-route regression (affected
  Weekly generated CLI admission/readback + direct-primary compatibility per
  the selected contract) at final hashes. It is 2 methods, not a second full
  acceptance; 43-method evidence stands as-is, untransferred and unrepeated.

## 3. Explicit correction of my own claims

- **Optimize.** My correction2/3 E1 language ("rejected before every git
  operation") is qualified: refusal uses Python `assert` in the correction2/3
  whole runners, which an optimized invocation (`-O`) can disable. The
  verified fact is the observed exact runs (`optimize 0`, absent overrides
  recorded per phase) — not safe refusal by construction under optimized
  mode. The small compat runner's explicit raises do not retroactively
  harden the whole runners. Final scripts remain exact-run evidence, not
  certified general rerun tools; I certify no saved tool.
- **Proof scope.** A/B/C are shared-`guard_overlay`/child-driver
  observations on synthetic 9-file disposable composites (pre-drift rc 1 no
  child; exit-7 observed; child0 + drift → post rc 1) — not independent
  shell invocations of every full-runner exit branch. Runner main exit
  mapping is separately source-inspected only.
- **Empty commit.** I make no no-empty-commit claim: the proof helper's
  disposable empty root commit (`--allow-empty`, parent for `HEAD~1`) was
  unrequested. It occurred only in an independent disposable proof DB — no
  candidate/reconstruct commit or Production mutation — and must not be
  repeated unchanged as precedent.
- **Modes/inodes/remotes.** Logical Git mode `100644` vs physical `0664`
  (neither executable); untracked new-file modes come from patch headers;
  inode nonsharing is same-filesystem bounded evidence; remote output is
  observed, not asserted for all configurations; byte-copy timestamp
  destination carries no absent-destination safety guarantee.

## 4. Verdict retained

**Whole initial LF-2I component BOUNDED_PASS** at correction3 final hashes,
with all qualifications: correction3 resolution (C1+P1–P3, seams
(a)–(j)+FIFO), 43-method exact-run evidence, same-guard proofs, saved-patch
replay onto an independent ORIGINAL409 copy, the §1 manifest annotation,
this §2 compat bound, and §3 claim bounds. Source remains an uncommitted
2M+7A overlay + caches, not a new HEAD. No full-publication, canonical-audit,
adoption, build-transfer, semantic/visual, or savings approval. Protected-DB
vs synthetic-fixture annotation stands: "no fixture-DB writes" means no
writes to protected original/candidate DBs; independent synthetic
DBs/commits/byte-copy are authorized test activity.

## 5. Next stop (no action by this review)

Root's next task — DM021 post-validated reader/editorial-correction contract
analysis after the Human Commit Point (implementing no reason now) — is
acknowledged; no approval is needed or given for a plan here. Ordinary
reconstruct Commit/Push remains Human-owned. Stop at closeout; whole
candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted.

*Reviewer independence:* fresh scope, no authorship of candidate code/tests/
harness/compat, no relabelling of Worker/root output; exact hashes above are
the basis.
