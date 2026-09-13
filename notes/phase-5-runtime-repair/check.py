"""Verify fixed support bytes, patch identity, and recorded test bindings offline."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=ROOT/".phase-5-inputs/runtime-repair-baseline"
CANDIDATE=ROOT/".phase-5-inputs/runtime-repair-candidate"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding="utf-8"))
support=read(HERE/"support-inputs.json")
for row in support["files"]:
    path=BASE/row["path"]
    assert sha(path)==row["sha256"] and path.stat().st_size==row["bytes"], row["path"]
rows=read(HERE/"candidate-files.json")
patch=""
for row in rows:
    rel=row["path"]
    assert sha(BASE/rel)==row["base_sha256"], rel
    assert sha(CANDIDATE/rel)==row["candidate_sha256"], rel
    patch+="".join(difflib.unified_diff((BASE/rel).read_text(encoding="utf-8").splitlines(True),
        (CANDIDATE/rel).read_text(encoding="utf-8").splitlines(True),fromfile="a/"+rel,tofile="b/"+rel))
assert patch==(HERE/"candidate.patch").read_text(encoding="utf-8")
results=read(HERE/"test-results.json")
assert results["tests_run"] == 58 and len(results["errors"]) == 6 and not results["failures"]
assert not results["skipped"]
assert all("test_survey_human_gate_revalidation_revision_v2.RevalidationRevisionTests" in e["test"]
           and "missing reviewed path" in e["traceback"] for e in results["errors"])
rerun=read(HERE/"git-aware-results.json")
assert rerun["successful"] and not rerun["errors"] and not rerun["failures"] and not rerun["skipped"]
assert rerun["suite_names"] == ["tests.test_survey_human_gate_revalidation_revision_v2"]
assert rerun["input_sha256"] == results["input_sha256"]
for rel,expected in results["input_sha256"].items(): assert sha(CANDIDATE/rel)==expected,rel
assert sha(HERE/"test_runtime_repair.py")==sha(CANDIDATE/"tests/test_runtime_repair.py")
old=read(HERE/"baseline-results.json")
assert sha(HERE/"baseline-test.txt")==old["raw_log_sha256"]
node=next(n for n in ast.parse((HERE/"test_runtime_repair.py").read_text(encoding="utf-8")).body
          if isinstance(n,ast.ClassDef) and n.name=="RuntimeRepairTests")
assert hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()==old["runtime_test_class_ast_sha256"]
for p in HERE.glob("*.py"): ast.parse(p.read_text(encoding="utf-8"))
report={"passed":True,"fixed_support_files":len(support["files"]),"patch_files":len(rows),
        "distinct_tests_covered":results["tests_run"],"first_run_passed":52,"git_aware_rerun_tests":rerun["tests_run"],"patch_sha256":sha(HERE/"candidate.patch"),
        "additional_test_sha256":sha(HERE/"test_runtime_repair.py"),
        "scope":"Offline artifact/test-binding check; not production validation or independent review"}
(HERE/"check.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report))
