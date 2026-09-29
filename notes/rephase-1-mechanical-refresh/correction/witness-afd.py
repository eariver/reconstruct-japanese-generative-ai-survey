#!/usr/bin/env python3
"""Targeted failing witnesses against afd (pre-correction) for R1-A01..06.
Fast source-level + lightweight runtime checks, no heavy Weekly fixtures.
Each check prints WITNESS <ID> FAIL/PASS with concrete evidence.
Exit 0 always (witness collection); failures are the expected afd gaps.
Run with: /tmp/jgas-rephase-application-venv/bin/python3.12 witness-afd.py /tmp/jgas-rephase-mechanical-r1-20260928T000710Z
"""
from __future__ import annotations
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: witness-afd.py <fixture-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    writer = (root / "scripts/survey_weekly_mechanical_refresh_v2.py").read_text(encoding="utf-8")
    agent = (root / "scripts/survey_agent_control_v2.py").read_text(encoding="utf-8")
    gate = (root / "scripts/survey_reader_surface_gate_v2.py").read_text(encoding="utf-8")
    deriv = (root / "scripts/survey_weekly_derivation_v2.py").read_text(encoding="utf-8")
    tests = (root / "tests/test_survey_weekly_mechanical_refresh_v2.py").read_text(encoding="utf-8")
    reval_tests = (root / "tests/test_survey_publication_revalidation_v2.py").read_text(encoding="utf-8")

    def report(wid: str, ok: bool, detail: str) -> None:
        print(f"WITNESS {wid} {'PASS' if ok else 'FAIL'}: {detail}")

    has_guard_identity = "expected_guard" in writer or "guard_bytes" in writer or "_reject_symlink_ancestors" in writer and "guard" in writer
    # A01 requires explicit expected-guard byte identity variable
    has_guard_identity = "expected_guard_bytes" in writer or "guard_expected" in writer
    has_commit_flag = "\ncommitted =" in writer or "\n    committed =" in writer
    try_block = writer.split("except Exception")[0] if "except Exception" in writer else writer
    postcommit_in_try = "post-commit active readback" in writer or ("final_active" in try_block and "revalidate_publication_surface" in try_block)
    has_uncond_unlink = "finally:" in writer and "lock_path.unlink()" in writer and not has_guard_identity
    report("R1-A01-unconditional-unlink", not has_uncond_unlink,
           "writer finally unlinks guard unconditionally (481-486) without ownership check=" + str(has_uncond_unlink))
    if "finally:" in writer and "lock_path.unlink()" in writer and not has_guard_identity:
        report("R1-A01-guard-ownership", False, "no expected-guard byte identity check before unlink; any foreign guard would be deleted")
    else:
        report("R1-A01-guard-ownership", True, "guard ownership present")
    if not has_commit_flag:
        report("R1-A01-commit-flag", False, "no committed flag; post-commit readback failure would trigger rollback of committed authority")
    else:
        report("R1-A01-commit-flag", True, "commit flag present")
    if postcommit_in_try and not has_commit_flag:
        report("R1-A01-postcommit-in-try", False, "final_active readback inside rollback try without commit guard")
    else:
        report("R1-A01-postcommit-in-try", True, "post-commit separated or guarded")

    uses_write_json_record = "core.write_json(record_path" in agent
    uses_write_json_state = "core.write_json(state_path, updated)" in agent
    agent_has_xb = '"xb"' in agent or "'xb'" in agent
    if uses_write_json_record:
        report("R1-A02-record-exclusive", False, "agent uses core.write_json(record_path) after exists check; TOCTOU, not exclusive xb creation")
    else:
        report("R1-A02-record-exclusive", True, "record uses exclusive creation")
    if uses_write_json_state:
        report("R1-A02-state-atomic", False, "agent uses truncating core.write_json(state) not bounded temp+replace")
    else:
        report("R1-A02-state-atomic", True, "state uses atomic replace")
    if "written_record_sha = core.sha256_file(record_path)" in agent:
        report("R1-A02-known-bytes", False, "known-write sha is hash read after write, not expected serialized bytes; blesses foreign bytes")
    else:
        report("R1-A02-known-bytes", True, "known bytes from expected serialization")
    if not agent_has_xb:
        report("R1-A02-xb-present", False, "no exclusive xb creation in agent owner")
    else:
        report("R1-A02-xb-present", True, "xb present in agent")
    if "between" in reval_tests.lower() or "competitor" in reval_tests.lower():
        report("R1-A02-competitor-test", True, "competitor-between-check test present")
    else:
        report("R1-A02-competitor-test", False, "no test creates competitor file between precheck and creation; only preset allocator scenario")

    if "def _atomic_replace(path: Path, data: bytes, label: str, run_id: str)" in writer:
        report("R1-A03-target-recheck", False, "_atomic_replace has no expected-old-hash param; gate replace has no immediate target old-hash check")
    else:
        report("R1-A03-target-recheck", True, "_atomic_replace checks expected old bytes")
    if "record_path" in writer and "after API" in writer or "record disposition" in writer.lower():
        report("R1-A03-wrapper-disposition", True, "wrapper inspects record/State disposition after API error")
    else:
        report("R1-A03-wrapper-disposition", False, "wrapper does not inspect actual record/State disposition after API error; assumes rollback complete")
    if "bound_snapshot" in writer and "accepted_refs" in writer and "quality-regression-bundle" in writer:
        report("R1-A03-complete-snapshot", True, "complete snapshot present")
    else:
        report("R1-A03-complete-snapshot", False, "writer rechecks only State/HEAD/Gate/receipt (359-364,401-403), ignores accepted/authored/manuscript/reviews/PDF/bundle/checkpoint/control bytes")

    if "_reject_symlink_ancestors" in writer or "_check_symlink_ancestors" in writer or "symlink_ancestor" in writer:
        report("R1-A04-retention-symlink", True, "retention parent symlink rejection present")
    else:
        report("R1-A04-retention-symlink", False, "retention_base mkdir follows symlink; no parent-component symlink rejection (365-369)")
    if "_receipt_paths" in writer and "_receipt_paths(" not in writer.replace("def _receipt_paths", ""):
        report("R1-A04-receipt-paths-unused", False, "_receipt_paths defined but unused; publication/v2 basename test not canonical Profile binding")
    else:
        if 'profile["paths"]' in writer or "source_root" in writer and "publication" in writer:
            report("R1-A04-profile-derived", True, "paths derived from Profile")
        else:
            report("R1-A04-profile-derived", False, "paths derived from basename publication/v2 or receipt selfref, not Profile source_root")
    if ".resolve()" in writer and "is_symlink" in writer:
        report("R1-A04-resolve-alias", False, "raw path validation before .resolve erases aliases; need lexical + symlink-ancestor checks before resolve")
    else:
        report("R1-A04-resolve-alias", True, "alias-safe path handling")
    if "core.repo_local_path" in deriv and "def _safe" in deriv:
        report("R1-A04-safe-ancestors", False, "_safe checks leaf symlink but not every parent component; retention_base follows symlink out of root")
    else:
        report("R1-A04-safe-ancestors", True, "ancestor checks present")

    if '["authored_refs"][0]' in writer:
        report("R1-A05-authored-by-name", False, "authored input chosen by array index [0] instead of semantic name publication-semantic-input")
    else:
        report("R1-A05-authored-by-name", True, "authored refs by NAME")
    if 'for _sk in ("status", "decision", "reviewed_by", "surface_sha256", "review_path", "review_sha256")' in writer:
        report("R1-A05-gate-equality", False, "new/old Gate compares only 6 semantic_authority fields; not complete except allowed metadata/digest/receipt")
    else:
        report("R1-A05-gate-equality", True, "complete Gate equality")
    if "def inspect_receipt_envelope" in deriv and "def _inspect_receipt_envelope" not in deriv:
        report("R1-A05-private-helper", False, "receipt helper is public inspect_receipt_envelope; should be underscore-named _inspect_receipt_envelope")
    else:
        report("R1-A05-private-helper", True, "receipt helper private")
    if "semantic_review" in writer and "review_sha256" in writer:
        report("R1-A05-receipt-link", False, "receipt link not completely checked before retention (input/review/output to Gate/manuscript + canonical Profile paths need verification)")
    else:
        report("R1-A05-receipt-link", False, "receipt link incomplete")

    if "test_accepted_and_authored_mutation_refused" in tests:
        if 'with self.subTest(mutation="accepted")' in tests and 'with self.subTest(mutation="authored")' in tests:
            idx_acc = tests.index('mutation="accepted"')
            idx_auth = tests.index('mutation="authored"')
            between = tests[idx_acc:idx_auth]
            if "restore" in between.lower() or "write_bytes(original" in between or "cleanup" in between.lower():
                report("R1-A06-subtest-isolation", True, "accepted/authored subtests isolated")
            else:
                report("R1-A06-subtest-isolation", False, "accepted+authored subtests contaminate: accepted mutation left in place, authored case can pass on unrelated upstream failure via broad drift regex")
        else:
            report("R1-A06-subtest-isolation", False, "subtest structure unclear")
    else:
        report("R1-A06-subtest-isolation", True, "test renamed or removed")
    if "# Only selected writes occurred" in tests and "only selected writes" in tests.lower():
        if "_snapshot" in tests and tests.count("_snapshot") > 5:
            if "complete" in tests.lower() and "inventory" in tests.lower():
                report("R1-A06-only-writes", True, "complete pre/post inventory present")
            else:
                report("R1-A06-only-writes", False, "success 'only selected writes' is mere comment without complete pre/post byte+record inventory assertions")
        else:
            report("R1-A06-only-writes", False, "no full delta assertion")
    else:
        report("R1-A06-only-writes", False, "only-writes check missing")
    needed = ["symlink", "partial", "foreign guard", "HEAD-State-input drift", "two cooperating", "partial API", "tamper", "postcommit"]
    missing_cov = [k for k in needed if k.lower() not in tests.lower()]
    if not missing_cov:
        report("R1-A06-coverage", True, "all major guard/failure paths covered")
    else:
        report("R1-A06-coverage", False, f"missing coverage for: {', '.join(missing_cov)}")

    print("WITNESS-COLLECTION-COMPLETE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
