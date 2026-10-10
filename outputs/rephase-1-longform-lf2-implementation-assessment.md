# LF-2I — bounded initial generated Longform integration completion

2026-10-10. Started after Human Commit/Push at reconstruct **a4dc0fd8d5ecbe5ab9d81f225c85cff25f69e930**, initially clean/local tracking synchronized without fetch. **LF-2I is bounded complete as a nine-file uncommitted overlay on409**, with Astra review and author-independent final resolution/supplement. Stop at Human Commit Point. Whole candidate **NOT_READY**, step4/B3 **OPEN**, canonical seven-point audit **unstarted**.

## 1. Exact source identity / preservation

Base HEAD **409b292756dd1277b9dfae87679934c0d2ce251c**, tree **8ce3699861505f32d1d60bdc185d4d4f635aedb2**, parent **34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4**, unchanged. That HEAD does **not** include the new component. Relative to409: **2 modified +7 added paths** (including LF-1). Relative to the preserved LF-1 component:3 modified +4 added paths. Config/legacy writer/dispatcher/fidelity/controller/revalidation schema remain unchanged.

| Path | SHA256 |
|---|---|
| `scripts/survey_reader_surface_gate_v2.py` | `e73058841cfa1a841030b96d5cd2fb756c6ba99d1b99522ddbf0131d1f06bbe4` |
| `schemas/reader-surface-gate-v2.schema.json` | `fe4a96f4aa87f2a527096c4d3040f92e0217ef972ddae1d7140498184a13322c` |
| `schemas/longform-publication-source-manifest-v2.schema.json` | `4dadf873096f31cf564a7db4fee42a1fc8cdd8fc039dd14a7ee01cf26043e8ca` |
| `schemas/longform-reader-input-v2.schema.json` | `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643` |
| `scripts/survey_longform_derivation_v2.py` | `c09c5558f9668906b7d2ed34c55281d5f6d9ed279d3237a8ffc18ac84ea41149` |
| `scripts/survey_longform_generated_v2.py` | `d480e11d1c398f79f3e894e2e1e1f56ceec507dfde376a163a58b0ebed97d3c2` |
| `scripts/survey_longform_semantic_publication_v2.py` | `4d235a388955dcedd34d6a7dc5ac7761f9fc91de8bc723eb11f68cec6a229195` |
| `tests/test_survey_longform_derivation_v2.py` | `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913` |
| `tests/test_survey_longform_publication_integration_v2.py` | `4a03b564f8fa4dd39f2b48766ddb7612cf2d8d4dacdcc42ac39f637d2bca11a4` |

- Active implementation: `/tmp/opencode/jgas-lf2-design-20261009T113013Z`. Physical source modes0664; non-executable Git mode100644. Bytecode caches from earlier runs are separately disclosed, not source authority or intended patch content.
- Independent saved-patch apply copy: `/tmp/opencode/jgas-lf2i-409bytecopy-20261010T033640Z`. ActualHEAD409, exact2M+7A after applying the saved full patch, all9 bytes/physical modes match. Zero shared object inodes with original409 observed; existing partial/shallow limits remain.
- Final [complete409→overlay patch](../notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/complete-overlay.patch) SHA256 **5c7e7503851f5cdbc30b6827560219f48ce75d4a6cf64ba13516ed97e0cea4f9**; [hash manifest](../notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/hash-manifest.json). Apply this to clean409, **not on top of LF-1 patch253e284b**: LF-1's files are already included.
- Original409 and LF-1 copies remain preserved. Recovery still requires existing b40 archive + DM001/01920pack + W1sevenpack + DM004final32pack to obtain actual409, then the complete9-path patch in a fresh independent copy. This is available-content preservation, not all-history/runtime backup or a new committed successor. Inherited26,309 missing blobs are distinct from sparse-absent worktree paths.

## 2. Selected contract implemented

[Contract4795a586](rephase-1-longform-lf2-contract-decision.md) and mandatory F1–F3 govern this **INITIAL THEMATIC/LONGFORM_SPECIAL four-family-lineage-v1** route.

