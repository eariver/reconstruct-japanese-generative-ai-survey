# Astra renewal implementation closeout — mandatory qualifications

2026-10-26. Author-side synthesis/review. **Selected bootstrap＋U/C versioned renewal operation BOUNDED IMPLEMENTATION COMPLETE, qualified composite.** [Assessment](../../outputs/rephase-1-versioned-renewal-implementation-assessment.md) gives scope/source/next task. Contract478f0051 including §11 and pre-code ROOT7d7d5a45 including §6 remain design authority; implementation/evidence corrections below govern this delivery. No whole-candidate/adoption approval.

## 1. Accepted source and API boundary

Final actual409/tree8ce + **40M53A=93**, intended742 files. Complete DIRECT409 patch **f898d33bfe6904fd29063d5a1ff462588d11f227f5aab6a3a2d505614941da2a /3423014B** in `source-packaging/final-depth-20261025T205432Z/`; manifest **d488c6ee48b7cfa781f39905c4f08a61561e7bd02b234d2c60a6a1e93953497c**. First92 `d6c72fb4…/3415062B` is obsolete: reviewed depth HIGH3db and testea2646 had not reached the candidate. Exact2-file delivery (+27/-0 HIGH, new test) and fresh final GEN/PROOF corrected this; the first artifact/proof is preserved.

Final runtime pins: HIGH **3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b**, H **74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d**, S **2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb**. P1 `825dba1d…`, PUB `3f4039fd…`, Reader `098a2c82…`, editorial-high `85814124…`, P3S `9e2a0ad6…` are fully pinned in the final manifest.

The public operation includes `prepare`, C `prepare-targets`, external review/QA inputs, `finalize`, detached receipt/set validation, `activate`, explicit `resume`, and history/readback. `prepare-targets` is accepted as the C preparation half, with unchanged authority and build-record-before-receipt rules. It is not a new permission surface.

Preserve LIVE public State validation and exact canonical/prePreview/Exception checks. History/source never call current State validation. File refs always hash complete serialized bytes; self-digests only occupy their explicitly named internal field. Historical tool inputs (including template style) bind owned commits; immutable output trio/evidence bind original live/COPY bytes. OLD50/NEW63 is owned-epoch contract/schema compatibility, not presence-only guessing. Whole-document schema pointer remains `""`.

## 2. Evidence composition — no global test total

The [independent evidence ledger](resume-20261025/independent-final-evidence-ledger.md) **with FINAL-BINDING addendum** is the per-case index. Its earlier LF/crypto-cycle/packaging “blockers” are superseded there, not silently ignored.

| Required category | Adopted bounded evidence |
|---|---|
| Genuine old R3 bootstrap / U / C | Both generated routes, original source721a04d before old authority; later real tool commits, U exact reuse, C style/source change and real5-page PDF/new reviews. Isolated synthetic identities, not candidate ancestry |
| Repeat | Both C→U→U; Longform failed same-epoch U3 is harness sequencing (G3+G4 both before U2), then actual G5→U3b succeeds. Old failed orphan preserved |
| renewal→editorial | Weekly current741 all public stages through real build/finalize/activate/history/current exit0, no manual module preload. LF newEDITORIAL63: failed/TIMEOUT writer attempts preserved, then clean explicit `resume ALREADY_ACTIVE`/set/history/receipt/State exit0 closure |
| Normal lifecycle | Both actual State `RELEASED / COMPLETE` through public stage/checkpoint/advance/Preview/profiled Freeze/release APIs and validate-state API+CLI on739 series. Earlier low-level files with VALIDATED State are not counted |
| R1 anchor | Two actual R1 refreshes→editorial→renewal, latest legacyr2 preserved; correction after initial wrong-DRAFT anchor bug tested before writes, original bad State retained. New-copy construction from exact before-COPY is fixture setup, not operational rollback |
| Orphan / IO | Complete same-intent orphan ordinary activation refuses, changed reason/time cannot allocate a second record; explicit full resume works and already-active retry is readonly. Record/temp/write/shortwrite/fsync/close/combined/replace/postread/foreign/path controls have case-specific windows/repairs |
| Depth/cycle | 30 provided typed legacy records＋actual editorial31＋public renewal32; next33 refused before R/record/temp/State writes. Gaps in filenames do not count as extra chain entries. Not32 actual operations. Public malformed-cycle SHA rejection and separate defensive cycle probe are different evidence |
| Affected regression | Report by module/source/run only. R1 33＋targeted pointer/healthy, P2R24＋inode-hook1, P3S25＋O1/current63 and fresh public2 routes, H2/S18, Reader7 skip0, bare-function15 actual assertions, H/perf/traversal and other original affected modules with their own scopes |

