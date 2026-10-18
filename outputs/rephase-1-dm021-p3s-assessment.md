# DM021-P3S — staged source materialization / replay assessment

2026-10-19 JST (final evidence 20261018 UTC). **BOUNDED IMPLEMENTATION COMPLETE** for the selected 3A/0M component under fixed [contract42eb8dbb](rephase-1-dm021-staged-source-contract-decision.md), with mandatory [Astra closeout resolution](../notes/rephase-1-dm021-p3s/astra-closeout-resolution.md) and fresh author-independent [final review](../notes/rephase-1-dm021-p3s/source-implementation/independent-final-review.md) + mandatory [final supplement](../notes/rephase-1-dm021-p3s/source-implementation/independent-final-supplement.md). Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN. Stop at Human Commit Point.

Workspace HEAD `6dcbb89` main Human commit at closeout; no new HEAD/candidate commit for this work. Production remains read-only; no intake refresh or standing commit permission. Co-Worker drafted this assessment; Astra reviewed and corrected it against the root closeout resolution and independent evidence.

## 1. Implemented scope

`materialize_staged_source(root, state_path, proposal_path, retention_manifest_path, scope_review_path)` owns only proposal-local `staged-source/{main.tex,references.bib,jgaisurvey.sty,staged-source-manifest.json}` once. Actual fresh scoped P2V occurs twice in its invocation; entry pins and first-observer supplemental bytes are hash-bound and never replaced by the second observation; original inventory admits only the exact owned delta. Manifest-last, per-file attempts/progress/close diagnostics, late original-input/identity checks; failed partials preserved. No overwrite/takeover/resume/cleanup.

`verify_staged_source(root, proposal_path, staged_manifest_path)` follows actual P2R retained State COPY→exact State.profile→KEEP Profile, uses the narrow Session-backed scope adapter and the fixed 37-route replay-dependency set (including transitives/style), checks full semantic manifest equality plus deterministic exact source bytes. No current State/P2V/HEAD-admission call. Dependent on intact retained/KEEP/scope/replay refs; not permanent self-contained backup or migration compatibility.

No existing-18 change. New strict manifest schema (`2.0-rc1` / `EDITORIAL_STAGED_SOURCE_V1` / `STAGED_ONLY`) and behavioral tests only.

## 2. Exact source / preservation

