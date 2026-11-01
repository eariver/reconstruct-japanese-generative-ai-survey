# Astra implementation review — working, not acceptance

2026-10-31. Human continued after scope reassessment; whole existing-map P1–P4 implementation is active. Root reviews code/evidence, General implements and runs tests. No ordinary Commit/Push or Human Commit readback.

## Initial source review — changes required

Read A/B/C implementation returns and actual workcopy source. Static parsing is not behavioral or authority proof. These findings remain within the selected technical map; no new pre-code cycle or broader reader feature is selected.

1. **A: present marker does not establish a claimed DCP binding.** `resolve_prepackage_root_effective` checks State's discovery claim only in the marker-absent branch. With a present valid marker, it returns without comparing the State's named DCP and its selected acceptance/path/hash. `STAGE_CLAIMED` is not merely a name for invalid input: a healthy claimed chain must remain supported and independently bound. Bind actual claimed checkpoint authority before returning; preserve initial marker-only pending case. No mere marker-presence or lifecycle permission.
2. **B: do not retain an effective-as-root default.** The ordinary runner uses `effective.get("root_records", discovery_records)` on its new eligibility path. The resolver contract carries root records; require that actual field and reject an invalid resolver result, rather than silently reintroducing E-as-R. No new behavior on legitimate DIRECT.
3. **C: historical context must bind Profile and canonical logical path to COPY.** `_context_from_before_state` currently loads request Profile and compares issue/research but does not compare its exact path/hash to `before_state.profile`. Loaders treat caller request `before_state.path` as canonical rather than deriving the Profile/config canonical State path. Restore the full map's identity constraints without reading LIVE State or imposing current Contract8.
4. **C: adopted-full must pass E as the graph discovery argument, R as separate root context.** It currently sets `disc_abs` to `root_path` and feeds it to ledger/completeness as their effective discovery input. This can reject legitimate DERIVED or validate the wrong graph. Audit every forwarded call for positional E versus trailing R/path distinction, not just absence of `None,None`.
5. **C: record-owned COPY derivation needs full retention/layout cross-binding.** Rehashing a retention-plan SizedRef alone does not establish its relation to the manifest/request/revision root; check the actual typed payload and required bindings before deriving the fixed COPY. Compare existing full predicates rather than inventing a second weaker parser. Keep D/S-only context acyclic and adopted-full three-argument interface.
6. Remove implementation-process-specific runtime `BLOCKER(workstream-A)`/optional helper detection after the mapped helper has landed; call the actual required API. It is fail-closed but not a shipping compatibility mode. Correct stale DIRECT-only/pure-I/O descriptions and verify real configuration/schema shapes with meaningful tests.

Tests must include healthy claimed-DCP marker and mismatched claimed-versus-valid-marker, exact COPY Profile/path mismatches, true DERIVED with R≠E through public HIGH and adopted readback, and retention-binding substitutions. A/B/C initial “complete/no gap” claims are author returns, not acceptance. Existing simplified fixtures must not be preserved by weakening runtime predicates.

## Preparation qualifications

The first preparation checked 768 source bytes but sampled Git inode separation; subsequent full-entry supplement is the current separation observation, not retroactive copy-time enforcement. PATH-only TeX absence was corrected by explicit TinyTeX executable probes. Original logs/reports remain preserved. Worker reports say their harness lacked an apply_patch binary and used exact-string file edit tools; retain that tool deviation, do not recast it as apply_patch execution.

## Status

Implementation incomplete pending corrections, fixed-source meaningful tests, fresh CURRENT proof, exact delivery and independent implementation review. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN retained. No Commit Point yet for this implementation unit.

## Test draft D — rejected as coverage evidence before execution

Root read all795 lines of the new test module. Its advertised25-test coverage is not substantiated by its bodies:

- all10 card “positive” only asserts absence of one error substring, allowing other validation failures; actual accepted task/card path is unproved.
- “three Profiles” relabels a Weekly Profile to Retrospective and substitutes hand-built profile data instead of real profile-specific upstream operation.
- “public parity” calls a private builder plus `_fake_original`, then greps the adapter's source. It never runs both public entries.
- “history readback” checks a function's source text for absence of an error string; no valid retained graph is read.
- “mismatched State claim” exercises a foreign expected marker path instead of a mismatched State DCP claim.
- HIGH negative uses a different revision_id and catches any Exception, so an early unrelated failure can pass without reaching the context/source/loss gate.
- LOW “DERIVED/Profile mismatch” builds no R≠E graph and tests neither Profile mismatch nor canonical-path binding. Report negative supplies missing unrelated files, so it cannot prove the named report predicate.
- “repeat correction” is an attempted reuse of the same revision_id, not a second legitimate correction, and no DERIVED case is built.
- file-name inventories omit bytes/modes/directories and cannot establish the claimed no-write condition. Several helper/API names need actual-source verification; syntax alone cannot certify they exist.
- new fixture code persists Git identity through `git config`; instruction requires process-scoped identity. Do not execute this path unchanged.

Preserve this initial draft and report as rejected author evidence. Replace/reassign meaningful tests using actual fixture APIs and exact behavioral oracles; do not run an expensive suite merely to obtain expected setup failures, nor count these names as demonstrated coverage. Pure-helper cases may remain honestly labelled as unit tests, but cannot replace operation/authority witnesses. Test corrections do not authorize weaker runtime validators or fake approval.

## Initial execution / independent early review disposition

