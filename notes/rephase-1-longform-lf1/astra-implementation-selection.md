# LF-1 internal design gate — selected source-only implementation

2026-10-09, after Human continuation at1610777. Read original proposal WITH `astra-design-feedback.md`, corrected proposal and `independent-design-gate-review.md`; preserve every earlier version. Independent **LF1_DESIGN_READY** concerns design only. This is Astra's internal implementation/path decision within the authorized LF-1 unit, not a new Human approval or publisher authorization. Human Commit Point follows this component's verified completion or concrete blocker.

## 1. Authority disposition and eligible operation

The selected contract already requires final summary heading `この号の総括`, at least three paragraphs, and end placement before references; source-only projection can encode this **format obligation** without representing an unbound JSON file as Human approval. The legacy publisher's file check, byte-hash manifest entry and lack of accepted producer remain unresolved for LF-2. No migration/drop of that check is selected here.

LF-1 loader eligibility is deliberately narrower: validated THEMATIC/LONGFORM_SPECIAL at **exact DRAFT_COMPLETE**, configured `next_action == stage:reader-publication-validation`, supported four-family format, accepted Architecture/Draft authority. No pending/later-state route now. If the legacy `editorial/post-architecture-directives-v2.json` entry exists (including dangling symlink), **refuse with unsupported directive-authority diagnostic before projection**, without loading it as authority. A clean new synthetic initial chain without that entry may prove the source-only component. This is a refusal of an unresolved input, not silent ignoring of an applicable directive. Existing substantive approved-Architecture/Human reading responsibilities and conflict stops remain; absence of this pathname is not a general proof that no external Human instruction exists.

No D1/D2/D3 policy is adopted. No new Human gate/schema authority/exception flag; no publisher acceptance or generic Thematic viability. The review's recommendation to stop before LF-2 is retained. Its internal-design Commit Point suggestion does not add a Human gate before the implementation already included in LF-1.

## 2. Selected path/API budget

Exactly three new candidate paths initially:

- `scripts/survey_longform_derivation_v2.py`: pure projection, read-only accepted-source loader, reader-object schema validation and canonical byte function.
- `schemas/longform-reader-input-v2.schema.json`: strict reader-only structure with explicit route/format and every emitted category.
- `tests/test_survey_longform_derivation_v2.py`: focused real-authority fixture and meaningful mutation/refusal/no-write/stability proof.

No shared helper/schema/config/Weekly closure edits, public CLI, source writer, receipt/Gate producer or lifecycle/admission modification. Necessary expansion returns to Astra with concrete reason. Reuse the independent409 copy; original source and restore stay untouched. Existing real loaders must bind actual checkpoint refs, current authority and accepted Draft/Architecture approval; canonical path presence is not sufficient.

Retain proposed `load_derivation(root,state_path,authored_path)`, pure `build_longform_reader_input(...)`, `validate_longform_reader_input(root,value_or_path)` and `canonical_reader_bytes(value)` APIs, with unambiguous `surface` plus separate mechanical `accepted_refs`/`authored_refs` context return. Exact private decomposition belongs to General. Reject unsafe repository escapes/aliases before reads, duplicate coverage/envelopes/IDs, malformed/unsupported authoring and schema inputs. No renderer entrypoint import or invocation. The loader returns memory values only and writes no reader file itself.

## 3. Reader identity / finite format

- Reader file contains no provenance/tool hashes/runner/free review-reference/raw audit timestamp. Mechanical context is separate. All emitted display strings, citation identities/order and list order stay in the reader object; raw Draft body text is not replayed.
- Use fixed deterministic object construction order and `core.json_bytes` (UTF-8, ensure_ascii=False, indent=2, trailing newline) for exact reader bytes; digest is SHA256 of those bytes. `sha256_object` is not the file identity. Prove equivalent reordered authoring dictionaries normalize identically if dictionaries are semantically unordered.
- Keep one edition descriptor in `visible_text`. Use actual Longform overrides and actual style display values. Explicitly include all note labels, section/box/table/kicker/reference labels and displayed repository/build/strapline values; no accidental Weekly value substitution.
- Select **`toc_title = 目次`** as the proposed reviewed format string. This is a future explicit setter requirement, not an observation of the installed class default. LF-2 must show actual renderer consumes it; LF-1 proves its representation only.
- Accepted single-DID/card and unique `primary_subject_id` entity; same entity title/URL/organization (`Unknown` only null/empty). Card-only matching sources, `explicit_source_id=None`, differing-timestamp ambiguity rejected. Enforce real Matrix/Materiality/Discovery/Draft eligibility; no sidecar source fallback.
- Token grammar proposed in correction is a narrow supported subset; validate unique accepted package IDs, DID/key collision and precise array/cardinality. URL subset is HTTP(S) with host, ASCII and no whitespace/control/braces/backslash/percent/fragment or other excluded delimiter from the declared policy; disclose ordinary URL/IRI exclusions, do not silently transform an accepted URL. If URL safety needs a different finite policy, return the exact issue, not a universal TeX parser. General must state the implemented reject set exactly in module documentation/tests.
- No operational CURRENT_CLOSURE/receipt in LF-1. In-memory mechanical refs include actual accepted artifacts/cards, State/Profile, authored input and Draft archive as appropriate; current tool/source pins in run evidence include the three new paths plus dependencies actually imported and fixed409 basis. LF-2 must later select full serializer/style/schema/control receipt closure. Do not claim an incomplete LF-1 list is that closure.

## 4. Verification / evidence execution contract

General implements/tests; Astra reviews. First real synthetic chain must reach State AT DRAFT_COMPLETE via current producers, actual stage checks/checkpoints and typed Architecture approval. If this fails for authority rather than fixture setup, stop with exact raw blocker. All synthetic research/review/Human records are type/identity test inputs, never genuine semantic sufficiency. One-DID initial positive is fine; order/ambiguity tests require meaningful multi-source cases where needed.

Targeted tests must mutate real source/authoring inputs or trusted constants and rederive, not merely alter returned JSON. Distinguish valid source changes from deliberately invalid refs and expected refusal. Test omission/duplicate/membership/source-hash/URL/access ambiguity, full constants/category coverage, unsupported lifecycle/Profile/directive presence, path aliases/escapes, stability with changed mechanical authored binding, exact no-write inventories before cleanup. Include multiple-entity unique-primary positive and `Unknown` fallback; no accepted-data success mocks. Output byte equality alone is not substantive review.

Save unique raw run commands/stdout/stderr/exits and strict **asserting** guards with no masked status/pipeline exit. Verify no inherited Git-root overrides, actual parent identity and exact candidate source snapshot before/after each focused run. Do not rerun saved observation script as a guard. Copy-time logs remain abbreviated, later `.git/index` difference cause unproved. Record all failed/setup runs without overwriting; no finally repair before no-write comparisons. Run only justified focused/affected tests, not all old suites.

No normal reconstruct commit/Push. **Do not create a candidate commit or new candidate branch in this call.** Return a precisely hashed three-path working-tree overlay on409, patch/new-file bytes and source snapshot, guard predicate allowing ONLY those intended new files, with test evidence bound to that composite identity. Existing synthetic test fixtures may use their own independent Git databases as required by the authorized Git-aware tests; never reconstruct/source DBs. This is not exact-committed-head implementation acceptance or a new shipping successor. Propose durable content packaging/independent apply verification without claiming an unchanged HEAD includes new code. Any later commit needs explicit authorization.

Return implementation/source/test evidence and STOP for Astra review; a fresh author-independent implementation/evidence reviewer follows. No automatic LF-2 work. Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted.