Actual detached HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`; composite 21 source 3M18A, separately fixed 84 caches, 105 raw status rows. These are uncommitted overlay identities, not a new candidate HEAD.

| Path | SHA256 | Bytes |
|---|---|---:|
| A `scripts/survey_editorial_staged_source_v2.py` | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` | 126181 |
| A `schemas/editorial-staged-source-manifest-v2.schema.json` | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` | 5627 |
| A `tests/test_survey_editorial_staged_source_v2.py` | `a3bb0f2369ffc131e8ad645759105d165a62fa114e9b4088a2497e4a13dfa036` | 147845 |

Final pins: `notes/rephase-1-dm021-p3s/draft-history-r11/static21.json` SHA256 `1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5` (21 entries: 18 inherited + 3 new; zero cache entries — cache84 authority is the separate recorded P2R `cache-inventory-static.json`, not rehashed by the independent reviewer).

- Active `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`.
- Apply copy `/tmp/opencode/jgas-p3s-final-20261018T154812Z/proof-apply21-clean409-copy`.
- GEN DB and absolute temporary index remain beside it under the same `/tmp/opencode` scratch root, outside notes (no embedded Git DBs in packet).
- Complete21 patch `notes/rephase-1-dm021-p3s/evidence-20261018T154812Z-final-packaging/gen-complete21/complete-p3s-21path.patch`: SHA256 `e449d029c8775ee28ee610f224997a57b0cd68664194c6720a6038ce9a3012fa`, 1233670 B. Applies DIRECTLY to clean actual409; contains the inherited18 overlay, so never layer old patches first.

Check actual availability before reuse. When copies are absent: restore actual409 from the [four portable409 inputs](../notes/rephase-1-dm021-contract/availability-at-closeout.md) with a NEW fail-closed procedure, then apply the full21 patch DIRECTLY. No old unsafe scripts, no layered old patches, no fake root, no network refresh. Inherited missing-26309-blobs / unbundled-runtime constraints remain.

## 3. Verification and bounds

26 DISTINCT methods have recorded successful runs, **not a single full26 run**. Module/schema unchanged since R5; test revisions and the final R1 fixture-script repair have their own identities. R10 shared fault-wrapper change forced the warranted affected6 rerun at R11; other passes stay pin-bound. This supports bounded final-R11 assessment, not unconditional PASS transfer.

Root resolution table (authoritative batch ran/success/fail timelines):

| Selected success | Recorded pin/run |
|---|---|
| O1/O2 (2) | R5 smoke2, 855.750s, child/runner/launcher0 |
| O3 (1) | R6 batch A: 2 ran 951.172s, O4 failed, batch exit1 |
| O4/O5/O6a/O6b (4) | R7 batch B: 5 ran 1975.991s, O7 failed, exit1 |
| O7 (1) | R8 batch C: 2 ran 953.654s, O8 failed, exit1 |
| O8/O11 (2; O11d's later affected rerun is selected below) | R9 batch D: 9 ran 4449.573s, 3 successes/6 failures, exit1 |
| O12a/O13/O14 (3; O12b–f's later affected reruns are selected below) | R9 batch E: 9 ran 5810.125s, 8 successes/R1 failed, exit1 |
| O9/O10/O11b/O11c/O11e/O11f (6) | R10 batch F: 7 ran 3664.477s, R1 failed, exit1 |
| R1 + affected6 = O11d + O12b–f five (7) | R11 batch G: 7 ran 5634.188s, all OK, child/runner/launcher0 |

All eight executed batches have preserved PRE/POST/static21/inherited18/cache84 guards and recorded `post_errors: []`; no skips or timeouts in terminal outcomes. Python `/usr/bin/python3` 3.14.4. No old P2V13+1/P2R25/P1-36 transfer. No PDF build or genuine semantic/Human review evidence. O12b–f is FIVE methods; affected6 = those five + O11d; final batch7 adds R1. O11d and O12b–f each have TWO recorded passes (R9 pins + R11 rerun).

Preserved failures (not relabeled green, no retroactive clean run): initial source and shape-only reviews missed real defects (schema-as-instance, unpinned config, output-root overwrite, missing preclaim/premanifest/original inventories, close masking, unverified staged claims, unparseable embedded scripts, held-fd-only ownership, over-restrictive dynamic-pin rule) — corrected by root R1/R2 and R3–R5 returns before first success; prior independent R1 shape-PASS superseded. First B2 runner called nonexistent `os.lexists` before try/outdir/PRE and ran ZERO tests; its own rc was never captured (later shell wait127 is not its exit); original caught-generic claim is false; B3 namespace repair + B4 same-parent launcher are the actual evidence tools. R6 semantic-extra-key State mutation reached layout refusal; R7 whitespace correction proves parsed-equal State/replay-positive/current-before-negative. Unsupported scope enum, accumulated/earlier tamper checks, no-op `%` edit, timeout-word search, early injection timing, nested error-code assumptions corrected test-only. R9-E R1 failed BEFORE refresh (unsupported refresh-module path vs allowlist); R10-F R1 failed AFTER successful refresh (snapshot-before-staging + file-only snapshot oracle defects); R11 repair (stage-then-snapshot + fixture snapshot + real TestCase) proves the same refreshed State/receipt chain. Two author-agent provider `server_error` responses occurred AFTER completed R6 batch A; terminal/raw recovered, no duplicate run or orphan-result inference; dedicated Edit/Write vs apply_patch adapter difference disclosed.

GEN and saved-patch PROOF each ran once with console/tool exit0, no primary/secondary errors. Proof established clean actual409 first (18 new absent, 3 restored to HEAD, disposable84 caches removed), applied the EXACT saved patch, checked exact21 bytes/sizes/modes/status with source unchanged. All-entry `.git` walks recorded 134 regular/96 directories, no shared-inode pairs, inert remotes/no alternates — checked-boundary observations only. Individual `git apply --check`/`apply` numeric exits were not separately persisted by B3; successful fail-closed progression plus proof0 supports success, not a missing-transcript claim. Proof freeze filenames retain historical `-b2` suffix despite B3 execution. Independent supplement rehashed active21 21/21 and compared the recorded applied21 freeze with static21 (0 mismatches); its cache statements rely on saved guard results. A separate final Co-Worker [closeout check](../notes/rephase-1-dm021-p3s/closeout-checks.md) actually rehashed current active21, current apply21 and active cache84 (all match), checked active105/apply21 statuses and resolved232 local links. That is current availability/consistency evidence, not a retrospective per-run or independent-audit claim.

Mandatory limits: OWNED_PARTIAL is the implementation's asserted CLAIM-phase partial-set label (contract text names INCOMPLETE); per-file fsync/close uncertainty can report INDETERMINATE while a missing manifest still makes the SET incomplete; later replay can verify a complete valid set left by failed manifest close without attesting invocation success. Initial mkdir→earliest-observable identity has a disclosed blind window; later checks prove only their observation boundaries. Runtime source-path/byte checking is a tripwire, not in-process hotpatch proof. Test snapshot/guard scopes and sampled independent child-raw reads are not an all-files/all-timings audit. No generic certified rerunner, globalCAS, crash-atomicity, power-loss guarantee, continuous no-drift, full-history/runtime backup, true approval, migration or adoption. No full-suite inference from scoped26.

P1 still destination-conflict after retention; P2R/P2V coexist and are not staged TeX consumers. P3S adds staged artifacts only. Full checked editorial transition, truthful reason/record, review-context/install-window/State/receipt admission, unadopted Candidate collision and adoption/migration remain design-open. No creator/bearer permission or automatic adoption.

## 4. Next bounded unit after Human continuation

**Concrete checked editorial admission / full-promotion contract analysis with the actual final21 source, before any implementation selection.** Bind versioned reviewed target/live output, genuinely checked transition and public post-adoption readback, truthful reason/record/chain/pointer semantics, owned live replacement/failure/recovery, existing unadopted Candidate collision, and normal fresh review/Candidate/Preview/Freeze/Release admission against the existing unresolved predicates (reason/State/receipt/review-context/install-window/Candidate collision). Do NOT start the next unit now and do NOT impose an arbitrary path-budget prohibition — the current deferral follows unresolved predicates, not file count.

Stop at current Human Commit Point. Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN. Ordinary reconstruct Commit/Push and any candidate-commit authorization remain Human-owned.
