# Astra integration corrections — active implementation, not closeout

2026-10-25. Human continuation at `f84fcf5`. Parallel read-only reviews, disjoint author repairs and fixed-input route tests are separate evidence. Contract478f0051 and pre-code ROOT7d7d5a45 including §6 remain binding. **Whole implementation NOT READY; no Human Commit Point or implementation acceptance yet.**

## Binding dispositions

* Preserve all cross-document refs as FILE-BYTE SHA256, including `proof.basis_ref`; SELF digests appear only in named internal fields. No exception to accommodate an earlier writer defect.
* Current-source verification must compare committed and loaded/live tools on every public readback. An artifact-only descendant HEAD is allowed only with unchanged eligible control/tool predicates; do not require blind HEAD equality or accept live-only hashes.
* U rederivation includes the **current template style**. `staged.style_input_ref` is historical T at its recorded producer commit; `staged.outputs.style` is immutable E at its original path. Do not rewrite old authority to make a style-change test pass.
* Supported editorial records can have OLD50 or NEW63 closures, selected from their actual owned epoch and finite contract/schema registry. Renewal→editorial is not permanently OLD50 just because the editorial kind is unchanged.
* Freeze must snapshot and alias-check the complete finite typed evidence dependency set. Group shared checkpoint wrappers by exact `(path,sha)` across their producer roles before checking the union of required artifacts. Never invent `sources/{issue}` paths, a required `R/qa-checks.json`, or exactly one historical scope. Follow Profile/retained provenance, bundle result refs and typed materialization lineage.
* The original operation review's “divergent target would be overwritten” claim is retracted: `_existing_compatible_bytes` refuses divergent files. The missing explicit renewal overlap/snapshot coverage was nevertheless a contract gap and is being repaired.
* `prepare-targets` is accepted as the declared C preparation half, with the same authority checks and build-record-before-receipt order. It creates no new authority or bypass and cannot rebuild already reviewed targets during finalize.
* P1 must dispatch a renewal receipt through its public current validator and use strict per-kind fields/typed scope lineage. A valid new-kind receipt must not fall through to the old canonical kind or be rewritten into an editorial receipt dictionary.

## Bounded history traversal optimization

Measured profiling shows repeated instance validation of the same historical evidence/schema node dominates deep-chain readback, and a valid P1 call on a seven-record chain exceeded its1200s test bound. Increasing timeouts alone is not a completeness result.

A General author may restructure **one public history invocation** so each unique typed `(source ref, schema path/pointer, schema epoch/hash)` node is fully validated once when independently derived at its owning ancestor. Subsequent predecessor-array edges in that same invocation still require strict row shape, safe fresh source-byte/ref checks, registered epoch/schema/pointer identity, canonical order and exact equality to the independently derived predecessor graph. Recheck all pinned live evidence before returning. No source/schema node may be accepted merely because a claimed row mentions it.

This is a finite graph traversal, not a persistent validation-result cache. No global/ambient authority cache, caller-supplied verified graph, public skip flag, cross-invocation permission or omitted predicate is authorized. Every public call starts fresh and independently validates all its unique nodes, current/history domains remain separate, and late byte changes refuse. Existing schema files and constraints remain unchanged. If these conditions cannot be met, return the exact blocker before changing semantics.

Before/after tests must compare complete public results and intended failure classes on the same real history graph, including malformed schema instances, unknown epochs/pointers, omission/duplication/order, late evidence mutation and repeated calls after mutation. Report actual source pins/times/call counts; a synthetic microbenchmark is not whole-operation work savings. Independent review must inspect this traversal before implementation closeout.

## Failure/resume oracle correction

The fault worker observed ordinary `activate_renewal` allocating r3 while a complete r2 for the **same sealed set/basis** was still inert and State remained before. That is a product defect against the selected explicit-resume contract, not a passing “max-advance” recovery case. Preserve the raw observation and reclassify it. Ordinary activation must refuse the existing matching intent before creating another record; changing free-text reason/time or choosing the next global sequence must not bypass this refusal. Explicit `resume_renewal_activation(record_path)` still performs complete current revalidation and exact intent checks. A distinct new publication set is not automatically the same intent; sequence allocation must not become latest-record adoption. Unknown/malformed reserved records cannot grant permission or be deleted/taken over automatically.

The Longform U3 same-epoch refusal is a separate harness ordering error: G3 and G4 were both committed before U2, leaving no new tool epoch for U3. Preserve that failed r5; actual G5→U3b supplies the missing changed epoch. Do not conflate it with the earlier chronology failure or weaken the genuine-change predicate to pass the harness.
