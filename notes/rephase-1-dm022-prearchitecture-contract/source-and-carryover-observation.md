# DM022 pre-Architecture — source-and-carryover observation (READ-ONLY)

Date: 2026-10-26 UTC. Human HEAD `d9fffb2` (after `f84fcf5`), branch `main`, `origin/main` same.
Scope: metadata/source availability check for new DM022 design unit ONLY.
Method was read-only: `git rev-parse/log/status/ls-files --stage/ls-tree/diff-tree/diff`,
filesystem `ls/cat/find`, `sha256sum`, stdlib `hashlib/json` file hashing.
No source/test/build/restore/network/Git mutation/cleanup/stage/commit.
No `submodule update/deinit/rm/config/cleanup`, no `git config` writes, no child-repo writes.

AGENTS.md permissions observed: fixed production baseline is read-only; ordinary
candidate/reconstruct commit/push is Human-owned; stop at Human Commit Point; this unit
writes ONLY the new files in `notes/rephase-1-dm022-prearchitecture-contract/`.
Prior packet/entries untouched. No remediation authorized or performed.

## 1. Root HEAD cleanliness (qualified)

- `git status --porcelain=v1`: 55 lines, all ` M` on gitlink paths under
  `notes/rephase-1-versioned-renewal-implementation/resume-20261025/*/raw/*/fork-*`
  (plus 2 `tmp-healthy-*` gitlinks). No `?` untracked lines outside gitlinks reported
  in this output; no staged (`M `/`A `) lines (`git diff --cached --raw` count 0).
- Submodule-aware breakdown (read-only flags, no config change):
  - `--ignore-submodules=all` → 0 status lines (HEAD tree otherwise clean).
  - `--ignore-submodules=untracked` → 1 line remains.
  - `--ignore-submodules=dirty` → 0 lines.
  - `git diff --raw --ignore-submodules=none` → 55 lines, every line same-SHA
    both sides (e.g. `e211e6e e211e6e M`); default `git diff --raw` shows only 1
    (the tracked-dirty child below).
- Meaning: all 55 recorded gitlink SHAs are unchanged in worktree vs index/HEAD;
  54 children carry untracked-content-only dirt, 1 child carries 1 tracked-file
  modification plus untracked content (representatives §3). This is a worktree-dirt
  qualification, NOT a HEAD-tree mismatch. Unknown/user work preserved; nothing cleaned.

## 2. Gitlink inventory (read-only count)

- `git ls-files --stage | grep -c '^160000'` = **55**.
- `git ls-tree -r HEAD | grep -c '^160000'` = **55** (same set).
- `.gitmodules`: absent (`ls: cannot access '.gitmodules'`). These are bare
  mode-`160000` gitlink entries WITHOUT submodule configuration, not configured submodules.
- 5 unique recorded SHAs across 55 paths:
  - `48515237ddc7e8e124c514c7433bea660138a884` (8 paths: boundary + current-dated failure cases)
  - `05e32ecd8dcad2d645051c717e1314c418cec4ae` (1 path: depth32-legacy)
  - `e211e6e07a84991d8e6c9f05e5c3dc4d844abe58` (35 paths: weekly fault-resume family)
  - `ce90246b907c86e9bdeb930dec0e83a5637f2805` (3 paths: typed33 family)
  - `37d9d5caf7aa555828d61419fe6be0fcb21c2a45` (8 paths: orphan-intent family)
- Full sorted path list was captured to `/tmp/opencode/stage-gitlinks.txt` (workspace-local
  scratch, not part of the unit record).

## 3. Which Human commit added the entries

- `git diff-tree --raw d9fffb2`: 55 lines `^:000000 160000 ... A` (true gitlink adds;
  an initial naive `grep 160000` overcounted 58 because 3 added `.sh` paths contain
  the literal string `T160000Z` in their filenames — corrected by anchoring on the mode field).
- Parent `f84fcf5`: `git ls-tree -r f84 | grep -c '^160000'` = 0, fork-path count 0.
- Therefore **Human commit `d9fffb2` added all 55 gitlink entries**; parent had none.
- `d9` also added the surrounding `longform-integration-repair/fork-prepreview-*`
  regular files and `p3s-runtime-correction/*.sh` (non-gitlink), per
  `git diff-tree --name-only -r d9` (87 fork/tmp-name paths total, 55 gitlinks + 32 files).

## 4. Representative child gitdir identity/status (explicit limited scope)

`.git` in checked children is a real directory (not a gitfile pointer). No writes made.

REP1 (untracked-only example):
`.../boundary-verification/raw/case-alias-samleaf-20261025T000000Z/fork-alias-samleaf`
- child `git rev-parse HEAD` = `48515237ddc7e8e124c514c7433bea660138a884` — matches recorded gitlink.
- child `git status --porcelain` = 10 untracked `??` (architecture-approval/review/summary/v2,
  architecture-v2, raw/, selection-v2, sources/, surveys/, views-accepted/, views-input/); 0 tracked modifications.
- child `git remote -v` = `origin https://example.invalid/versioned-renewal-faultresume-current-weekly.git` (inert example.invalid, fetch+push same).
- `.git/objects/info/alternates`: absent. `.git/commondir`: absent.

REP2 (tracked-dirty example — the single `git diff --raw` default-visible entry):
`.../failure-resume-verification/raw/case-drift-tool-20261025T150400Z/fork-drift-tool`
- child HEAD = `e211e6e07a84991d8e6c9f05e5c3dc4d844abe58` — matches recorded gitlink.
- child status = 11 lines: ` M scripts/survey_quality_v2.py` + same 10 untracked classes as REP1.
- remote = `https://example.invalid/versioned-renewal-faultresume-weekly.git` (inert).
- alternates absent (commondir not separately rechecked on REP2; covered in all-55 sweep below).

