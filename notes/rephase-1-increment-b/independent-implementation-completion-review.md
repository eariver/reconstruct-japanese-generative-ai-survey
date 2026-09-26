# Increment B — final independent bounded implementation review

2026-09-26 JST. **PASS for the bounded Increment B implementation at `c04f32ad46109403e8a63faaa8394a90ee6b869c`, against Increment A.** I identified no unresolved blocking finding within the selected Weekly complete-reader-input, independent derivation and bounded pending-publication contract. This is my own final independent judgment after inspecting the complete runtime/schema/style/caller delta and its relevant test oracles. It completes the independent implementation-review step for this increment; it does not complete whole B3, the canonical seven-point audit, application acceptance or production adoption.

## Independence, scope and exact binding

I am the fresh independent reviewer who produced [independent-resolution-review.md](independent-resolution-review.md), separate from the candidate authors, test executors and root's author-side assessment. Root subsequently extended the task from two-finding resolution to the full bounded Increment B implementation review. I reused my own exact-candidate/evidence verification and independently inspected the remaining implementation; the earlier Auditor's observations served as navigation, not substitute approval.

The prior [independent-review.md](independent-review.md) remains unchanged and IN PROGRESS, without that Auditor's final successor judgment. My scoped resolution report also remains unchanged. This new report supplies my final bounded implementation judgment, rather than retroactively relabelling either earlier report.

| Identity | Exact value |
|---|---|
| Candidate | `c04f32ad46109403e8a63faaa8394a90ee6b869c` |
| Tree | `7dbcbbdb499ea6c7d33417a16144107320e1fd06` |
| Immediate parent | `cb96ab97045b0d0767f38806809d33e383bac73d` |
| Increment A comparison base | `1a9649129d1745fed0b98db46ef15f014407e6fc` |
| Fixed production baseline | `774dd39a951c9ac3818e83dfffd4c7666efb0a20` |
| A-to-candidate patch SHA-256 | `bdff2c296867b31dbc2946526ec97490c054bc48c4ab9a8473eb5ded1248ab81` |
| Patch bytes / changed paths | 287397 / 21: 13 runtime/schema/style and 8 tests |

My preceding report records independent verification of [candidate.json](candidate.json), all 21 committed/worktree/packet-copy bytes and hashes, exact binary [patch](increment-b.patch), clean tracked fixture, inert origin and no alternates. The same fixed candidate and raw artifacts are used here. This review read the isolated `/tmp/jgas-rephase-increment-b-sol-implementation` source and its A comparison objects only. No production/main/network access, candidate mutation, tests, commits, or fixture object creation was performed by this reviewer.

## Implementation reviewed and conclusions

### Complete reader input, accepted sources and rendering

I inspected the new [Weekly derivation helper](changed-files/scripts/survey_weekly_derivation_v2.py), the [publisher](changed-files/scripts/survey_weekly_semantic_publication_v2.py), the three changed/new schemas, and the old publisher's corresponding source against A. The new object includes emitted cover, frontmatter, heading/summary/section text, exact accepted Result blocks including Result-only Claim Boundaries, visible issue/window/date values, ordered citation placements, ordered bibliography values and the generated route's displayed style labels. Main TeX and bibliography consume this same object. The complete reader schema is strict, and the schema helper uses a format checker for dates. The obsolete partial builder fails explicitly rather than producing an incomplete object.

`load_derivation` (helper line 448) validates current State and resolves exact checkpoint-bound Profile, Architecture, Draft Package/Result, Synthesis, Evidence, Candidate Matrix, Materiality and Discovery inputs. Its receipt separately records authored publication/archive inputs. Draft Result and Synthesis validators still run. The Weekly closing source is precisely the contract-selected accepted `profile_payload.current_interpretation`; its exact inclusion in the final summary is required. This resolves the old contradiction with the valid empty Weekly publication payload without adding a general fallback. Publisher lifecycle remains DRAFT_COMPLETE, and current controller validation replaces the obsolete hard-coded action string.

The [shared citation resolver](changed-files/scripts/survey_drafting_citation_refs_v2.py) is a faithful extraction of the existing exact-one, package-authorized resolution, including NONE rules, ordered deduplication and claim/event/limitation behavior. The drafting caller delegates to it. Projection compares rerun deck and per-block refs against accepted Result refs, rather than assuming matching prose or archive hashes imply citation identity. Bibliography selection loads the actual accepted Evidence cards and their exact hashes via the real acceptance validator, joins their URLs/access dates to accepted Discovery/Matrix/Materiality, rejects inconsistent status/materiality and ambiguous captures, and does not consume the unaccepted interactive Evidence selector. The literal `Unknown` author fallback is the selected contract, consistent with the old production join's absent organization value.

