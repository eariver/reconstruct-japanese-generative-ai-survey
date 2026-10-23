#!/usr/bin/env python3
"""R4 Bug2 focused: runtime_tool override patches all instances, checked historical only.

- Creates two fake evidence module instances (simulating weekly/longform split) +
  real DST runtime_tool; verifies current_stage_basis_override patches ALL.
- Verifies historical State SHA drift allowed ONLY when acceptance binds exact
  package hash (content-addressed), otherwise still fails (no broad skip).
- Verifies non-state drift still fails, and non-acceptance still fails.
Saved BEFORE execution. Temp dirs only.
ENV must be set BEFORE startup.
"""
from __future__ import annotations
import os, sys, pathlib, tempfile, types, hashlib, json

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER PYTHONDONTWRITEBYTECODE!=1"); sys.exit(2)
if not os.environ.get("PYTHONPYCACHEPREFIX","").startswith("/tmp/opencode/"):
    print("BLOCKER PYTHONPYCACHEPREFIX"); sys.exit(2)

DST = pathlib.Path("/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60")
sys.path.insert(0, str(DST))
for m in list(sys.modules.keys()):
    if m.startswith("scripts."):
        del sys.modules[m]
if "scripts" in sys.modules:
    del sys.modules["scripts"]

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main() -> int:
    import scripts.survey_agent_tool_v2 as rt
    import scripts.survey_evidence_v2 as ev_real
    # fake second evidence instance (duplicate module object)
    ev_fake = types.ModuleType("scripts.survey_evidence_v2")
    # copy real funcs
    ev_fake.validate_evidence_package_basis = ev_real.validate_evidence_package_basis
    # register both in sys.modules under different keys to simulate split
    import sys as _sys
    _sys.modules["test_fake_evidence"] = ev_fake
    # collect via _instances: should find both rt.evidence, ev_real, ev_fake? Our fix scans suffix
    # ev_fake name does not end with suffix, so manually test patching logic:
    # Instead test real fix: patch all sys.modules ending with suffix
    # Create a second real-like module with same __name__ suffix
    ev_dup = types.ModuleType("dup.survey_evidence_v2")
    ev_dup.validate_evidence_package_basis = ev_real.validate_evidence_package_basis
    _sys.modules["dup.survey_evidence_v2"] = ev_dup
    # Now override should patch ev_real, ev_dup, and rt.evidence (which is ev_real in single-root)
    orig_real = ev_real.validate_evidence_package_basis
    orig_dup = ev_dup.validate_evidence_package_basis
    with rt.current_stage_basis_override():
        # both should be wrapped (different objects)
        assert ev_real.validate_evidence_package_basis is not orig_real, "real not patched"
        assert ev_dup.validate_evidence_package_basis is not orig_dup, "dup not patched"
        print("MULTI_INSTANCE_PATCH PASS")
    # after context, restored
    assert ev_real.validate_evidence_package_basis is orig_real, "real not restored"
    assert ev_dup.validate_evidence_package_basis is orig_dup, "dup not restored"
    print("RESTORE PASS")
    # checked historical: temp package/acceptance
    with tempfile.TemporaryDirectory(prefix="r4-bug2-", dir="/tmp") as td:
        root = pathlib.Path(td)
        # minimal repo files for core.sha256_file etc.: use real core with temp root
        import scripts.survey_production_v2 as core
        # create state file (current) and package with old SHA
        state_path = root / "state.json"
        state_path.write_bytes(b'{"a":1}')
        cur_sha = sha(b'{"a":1}')
        old_sha = sha(b'{"a":0}')
        pkg_dir = root / "pkg"
        pkg_dir.mkdir()
        pkg_path = pkg_dir / "package.json"
        pkg = {"schema_version": "2.0-rc1", "issue_id": "I", "research_profile": "WEEKLY",
               "basis": {"profile_path": "p.json", "profile_sha256": "0"*64,
                         "state_path": "state.json", "state_sha256": old_sha,
                         "discovery_path": "d.jsonl", "discovery_sha256": "0"*64,
                         "screening_acceptance_path": "s.json", "screening_acceptance_sha256": "0"*64},
               "prompt": {"path": "x", "sha256": "0"*64},
               "contracts": {"run_package": {"path": "y", "sha256": "0"*64},
                             "task": {"path": "y", "sha256": "0"*64},
                             "card": {"path": "y", "sha256": "0"*64}},
               "tasks": [], "expected_outputs": {"one_result_per_task": True, "filename_rule": "same-basename-as-task"},
               "rules": []}
        # Need full basis files to pass original checks beyond state? Our wrapper only tests state drift path,
        # but original will fail on other basis first. Simplify: test wrapper directly via _historical_state_basis_wrapper
        from scripts.survey_agent_tool_v2 import _historical_state_basis_wrapper
        def orig_fail(repo_root, package_path, package, impl_sha):
            # fail only on state_sha, like real
            import scripts.survey_production_v2 as c2
            p = package["basis"]
            # simulate real check: state file sha vs basis
            cur = c2.sha256_file(repo_root / p["state_path"])
            if cur != p["state_sha256"]:
                raise ValueError("Evidence package basis drift: state_sha256")
            return ("ok", [])
        wrapped = _historical_state_basis_wrapper(orig_fail, error_text="Evidence package basis drift: state_sha256",
                                                   acceptance_name="evidence-accepted.json",
                                                   changed_text="accepted Evidence package copy changed", label="Evidence")
        # acceptance binds package
        acc_path = pkg_dir / "evidence-accepted.json"
        pkg_bytes = json.dumps(pkg, sort_keys=True).encode()
        pkg_path.write_bytes(pkg_bytes)
        acc = {"package_sha256": sha(pkg_bytes)}
        acc_path.write_text(json.dumps(acc))
        # should allow historical (adjust to current)
        try:
            wrapped(root, pkg_path, pkg, "impl")
            print("CHECKED_HISTORICAL_ALLOW PASS")
        except Exception as e:
            print(f"FAIL checked should allow: {e}"); return 2
        # tampered package (acceptance no longer binds) must still fail
        pkg_path.write_bytes(b'tampered')
        try:
            wrapped(root, pkg_path, pkg, "impl")
            print("FAIL tampered should refuse"); return 2
        except ValueError as e:
            assert "changed" in str(e) or "drift" in str(e), e
            print("TAMPERED_REFUSED PASS")
        # non-state error must not be swallowed
        def orig_other(repo_root, package_path, package, impl_sha):
            raise ValueError("some other drift")
        wrapped2 = _historical_state_basis_wrapper(orig_other, error_text="Evidence package basis drift: state_sha256",
                                                    acceptance_name="evidence-accepted.json",
                                                    changed_text="changed", label="Evidence")
        try:
            wrapped2(root, pkg_path, pkg, "impl")
            print("FAIL other should propagate"); return 2
        except ValueError as e:
            assert "other" in str(e), e
            print("OTHER_PROPAGATED PASS (no broad skip)")
    print("BUG2_FOCUSED PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
