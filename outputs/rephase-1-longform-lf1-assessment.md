# LF-1 — bounded source-only Longform reader-input completion

2026-10-09. Human continuation began at clean reconstruct **1610777e7948a94a725dd4836d23337256a49f53**, local tracking synchronized without fetch. **LF-1 is bounded complete as an uncommitted three-file overlay on fixed409.** Astra source/oracle/evidence review and separate author-independent correction resolution support that component only. Stop at Human Commit Point. Whole candidate **NOT_READY**, step4/B3 **OPEN**, canonical seven-point audit **unstarted**.

## 1. Exact identity and preservation

The Git HEAD is still **409b292756dd1277b9dfae87679934c0d2ce251c**, tree **8ce3699861505f32d1d60bdc185d4d4f635aedb2**, parent **34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4**. It does **not** contain the new LF-1 files. No candidate commit/branch or reconstruct commit/Push was made. Review/test identity is this base PLUS the following exact working-tree overlay:

| New path | SHA256 |
|---|---|
| `scripts/survey_longform_derivation_v2.py` | `233e86557f1627203a4f1e4129c953bf34e1319bd8949b1d58b7d417b0744cf7` |
| `schemas/longform-reader-input-v2.schema.json` | `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643` |
| `tests/test_survey_longform_derivation_v2.py` | `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913` |

- Implementation copy: `/tmp/opencode/jgas-lf1-design-20261009T001653Z` (independent byte-copy, inert origin, no alternates/object inode sharing observed).
- Fresh apply-verification copy: `/tmp/opencode/jgas-lf1-verify-20261009T023000Z` (same base + identical three-file overlay, no new commit).
- Original409 `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` stays clean. Root and independent reviewer separately observed identities/hashes/status; overlay status is exactly three untracked files, no tracked differences.
- Final durable [patch](../notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2/overlay.patch) SHA256 **`253e284b08a209f855d06fd2154a3f34c49315f4014118d98fc54b49c3eae881`**. [Apply record](../notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2/verify-apply.log): fresh409 copy, `git apply --check`/apply exit0, exact file hashes/status. This is content/application proof, not a new committed history identity or runtime rerun on the verification copy.
- Base recovery still needs b40 archive + DM001/01920-object pack + W1seven-object pack + DM004final32-object pack. Add this LF-1 patch only after fresh identity/hash/absent-path checks in an independent copy. Inherited26,309 missing blobs/unbundled runtime limits remain; no full-history backup claim. Old saved runners/restore scripts are not reusable certified tools.

## 2. Implemented boundary

Selected [generated contract](rephase-1-special-support-contract-decision.md) and [internal LF-1 path decision](../notes/rephase-1-longform-lf1/astra-implementation-selection.md) are implemented within these limits:

- Read-only loader requires exact **DRAFT_COMPLETE**, configured `stage:reader-publication-validation`, THEMATIC/LONGFORM_SPECIAL. It uses real State/checkpoint and accepted Evidence/Card/Matrix/Materiality/Discovery/Draft/Synthesis loaders, including the existing narrow historical-State-basis revalidation mechanism. No success validator mocks.
- Pure projector and strict reader schema cover cover/frontmatter, accepted headline/deck, visible kicker/order/date values, revision prose/timeline/synthesis/boundaries/technical notes, four-family comparison, final summary, bibliography/citations and fixed helper/style labels. `toc_title=目次` is a proposed explicit reviewed format value, not a claim about an installed TeX class default.
- Exact reader bytes use deterministic construction + `core.json_bytes`; file identity is their SHA256, not `sha256_object`. Provenance/runner/review-reference stay in separate mechanical context. Legitimate runner/review-reference changes preserve reader bytes while authored binding changes.
- Archive package/block coverage and every assigned DID must agree with accepted Draft Package/Result refs; extra/duplicate archive rows cannot enlarge a package's source authorization. Primary entity/card-only URL/access mapping, explicit no-source-selection heuristic, duplicate notes and citation-key collisions fail closed. Dotted keys agree between module and schema.
- Existing read-only leakage scanner is retained. Evidence run-tree package/tasks/results aliases are rejected before that tree's content loader; top-level path containment and contained reader-schema path loading are exercised. Scope is these concrete paths, not a universal repository/path parser.
- **Directive eligibility:** if the legacy `editorial/post-architecture-directives-v2.json` entry exists (including dangling symlink), LF-1 refuses without accepting it as authority. For eligible initial input, final-summary heading/paragraph-count/end placement remain mandatory format rules. Existing approved-Architecture/Human substantive reading/conflict obligations remain. Absence of a filename does not prove absence of every possible Human instruction.
- No CLI, reader-file writer, main/bib/style output, receipt/Gate/PASS producer, shared lifecycle/admission/config/Weekly change. All code changes are the three new files above.

## 3. Verification and review