All-55 sweep (read-only, no per-file content comparison):
- `git -C <each-path> rev-parse HEAD` vs recorded stage SHA: **55 checked, 0 mismatches**.
- `.git/objects/info/alternates` and `.git/commondir` existence check across all 55: **none found**.
- Root `.git/objects/info/alternates`: absent. Root gitdir is
  `/home/eariver/git/reconstruct-japanese-generative-ai-survey/.git`.

## 5. Fixture-object independence vs root sharing (explicit scope limit)

Checked ONLY: child HEAD equality (§4), inert `example.invalid` remotes (2 representatives +
proof-copy §6), `alternates`/`commondir` absence (all 55 + root + proof-copy), separate
absolute gitdirs (root vs one proof-copy; child `.git` dirs are path-local directories).
**Did NOT perform any full object-store inode/hardlink comparison** (no `find -samefile`,
no all-object `ls -i`, no pack-by-pack audit). Therefore: no claim is made that fixture
objects are fully independent of root object storage at the inode level, and no global
"no sharing" certification is offered. The observed mechanism (separate gitdirs, no
alternates file) is consistent with, but does not prove, object independence.

## 6. `no Git DB in packet` — scope correction (do not overgeneralize)

- The `packet-find-git empty / no .git inside packet` claim in
  `notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-20261025T205432Z/`
  (`commands.log`, `independent-final-packaging-review.md:76`, `README.md:22`) covers
  **that source-packaging packet directory only** (`find $PACKET -name .git -print` empty).
- It does NOT cover: (a) the ignored PACKROOT
  `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/`
  whose `proof-copy/.../.git` and `gen-copy/...` DO exist; (b) the 55 `resume-20261025/...`
  fork-* children which DO contain `.git/` directories (§4). Do not cite the packet claim
  as global backup evidence.

## 7. Carryover qualification (portable commit vs working bytes)

A portable clone/fetch of Human commit `d9fffb2` carries ONLY the 55 gitlink SHAs
(manifested in `ls-tree`), plus the regular files committed alongside them. It does
**not** carry: child `.git/` object bytes, child untracked files (the ~10 per-child
classes in §4: architecture JSONs, raw/, sources/, surveys/, views-*/), or the 1 tracked
worktree modification (`survey_quality_v2.py` in REP2). Any downstream user that clones
only the reconstruct HEAD must treat those child contents as absent/unauthored until
independently provided; the gitlink SHA alone is a pointer, not the authority bytes.

## 8. Final-93 source pin availability (strict no-overwrite observed)

No clone/restoration was needed; the applied proof source is AVAILABLE in place.

- Proof-copy: `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  - `.git/HEAD` = `409b292756dd1277b9dfae87679934c0d2ce251c` (matches expected HEAD409).
  - `git -C proof-copy rev-parse HEAD HEAD^{tree}` = `409b292…` / `8ce36998…`
    (matches expected tree8ce; root reconstruct DB does NOT contain 409 — expected,
    verified read-only `rev-parse 409^{tree}` fails in root).
  - `find -path */.git -prune -o -type f -print | wc -l` = **742**, `__pycache__` count 0.
  - proof gitdir absolute path is under proof-copy (own GitDir ≠ reconstruct root);
    remote `https://example.invalid/rephase-candidate-recovery.git` (inert); alternates absent.
  - gen-copy sibling also present (existence only; no content audit this unit).
- Saved patch: `notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-20261025T205432Z/complete-versioned-renewal-409.patch`
  - fresh `sha256sum` = `f898d33bfe6904fd29063d5a1ff462588d11f227f5aab6a3a2d505614941da2a`, 3423014 B — matches AGENTS.md pin.
- Manifest: `.../complete-versioned-renewal-manifest.json`
  - fresh `sha256sum` = `d488c6ee48b7cfa781f39905c4f08a61561e7bd02b234d2c60a6a1e93953497c`, 43355 B — matches AGENTS.md pin.
  - fields: `head 409b292…`, `head_tree 8ce36998…`, `delta_count 93`, `files 93`,
    `tracked_modified 40 / untracked_new 53` (40M53A), `intended_final 742`,
    `scope: scoped 689 tracked at HEAD + 53 absent → 742`.
- Fresh stdlib-`hashlib` rehash (read-only, no project imports) of 5 proof-copy files vs manifest `sha256` — **5/5 match**:
  - `scripts/survey_versioned_renewal_v2.py` (HIGH) `3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b`
  - `scripts/survey_versioned_renewal_history_v2.py` (H) `74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d`
  - `scripts/survey_versioned_renewal_source_v2.py` (S) `2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb`
  - `scripts/survey_agent_control_v2.py` (delta agent) `a32072e7b4f239417bfd855850bdcbb4c8d700f29805afa9e0d502969f06a2b9`
  - `scripts/survey_evidence_v2.py` (delta evidence) `a57bce69f9a295273fff6059cfd66da170f80987815816b8523a24a3a34fce6f`
- Explicit scope: full-93/742 rehash NOT performed this unit (fast stdlib path was
  available but not exercised beyond the 5 above); this observation does NOT recertify
  the prior all-entry guard. No source identity mismatch found in what was checked, so
  the independent complete code in the final93 patch is unaffected by the §7 gitlink
  carryover qualification. Intended overlays beyond the 93 (missing26309/bulk31466/
  runtimeTeX, 5 apply whitespace diagnostics) remain as previously qualified, unaltered.

## 9. What is NOT claimed / no new workflow

- Facts only; no remediation, no cleanup/stage/commit, no submodule operations.
- No new blocking approval workflow is introduced by this note; DM021+022 OPEN,
  whole NOT_READY, and prior evidence bounds carry over unchanged.
- Root unit documentation should use this note; prior packet/entries were not edited.
