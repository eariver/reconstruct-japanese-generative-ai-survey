# Residue inventory — __pycache__ + tmpvr07sdme (preserve, no delete)

No DST edits for inventory (read-only `find`/`git ls-files`/`stat`, exits 0). No clean/reset/commit/network. Unknown artifacts preserved, not claimed source-clean.

## DST current (implementation copy, HEAD 409b292, uncommitted)

- `scripts/__pycache__/` — 22 files, type `.pyc` bytecode cache, e.g. `survey_editorial_publication_v2.cpython-314.pyc`, `survey_schema_v2.cpython-314.pyc` (full list via `Glob scripts/__pycache__/*`, 22 entries). Provenance: Python bytecode from prior test/smoke runs that did not set `PYTHONDONTWRITEBYTECODE=1` + external `PYTHONPYCACHEPREFIX` (some runs used default in-tree cache). Hash/provenance: not hashed (binary cache, regenerable, not authority); `stat` shows regular files, not symlinks. Action: preserve in place, exclude from future SOURCE snapshots.
- `tests/__pycache__/` — 1 file: `test_survey_publication_set_v2.cpython-314.pyc`. Same provenance/action as above.
- `tmpvr07sdme/` — 43 files, types: `src/*.json` (production-profile, architecture, checkpoints, evidence, gates, etc.), `survey/main.tex`, `references.bib`, `main.pdf`, `src/publication/v2/*` (manuscript, gate, bundle, reviews). Provenance: tooling residue from prior `_make_source_root`/`TemporaryDirectory` style test fixture runs (8-char random suffix, no explicit prefix; exact creator not re-attributed by guess). Example paths: `tmpvr07sdme/src/production-profile.json`, `tmpvr07sdme/survey/main.tex` (full list via `Glob tmpvr07sdme/**/*`, 43 entries). Hash/provenance: JSON/TeX/PDF fixture bytes, not authority; preserved. Action: preserve in place, exclude from future SOURCE snapshots. Never `rm -rf`, never `git clean`.

## FIX23 SOURCE commit (old fixture epoch, HEAD feb4d1fc, attempt23)

- `git ls-files -s | wc -l` → `759` (exit 0).
- `git ls-files | grep -c "^tmpvr07sdme/"` → `43` (exit 0). `git ls-files | grep -c "__pycache__"` → `0` (exit 0).
- Intended source ≈716 = 759 − 43 residue. Extra 43 are `tmpvr07sdme/` files committed via `cp -a DST` + `git add -A` (which included residue present in DST at copy time). `__pycache__` correctly excluded via `rm -rf .../__pycache__` before `add` (0 tracked).
- Disclosure: old fixtures DID commit extra `tmpvr07sdme/` files; cannot retroactively clean (no history rewrite, preserve old epochs). Future snapshots must use explicit intended file list, not `cp -a` whole dir + `add -A`.
- No embedded Git DB contamination: `ls .git/objects/info/alternates` → `No such file` (exit non-zero, expected absent, no sharing); `git remote -v` → empty (inert, no network); `ls -d .git` present (independent DB, not shared). No `.git/` in subdirs (spot-checked via `Glob **/.git`, none beyond root – full worktree `ls-files` shows no nested DB paths).
- No hardlink sharing: `stat -c %d:%i` FIX23 vs DIAG copy differ (`45:718801` vs `45:720964`, link count `1`), `cp -a` without `--hard-links` creates independent inodes (verified).
- Actual imported code hashes: smoke runs set `PYTHONPATH=$FIX` only, `sys.path[0]=FIX_ROOT`; `sys.modules["scripts.*"].__file__` resolves under `$FIX/scripts/*.py` (not DST). Recorded FIX23 blobs (e.g., `survey_editorial_publication_v2.py` `cf0687c8...`) match FIX23 worktree file at SOURCE commit time (pre-authority); post-smoke authority outputs are untracked (`sources/`, `surveys/`, 10 lines) and do not affect SOURCE blobs. DST current (`5aee10f9...`) differs (later ALREADY_ACTIVE + review/bundle/Gate/seal/collect/visual/declared fixes) – old fixture must not be rebound to new pins; new epoch must regenerate authorities.
