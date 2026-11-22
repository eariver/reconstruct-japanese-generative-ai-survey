#!/usr/bin/env python3
"""Stdlib-only launcher for normal Selection validation (operation evidence, not shipping source).

Executes unchanged scripts.survey_stage_validation_v2 main through runpy with
exact normal CLI argv. Registers periodic faulthandler stack dumps every 300s
(repeat) to separate packet stack file for phase observability. No project
function mock/wrap, no fake proof, no checked context, no source/State patch,
no return/timeout semantics change.
"""
from __future__ import annotations

import faulthandler
import runpy
import sys
from pathlib import Path


def main() -> int:
    # argv: [launcher, stackfile, repo-root, config, state, artifact1, artifact2, output, recorded-at?]
    # Exact normal CLI is reconstructed inside from args (see packet README for full argv).
    if len(sys.argv) < 8:
        print("launcher usage: launcher.py <stackfile> <repo-root> <config> <state> <artifact NAME=PATH>... --output <report> [--recorded-at <instant>]", file=sys.stderr)
        return 2
    stackfile = Path(sys.argv[1])
    stackfile.parent.mkdir(parents=True, exist_ok=True)
    # Mirror `python -m` (cwd on path): ensure repo-root is importable via stdlib only.
    try:
        _args = sys.argv[2:]
        _repo = _args[_args.index("--repo-root") + 1] if "--repo-root" in _args else "."
        if _repo not in sys.path:
            sys.path.insert(0, _repo)
    except Exception:
        pass
    # Periodic dumps, repeat, separate file (operation evidence only).
    fh = stackfile.open("w")
    try:
        faulthandler.dump_traceback_later(300, repeat=True, file=fh)
        # Exact normal module main via runpy, argv[1:] replaced with normal CLI argv.
        # sys.argv[0] is launcher; sys.argv[1] is stackfile (launcher-only); rest is normal CLI.
        normal_argv = ["scripts.survey_stage_validation_v2"] + sys.argv[2:]
        sys.argv = normal_argv
        try:
            runpy.run_module("scripts.survey_stage_validation_v2", run_name="__main__", alter_sys=True)
        except SystemExit as exc:
            code = exc.code
            if isinstance(code, int):
                return code
            return 0 if code is None else 2
        return 0
    finally:
        try:
            faulthandler.cancel_dump_traceback_later()
        except Exception:
            pass
        try:
            fh.close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
