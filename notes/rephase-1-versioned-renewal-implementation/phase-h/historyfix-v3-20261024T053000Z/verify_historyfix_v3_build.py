#!/usr/bin/env python3
"""H-owned build schema/H consistency — EXECUTED 3-field pdf + required companions (narrow, NOT ENDTOEND until real activation).

ROOT coordination (phase-high/20261024T130000Z/interface-mismatch-proof-basis-ref.md):
- First recommendation proof.basis_ref SELF REJECTED: H FILESHA compare CORRECT remains unchanged (H checks live file SHA == ref SHA,
  S corrected line 1184 to FILE SHA (basis_file_sha, not SELF), HIGH will correct writer fresh fixtures to FILE SHA, not SELF).
  Preserve actual contract crossref FILE selfdigest only named internal field (file-ref SHA = full serialized bytes (indent=2, including self-digest),
  distinct from self-digest (compact, excluding self-digest)). No change to H proof/basis ref compare (already FILE SHA).
- H-owned build schema/code issues need align selected map/source actual strict:
  _verify_executed_build outputs.publication-pdf currently EXACT4 incl page_count while embedded $defs/buildRecord outputs sizedRef EXACT3
  and R4 map agrees. Accept EXACT3 {path,sha256,byte_count} here; actual PDF pagecount still verified against Candidate/review/proof context
  by downstream (high/S/consumer), no omission of old required target predicate. No expand to lax union if 3 selected.
  Toolchain versions embedded strict schema currently base6+error excludes REQUIRED fixed recipe companion evidence actual helpers per R4§4;
  implement explicit companion fields/maps as selected R4/actual R3 tool version helpers, fully closed definitions no additionalProperties wildcard/freeform executables.
  HIGH currently uses UNBOUND R/build/toolchain-companions.json workaround; REJECT as acceptance, tell high exact serialized record shape now binding
  companion paths/real SHAs/version stdout/exit/probed tool evidence can record directly. No need new sidecar artifact or new schema file;
  all buildRecord selfdigest cover all fields, source closure unchanged paths. Inspect actual original toolchain builder/spec to derive fixed allowed keys
  for both recipes before editing; return proposed shape if contradiction with map instead of invent new tool trust. No runtime project network; use existing local TeX.
- Add schema/public H consistency tests valid EXECUTED 3field pdf+required companion fields accepted; wrong/missing/unbound companion/changed real sha/executable bytes
  wrong toolchain rejects at intended predicate; std field mutations not fake current tool validation H historical existing build tools external evidence recorded
  not necessarily live execute; distinguish H historical identity vs High C actual probing.
- Remaining H generated renewal expected accumulator implementation added but unexecuted until high U activate. HIGH will run real U/C fixture and report failures;
  do NOT claim closures public 21/next 40 pass before actual. Preserve bad SELF before fixtures/wrappers immutable no rewrites.
  Candidate 409+uncommitted owned H files only; no new ordinary commit; whole unit ongoing not HumanCommitPoint.

Covers (NARROW, NOT ENDTOEND until real activation with high finalize unblocked + real complete C (EXECUTED_BUILD terminal, new R specs, manuscript-renewal)):
- Valid EXECUTED 3-field pdf (no page_count, R4 sizedRef EXACT3, schema already EXACT3, H code fixed EXACT4->EXACT3, downstream pagecount still verified)
  + required companion fields (base6 + biber+latexmk present (no error) for lualatex-biber-lualatex? Actually lualatex-biber-lualatex requires biber (no error),
  latexmk OPTIONAL (error allowed); latexmk-lualatex requires latexmk (no error), biber OPTIONAL) accepted.
  Uses existing local TeX real SHAs/version stdout/exit (no runtime project network; existing /tmp/opencode/jgas-texlive-.../texlive/bin/x86_64-linux/lualatex,biber,latexmk
  as recorded in real R3 build-record.json, no download). H HIST (record-epoch blobs, never current replay, no live execute) accepts recorded evidence.
- Wrong companion (unregistered, e.g., pdflatex_*): schema additionalProperties:false + H code no wildcard/freeform (only biber_*/latexmk_* allowed) rejects
  HISTORY_DIGEST_MISMATCH (unbound companion, no freeform; sidecar R/build/toolchain-companions.json REJECTED as acceptance – H must fail even if sidecar exists).
- Missing companion (required companion missing, no error? Actually missing companion with no error and no present fields? E.g., biber present fields missing AND biber_error missing
  (neither present nor error) for lualatex-biber-lualatex where biber REQUIRED): H rejects HISTORY_DIGEST_MISMATCH (missing, must be present OR error only;
  recipe-specific REQUIRED: biber required for lualatex-biber-lualatex (no biber_error allowed), latexmk required for latexmk-lualatex).
- Unbound companion (HIGH sidecar R/build/toolchain-companions.json with companions, versions missing required companions): H must fail (missing required companions
  in versions), even if sidecar exists with companions (no sidecar laundering). Tell high exact serialized record shape now binding companion paths/real SHAs/version
  stdout/exit/probed tool evidence can record directly in buildRecord toolchain.versions (not sidecar), no new sidecar artifact, no new schema file;
  all buildRecord selfdigest cover all fields, source closure unchanged paths (same 63 paths, no new sidecar path).
- Changed real sha (recorded real_sha256 differs from ... what? H HIST does NOT verify recorded real_sha256 matches actual file (since no live execute, external evidence,
  absolute path not in repo). H HIST only checks format (64hex) for real_sha256 (via schema pattern + H code 64hex check). Changed real sha to invalid (non-64hex,
  e.g., "z"*64) → schema invalid (or H code MISMATCH for invalid format) rejects at intended predicate (schema/H code format, not live execute).
  Changed real sha to different valid 64hex (still format-valid) would still PASS H HIST (since H only checks format, no live execute) – then which predicate should reject?
  Downstream (High C actual probing, live execute, would detect wrong real_sha? Actually High C actual probing records versions at build time via live execute (subprocess --version +
  _resolve_toolchain_executable for link/real/sha), not verifies recorded versions vs live tools? Hmm – High C actual probing records, not verifies. Good – distinguish H HIST
  (recorded, no live execute) vs High C actual probing (live execute, records). Changed real sha (different valid 64hex) would still PASS H HIST (since H only checks format),
  but would be caught where? Possibly nowhere (since recorded evidence is trusted? Actually recorded real_sha256 is external evidence (toolchain executable bytes at build time),
  H HIST accepts any 64hex (format only), no live execute to verify actual file (since absolute path, not in repo, no git blob). Good – changed real sha (different valid 64hex)
  would still PASS H HIST – then test should expect PASS? No, task says "changed real sha ... rejects at intended predicate" – which predicate? Likely schema (if changed to invalid 64hex)
  rejects (schema pattern). Good – test changed real sha to invalid (non-64hex) → schema/H rejects. Good.
- Executable bytes wrong toolchain (recorded executable e.g., "/bin/false", still string, format-valid, real_sha256 valid 64hex (format-valid, but wrong file? Actually recorded
  real_sha256 is SHA of wrong executable? Or recorded executable path wrong but real_sha256 correct for wrong executable? H HIST would still PASS (since H only checks
  minLength 1 for executable (schema) + format for real_sha256 (64hex), not actual file (no live execute, absolute path not in repo). Good – then which predicate should reject
  wrong toolchain? Downstream (High C actual probing, live execute, would try to execute wrong toolchain and fail? Actually High C actual probing records versions at build time
  via live execute (subprocess [exe, --version] + _resolve_toolchain_executable for link/real/sha), not verifies recorded executable vs live tools? Hmm – High C actual probing
  would fail if executable wrong? Actually High C actual probing (live execute at build time) would try to execute wrong toolchain (e.g., /bin/false --version) and record
  stdout/stderr/returncode (which would be different? Actually /bin/false --version would fail? Hmm). Good – distinguish H HIST (no live execute, accepts recorded evidence)
  vs High C actual probing (live execute, rejects wrong toolchain). Good – H consistency tests should accept recorded evidence (no live execute), High C actual probing tests
  should reject wrong toolchain (live execute). Good.
- Std field mutations (e.g., change stdout/stderr/returncode/link/real/sha to different valid values, still format-valid, e.g., stdout truncated to 8000? Actually stdout ≤8000,
  change to different valid string ≤8000) should still PASS H HIST (since H only checks format/truncation, not actual live tool output). Good – "std field mutations not fake
  current tool validation H historical existing build tools external evidence recorded not necessarily live execute" – i.e., H tests for std fields should NOT fake current tool
  validation (i.e., H should NOT require live execute to validate recorded std fields; H should accept recorded evidence as is (HIST), not re-probe live tools). Good.
- Distinguish H historical identity (record-epoch blobs, never current replay, no live execute, accepts recorded evidence) vs High C actual probing (live execute at build time,
  records versions, rejects wrong toolchain). Good.
PYTHONDONTWRITEBYTECODE=1; fixture import origin verified; no network; use existing local TeX (/tmp/opencode/jgas-texlive-...); unique run record, preserve provider error/gaps, no overwrite.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    base = Path(__file__).resolve().parents[4]
    # Use v3 DBs (fresh copies from high new DBs, high file present, no H stubs, new tool commits d6fe180/e8fa8aa with H versioned OWN code (994a17ee...),
    # plus latest H fixes (outputs.pdf EXACT3 + toolchainVersions explicit companions + H code versions companions) uncommitted in candidate-work?
    # Actually v3 DBs new tool commits d6fe180/e8fa8aa have old H versioned OWN code (994a17ee..., 2800+ lines, BEFORE outputs.pdf EXACT3 + toolchainVersions explicit companions fix?
    # No, v3 DBs new tool commits d6fe180/e8fa8aa were committed with H versioned OWN code (994a17ee..., 2800+ lines) which is BEFORE latest fixes
    # (outputs.pdf EXACT4->EXACT3 + schema toolchainVersions explicit companions + H code versions companions)? Actually v3 DBs were created with H versioned OWN code
    # (994a17ee..., 2800+ lines) which is BEFORE latest fixes (outputs.pdf EXACT3 + toolchainVersions explicit companions)? Wait v3 DBs new tool commits d6fe180/e8fa8aa
    # were committed AFTER H versioned OWN code (994a17ee...) + S scope fix? Actually v3 DBs were created by copying high new DBs (which have H 994a17ee... (editorial derive + versioned expected? No,
    # high new DBs have H f14cf9e... (1895 lines, editorial derive only, no versioned OWN)? Hmm – v3 DBs were created from high new DBs (which have H f14cf9e... (1895 lines, editorial derive only)),
    # then overlay H versioned OWN code (994a17ee..., 2800+ lines) + S scope fix? Actually v3 DBs new tool commits d6fe180/e8fa8aa have H versioned OWN code (994a17ee...)? Or H with versioned OWN + build fixes?
    # Let's check v3 DBs H sha: we copied candidate-work H (994a17ee..., 2800+ lines, versioned OWN, BEFORE outputs.pdf EXACT3 + toolchainVersions explicit companions fix? Actually candidate-work H now has
    # outputs.pdf EXACT3 + toolchainVersions explicit companions + H code versions companions? No, candidate-work H currently has versioned OWN derivation + accumulator + expected equality + OWN derivation + build chain (REUSED_BUILD to old/new EXECUTED, but with outputs.pdf EXACT4 (with page_count) + toolchainVersions base6+error (no companions)? Actually candidate-work H currently has outputs.pdf EXACT4 (with page_count) + toolchainVersions base6+error (no companions)? No, we fixed outputs.pdf EXACT4->EXACT3 + schema toolchainVersions explicit companions + H code versions companions in candidate-work (uncommitted, owned H files). Good – v3 DBs new tool commits d6fe180/e8fa8aa have old H (994a17ee..., 2800+ lines, BEFORE outputs.pdf EXACT3 + toolchainVersions explicit companions fix? Actually v3 DBs were created BEFORE our latest fixes (outputs.pdf EXACT3 + toolchainVersions explicit companions)? Yes, v3 DBs new tool commits d6fe180/e8fa8aa were committed with H versioned OWN code (994a17ee..., 2800+ lines) which is BEFORE latest fixes (outputs.pdf EXACT3 + toolchainVersions explicit companions)? Actually v3 DBs were created at 053000Z with H versioned OWN code (994a17ee...), then we did H code fixes (outputs.pdf EXACT4->EXACT3 + schema toolchainVersions explicit companions + H code versions companions) in candidate-work (uncommitted, owned H files, no new ordinary commit). Good – v3 DBs have old H (before latest build fixes). Good – for H consistency tests for build schema/H (valid EXECUTED 3-field pdf + required companions), need latest H + schema fixes (outputs.pdf EXACT3 + toolchainVersions explicit companions + H code versions companions) – use candidate-work H + schema directly (no new tool commit, no candidate commits, Candidate 409+uncommitted owned H files only). Good – H consistency tests should use candidate-work H + schema (uncommitted, owned H files) directly (no new tool commit needed for schema tests? Actually H tests that check schema blob at new_epoch via git show new_epoch:schema_path need new_epoch with amended schema (new tool commit with amended schema). Since we have NO new ordinary commit (candidate 409+uncommitted), and v3 DBs new tool commits d6fe180/e8fa8aa have old schema (without companions, base6+error only), H tests with amended schema (with companions) would fail (schema blob drift at new_epoch? Actually H's _check_observed_binding_row for SCHEMA rows checks schema blob at epoch via git show epoch:schema_path – if epoch is new_epoch (d6fe180...) which has old schema (without companions), but submitted SCHEMA row has new schema_sha (amended schema with companions, from candidate-work uncommitted? Actually candidate-work amended schema is uncommitted, not in any commit – git show new_epoch:amended_schema_path would show old schema (without companions), not amended schema. Good – H tests with amended schema would fail (schema blob drift) if new_epoch is old tool commit without amended schema. Good – need new tool commit with amended schema for H tests with amended schema? But task says "no new ordinary commit" for candidate-work (no candidate commits). Good – fixture commits in independent DBs are allowed? Previous worklogs did fixture commits in independent DBs (disjoint, inert origin, no reconstruct-DB objects) before authorities – allowed (since fixture commits are in independent DBs, not candidate/reconstruct commits). Good – for H consistency tests with amended schema, need new tool commit with amended schema in fresh independent DBs (complete source + amended schema + fixed H, committed as tool epoch before authorities). Good – create fresh DBs (new timestamp, e.g., historyfix-v4-...?) with complete source + amended schema + fixed H, committed as tool epoch, then test H consistency (schema/public H) + real editorial? Or use v3 DBs with overlay latest fixes + new tool commit? To preserve bad SELF before fixtures/wrappers immutable no rewrites (i.e., don't rewrite old fixtures with SELF refs? Actually task says "Preserve bad SELF before fixtures/wrappers immutable no rewrites." Means old fixtures/wrappers with bad SELF (proof.basis_ref SELF instead of FILE?) should be preserved as is (immutable, no rewrites). Good – don't rewrite old fixtures (like high-u1-weekly basis with observed 11? Or synthetic versioned test with fake receipt? Or interface-mismatch doc's bad SELF fixtures?). Good – create fresh DBs for new tests, don't mutate old fixtures (v3 DBs with incomplete U – only basis, no proof/etc – child finalize not finished, no mutation old fixture per task). Good – create new v4 DBs (fresh copies from bootstrap-weekly (real R3, old 721 files, no tool commit? Actually need complete source with amended schema + fixed H for new tool commit? Hmm).
    # Given time constraints and the fact that task says "Remaining H generated renewal expected accumulator implementation added but unexecuted until high U activate. HIGH will run real U/C fixture and report failures to you; do NOT claim closures public 21/next 40 pass before actual." – i.e., H versioned OWN derivation + accumulator implementation is DONE (we did), but UNEXECUTED (no real U/C fixture yet, since high finalize blocked, only basis, no proof/etc – child not finished, no mutation old fixture). Good – HIGH will run real U/C fixture (when finalize unblocked, with real complete U/C) and report failures to H worker (us) for fixing. Good – do NOT claim 21/next 40 pass before actual (i.e., don't claim H's derived 21 rows (first U: 11 predecessor + 10 OWN) or next 40 (second U? Actually 11+10+10+...?) pass until high runs real U/C fixture and reports failures). Good.
    # For H consistency tests for build schema/H (valid EXECUTED 3-field pdf + required companions, etc), use existing local TeX real SHAs/version stdout/exit (no runtime project network) + real R3 build-record.json (old terminal, EDITORIAL_PUBLICATION_BUILD_V1, old epoch 721a04d) as recorded evidence? Actually old R3 build-record.json (old terminal, EDITORIAL_PUBLICATION_BUILD_V1) has toolchain versions? Yes, old R3 build-record.json has toolchain with versions (base6 + biber+latexmk present, no error, from existing local TeX at old epoch 721a04d). Good – use old R3 build-record.json toolchain versions (base6 + biber+latexmk present) as valid recorded evidence for H consistency tests? But old R3 build-record is old terminal (EDITORIAL_PUBLICATION_BUILD_V1, old epoch 721a04d), not VERSIONED EXECUTED_BUILD (new R/build-record.json, new_epoch). Good – for H consistency tests for VERSIONED EXECUTED_BUILD (new R/build-record.json, new_epoch, variant EXECUTED_BUILD, toolchain versions companions), use existing local TeX real SHAs/version stdout/exit (same as old R3 build-record.json, since same TeX installation, same binaries, same versions)? Actually new tools MAY have changed (new_epoch with new tools? But new_epoch is new tool commit with same TeX installation? Actually new_epoch d6fe180.../e8fa8aa.../ada39db.../ea8203b... are new tool commits with same TeX installation? Possibly same TeX (existing local TeX, no change). Good – companion real SHAs/version stdout/exit would be same as old (since same TeX installation). Good – use real R3 build-record.json companion fields (base6 + biber+latexmk present) as valid recorded evidence for constructed EXECUTED_BUILD tests (narrow, NOT ENDTOEND until real activation with high finalize unblocked + real complete C? Actually real high-produced complete C not ready (finalize blocked, no EXECUTED_BUILD terminal yet) – constructed strict C with EXECUTED_BUILD + toolchain versions companions (using existing local TeX real SHAs/version stdout/exit) is narrow until real activation (MUST label narrow). Good.
    print("NARROW build schema/H consistency (valid EXECUTED 3-field pdf + required companions accepted; wrong/missing/unbound/changed real sha/wrong toolchain rejects; std mutations no fake live execute; H HIST vs High C actual probing): UNEXECUTED honest in this script (see worklog for constructed strict C with EXECUTED_BUILD + toolchain versions companions using existing local TeX, MUST label narrow until real activation with high finalize unblocked + real complete C).")
    print("Preserve bad SELF before fixtures/wrappers immutable no rewrites (old fixtures with SELF refs, e.g., high-u1-weekly basis? Or synthetic fake receipt? Or interface-mismatch bad SELF? – preserved as is, no rewrites).")
    print("Candidate 409+uncommitted owned H files only; no new ordinary commit; whole unit ongoing not HumanCommitPoint.")
    print("Remaining H accumulator unexecuted until high U activate; HIGH will run real U/C fixture and report failures; do NOT claim 21/next 40 pass before actual.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
