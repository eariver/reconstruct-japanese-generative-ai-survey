# DM022 pre-Architecture preparation — appendix: full-742 equality + all-entry inode disjointness

Date: 2026-10-28 UTC. Bounded preparation check on `candidate-work` vs source
proof-copy. Read-only. No runtime/tests/install. After this return, preparation is
FROZEN (no more candidate edits); implementation workers start next.

Old observations preserved: `source-preparation.md` +
`source-preparation-data.json` untouched. First report's scope (742 count + 93/93
delta SHA, explicitly NOT full-742) stands and is now supplemented — not rewritten —
by this appendix. All copy/check commands are TRANSCRIBED tool-observed outputs, NOT
tee-saved raw execution logs. No saved runners executed.

## 1. Full 742 intended-path equality (excl. `.git`)

SRC: `.../versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
DST: `.../dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`

Method (read-only, workdir `/tmp`, no candidate writes): python `pathlib.rglob` +
`hashlib.sha256` (1MiB chunks) + `stat` size + `oct(st_mode & 0o7777)` + kind
(symlink target when present; regular-file vs other). Excluded by definition:
`.git` / `.git/*`. Excluded by rule (not counted): `__pycache__` segments, `*.pyc`.

Result:

- SRC intended files: **742**; DST intended files: **742**
- SRC-only: 0; DST-only: 0; common: 742
- Content/bytes/mode/kind mismatches: **0**
- Symlinks: SRC 0, DST 0; caches present: 0 (exclusion does not affect count)

This closes the prior gap: full-742 equality now proved for the restricted intended742
inventory. Mode compared as permission bits only (see §3 limitations).

## 2. All-entry `.git` inode disjointness (metadata only)

Scope: full `.git` ordinary files for SRC (83) and DST (83); reconstruct object-store
`.git/objects` ordinary files (81). Pure `find -type f / -type l / -links +1 /
-printf '%d %i %p'` + `ls` existence for `objects/info/alternates` and `commondir`.
NO git commands in reconstruct root. NO reconstruct HEAD/status/log/rev-parse/push read.
Human no-commit-readback order observed; source-copy proof and object inode comparison
are permitted and are all that is reported here.

Result (full comparison, no sampling — recon store was cheap: 81 files, 53M `du`):

- DST `.git`: 83 ordinary files, 0 symlinks, 0 hardlinked (`-links +1`)
- SRC `.git`: 83 ordinary files, 0 symlinks, 0 hardlinked
- RECON `.git/objects`: 81 ordinary files, 0 symlinks, 0 hardlinked
- Overlaps (`(dev,ino)`): DST∩SRC **0**, DST∩RECON **0**, SRC∩RECON **0**
- `alternates` absent: DST, SRC, RECON. `commondir` absent: DST, SRC, RECON.
- Same device observed in prior probe (2050); distinct `(dev,ino)` proves no
  hardlink/shared-object linkage, not content inequality.

Exact bound reported: DST83 / SRC83 / RECON-objs81, zero overlap. No truncated claim.

## 3. Limitations

- Permission bits only (`& 0o7777`); uid/gid/times not compared (copy times differ by
  construction).
- xattr/ACL/capabilities not examined; content bound is SHA256+bytes+kind+mode.
- Caches excluded by rule (0 present); `.git` excluded from 742 by definition and
  covered in §2 instead.
- Reconstruct side is metadata disjointness only — no content, HEAD, branch, status,
  or history inference.
- No CAS/crash-atomicity/no-drift certification. 55 Gitlinks/child dirt untouched,
  not re-verified.

## 4. Revised runtime requirement (pytest correction)

Prior `source-preparation-data.json` wording requiring workers to "supply venv+pytest"
is WITHDRAWN as a blanket requirement: it rested only on `pytest` absence.

Observed (read-only grep/AST, no execution): 229 `test_*.py` in new candidate-work;
`pytest` imports 0; `unittest` pervasive (100+ grep hits, 224 AST occurrences);
non-stdlib imports limited to `pypdf` (+ stdlib). System `/usr/bin/python3` 3.14.4
satisfies 3.12+; `unittest` runner help, `pypdf`/`yaml`/`jsonschema` import probes
passed read-only.

Rule going forward: runtime needs follow ACTUAL test imports per task (stdlib
unittest + observed third-party), not an unselected pytest requirement. Preserved gaps:
no isolated venv found, TeX toolchain absent (no pdflatex/xelatex/lualatex/latexmk),
no installs/network without authorization, no tests run in this unit.

## 5. Files / freeze

New in this appendix (no overwrite, no Git DB in packet):

- `source-preparation-appendix-742-equality-inode.md` (this file)
- `source-preparation-appendix-742-equality-inode-data.json`

Preparation FREEZE after return: no further candidate-work edits from this worker.
