#!/usr/bin/env python3
"""HIGH-phase longform renewal->editorial driver — overlay+commit, U3, probe.

Longform fixture (U2-active r4, G2 epoch): overlay CURRENT workdir (P1 renewal
integration + current HIGH), commit genuine epoch, run U3-longform
(prior=U2 r4, fresh proof at new HEAD), then P1 prepare probe with genuinely
changed longform authoring (longform_revision bump + cover/summary edits).
P1 prepare is read-only; success means the renewed prior is accepted with
KEEP/COPY discipline and no false identical-reader refusal. Full editorial
activation continues only if the probe passes.
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z"
EVID = EVID_BASE / "run60-20261025T100000Z"
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z"
sys.path.insert(0, str(EVID_BASE))
from run_chain import overlay_commit  # noqa: E402 (proven overlay helper)
from run_repeat import U_QA_BUILDER  # noqa: E402 (generic U QA builder)

ISSUE, PROP = "SP001", "lf-boot-1"

PROBE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, prop_new = sys.argv[1:3]
import faulthandler, os
try:
    _dp = os.environ.get("ED_PROBE_DUMP_PATH", "")
    if _dp:
        faulthandler.dump_traceback_later(300, repeat=True, file=open(_dp, "w"))
except Exception:
    pass
from pathlib import Path
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as p1mod
assert str(Path(p1mod.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
pdir_old = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}"
pdir_new = f"sources/{ISSUE}/publication/v2/editorial-corrections/{prop_new}"
old_auth = json.loads((root_p / pdir_old / "authoring-input.json").read_bytes())
new_auth = json.loads(json.dumps(old_auth))
new_auth["cover"]["headline"] = ("Renewal-editorial longform probe headline: thematic lineage gains "
    "a fixture-local amendment after versioned renewal; no genuine approval implied.")
new_auth["final_summary"]["paragraphs"] = (["Probe paragraph: changed longform reader must NOT trip "
    "NO_EDITORIAL_CHANGE on a U3-activated prior."])
if isinstance(new_auth.get("longform_revision"), dict):
    new_auth["longform_revision"]["revision"] = str(new_auth["longform_revision"].get("revision", "r1")) + "-probe"
elif "longform_revision" in new_auth:
    new_auth["longform_revision"] = {"revision": "r1-probe", "note": "changed-reader probe"}
else:
    new_auth["longform_revision"] = {"revision": "r1-probe", "note": "changed-reader probe"}
assert json.dumps(new_auth, sort_keys=True) != json.dumps(old_auth, sort_keys=True), "change must differ"
dest = root_p / pdir_new / "authoring-input.json"
dest.parent.mkdir(parents=True, exist_ok=True)
if dest.exists():
    print(json.dumps({"probe": "REFUSED_TARGET_EXISTS", "path": str(dest.relative_to(root_p))}))
else:
    dest.write_bytes(core.json_bytes(new_auth))
    res = p1mod.prepare_proposal(root_p, root_p / f"sources/{ISSUE}/production-state.json",
                                 dest, prop_new,
                                 "Renewal-to-editorial longform probe: changed reader on renewed prior")
    print(json.dumps({"probe": "PREPARED", "proposal_id": prop_new,
                      "keys": sorted(res.keys()) if isinstance(res, dict) else type(res).__name__}))
"""


def run(cmd: list[str], tag: str, env: dict, timeout_s: int = 900) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True,
                          timeout=timeout_s, env=env)
    (EVID / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID / "commands.log", "a", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}...  # -> exit={proc.returncode}\n")
    return proc


def cli(root: str, args: list[str], env: dict, tag: str) -> subprocess.CompletedProcess:
    import json as _json
    return run([sys.executable, "-c",
                "import sys; sys.path.insert(0, sys.argv[1]); "
                "from scripts.survey_versioned_renewal_v2 import main; "
                "sys.exit(main(sys.argv[2:]))",
                root] + args, tag, env)


def main() -> int:
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "commands.log").write_text("", encoding="utf-8")
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(name):
            print(f"FATAL: inherited {name}", file=sys.stderr)
            return 1
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"
    env["ED_PROBE_DUMP_PATH"] = str(EVID / "ed-probe-stacks.txt")
    dst = PARENT / "renewal-longform"
    root = str(dst.resolve())
    now_iso = datetime.now(timezone.utc).isoformat()
    state = f"sources/{ISSUE}/production-state.json"
    pdir = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}"
    mspec = f"{pdir}/manuscript-spec.json"
    rid, r_dir = "high-u3-longform", f"{pdir}/renewals/high-u3-longform"
    py = sys.executable
    head = overlay_commit(dst, "longform",
                          "HIGH phase TEST-ONLY: G3LF epoch (P1 renewal integration + current HIGH)",
                          env, EVID, "g3lf")
    print(f"G3LF epoch {head[:12]}", flush=True)
    import json as _json
    ok = True
    p = cli(root, ["prepare", "--root", root, "--state", state, "--renewal-id", rid,
                   "--intent", "REUSE_TARGETS", "--manuscript-spec", mspec,
                   "--executor", "high-phase-fixture", "--recorded-at", now_iso],
            env, "u3-prepare")
    print(f"u3-prepare: exit={p.returncode}", flush=True)
    ok &= p.returncode == 0
    if ok:
        basis_rel = f"{r_dir}/renewal-basis.json"
        q = run([py, "-c", U_QA_BUILDER, root, basis_rel, r_dir, pdir, now_iso,
                 "high-phase-fixture repeat-chain fresh re-assertion"],
                "u3-qa", env)
        (EVID / "u3-qa-stdout.txt").write_text(q.stdout or "", encoding="utf-8")
        (EVID / "u3-qa-stderr.txt").write_text(q.stderr or "", encoding="utf-8")
        (EVID / "u3-qa-exit.txt").write_text(str(q.returncode), encoding="utf-8")
        print(f"u3-qa: exit={q.returncode}", flush=True)
        ok &= q.returncode == 0
    if ok:
        checks_rel = (EVID / "u3-qa-stdout.txt").read_text().strip()
        f = cli(root, ["finalize", "--root", root, "--state", state, "--basis", basis_rel,
                       "--checks", checks_rel, "--executor", "high-phase-fixture",
                       "--recorded-at", now_iso], env, "u3-finalize")
        print(f"u3-finalize: exit={f.returncode}", flush=True)
        ok &= f.returncode == 0
    if ok:
        fout = _json.loads((EVID / "u3-finalize-stdout.txt").read_text())
        a = cli(root, ["activate", "--root", root, "--state", state,
                       "--set", fout["set_path"],
                       "--reason", "Core change: G3LF epoch P1 renewal integration",
                       "--executor", "high-phase-fixture", "--recorded-at", now_iso],
                env, "u3-activate")
        print(f"u3-activate: exit={a.returncode}", flush=True)
        ok &= a.returncode == 0
    if ok:
        aout = _json.loads((EVID / "u3-activate-stdout.txt").read_text())
        h = cli(root, ["history", "--root", root, "--record", aout["record_path"]],
                env, "u3-history")
        print(f"u3-history: exit={h.returncode} (expect 52 bindings)", flush=True)
        ok &= h.returncode == 0
    if ok:
        pr = run([py, "-c", PROBE, root, "ed-renew-lf-1"], "ed-probe-lf", env, timeout_s=2400)
        print(f"ed-probe-lf: exit={pr.returncode}", flush=True)
        ok &= pr.returncode == 0
    print("LONGFORM-EDITORIAL " + ("OK" if ok else "OPEN"), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