- New public two-pass CLI: pass1 materializes canonical reader bytes only; pass2 requires an existing exact reader file and a persisted pre-TeX semantic PASS loaded through the real existing validator. No implicit pass1 in pass2, no generated semantic PASS, no legacy writer/deletion path.
- Pure main/bibliography serialization consumes the complete reviewed object, including labels/TOC/title/date/citations/final summary; copied trusted style is pinned. Finite heading/optional-argument/token/URL policies and the existing fidelity parser enforce the selected traceability boundary before source writes. This is not a universal TeX parser or generic-Thematic acceptance.
- Raw-first containment precedes file capture/read. Writer ties State/input/review captures to validation, uses the exact named Draft archive path/hash from derivation, checks accepted refs/reader/review files from disk and re-runs all-control-root/committed-source predicates before writes and receipt installation. Prospective receipt is validated before writes; installed receipt must equal it. Drift cannot be adopted merely by refreshing hashes.
- All predictable output/alias/partial-set checks precede mkdir/source writes. Exclusive creation retains/reports owned partial files on write/close/receipt failure; retries refuse partials unchanged. Same-byte pass1 reuse distinguishes no set, complete replay-valid set and partial/inconsistent set. No silent deletion, global CAS or crash-atomicity promise.
- Public receipt replay **itself reloads persisted review**, rederives canonical reader FILE bytes, exact accepted/authored/current-tool authority and main/bib/style outputs. Gate independently reloads review, scans all nested Longform display categories, requires `LONGFORM_GENERATED_V1 / LONGFORM_MAIN_BIB_STYLE` and exact selected manuscript/output support closure. Wrong same-issue manifests are refused at both stage-Gate sites.
- Default loader retains DRAFT_COMPLETE eligibility; read-only loader allows validated healthy DRAFT_COMPLETE/VALIDATED_DRAFT/RELEASE_CANDIDATE/FROZEN/RELEASED. Generation-State SHA is historical provenance, not later-state equality. No fake old-State dictionary/pending-basis bypass.
- Legacy directive presence still refuses. Normal Architecture/fidelity/depth/layout/Preview authority is preserved. Existing control-root +14-file closure pinning justifies leaving config registration unchanged; config/unlisted-helper drift is covered by the actual control-root check at snapshot boundaries.

The committed-tool guard remains strict: the uncommitted working overlay is not silently accepted as a committed publication basis. Runtime proofs use independent **synthetic committed fixtures** containing the selected source bytes. No candidate or reconstruct commit was created.

## 3. Verification, roles and proof limits

General implemented; a separate General corrected. Astra reviewed actual source/schema/tests/runner/raw evidence and raised R1–R3. An author-independent reviewer found C1 and resolved all corrections, including explicit correction of earlier missed findings. [Final resolution](../notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/independent-final-resolution.md), mandatory [Astra qualification/manifest annotation](../notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/astra-closeout-qualification.md) and [independent closeout supplement](../notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/independent-closeout-supplement.md) support **BOUNDED_PASS** for this exact component. Root did not implement or run runtime tests.

| Final-source run | Result / scope |
|---|---|
| `evidence-20261010T120000Z-correction3/run.log` | **43 successful methods /1822.421s**, no failures/skips:13 integration +27 Gate +3 LF-1 loader controls; CPython3.14.4, recorded pre/post nine-file hashes/modes/base/status, child0 |
| `evidence-20261010T035424Z-cli-compat/` | **2 successful existing CLI methods /99.827s**, same final nine-file pins: generated Weekly accepted-chain/receipt/CLI/readback and direct-primary absolute/relative/different-cwd admission; original bodies/fixture identity setup unchanged |

These are45 successful distinct methods across two bounded runs, **not one45-method suite**, not old6+33/44/42/31 transfer and not broad CI/canonical acceptance. Existing Weekly/direct-primary positive compatibility was explicitly checked rather than inferred from the added Longform branch.

Runtime proof includes actual subprocess Longform and Gate CLI, real synthetic accepted chain through both admissions and normal typed Preview→Freeze→release-checkpoint to healthy FROZEN/RELEASED readback. Same-issue decoy Gate backstops, fresh-rehash tamper/alternate serialization/canonical-path negatives, before/after snapshot seams, write/close/receipt-install faults, retained partial retry refusal, FIFO no-read alias probes and mechanical-only initial-operation variants are exercised. The PDF is a synthetic parseable blank page; semantic/visual/Human records are explicitly type/identity fixtures. No real TeX build/quality judgment/publication or operational regeneration owner is proved.

