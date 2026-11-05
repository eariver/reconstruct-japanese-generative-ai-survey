# W34 dispose+run r2 — source review note (DO NOT EXECUTE)

r2 preserves v1 (`w34-operator-dispose-run-20261104.py` 43406B `68253077...`)
untouched and fixes independent review B1-B3 (source-only, no execution yet).
No subagents, no project import/run, no network/Production/reconstructGit.

## B1-B3 fixes

- B1 invented accepted dirs: v1 `.get("accepted_evidence_dirs",[])` (keys do
  not exist) -> old bf208/f744 counted as new -> definite `len(new)!=1`.
  r2 derives known old dirs from FROZEN `w34_tree_full` entries + accepted
  file-pin parents, asserts exactly 1+1 before run, passes real sets to
  post-run layout (`ctx["old_ev_dirs"]/["old_view_dirs"]`).
- B2 after-import re-hash: r2 re-hashes all 9 modules after import
  (hash == pre hash, root inside e84) + refuses `__pycache__`.
- B3 strict State: r2 uses `R6._strict_json` duplicate-key strict for State
  (not `json.loads`).
- READY exact `retained_pkg_dir` path verified (no glob guess).
- No fallback metadata/default invented facts (exact keys required, no
  `.get(...,[])`/`0o644` defaults for counts/paths).
- Retains: true R369/E439, all source771 + triangulated test, source per
  remove/backup both, preservation layout, EFFECTIVE 439 validators
  (not SP root 369), audit archived path+bytes, umask modes, packet-only
  retention, failure preserve/no retry.

## Files (packet only, no active writes)

- NEW wrapper `w34-operator-dispose-run-r2-20261104.py` 50975B
  `a77dbb8848d6e696e1a191807ce924951038a53532a1d0a6e512e8535ff0c8ba`
- NEW launcher `w34-dispose-run-launcher-r2-20261104.sh` 1099B
  `22c0fee3c82141b1c8f1d7122050e24c47bf2c962bcc564a8bff30f71b9e8efc`
- NEW checks `w34-dispose-run-r2-checks-20261104.py` 7250B
  `15f3c1b9ef0931f08683efdf0625661a20e1d20781959364a3818616f93024dc`
  + raw `...raw.txt` 1290B `b32371b2...` — **20/20 PASS**
- Same manifest `cede7e46...` 991185B / input `1ea56297...` / READY
  `473bf85b...` / supplement `ce6f...` / SP helper `2c6f...` unchanged.

## Stdlib tests (REAL manifest/tree, actual DATA)

Old bf208/f744 from frozen dirs + pin parents (not invented); live has old;
baseline yields 0 new; simulated 1+1 admissible. Root JSONL 369 lines vs
effective 439 lines; ledger 439 == effective (root 369 rejected). Screening
439 decisions. Staged `1ea562...` == r2 packet; mismatch refused. Wrapper
derives old dirs, no default keys, READY exact pkg, strict State, re-hash.
No project imports; truthful exit 0; preserved raw.

## Limitations / no execution

Dead placeholder code removed; no token-tests. Source-read helper
signatures only. SP plan does not authorize W34. No execution until Root +
independent source review.
