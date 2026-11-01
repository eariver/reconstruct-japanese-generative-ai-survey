# Rejected test draft D — archive manifest (no coverage claim)

2026-10-31. Root rejected the initial test draft D as coverage evidence
before execution (see `../astra-implementation-review.md` § "Test draft D —
rejected..."). This directory preserves the exact candidate initial test
bytes BEFORE future test owners revise, per root instruction. No
delete/overwrite of the originals; no candidate source edits; no
runtime/tests/fixture/Git execution in this archival invocation.

Archive: `notes/rephase-1-profile-support-implementation/rejected-test-draft-d-20261031T155231Z/`
Archived at UTC: 20261031T155231Z

## Byte identity (archived copy == candidate source at archive time)

| Archived file | Source path | SHA256 | Bytes |
|---|---|---|---|
| test_run_evidence_v2_interactive.py | `.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work/tests/test_run_evidence_v2_interactive.py` | 9d668bae9aca7437dc05a21c17724f50407b8e2c338bbc5fdf123909f50eb0e3 | 7721 |
| test_dm022_prearchitecture_acceptance_v2.py | `.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work/tests/test_dm022_prearchitecture_acceptance_v2.py` | 9e245143b765cfe76532b2e9da65de954278eb45253703732ae5e5ce609bf5aa | 84843 |
| test_profile_support_upstream_repair_v2.py | `.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work/tests/test_profile_support_upstream_repair_v2.py` | c4838e4e55741d0a688fc3db06ee556be2f5e0b2b267b292c48b067b237aab65 | 46647 |
| workstream-d-test-preparation.md | `notes/rephase-1-profile-support-implementation/workstream-d-test-preparation.md` (pre-withdrawal bytes) | ceee05c8eb268e883b24a2f0cd41a80f997aa6677421486acb4807b5cf4b1bc9 | 15864 |

Total: 155075 bytes across 4 files. Copy was byte-preserving (`cp -a`);
source and archived hashes match (see archival transcript). Line counts are
not authority; bytes/hashes above are.

## What this archive IS and IS NOT (explicit correction scope)

- IS: a byte-faithful capture of the rejected author draft (3 test files +
  pre-withdrawal report) for audit continuity. Preserved as rejected author
  evidence; original errors are retained, not erased.
- IS NOT: coverage evidence, API-validity proof, or an execution result.
  The draft was verified by static AST parse only (no imports, no fixtures,
  no suite run). Syntax alone does not certify that any named helper/API
  exists in the runtime source or behaves as the test bodies assume.
- Helper-only vs promised public coverage (per root rejection, accepted):
  pure-helper cases (e.g. leaf mappings, universe/loss/derive units) may
  remain honestly labelled as unit tests, but they CANNOT replace
  operation/authority witnesses. The draft's advertised "25-test" public
  coverage — all10 accepted task/card path, three real Profiles, both-entry
  public parity, valid retained-graph readback, mismatched State DCP claim,
  HIGH context/source/loss gate, LOW R≠E/Profile/canonical-path/report
  binding, second legitimate correction — is WITHDRAWN as unproved for the
  reasons in the root § (substring-only card assertion; relabelled Weekly
  profile; private-builder + source-grep parity; source-text history check;
  foreign-marker instead of State-claim mismatch; wrong-revision_id/any-
  Exception HIGH negative; no R≠E graph and unrelated-files report negative;
  same-revision_id repeat instead of second correction; filename-only
  inventories; unverified helper/API names; Git-config identity path that
  must not be executed unchanged).
- No new tests are added here; no repeat plan is proposed. Root will
  reassign actual tests using real fixture APIs and exact behavioral
  oracles. Test corrections do not authorize weaker runtime validators or
  fake approval.

## Method (this archival invocation only)

- Created this NEW directory; copied the 4 files byte-preserving; computed
  SHA256 + byte counts; wrote this manifest. No candidate source edits, no
  runtime/test/fixture/Git operations, no root-Git read, no network.
- Appended an explicit withdrawal/correction section to the original
  `workstream-d-test-preparation.md` (append-only; original §§1–7 preserved
  as rejected history). Did not rewrite runtime or old reports to erase
  errors.
