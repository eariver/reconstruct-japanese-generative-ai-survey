# Interface mismatches — RESOLVED by owners (this file preserved as history)

2026-10-24 turn 1: HIGH returned the proof.basis_ref SELF-vs-FILE contradiction
and H build-container gaps instead of bypassing. 2026-10-25: ROOT rejected the
SELF exception (contract §11.2: ALL cross-doc refs are FILE BYTE SHAs, H
compare KEEP); S fixed to FILE linkage (d5472266: `_load_basis` returns
`basis,self_sha,file_sha,rel`, verify compares FILE, returns distinguish both
SHAs); H corrected build schema/code per actual R4 (EXECUTED pdf 3-field
sizedRef, explicit companion fields, required companion per recipe).
HIGH writer converted to FILE-everywhere (proof.basis_ref at both assembles +
inner comparison; record/seal/receipt/manuscript/Candidate/bundle/Gate refs);
unbound sidecar REMOVED (companions directly in versions); live C probing
hardened (required companion + exe exit + post-build reverify). Original
sections below preserved unmodified; their recommendations are SUPERSEDED by
the owner fixes above (no dual field, no either-tolerance, no H weakening).

2026-10-25 turn 2 RESOLUTION CONFIRMED BY EXECUTION: U1/U2 activate green both
routes; H verifies 21 (U1) and 31 (U2) bindings live. The H-1594 compare passes
UNMODIFIED under FILE-everywhere (both sides FILE SHAs); S-1155 compare passes
under FILE linkage. No owner code change was needed beyond the already-landed
S-FILE + H-schema fixes. SELF-era sealed sets (run≤14 fixtures) remain
preserved/qualified as non-positive history, never retrofitted.

--- original report (superseded recommendations, preserved evidence) ---

2026-10-24. HIGH+consumer worker returns this to root/S/H instead of bypassing
or weakening any check. No HIGH/S/H semantics changed to work around it. Whole
U finalize passes on both routes; activate refuses deterministically on this
single contradiction. Evidence: `run14-20261024T210000Z/activate-u-weekly-stderr.txt`
tail (`SEAL_BIND: low activation-record validation failed: versioned activation
history invalid: HISTORY_DIGEST_MISMATCH: versioned ancestor proof/basis ref
mismatch (exact path+SHA)`).

## The contradiction (all three sites read, not inferred)

Workdir `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/`,
HEAD 409b292 + uncommitted (no commits by this phase):

1. H `scripts/survey_versioned_renewal_history_v2.py:1594`
   (`_verify_versioned_ancestor`): `pbr = proof.get("basis_ref")` must equal
   `basis_ref = record.get("renewal_basis_ref")` in EXACT path+SHA.
2. H same function `:1580`: record's `renewal_basis_ref` (and set/proof refs)
   go through `_require_authority_live` = `_check_authority_ref` (`:409-421`),
   which compares LIVE FILE bytes SHA to the ref sha. Hence record-side refs
   MUST carry FILE SHAs.
3. S `scripts/survey_versioned_renewal_source_v2.py:1153-1155`
   (`verify_renewal_source_proof`): `proof.basis_ref.sha256` must equal
   `basis.get("basis_sha256")`, which `_load_basis_strict` defines as the
   object SELF-digest (compact sorted, `core.sha256_object` over all-except-self).
   Hence proof-side basis ref MUST carry the SELF digest.

FILE SHA ≠ SELF digest by construction (indented file bytes vs compact sorted
object). No single value satisfies both (1)+(2) and (3): with record=FILE,
H-1580 passes but H-1594 fails against S-conformant proofs; with record=SELF,
H-1580 fails. HIGH currently writes record/seal/receipt basis+proof refs as
FILE SHAs (satisfying H-1580, H seal==record bindings, H OWN live checks, S
file-based checks) and proof.basis_ref as SELF (satisfying S-1155) — the only
remaining failure is H-1594.

## Recommended resolution (H-owned, one spot, no contract broadening)

At H `:1594`, compare `proof.basis_ref` against the LOADED basis identity
`{path: <record basis path>, sha256: <recomputed basis SELF digest>}` (basis
is already loaded at `:1584` and self-verified at `:1612`) instead of the
record FILE ref. Preserves H-1580 (record refs stay FILE), S-1153 (proof refs
stay SELF), and every other cross-binding. Alternatives (S-side change at
`:1155`, or a dual-field proof schema addition) both require broader review;
the H-side comparison is the minimal closure of the existing two conventions.

Related convention already applied in HIGH (for owner verification, not as a
bypass): ALL other cross-document refs are FILE SHAs; `proof.basis_ref` alone
is SELF (S-required). H OWN candidate/bundle/gate/manuscript checks, H chain
terminal resolution, S file checks, and seal==record bindings are all
consistent with this split — verified by reading, with U finalize green on
both routes as behavior proof up to activate.

## Impact if unresolved

Blocks every activation (U and C, both routes), hence repeat C→U→U (needs U2
activation), renewal→editorial (needs an activated renewal prior for the
mixed-chain test), normal direct lifecycle on renewed sets, ALREADY_ACTIVE and
resume oracles. C1 finalize (no activation needed) can still proceed and will
be reported separately.

## Third exact mismatch (H-internal: EXECUTED outputs page_count + companions)

- H code `:1493-1499` requires EXECUTED `outputs.publication-pdf` EXACTLY
  `{path,sha256,byte_count,page_count}`; H-owned schema `#/$defs/buildRecord`
  pins it to `sizedRef` = `{path,sha256,byte_count}` (R4 §4 agrees: sizedRefs).
  HIGH writes schema-conformant outputs (container validation passes), H code
  then refuses. Recommend H aligns `:1494` to sizedRef.
- H-owned schema `#/$defs/toolchainVersions` (`additionalProperties: false`,
  base 6 + `error` only) forbids the R4 §4-required per-companion keys
  (`<comp>_stdout/_returncode/_link_path/_real_path/_real_sha256/_error`).
  HIGH conforms to the enforced schema and preserves the measured companion
  evidence in `R/build/toolchain-companions.json` (declared C evidence inside
  R, unbound pending schema fix). Recommend H adds explicit companion
  properties per R4 §4 (or amends the map); no silent drop on either side.
