# LF-2 design-review resolution / LF-2I entry conditions

2026-10-09. Astra author-side disposition of the [independent design review](independent-design-review.md), not relabelled independent approval. Selected [contract](../../outputs/rephase-1-longform-lf2-contract-decision.md) remains byte-unchanged, SHA256 **`4795a586c4fc77ff2cb168ca98216f6ecbb084f26e0fd10268b7c5d6778a36d6`**. Independent verdict is **DESIGN_BOUNDED_PASS**, no implementation/test acceptance.

## Findings and binding next-task instructions

| Finding | Resolution |
|---|---|
| F1 — Major proposal/contract conflict, resolved by precedence | **General `design-correction.md` §6's “Longform preserves that split” is superseded.** LF-2I must follow selected contract §4: “Public Longform receipt replay itself reloads and validates the persisted semantic review … Gate also reloads the review independently and binds the same file SHA.” Receipt self-digest + outer-Gate-only checking is insufficient for the new public receipt validator. Original correction remains historical, not executable task authority. |
| F2 — Minor count typo | Correction §6 says “five” but enumerates **six** categories. Treat this addendum as the correction; no merging of receipt object digest and review object digest, no conflation with file SHAs. Selected contract §4 defines exact fields/digest meanings. |
| F3 — Minor feasibility clarity | LF-2I must prove healthy FROZEN/RELEASED readback with valid synthetic current authorities, in addition to the two stage admissions. If an actual later-state fixture cannot be constructed under existing validators, STOP with exact raw/source blocker and proposed unsupported scope for Astra. Do not silently omit it and still claim the selected integration complete. |

The selected route is NEW, initial, and explicitly rejects legacy directive presence. It preserves substantive final-summary/Architecture/Human responsibilities while leaving directive-bearing-edition adoption unresolved. It uses direct agent-first validators/checkpoints, not the legacy dispatcher registry. These findings do not authorize a new Human gate, legacy directive check deletion, publisher migration or schema-allowed metadata promoted to authority.

## LF-2I first action after Human continuation

1. Verify `/tmp/opencode/jgas-lf2-design-20261009T113013Z` still matches fixed409 + exact LF-1 overlay, and original/LF1 copies unchanged. Use [contract §6](../../outputs/rephase-1-longform-lf2-contract-decision.md) as the implementation path/API/oracle budget. No recovery/31-suite/Summary refresh by default.
2. General fixes the concrete serializer/receipt/source-control closure list and evidence runner before implementation verification; any extra changed path must have an actual caller/contract gap and Astra selection. LF-1 load/readback separation and Gate schema/runtime/scanner changes are real deltas, not read-only reuse.
3. Implement one integrated initial route and obtain meaningful tests/source review/author-independent resolution on the exact final composite. Source-only or receipt-only writer is not the selected completion. Use existing independent synthetic committed fixtures for Git-aware predicates, without weakening production dirty/untracked-source checks. The unchanged HEAD must never be presented as containing new code.
4. No candidate commit/branch/ordinary reconstruct Commit/Push is authorized by this design verdict. Production read-only/baseline774/no new intake boundaries remain. A coherent implementation closeout or a concrete authority/feasibility blocker is the next Human Commit Point.

## Evidence qualification and full document pins

Root re-hashed the current documents after reading the report (which prints abbreviated hash identifiers):

- Contract: `4795a586c4fc77ff2cb168ca98216f6ecbb084f26e0fd10268b7c5d6778a36d6`.
- General original proposal: `23b2e4dc61a92963b010d495a9377720a9de206c1eab0aca1fbff86f30ed4bf3`.
- General correction: `042d0491723f496c02ebe2dbbd84b9d86ac54526bb7f9606bb303ddb0f150729`.
- Independent report: `bb516177400e9078cf6b9105cb425060d3859cf9934dc79624e6c674aa9646ac`.

Preparation [qualification](evidence-20261009T113013Z/preparation-qualification.md) is mandatory.689 compared entries are materialized tracked files,31466 both-absent tracked paths are sparse absence, not26309 inherited missing Git blobs. First copy succeeded then sparse comparison failed; that attempt's destination was removed/recreated, logs retained, saved script now reflects corrections rather than the first-attempt bytes. Original input copies were not reset. Initial guard omission/config-exit/retry limitations remain; later current verification only corroborates current identity/separation.

Additionally, `current_verify.py` logs sparse lists rather than asserting their equality, and checks origin fetch/push rather than asserting the absence of every other remote. Its output is a bounded current observation, not a certified all-configuration or rerun guarantee. Root/reviewer actual source/identity reads support the design basis only. No LF-2 candidate code/test/fixture/build execution occurred; LF-1's final31 result remains historical at its exact hashes/runtime.

Stop at this design Human Commit Point. Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted; LF-2I implementation has not begun.
