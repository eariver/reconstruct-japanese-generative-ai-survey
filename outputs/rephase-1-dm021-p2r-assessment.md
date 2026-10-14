# DM021-P2R — retention capture/readback implementation assessment

**Successor design 2026-10-15 JST:** §4's retained-aware authority analysis is now complete as [P2V contract2ea1d98f](rephase-1-dm021-current-authority-contract-decision.md), with [independent design review / mandatory Astra V1–V5](../notes/rephase-1-dm021-current-authority/README.md). P2R source/evidence/fullpatch5b79218e unchanged. P2V is unimplemented; next is its concrete interface/fixture return before code, not repeating §4 analysis. Full promotion and DM021 remain open.

2026-10-14. **BOUNDED COMPLETE** under fixed [contract194fd7de](rephase-1-dm021-retention-contract-decision.md), with mandatory [Astra closeout resolution](../notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/astra-closeout-resolution.md) and [fresh independent final resolution including §10](../notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/independent-final-resolution.md). **Retention-only completion: DM021 remains OPEN, whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted.** Stop at Human Commit Point.

Started after Human Commit/Push `a45e1bfea675b496b44b01f50460d1458675c840`, clean/local tracking synchronized without fetch. General performed interface analysis, independent candidate copying, implementation/corrections and tests; Astra reviewed concrete interfaces/source/oracles/evidence; author-independent reviewers were separate. The interrupted correction worker was resumed after Human instruction, without duplicating a live test process. Earlier broad PASS was corrected by root R2; only the final qualified review applies.

## 1. Implemented boundary

Three added paths only, no modifications to P1 or other inherited code:

| Path | SHA256 |
|---|---|
| `scripts/survey_editorial_retention_v2.py` | `3833b14a281ab82999410d91361d5aace3c77015484e621c62077e480b73f5b2` |
| `schemas/editorial-retention-manifest-v2.schema.json` | `347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c` |
| `tests/test_survey_editorial_retention_v2.py` | `4155baab733e8bddc0b7cbc34b83fe801def2927a716d43132321f8f083d614e` |

- `capture_retention(root,state_path,proposal_path)` calls unmodified P1 before writes, without a semantic-scope review. A valid REVIEW_REQUIRED proposal permits retention, not promotion. The previously absent `retained/` root is claimed exclusively. COPY destinations mirror exact original paths; KEEP refs remain required immutable dependencies. Only planned files/directories and final manifest are permitted.
- Input/raw path/type safety, declared controls/edition snapshots, current HEAD, bytes and ownership identities are checked around capture. Writes are dirfd-relative, exclusive, close/readback checked. Failure preserves observed partials with structured disposition; existing equal/empty/partial/foreign roots refuse. No overwrite, retry/adopt, rollback or deletion-to-rerun.
- Manifest-last publication is followed by independent readback and fresh input/control/edition/retained/original-byte checks before capture success. In-place same-inode same-size edits after readback cannot be accepted as newly observed truth.
- `verify_retention(root,proposal_path,manifest_path)` is read-only and makes no P1/Git/current-State admission call. Exact proposal→retained State COPY→State.profile→matching KEEP Profile establishes historical namespace. Exact COPY/KEEP/staged/proposal bytes, sizes, row ordering, paths, schema and closed inventory are checked and rechecked. Required KEEP drift fails. A changed mutable live State/COPY original does not by itself invalidate retained-set persistence.
- `RETAINED_SET_CAPTURED` and `RETAINED_SET_VERIFIED` do not establish current correction eligibility, genuine semantic approval, historical successful invocation or State adoption. Producer fingerprints without retained bytes remain observations, not attestation or implicit current-code authority. The set is dependency-bearing, not a self-contained backup.

P1's destination-absence refusal remains unchanged after capture. No CLI, config registration, reason enum, publisher/receipt/Gate/controller change, new Human role/Gate, live replacement or State transition was added.

## 2. Exact identity / available content

- Active: `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`.
- Final saved-patch apply copy: `/tmp/opencode/jgas-dm021p2r-verify-20261014T000007Z/candidate-partial-b40de60`.
- Actual detached HEAD **409b292756dd1277b9dfae87679934c0d2ce251c**, tree **8ce3699861505f32d1d60bdc185d4d4f635aedb2**, plus **16 uncommitted paths (3M+13A)**. HEAD alone does not contain P1/LF2I/LF1/P2R. Physical0664/logicalGit100644 at saved pins. No staged/intent delta observed; this is not a literally empty tracked-file index. No new candidate branch/commit.
- Active has **84 preexisting cache files**, separately pinned and preserved. Final v9 full raw status was exactly16 source rows +84 preknown cache rows; both sets and source/cache hashes/modes/sizes were guarded. Fresh absent PYTHONPYCACHEPREFIX + disabled bytecode writes prevented reuse/rewrite of in-tree cache residue in that run.
- [Final packet](../notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/) `expected16-correction2c.json`, `inherited13-static-freeze.json`, `cache-inventory-static.json`, v9 pre/post and proof clean/applied JSON bind the content. P1 original active and apply copies were preserved; inherited13 match final P1 freeze.
- Complete saved patch **`complete-p2r-16path-v3.patch`**,830622B, SHA256 **5b79218e3c90fc8bcb11e39571e2ab1e8dfc52e04f5e98843937e4e876515208**. Final proof v7 checked saved hash, independent byte-copy separation (134 regular +96 directories per Git tree), clean409, direct `git apply --check`/apply and exact16 bytes/modes/status. Disposable-copy-only overlay/cache removal is disclosed; active was not cleaned.