H batching/traversal optimization was measured and reviewed: immutable raw Git batching is per invocation, each unique owned typed source/schema node receives full validation once per public history call, repeated edges retain fresh pin/registry/order/exact predecessor checks, and final E pins are rechecked. No persistent/global authority result cache, caller-verified graph or public skip flag. Microbenchmark gains are not measured total lifecycle savings.

## 3. Rejected implementations, findings and recovery qualifications

* Initial M1 was an unsafe scaffold, not faithful implementation: basename-only State check, invented pointer/layout fallbacks, placeholders and shallow static tests. Its new-root Git identity `a8890d4` is preserved but rejected as actual candidate ancestry. A fresh independent actual409 workcopy with exact721 input and25M32A was established; full input comparisons and setup failures are recorded separately.
* H/S drafts contained optional required checks, swallowed errors, missing schema instance/scope validation, E-at-tool-commit and live-before-State mistakes, incomplete observed bindings, caller-row-derived epochs, and hash-only accepted graphs. Root/independent corrections are preserved. Final evidence does not promote early5/7 static/shape tests to operation acceptance.
* Source reverify compared fresh bytes to fresh bytes; Discovery JSONL had an unchecked second read; CURRENT tools lacked committed-tree checks; C manuscript could omit serialized proof; HIGH aliases/pin rechecks and Freeze dependencies were incomplete. All were corrected with bounded public/mutation controls and code review. The review's original “divergent Freeze target would be overwritten” exploit claim was wrong: `_existing_compatible_bytes` already refused divergent bytes. Missing explicit overlap/transitive snapshot coverage nevertheless required repair.
* P1 dispatcher and editorial-high archive selection did not fully recognize the renewal receipt; P3S required test-side preloading of its expanded dependencies. Strict per-kind public receipt handling and P3S function-local CURRENT imports corrected these. No foreign module reloading/rebinding or relaxed tool pins.
* SELF-in-`proof.basis_ref` was a writer/validator defect. The proposed H exception was rejected; all refs use FILE SHA. Old SELF-era sealed sets are nonpositive history. Unbound companion sidecar creation was rejected; companion evidence is inside the build record/self-digest.
* Ordinary activation of the same inert set/basis could allocate r3 around orphanr2. That observed `ACTIVATED` is a **product defect**, not a successful “max-advance” recovery test. HIGH now refuses matching intent; unrelated new set remains distinct. Wrong legacy anchor and late33 refusal were likewise repaired before writes. A planned-after-State structural check is a pre-install consistency check, not replacement LIVE authority or a public synthetic-State bypass.

No unsupported reset, rollback, cleanup or overwrite is inferred from successful later cases. Partial or complete valid artifacts can remain after a failed invocation; that does not make the invocation successful. Explicit resume/readback on those bytes is separate evidence.

## 4. Failure and evidence-loss record

Preserve the earlier provider failure/empty/cancelled returns and the lagging TURN3 summary. Subsequent run35–61 activity existed despite missing return text; it was reconciled, not deemed unexecuted from a hash mismatch. Human asked to stop investigating the cause; work resumed using fixed snapshots and disjoint parallel tasks.

