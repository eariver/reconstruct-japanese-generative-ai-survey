# Relocation record — tool-created nested Git worktrees moved out of the packet

2026-10-15 JST (parent stamp `20261015T171102Z`). Pre-commit packaging: B4
GEN/PROOF outdirs inside `notes/rephase-1-dm021-p2v/source-correction/`
contained nested Git worktrees (`disposable-copy/`, `clean409-copy/` with
`.git/`). Left in place they would become embedded gitlinks in the Human
commit. All 5 worktrees + 2 tool temp indexes were MOVED (exact `mv`, no
copy-time fabrication) to the NEW unique parent
`/tmp/opencode/jgas-dm021p2v-preserved-proof-20261015T171102Z/` (verified
absent before creation). Nothing deleted; all proof/gen raw/hash/patch files
stay at their original packet paths. Raw old worktree locations below remain
historical; the mapping explains current availability.

Temporary workspace-nested DB layout was always an independent DB (byte copy,
inert remote, no alternates/object-sharing per B4 evidence) — but a packet
directory is not its intended durable location. Disclosure, not a content
change: worktree bytes/HEAD/tree/status/DB counts verified identical
before→after (cross-filesystem `mv` re-allocates inodes; identity is by
content: HEAD/tree/counts/hashes, all equal).

## Mapping (old → new actual paths)

| # | Old packet path (historical) | New actual path | Kind |
|---|---|---|---|
| 1 | `source-correction/evidence-20261016T000000Z-gen/disposable-copy` | `…/preserved-proof-20261015T171102Z/gen-failed-disposable-copy` | GEN1 failed-attempt worktree (relative-outdir refusal) |
| 2 | `source-correction/evidence-20261016T000000Z-gen2/disposable-copy` | `…/gen2-disposable-copy` | GEN2 disposable worktree |
| 3 | `source-correction/evidence-20261016T000000Z-gen2/disposable-index` (file, sha `2a4a0245…`, 5766188B) | `…/gen2-disposable-index` | GEN2 tool temp index (hash preserved) |
| 4 | `source-correction/evidence-20261016T000000Z-proof2/clean409-copy` | `…/proof2-clean409-copy` | PROOF2 (v4 patch `71d5154d…`) apply copy |
| 5 | `source-correction/evidence-20261016TB1-gen/disposable-copy` | `…/TB1gen-disposable-copy` | TB1 GEN disposable worktree |
| 6 | `source-correction/evidence-20261016TB1-gen/disposable-index` (file, sha `36ac2f56…`, 5766188B) | `…/TB1gen-disposable-index` | TB1 GEN tool temp index (hash preserved) |
| 7 | `source-correction/evidence-20261016TB1-proof/clean409-copy` | `…/TB1proof-clean409-copy` | **Final TB1 apply copy** (v5 patch `dc5ae07b…`) |

Untouched: reconstruct `.git`, P2R/P2V active copies, all other user files
(never listed, never entered). No source/runtime/test/HEAD/refs edits, no old
scripts run, no staging/commits/deletion/restore/network/tests.

## Before → after observations (checked, read-only git)

All 5 worktrees, before and after: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`. Status rows: disposable
copies 102 each (18 source + 84 caches, overlay intact); clean409 copies 18
each (patch-applied state). `.git` entry counts identical before→after:
gen-failed/proof2/TB1proof `134 files/96 dirs`; gen2/TB1gen disposable
`152 files/106 dirs` (the +18/+10 vs pristine is GEN's own `git add` blob
hashing inside the disposable COPY's object DB during patch generation —
tool-side effect confined to the copy; active candidate untouched).
Temp index hashes identical before→after (see table). Full per-item record:
`relocation-record.json` in this packet.

## Final TB1 apply copy independent verification (new location)

`/tmp/opencode/jgas-dm021p2v-preserved-proof-20261015T171102Z/TB1proof-clean409-copy`:
actual HEAD `409b292…`, tree `8ce36998…`; **all18 sha256+bytes+mode vs
`expected18-source-correction-v5.json`: ALL_MATCH** (incl. test `c567715d`);
full status exactly the canonical 18 rows (`3 M` reader-surface-gate paths +
`15 ??` P2V overlay paths, no cache rows — caches were declared-removed in
the copy per proof design). Available apply-copy path for review (above).

## Packet state after relocation

`find notes/rephase-1-dm021-p2v -name .git` → empty; no nested `.git` files or
dirs, no `disposable-index` files remain in THIS packet (verified by
specialized inventory, not shell glob alone). All original proof/gen
raw/hash/patch/status/meta files keep their packet paths; only the 7 listed
worktree/index entries moved. Source/manifests unchanged (P1 `cdd69fe7`,
observer `79a3396c`, test `c567715d`, v5 manifest hash verified after ops).
No `.gitignore` workaround, no broad ignore flags.
