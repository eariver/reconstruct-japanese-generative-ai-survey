#!/usr/bin/env python3
"""HIGH-phase failure/resume oracle driver — explicit refusal codes, no writes
beyond the refused attempt's preserved partials. Runs in the high21 fixtures
(U1+C1 R-dirs present under other ids, T1 epoch). No activation needed.

F1 duplicate prepare id -> RECORD_COLLISION (exit 2, old pointer unchanged).
F2 C finalize without targets -> BUILD_TARGETS_MISSING (exit 2).
F3 U finalize with stale QA (bootstrap checks, recorded before basis) ->
   QA_MISSING (exit 2, no fresh-QA bypass).
F4 resume on editorial r1 (not a renewal activation) -> RECORD_COLLISION.
F5 R1 mechanical refresh on LIVE versioned-active editorial State -> refusal
   before any write (existing versioned-mode refusal, both kinds).
F6 H verify on prior r1 chain in C1 fixtures (regression: C1 activity did not
   corrupt the prior chain; 11 bindings expected).
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z"
EVID = EVID_BASE / "run30-20261025T020000Z"
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-high21-20261025T020000Z"
W = "sources/2026-W37/production-state.json"
PDIR = "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1"


def run(cmd: list[str], tag: str, env: dict) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True,
                          timeout=600, env=env)
    (EVID / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID / "commands.log", "a", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}...  # -> exit={proc.returncode}\n")
    return proc


def main() -> int:
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "commands.log").write_text("", encoding="utf-8")
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(name):
            print(f"FATAL: inherited {name}", file=sys.stderr)
            return 1
    root = str(PARENT / "renewal-weekly")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"
    py = sys.executable
    now_iso = datetime.now(timezone.utc).isoformat()
    state_before = Path(root, W).read_bytes()

    f1 = run([py, "-c",
              "import sys; sys.path.insert(0, sys.argv[1]); "
              "from scripts import survey_versioned_renewal_v2 as high; "
              f"high.prepare_renewal(sys.argv[1], '{W}', 'high-u1-weekly', "
              f"'REUSE_TARGETS', '{PDIR}/manuscript-spec.json', None, 'x', '{now_iso}')",
              root], "f1-dup-prepare", env)
    print(f"F1 dup-prepare: exit={f1.returncode} (RECORD_COLLISION expected)", flush=True)

    f2prep = run([py, "-c",
                  "import sys; sys.path.insert(0, sys.argv[1]); "
                  "from scripts import survey_versioned_renewal_v2 as high; "
                  "import json; "
                  f"r = high.prepare_renewal(sys.argv[1], '{W}', 'high-c9-weekly', "
                  f"'RENDER_TARGETS', '{PDIR}/manuscript-spec.json', "
                  f"'{PDIR}/toolchain-spec.json', 'x', '{now_iso}'); "
                  "print(json.dumps({'basis_path': r['basis_path']}))",
                  root], "f2-prep-c9", env)
    print(f"F2 prep-c9: exit={f2prep.returncode}", flush=True)
    if f2prep.returncode == 0:
        import json as _json
        brel = _json.loads((EVID / "f2-prep-c9-stdout.txt").read_text())["basis_path"]
        f2 = run([py, "-c",
                  "import sys; sys.path.insert(0, sys.argv[1]); "
                  "from scripts import survey_versioned_renewal_v2 as high; "
                  f"high.finalize_renewal(sys.argv[1], '{W}', '{brel}', "
                  f"'{PDIR}/renewal-qa-checks-high-c1-weekly.json', "
                  f"'{PDIR}/renewals/high-c1-weekly/reviews/semantic-review-v2.json', "
                  f"'{PDIR}/renewals/high-c1-weekly/reviews/visual-review-v2.json', "
                  f"'x', '{now_iso}')",
                  root], "f2-finalize-no-targets", env)
        print(f"F2 finalize-no-targets: exit={f2.returncode} (BUILD_TARGETS_MISSING expected)", flush=True)

    f3prep = run([py, "-c",
                  "import sys; sys.path.insert(0, sys.argv[1]); "
                  "from scripts import survey_versioned_renewal_v2 as high; "
                  "import json; "
                  f"r = high.prepare_renewal(sys.argv[1], '{W}', 'high-u9-weekly', "
                  f"'REUSE_TARGETS', '{PDIR}/manuscript-spec.json', None, 'x', '{now_iso}'); "
                  "print(json.dumps({'basis_path': r['basis_path']}))",
                  root], "f3-prep-u9", env)
    print(f"F3 prep-u9: exit={f3prep.returncode}", flush=True)
    if f3prep.returncode == 0:
        import json as _json
        brel9 = _json.loads((EVID / "f3-prep-u9-stdout.txt").read_text())["basis_path"]
        f3 = run([py, "-c",
                  "import sys; sys.path.insert(0, sys.argv[1]); "
                  "from scripts import survey_versioned_renewal_v2 as high; "
                  f"high.finalize_renewal(sys.argv[1], '{W}', '{brel9}', "
                  f"'{PDIR}/deterministic-checks.json', None, None, 'x', '{now_iso}')",
                  root], "f3-finalize-stale-qa", env)
        print(f"F3 finalize-stale-qa: exit={f3.returncode} (QA_MISSING expected)", flush=True)

    r1rec = "sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json"
    f4 = run([py, "-c",
              "import sys; sys.path.insert(0, sys.argv[1]); "
              "from scripts import survey_versioned_renewal_v2 as high; "
              f"high.resume_renewal_activation(sys.argv[1], '{W}', '{r1rec}')",
              root], "f4-resume-editorial-r1", env)
    print(f"F4 resume-editorial-r1: exit={f4.returncode} (RECORD_COLLISION expected)", flush=True)

    f5 = run([py, "-c",
              "import sys; sys.path.insert(0, sys.argv[1]); "
              "from scripts import survey_production_v2 as core; "
              "from scripts import survey_weekly_mechanical_refresh_v2 as r1; "
              "from pathlib import Path; "
              "root = Path(sys.argv[1]); "
              "cfg = core.load_json(root / core.DEFAULT_CONFIG); "
              "state = core.load_json(root / 'sources/2026-W37/production-state.json'); "
              "from datetime import datetime, timezone; "
              "from pathlib import Path as _P; "
              "r1.refresh_mechanical_evidence(root, cfg, _P('sources/2026-W37/production-state.json'), "
              "'test', 'x', datetime.now(timezone.utc))",
              root], "f5-r1-versioned-refusal", env)
    print(f"F5 r1-versioned-refusal: exit={f5.returncode} (refusal before any write expected)", flush=True)

    f6 = run([py, "-c",
              "import sys; sys.path.insert(0, sys.argv[1]); "
              "from scripts import survey_versioned_renewal_history_v2 as hist; "
              "import json; "
              f"v = hist.verify_versioned_history(sys.argv[1], '{r1rec}'); "
              "print(json.dumps({'chain_length': v['chain_length'], "
              "'n_bindings': len(v['observed_source_bindings'])}))",
              root], "f6-history-r1-regression", env)
    print(f"F6 history-r1-regression: exit={f6.returncode} (11 bindings expected)", flush=True)

    if Path(root, W).read_bytes() != state_before:
        print("FATAL: LIVE State moved during refusal oracles", file=sys.stderr)
        return 1
    print("STATE-PINNED (old pointer unchanged across all refusal oracles)")
    print("DONE FAIL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