Check actual availability before reuse. If copies disappear, verify the [four portable409 inputs](../notes/rephase-1-dm021-contract/availability-at-closeout.md), restore actual409 with a **new** fail-closed/member/hash/isolation procedure, then apply this **complete16patch directly**. Do not first layer P1/LF2I/LF1 patches, rerun old restoration/runner scripts, create a fake-root history or fetch current main. Partial/shallow DB,26309 missing blobs and unbundled runtime limits persist; this patch is content preservation, not full-history backup.

## 3. Final verification / evidence scope

**25 successful focused methods / 7936.817s / no skips / child0 + wrapper0**, final v9 at module3833/test4155/schema347, CPython3.14.4. Separate affected2/440.248s verified two repaired test mechanisms before v9; they are not additional distinct final coverage. Separately guarded optimized Weekly-positive1/250.016s passed; full-suite -O is unproved. No old P1-36/LF2I43+2 or intermediate10/19 transfer.

Actual accepted-chain synthetic Longform prose, Weekly envelope and real R1×2 predecessor controls exercise persistence, original-vs-active history, post-capture P1 refusal, no-P1/Git readback, lexical/alias/FIFO refusal, exact typed State/Profile chains and schema/row/input bindings, live-State replacement vs retained/KEEP/staged drift, short-write/zero-progress/fsync/close/identity failures, primary+secondary error preservation, root/ancestor/file replacement, late control/edition/retained inventory and post-readback in-place mutation. Source/test fixtures and review/PDF/Human records remain synthetic engineering evidence, not genuine approval or rendered publication acceptance.

Mandatory bounds:

1. **Initial/intermediate claims preserved:** root R1/R2 found actual path/snapshot/metadata/fault/oracle/guard gaps despite green runs. Initial10 and correction19 do not close those gaps. Fresh final review supersedes the earlier blanket R1–R6 resolution.
2. **Interrupted result:** correction v4 failed18 (17 successful); v5 has only pre/meta and no reconstructable result. No inferred success. Final v9 followed v8's failed25 (23 successful) and two test-mechanics corrections, with all raw/version history preserved.
3. **Oracle precision:** the final late-plant test removes its injected file/dir before strict equality; immediate `post` is captured but unused. It proves final-inventory refusal and post-removal equality, not preservation/no-write at the injected path. Other immediate no-write oracles and read-only source support the component. Read root qualification and independent §10; blanket “every mutation compared before repair” is withdrawn for this case. Generic KEEP distinctions do not prove all X Profile topologies.
4. **Proof scope:** v7's actual application/all-entry/static-pin outputs support this run. Its logger `_emit` can suppress output flush/close errors, so it is not a generic certified logging/proof tool. Effective-config observations are bounded, not an arbitrary future configuration guarantee. Snapshot equality is not continuous no-drift/global CAS/crash atomicity.
5. **Proof setup failures:** v3b–v6 freeze attempted to read NEW files that the proof itself had deliberately removed to make clean409. Final `freeze_clean` corrected that logic. External deletion/timer/sparse/stray-process hypotheses were retracted; this was a Worker proof defect, not a new unexplained source disappearance. Diagnostic scratch and strace remain evidence.
6. **Historical preservation:** one UNEXECUTED proof draft was accidentally deleted/restored from transcript without byte-certification. Tool substitutions, wrong-cwd collection, cache residue, initial print-only/filter guards and missing exit/post records remain disclosed. Final test is **1818 lines**, correcting report1802; exact hash/size/method count was correct. Saved scripts remain historical exact-run evidence.

## 4. Next bounded unit after Human continuation

**General: retained-aware current-authority validation contract analysis, before code**, on exact409+16file composite with contract194fd7de/P1 constraints and saved intakeafdb3df3. Reuse available copies; no old-suite/recovery/intake refresh by default.

Return to Astra:

1. Exact current authority predicate binding fresh canonical State/Profile, original checkpoint, active-before receipt/Gate/accepted upstream/current controls and the immutable proposal against an already verified retained set.
2. Minimal public/helper split or separate verifier alternative that preserves P1's strict existing behavior while allowing a fully checked retained-context path; no permissive ignore-destination flag, trusted caller assertion, live-byte rollback, deletion or manufactured former State.
3. How stale State/epoch/upstream, changed retained/KEEP bytes, mismatched proposal identity and partial retention refuse; snapshot/failure boundaries and meaningful Longform/Weekly/R1 oracles. Readback consistency is not current eligibility.
4. Exact path/API/schema/test budget and cost comparison, including whether this read-only component can be bounded independently of the still-open staged-review-path/materialization/receipt/Gate/QA/reason/State adoption cycle. Return exact blockers instead of assuming that cycle solved.

No full promotion architecture or new reason/State pointer is selected by P2R PASS. Existing independent semantic/fidelity/visual review and normal Human Architecture/Preview/Freeze/Release remain separate obligations. Stop here; ordinary reconstruct Commit/Push and candidate-commit authorization remain Human-owned.
