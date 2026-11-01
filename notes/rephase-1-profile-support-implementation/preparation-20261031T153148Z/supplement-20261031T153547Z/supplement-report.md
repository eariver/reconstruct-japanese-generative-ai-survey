# Supplement report — preparation qualification 20261031T153547Z

Bounded qualification/correction to `preparation-20261031T153148Z/source-observation.md`
§§3/5. Appended as §9; existing report/logs unmodified. No source editing, no
tests/fixtures/commits, no subagents. A/B/C concurrent edits untouched (no worktree
content hashed here).

## New raw outputs (all NEW, exit 0)

Under `supplement-20261031T153547Z/logs/`:

- `gitdb-kinds-stdout/stderr/exit.txt` — full candidate `.git` entry kinds:
  83 files / 0 symlinks / 49 dirs; `objects/info/` absent (no `alternates`);
  `shallow` baseline774; origin inert; sparse cone true.
- `gitdb-shared-stdout/stderr/exit.txt` — full `(dev,ino)` comparison:
  candidate `.git` 83 vs proof `.git` 83 → shared 0;
  candidate vs reconstruct `.git/objects` 5377 (OBJECTS ONLY) → shared 0;
  symlinks 0/0; internal duplicates 0. No reconstruct HEAD/ref/history readback.
  No child Gitlinks inspected.
- `mode-check-stdout/stderr/exit.txt` — `lstat`-only mode vs manifest:
  768/768 present, 768/768 physical-mode match. Mutated worktree; NOT initial-byte
  proof; does not replace copy-time 768/768 sha+bytes verification.
- `candidate-head-tree-stdout/stderr/exit.txt` — candidate-only plumbing, no mutation:
  `HEAD` `409b292756dd1277b9dfae87679934c0d2ce251c`,
  `HEAD^{tree}` `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (match expected).
- `tinytex-stdout/stderr/exit.txt` — explicit paths exist:
  `.../lualatex` → `luahbtex` (LuaHBTeX 1.24.0), `.../biber` (2.22);
  PATH has no TeX. Corrects §5 "TeX absent" to PATH-absence. No install/build.

## Qualifications retained

- First copy pipeline exits (tar 0, `cp -a` 0) and sample-inode limits preserved;
  no retroactive atomic guard/copy-time enforcement claim.
- Sparse/promisor/partialDB inherited (`*.promisor`, `*.rev`, packs observed only).
- Read-only env verification; `GIT_*` unset at prior check; no mutation.

## Blocker

None. Full-DB separation holds; explicit TeX available if needed.
Supplemental preparation evidence complete.