I compared old/new rendering and read the entire copied [style](changed-files/templates/survey/jgaisurvey.sty). The changed style labels preserve existing defaults and layout interfaces, while the Weekly renderer explicitly supplies their reviewed values. Unused Special interfaces remain unchanged. Dynamic per-result/block comments were removed rather than permitting unreviewed text to execute through comments. Main prose is escaped by the existing helper; bibliography title/author escaping, unsafe controls/backslash/URL-brace rejection, citation-key syntax, and literal URL/access-date preservation are explicit. The selected fixed main/bib/style include boundary and closed local directory are checked; this is not a general TeX interpreter or a guarantee about arbitrary future trusted-style changes.

The nonreader separation is real at projection level: internal runner annotations are not serialized into the reader object. Exact upstream authority still rejects in-place checkpoint drift. No new authority is inferred from an unchanged reader projection.

### Gate, exact target, independent replay and current implementation

I read the complete [Gate delta](changed-files/scripts/survey_reader_surface_gate_v2.py), current exact-manuscript admission/readback, the [reader wrapper](changed-files/scripts/survey_reader_publication_v2.py) and both [stage call sites](changed-files/scripts/survey_stage_validation_v2.py). The explicit derivation block is required and included in the Gate digest. An explicit structured surface must match the persisted review target. A non-primary review target is admitted only as the schema-valid supported Weekly generated route; malformed objects and other profiles do not fall back to best-effort scanning. Direct-primary admission requires the exact primary target and is explicitly `PRIMARY_ONLY`.

Generated Gate creation and readback call `validate_receipt`, which verifies the receipt schema/digest, exact named inputs, current implementation/contract, current accepted authorities, complete independently recomputed reader object, deterministic main/bib bytes and copied style bytes. Gate checks then link that receipt to the persisted semantic review and the selected manuscript's primary plus exactly the bibliography/style support files. A freshly rehashed output or reader object therefore cannot succeed on self-reported hashes alone. Both stage sites and actual publication revalidation continue to supply the exact selected manuscript and now also the actual State path.

Current-tool validation (helper line 550) checks that the generating commit exists and is an ancestor; all configured implementation roots, the config itself, contracts and style are unchanged across that commit and current HEAD and clean against committed bytes. The eight-member explicit closure is exact by name/path/hash and is checked at both commits. The unchanged config's implementation roots cover scripts/schemas/config/workflows, so the new helper/schema paths are not outside this comparison. Artifact-only HEAD movement is permitted without substituting initialization identity or transferring an independent review to a new candidate.

The canonical directory/output-path correction is independently resolved in my earlier report: the guard runs before generated source/receipt writes and on replay, rejects all undeclared entries and aliases, and cannot be redirected to identical decoy outputs. No new issue was found on the broader review.

### Pending publication, immutable predecessor and authority writes

I inspected the full [agent-controller delta](changed-files/scripts/survey_agent_control_v2.py), surrounding strict State/checkpoint validation and revalidation producer, and the [runtime wrapper](changed-files/scripts/survey_agent_tool_v2.py). The public State validator remains strict. The private pending object is not a persisted record or approval; it binds actual canonical State bytes/path, repository, config, current HEAD, validation reference, exact changed/preserved row snapshots and predecessor pointer. It applies only at pre-decision VALIDATED_DRAFT with intact approved Architecture, pending downstream gates/checkpoints and inactive Exception Gate.

The allowed changed rows come from configured canonical validation artifact roles plus the canonical Reader Gate. Duplicate/unknown/changed upstream roles cannot enter that replacement set. `_verify_pending_binding` rechecks the actual files, and `_validate_agent_state` continues schema/Profile, deterministic checkpoint result, lifecycle/controller/history and Architecture approval validation. The private resolver refuses pending validation outputs as upstream accepted authority. The Evidence basis wrapper forwards this context to the same complete validation and restores patched functions in `finally`; its older historical accepted-package exception is not expanded to arbitrary non-State drift.

For an existing pointer, immutable predecessor validation retains pointer/file SHA, schema, issue, exact prior checkpoint, pre-decision establishment, bounded chain/chronology and exact superseded/preserved row-union checks. QA references must agree with their artifact rows. Historical predecessor live-publication-byte comparison is skipped only in that historical read; active authority validation still compares live bytes and preserves Human/Freeze/Release agreement. A malformed predecessor is not accepted merely because publication files changed.

The real revalidation operation rebuilds the pending basis, requires exact agreement with the superseded/preserved rows, validates manuscript/quality/semantic/visual/Gate evidence, and rechecks the basis immediately before writing. Only this operation writes the new immutable record and State pointer. Post-validation failure restores the State bytes it wrote and removes its newly created record, while refusing to overwrite a concurrently changed State. This is the selected bounded rollback, not crash-safe general transactions or concurrent-writer certification.

## Evidence and oracle assessment

The already independently verified [final script](final-matrix-c04f32a.sh), [raw log](final-matrix-c04f32a.log) and [exit](final-matrix-c04f32a.exit) record **132 methods across 14 modules, 534.724 seconds, OK with one skip, exit 0**, at the exact candidate/tree/parent above. The 132 count is methods including the skip; it does not add subtests as separate methods. Python 3.12.14 is recorded. The `pip show` metadata attempt failed (`No module named pip`), so dependency versions are not independently established by that command. The sole unavailable W34 historical-object test remains skipped, not passed.