Ordinary verification returned21/24 and separate14/14, with three claimed-DCP setup blockers. DM022 batches mostly failed at the common fixture setup gate; no HIGH/LOW operation proof resulted. Preserve the raw outcomes. Once a common positive setup fails, stop that dependent batch and repair its fixture before further broad runs. A started timed-out batch is **INCOMPLETE/TIMEOUT**, not “not-run”; a deliberately missing required-keyword TypeError oracle is not an unmigrated caller defect. Exact raw counts must replace approximate summaries.

Root read `survey_agent_tool_v2.py:42–50,121–143` and `survey_production_v2.py:959–995`. Existing agent-first stage execution uses `current_stage_basis_override`, which installs the strict agent validator; the bare production verifier expects legacy machine attestations. These are distinct contracts. Test Stage-Checkpoint states using the actual appropriate facade and strict validator; do not replace a Stage record with an attestation or bypass validation. A legacy fake-SHA fixture does not authorize threading a fake implementation into the new PATH-only resolver: migrate to real committed synthetic source at fixture construction, before acceptance. If an actual shipping caller cannot establish the required authority, return its concrete route, not a test-only workaround.

Independent early review is CHANGES_REQUIRED at its pinned snapshot. Root dispositions:

- **B0 and B3 accepted:** prepackage DCP call has an extra positional Profile argument; healthy claimed authority is therefore broken. Exactly-one matching artifact role must not become exactly-one total artifact; rehash all allowed extra rows and keep report equality.
- **B1 claimed bypass not established:** `evidence.validate_screening_acceptance:556–564` already resolves the actual effective path, enforces caller path/SHA equality and returns `effective["records"]`. Thus `discoveries` is not raw unvalidated caller input. Using one resolved pair is reasonable consistency, but do not claim a proved bypass from this call alone. Check changed-byte windows without inventing atomicity.
- **B2 is not authority to impose ordinary3/5 semantics on DM0227.** Precode ROOT/R4/R5 explicitly preserve the seven-field request; its schema makes empty dimension/description fallback unreachable. Ordinary automatic trace derivation and residual-union policy do not, by themselves, select a new historical DM022 rule. Profile-only explicit references may have distinct supported semantics. Reviewer must distinguish reachable defect from old dead code and prove any proposed change against the actual selected DM022 contract/full validators before implementation. No blind tightening or LOW new-policy gate.
- Early review's first contract hash is mistranscribed (`…54de…` vs correct `…54bde…`); preserve and correct by annotation, not alternative identity.

Proceed with the established technical map, targeted fixture repair and meaningful positive controls. Actual current-stage wrappers are reused, not new permission tokens. No new pre-code cycle or generic reader unit is selected.

## DERIVED fixture identity disposition

The reported `local:` parent-vocabulary conflict does not yet demonstrate a shipping contract gap. Root re-read unchanged `screening.validate_discovery_expansion:246–322` and Discovery normalization. **Accepted root Discovery and Screening-derived effective JSONL are distinct artifacts with distinct edge vocabularies.** Root acceptance uses Discovery's normalized graph contract; a Screening-derived child references exact accepted root DIDs in its `parent_refs` and is checked by `validate_discovery_expansion`. Do not submit that effective child set as a new root Discovery acceptance to make the fixture pass.

Build an accepted root R (e.g. valid BASE records with named obligations), then a distinct effective E with raw root-DID parent refs, preserving source identity/Raw union/all-parent coverage. Bind DCP to the root acceptance and SCP to the E-based Screening acceptance. Request Discovery binds E. No shipping normalization, relabel, source rewrite or DIRECT-only narrowing is selected. If this actual sequence fails, return its exact rejecting predicate; pure-loss helper examples are not a DERIVED operation witness.

## Final evidence/oracle corrections before closeout

The new verifier captured eight real verbose batches on fixed source770. They replace neither initial setup failures nor summary-only logs; loader-probe failures are separate. Runtime bytes remain stable. Independent final review requires narrower C negatives and immediate SHA-bearing inventories; root accepts that requirement, with failure windows kept honest (a late content failure may preserve owned partial revision output rather than guarantee zero writes).

Root additionally read new C test lines382–412: it writes retained artifacts to a **hardcoded reconstruct absolute path** and overwrites the same `rev-c-derived-1` filenames on every run. This is not suitable shipping test behavior or run-specific retention evidence. Remove the hardcoded destination. Only an explicit test-harness retention directory may enable extra preservation, using a fresh exclusive per-run/test directory; ordinary execution stays within its temporary fixture. Preserve the currently available retained bytes and qualify prior overwrites; do not retroactively bind them to an earlier invocation.

N8 currently adds a `sha256` key rather than demonstrably mutating an existing schema-valid retention field; N9 mutates request pins without keeping manifest request binding, so a generic SizedRef refusal is not proof of CURRENT tool drift. Correct these or narrow their claim, with healthy controls and exact errors. N7 ghost-record refusal may legitimately occur after an owned COPY under existing prepare failure semantics: assert the actual permitted owned-write window and canonical/State preservation, not an unselected all-content-prewrite guarantee. Do not modify shipping runtime merely to make an overbroad test claim true.

Only the new C test module needs the selected oracle/retention correction unless execution reveals a real source defect. After that, run its affected methods on the final applied source and regenerate the complete patch/manifest in a NEW packet; keep the first packaging and raw runs. Unchanged runtime/other-test evidence may be carried as an explicitly source-bound composite, not a fictional full-suite rerun.