Preserve source-copy/index omissions, `.latexmkrc` missing test fixtures, EDQUOT/setup failures, CLI/harness errors, invalid authoring, premature/wrong-root calls, wrong outcome-key assertions, metadata chronology errors, failures/skips/TIMEOUTs and incomplete outputs. P2R's `unlink+write` hook reused the same inode on ext4, so no replacement occurred; a baseline/control and rename-held-old-inode test corrected the oracle, not the product guard. R1's pointer-message oracle and P3S's old50 assertion were corrected only for the intended current refusal/63 membership. Reader tests now use matching epochs/import roots instead of ignoring genuine drift; pytest-style bare functions were actually invoked, not counted as0-test passes.

The first healthy-u1 run had no original terminal raw; later metadata reconstruction is **observation-only**, not recovered execution evidence. Missing exits, empty command logs and preempted seams keep their own limits. The confused worker16-HIT aggregate is withdrawn; use named ledger rows. Temporary/cache deletions and the earlier inaccurate claim that fixture parents were removed are disclosed in the preserved worklog; root did not certify losslessness or generic rerunners. Some original test-owned scratch cleanup remains outside a universal preservation claim. No continuous no-drift, global CAS, crash atomicity or filesystem immutability guarantee.

## 5. Independent conclusions and delivery scope

* [Authority review](resume-20261025/independent-authority-review.md) **§§14–15**: bounded H/S/authority PASS, qualified source composition, final3db delivery bound.
* [Operation review](resume-20261025/independent-operation-review.md) **final delivered-source and FINAL-BINDING conditions resolution**: bounded operation/consumer/IO/evidence PASS. Its earlier six affected-test/pytest conditions are disposed by the later actual test-only runs; original failures remain.
* [Evidence ledger](resume-20261025/independent-final-evidence-ledger.md) **FINAL-BINDING addendum**: LEDGER_BOUNDED_PASS, no essential category blocker. No count summation or full-matrix inference.
* [Reader/visual review](resume-20261025/independent-reader-visual-review.md): actual4 PDFs/20pages fidelity/visual bounded PASS, **Production semantic/representative-quality NO-GO**.
* [Final packaging review](source-packaging/final-depth-20261025T205432Z/independent-final-packaging-review.md): all93 SHA/byte/mode and all742 intended bytes across candidate/GEN/PROOF checked, saved DIRECT409 apply0/check0, bounded packaging PASS.

None is the final independent seven-point whole-candidate audit, Human adoption or genuine approval. Source proof is scoped689 available base＋53 new; missing26309/bulk31466/runtime/TeX limits and5 apply whitespace diagnostics remain. Full hydrated/tree-clean/history backup or certified safe rerun is not claimed.

## 6. Next task / stop

After Human continuation, General/Explore analyze **DM022 pre-Architecture accepted-upstream correction applicability and its integrated contract** on final93 plus existing narrow capture. Include necessary Profile constraints and normal regeneration alternatives, exact old/new accepted authority, downstream invalidation, failure/resume and cost; compare to post-VALIDATED correction/renewal without conflating them. No Production refresh/rebaseline/network or implementation of an unselected migration is implied.

**Stop at Human Commit Point.** Ordinary candidate/reconstruct Commit/Push remains Human-owned. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN; necessary Profile/representative quality/fixed candidate/adoption/real operation/savings remain open.

## 7. Closeout documentation checks

The read-only closeout check confirmed current entry links and the final-review precedence. It found transcription errors in evidence-ledger D3's long hashes; the ledger author appended **D7 FILEHASH ERRATUM** and JSON `D7_file_hash_erratum`, preserving the mistaken strings as history. D7 overrides D3 for those hashes; scope/verdict/counts do not change.

Root then freshly rehashed the selected contract478f0051, pre-code ROOT7d7d5a45, FINAL patchf898d33b and manifestd488c6ee and confirmed the complete hashes shown in this closeout. `git diff --check` passed. These are document/delivery checks, not additional runtime tests or a new full-source guard certification. No ordinary Commit/Push was performed.