I read the new B integration/boundary tests and all changed legacy test diffs, rather than treating the result count as the oracle. The test fixture initializes its own independent inert-origin Git database from copied tracked source and uses real accepted producer/checkpoint validators. Research, authored review decisions and the parseable blank PDF remain synthetic. The only authority-validator fault injection in the generated integration method is confined to the explicit post-write failure/rollback negative.

| Obligation | Evidence inspected and assessment |
|---|---|
| Two-pass producer and review stop | Main B integration method materializes the complete surface, rejects missing/non-PASS/wrong-target review before TeX/Bib/style/receipt writes, then generates successfully. |
| Ten historical omissions plus two controls | Projection/render variants change the reviewed object and rendered main, and persisted stale review fails. These are twelve variants in one method, not twelve accepted editions. |
| Actual accepted distinct-ID substitution | New live two-ID producer/checkpoint chain has a positive baseline; archive-only replacement with unchanged accepted Result refs fails at exact placement comparison. B-IR-01 resolved. |
| Independent replay and support | Freshly rehashed main/bib/style mutations fail deterministic replay; a rehashed unrelated reader object fails recomputation; undeclared local entries and rehashed decoy receipt fail actual receipt/Gate validators. B-IR-02 resolved. |
| Bibliography and evidence | Actual accepted-card join, date/URL/title/key/order assertions, ambiguity boundary using a real accepted-content loader, and stale card hash rejection. The alternate acceptance is not State-adopted. |
| Current source identity | Dirty helper/config, committed implementation/config changes, missing/unrelated commit fail; an artifact-only commit with unchanged closure succeeds. |
| Pending and actual renewal | Generated Gate/receipt after VALIDATED_DRAFT, real first and repeat metadata renewal/revalidation/readback, malformed pointer/chain, rehashed predecessor QA mismatch, copied/aliased State, stale row snapshot, wrong role/path, unrelated controller/history and upstream drift negatives. |
| No-write and rollback | Malformed QA and wrong implementation override preserve State/record history; post-write validator fault injection restores State and removes the new record; subsequent real positive path uses actual validators. |
| A and adjacent regressions | Exact selected-manuscript tests, existing stage/controller/Evidence-basis/revalidation/revision/Freeze/cross-package-ref and bibliography modules are included at this head. Their earlier green results were not transferred. |

The two old mocked publisher review-stop tests are replaced by the real accepted-chain integration assertions; the old publication-payload fallback pseudo-test is replaced by positive valid-empty-payload and exact approved source negatives under the selected contract. Gate/revalidation legacy fixtures now explicitly review the primary route, retaining those tests' exact-target purpose without pretending malformed old JSON is generated-route evidence. The two obsolete API modules retain their applicable assertions against current interfaces. No schema or authority validator was weakened to make their old fixtures pass.

The initial cb96 matrix remains **131 methods / 366.832 seconds / six obsolete-API errors / one skip / exit 1** in [attempts/cb96ab9](attempts/cb96ab9/). Earlier setup/integration failures and interrupted work remain historical evidence. The final green matrix does not rewrite them. My own read-only inspection encountered an unavailable WSL `rg` executable and used Python search; this was a tooling fallback, not test execution.

## Findings and final limits

- **B-IR-01, P2:** resolved at the final head by the live accepted-ID oracle, as independently detailed in [my resolution report](independent-resolution-review.md).
- **B-IR-02, P2:** resolved at the final head by canonical closed-directory admission plus real receipt/Gate/producer negatives, under the selected scope.
- **New unresolved blocking findings:** none identified in this bounded implementation review.

The evidence supports Increment B's selected Weekly input/derivation boundary and bounded pending metadata revalidation. It does not establish actual research truth/editorial sufficiency, real Human approval, real TeX/Bib rendering or visual correctness. The unchanged build workflow has no demonstrated auxiliary cleanup integration: `.aux`/`.bbl` and other undeclared build entries deliberately stop admission. External packages/search paths and global build behavior remain separate responsibilities.

Direct-primary remains primary-only; LONGFORM/Special/Retrospective support and whole-profile publication are not accepted here. The generated renewal fixture changes publication metadata, not publisher CLI regeneration after a Core change: that CLI remains DRAFT_COMPLETE-only and refuses existing artifacts. Full #495/application integration, Windows, Actions, the missing W34 historical regression, clean full application-patch proof, canonical seven-point audit and net lifecycle savings remain unproved. Historical RELEASED editions are neither revalidated nor invalidated.

**Final judgment: bounded Increment B independent implementation review complete/PASS at this exact candidate. Whole B3 remains OPEN; the whole candidate remains NOT_READY. Production adoption, ordinary reconstruct commit/Pull/Push and real Human Gates remain Human-owned.**