General performed initial design/implementation; a different General corrected code/tests/evidence. Astra reviewed actual source, schema, test oracles, raw logs and guard code, raising R1–R6 and R2 corrections. A separate reviewer returned CHANGES_REQUIRED (schema dot mismatch and missing final-hash methods), then [BOUNDED_PASS](../notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2/independent-final-resolution.md) with a mandatory [evidence supplement](../notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2/independent-evidence-supplement.md). Root did not implement or run runtime tests.

**Final full module:31 successful methods, 2225.376s, exit0, no failures/errors/skips**, on the exact overlay above, `/usr/bin/python3` **CPython3.14.4**. [Raw full run](../notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2/run-full-module.log) SHA256 `6f05aa44a957f1ffef6b3af61eebb2ddc8f200d05227e954e8e0ada3558fe9fc`. The unchanged historical5-method provenance regression is separately retained, not added to this final31. No transfer of earlier20/25/9 results or old3.12.14 runtime claims.

- Real synthetic Thematic chain advances through current stage validation/checkpoint producers and typed Architecture approval to State AT DRAFT_COMPLETE. This proves type/identity feasibility, not genuine research/Human approval or sufficient four-family evidence.
- Full run includes directive file/symlink, lifecycle, path escapes/aliases, exact archive/citation authorization, omitted/duplicate notes, URL/access ambiguity plus equal-timestamp control, Unknown organization, two-package ordering, dotted DID, returned-surface isolation, nonreader stability and scoped no-write checks.
- 35 authoring mutation rows reuse an accepted chain. Derived accepted-value changes use an actually loaded context then **pure projection**; style-label tamper is **schema-only**, kicker tests are **helper-level** plus loader ordering. They are not fresh acceptance of changed upstream research or renderer/build probes. HOLD mutation is projector-level, NEEDS_MORE rejection is upstream readiness. Multi-DID/card non-constructibility is limited to this fixture family; an unexecuted code guard is not a tested ambiguity claim.
- Final Python runner compares pinned HEAD/tree/status/base/three hashes before AND after, creates its log exclusively, records runtime/argv/cwd/environment, and propagates child/postguard failure. Wrong-HEAD refusal and failing-child observations are saved; [v2 post-drift capture](../notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2/proof-postdrift-v2/capture.log) directly records child0 → runner3 in a separate disposable copy. That one fast helper test is a guard diagnostic, not a second31-method run.

## 4. Preserved failures and residual limits

Mandatory [evidence qualification](../notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2/evidence-qualification.md) and both independent final records govern any earlier stronger wording.

- Original proposal mixed provenance into reader identity and treated runner metadata as route authority; both corrected. Directive missing-authority argument was narrowed to explicit input refusal/source-only format obligation, leaving publisher integration unresolved.
- First Bash runner only printed values and masked child failure. Second asserted preconditions but only printed postconditions, used nonexclusive log creation and unchecked `cd`. Both “strict guard” claims, including the initial independent review's runner PASS, are retracted. Their logs remain historical, not current guard proof.
- Copy-time command file is abbreviated reconstruction, not an exact raw script. Later `.git/index` difference cause was not proved. Current identity observations do not retroactively certify every copy-time action.
- First post-drift shell pipeline reported tee's exit0. A second invocation overwrote the first proof transcript despite preservation instructions; first raw is lost. Appended3 was from that separate invocation, not one unbroken capture. The new v2 script/raw directly captures numeric3 and does not repair the lost history. This deviation stays disclosed.
- Final runner is **exact-run evidence, not certified rerun tooling**: multilink `find` exit is not checked, proof mode does not enforce a distinct destination, timeout discards partial output. No timeout occurred; observed post-drift proof used independent disposable copies. Do not execute saved proof flags against the real candidate.
- Alias sentinel is valid JSON but not an Evidence card. Evidence is pre-validator alias refusal plus no-read observation, not a malformed-JSON parser trap. No-write inventories cover the fixture tree and Git plumbing with explicit `.git` walk exclusion, not global filesystems or race/CAS safety.
- Finite ASCII HTTP(S)/token restrictions exclude ordinary percent-encoded URLs/fragments/IRIs. Generic Thematic/Retrospective/manual support, publisher/receipt/Gate replay, later-state regeneration, real TeX/PDF/visual acceptance, net lifecycle savings and canonical audit remain open.

## 5. Next unit — LF-2 integration proposal before code

After Human continuation, use an independent copy of **409 + the exact LF-1 overlay**, not bare409. General first returns a bounded concrete proposal for the initial two-pass publisher path, persisted pre-TeX review loader, exact same-input serialization, receipt/Gate/admission threading and later readback. Resolve the legacy directive's existing authority/control relationship before any route can consume it or replace its publisher check; no authority inferred from filename/hash/format constant. Keep unsupported input/lifecycle refusal before legacy deletion. Select actual path budget/fixtures/oracles with Astra before code.

Do not repeat LF-1 suites/recovery/Summary/contract alternatives by default. Do not claim new candidate HEAD or transfer this overlay review automatically to a later commit/base/merge. Any candidate commit requires explicit authorization; ordinary reconstruct Commit/Pull/Push remains Human-owned. LF-2 is **not started** at this Commit Point.