## 4. Preserved failures / qualifications

- Initial pass2 silently generated reader input; alias checks happened after resolution; snapshot values were unused; archive was reserialized; partial files were silently removed; complete patch omitted7 new files. These first-return code bytes/dev logs and six-method result are preserved.
- Subsequent root/independent findings corrected missing Draft archive, memory-vs-memory snapshot checks, caller-resolved publication aliases, mkdir-before-refusal, late receipt hash absorption, capture-before-path-safety and unlisted-control drift. Earlier reviewer PASS statements are explicitly superseded, not transferred.
- Initial runners did not pin all changed hashes, did not enforce all claimed environment restrictions, and offered toy hash/child probes as guard proof; early apply checked2M then copied7A from live source. Final saved patch is actually applied as saved on independent actual409. Test setup failures (including user-site/pypdf and missing proof parent) remain saved.
- Final same-guard A/B/C tests are guard/child-driver observations, not separate shell proof of every runner exit branch. Saved runner uses `assert` in its optimization/routing check, so safe optimized invocation is not certified; the actual run recorded optimize0/absent overrides. Apply has observed destination/remotes/modes/inodes, not a generic safe-restorer guarantee.
- Disposable proof setup used unrequested `--allow-empty` root commits; this procedural deviation is disclosed. Those were independent synthetic proof DBs, not candidate/reconstruct/Production commits. Do not repeat saved proof setup unchanged.
- Two stale hashes in correction3's pre-edit preservation manifest are superseded by the mandatory root annotation, with actual preserved files independently re-hashed. Correct final `hash-manifest.json`/patch/raw test bindings are unaffected.
- No-write covers selected owned fixture trees/Git observations with explicit fault-injection deltas and cache exclusions; no global filesystem/CAS claim. Partial/shallow available objects and unbundled Python/user-site dependencies remain limitations. Success does not erase older failures.

## 5. DM-021 incorporated / next bounded unit

Human-authorized [DM-021 intake/disposition](../notes/rephase-1-dm021-intake/README.md) captured one Summary at **afdb3df3faa20af3bb5798be429bba8dbd2100b1**, blob62ee6a6b, SHA2567c84b6d8. It reports no truthful revalidation reason for post-VALIDATED_DRAFT editorial corrections and a one-off TS-003 exception closure, status **OPEN_CORE / EDITION_WORKAROUND**. Fixed409 source independently corroborates the `REVIEWED_CORE_CHANGE`-only enum; edition reproduction/exception details remain secondary, primary links unread.

LF-2I does not implement that renewal or consume `EXCEPTION_*` records, relabel editorial changes, rewrite immutable checkpoints or waive exact PDF/review/Human bindings. DM-021 is not CORE_FIXED. Latest capture supplements, not replaces as baseline, the prior20 dispositions; no blanket maintenance batch was authorized.

**Next General unit after Human continuation: DM-021 post-validation reader/editorial-correction contract analysis before code.** Use the exact nine-file LF-2I composite and saved Summary. Trace existing pending-basis/reason/supersession/current-authority APIs for Weekly and generated Longform, distinguish unchanged-reader mechanical renewal from changed-reader editorial correction, identify an existing legitimate decision/review producer and exact retention/normal Candidate→Preview→Freeze→Release continuation. Preserve accepted upstream/history and original Core-change behavior; propose minimal paths, true/false reason/provenance/byte-drift/repeated-correction oracles and lifecycle cost. A new reason string alone is not a repair. Do not import the TS-003 exception or silently add a review role; return any concrete authority/primary-evidence gap before code/intake expansion.

Real rendered/build-transfer acceptance, directive-bearing editions, general Thematic/Retrospective/manual sources and canonical audit remain separate open dispositions. Candidate fixation/commit still requires explicit authorization; ordinary reconstruct Commit/Pull/Push remains Human-owned. No automatic next unit or successful-suite/recovery/Summary rerun at this Commit Point.
