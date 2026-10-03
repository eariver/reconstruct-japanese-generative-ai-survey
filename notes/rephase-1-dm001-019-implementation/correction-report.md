# DM-001/019 correction return — 490414c CHANGES_REQUIRED → ff6c67f

2026-10-03. Correction within the same unit per `correction-task.md` and the
author-independent review. `490414c` and all first-run evidence preserved
(parent/history). Same 3-path budget. No agents, Production, network,
reconstruct Commit/Push, parent-witness rerun, or old-script reuse.

## 1. New candidate

- **`ff6c67f68e12b3093901248219f2de2872e54d73`**,
  tree **`664c796da983f322f1d244500d8b9b88198b772a`**,
  direct parent **`490414cef5be71d3b373171d8abeb0674b1f1c71`**
  (b40 ancestry intact). Branch `codex/dm001019-freeze-implementation`,
  normal single correction commit, no amend/reset/hook bypass, tracked-clean.
- Changed paths (only): `scripts/survey_publication_v2.py`
  (blob `30a42fee…`), `scripts/survey_profiled_freeze_v2.py`
  (`433c6096…`), `tests/test_survey_dm001_019_freeze_equivalence_v2.py`
  (`4f49114c…`, now 34 methods). Copies verified against committed blobs.
  `git diff --check` exit 0; public `build_freeze` signature still unchanged.

## 2. Correction → finding → test matrix

| Finding | Runtime change | Proving test(s) |
|---|---|---|
| F1 nested outputs | Preflight rejects either output equal/ancestor of the other pre-write/mkdir, both directions | `test_l9_…` both nestings, no target/parent created |
| F1 lexical `..` | `_lexical_repo_path` rejects any `..` segment before normalization | `test_l9_…` dotdot case, nothing created |
| F1 consistent target | Manifest builder receives `(freeze_sha, normalized_freeze_target)`; payload refs and install share one target | L-2/W-3b byte equality unchanged |
| F2 collision revalidation | `FileExistsError` branch does lstat/type/symlink/ancestor rechecks before read (no FIFO block) | identical-byte symlink refusal; FIFO refusal unit |
| F2/F6 post-mkdir | `_ensure_parent_dir` rechecks ancestors after mkdir (cheap narrowing, no global claim) | ancestor-symlink matrix case still green |
| F3 close error | Close failure always raises `ValueError`; verified-complete bytes retained with explicit failure + safe retry; best-effort fd release | real-close-then-raise injection, freeze + manifest variants; retry byte-equal |
| F4 PDF alias | `candidate["pdf"]` in protected input set (spelling + inode) | PDF-as-target alias refusal (pre-write, not incidental) |
| F4 wrapper State | Wrapper guards fixed outputs against the State path; State bytes join the install snapshot | snapshot assertions (direct overlap untriggerable via fixed paths; documented) |
| F5 duplicate | Second `_write_immutable` deleted; single copy serves all legacy producers (behavior identical) | publication 8/8 + profiled 4/4 green |
| F5 narrow API | `prepare/build_freeze_payload/build_manifest_payload/preflight/install` privatized (`_…`); slug authority stays the single public helper pair; no unvalidated tag-write API | suite updated to private names; no external caller |
| Item 6 snapshot | Prepare snapshots 9 authority files; recheck before first write, before second install (split `_install_freeze_target/_install_manifest_target`); wrapper merges State snapshot | drift-before-first-write (no outputs); drift-before-second (Freeze retained) |
| Item 7 lstat cleanup | `_remove_owned_partial` uses lstat; symlink/identity-change/non-prefix residuals preserved with explicit errors | identity-replacement, non-prefix, symlink units |
| Wrapper mixed (real) | — (honest path, see §3) | `test_w4c_…`: real valid State + approved C1, C2 installed at wrapper path → real State-provenance refusal, State/inputs/targets byte-proved unchanged; prepare-level exact rejection kept |
| Legacy positive | — | `test_w1c_…`: alt-path canonical VISUAL + valid legacy at hardcoded path; both builders succeed byte-equal, legacy untouched |
| Reformat bytes | (existing `_existing_compatible_bytes` semantics, now covered) | L-10 canonical + W-7 wrapper: reformatted Freeze kept byte-exact, Manifest references actual SHA; reformatted Manifest preserved |
| Weekly equivalence | — | `test_w2b_…`: Weekly wrapper→reset→canonical byte-equal |
| No-write snapshots | `_snap_state_targets` helper | W-1 (State provably unrewritten), all W-4 subcases, nested/alias cases |
| Workflow env | `GIT_NO_LAZY_FETCH=1`, `GIT_ALLOW_PROTOCOL=file` added to extraction runner env | S-2 re-green with constrained env |
| Malformed target | (pre-existing divergent refusal, now pinned) | invalid-JSON target subcase in L-6 |

## 3. Honest corrections to the first report

- Initial run1 was **not exclusively harness-side**: the directory-target
  specificity failure prompted a **runtime preflight reorder** (divergent/
  type checks before the conservative Manifest-without-Freeze refusal),
  shipped in 490414c. The other two run1 items were oracle-side. Raw run1
  logs stay intact; this corrects `implementation-report.md §5`, it does
  not rewrite history.
- `.gitattributes` packet `-text` rule is Astra's change, not mysterious
  Human work; left untouched.
- No per-method HEAD pinning claimed before; correction runs now carry
  per-module HEAD/tree/parent/source-hash/argv/env/exit headers
  (`evidence-corr-…/10-runs/*.log`, `STATUS_CLEAN=True`).

## 4. Final exact-head results (corrected `ff6c67f`)

New module **34/34 OK**; affected publication 8/8, profiled 4/4,
freeze-stage 8/8 — **54 methods, 0 failures/skips**, all with header-bound
logs at the committed HEAD. Parent witnesses not rerun (parent code
unchanged; correction does not affect their validity).

## 5. Limitations

- Manifest-without-Freeze compatible case still fails closed by documented
  conservative disposition (tested), not auto-resumed.
- Close-fault injection patches `os.close` at the real boundary (real close
  first, then raise; best-effort release; no leaked fd in test path). No
  buffered-flush test exists — none is claimed (writer uses unbuffered
  `os.write` only).
- L-8(a) read-only-dir refusal assumes non-root (uid 1000).
- Cross-process races narrowed (FileExists revalidation, post-mkdir
  recheck), not globally eliminated — as selected, no CAS/lock claim.
- Retrospective full flow, DM-003/004/016/017/018/020, build transfer,
  findings transport, whole-candidate audit remain out of scope.
- Restored DB cannot `git log` (parent history absent by delta design);
  parent linkage verified via commit header instead.

## 6. Packaging and offline restore

- `evidence-corr-…/20-packaging/`: enumerated 7-object `successor-pack.pack`
  (42,089 B, `pack-objects` over explicit `rev-list --objects 490414c..ff6c67f`,
  no history hydration), machine-generated `successor-manifest.json`
  (HEAD/tree/parent, 3 file modes+blobs+worktree SHAs, patch bytes/hash),
  `changed-files/` copies + SHA256 list (all 3 match committed blobs).
  Label: **patch+object delta, not a full backup**; parent portable snapshot
  (`candidate-partial-b40de60.tar.gz`, SHA256 `faf6792f…`, untouched) is the
  stated prerequisite for full history.
- `30-restore/restore_successor.py` (new fail-closed, absent-destination
  gate, hash gates, no old scripts): first attempt with `--strict` failed
  (`object of unexpected type` — delta links dangle without parent history;
  log preserved as `restore-run-attempt1-strict-linkage.log`), corrected to
  strict-less unpack with exactness enforced by gates instead.
- Clean restore into new absent DB: **RESTORE_RESULT=OK** — exact HEAD/tree,
  parent linkage `490414c`, all 7 objects present, all 3 blob SHAs + exact
  file bytes match, no remotes, no alternates, fresh object-store inodes.
  Identity/inventory verification only; no suite rerun in the restored DB.

Root review, then the same independent reviewer may resolve findings. Whole
candidate remains NOT_READY; no next unit before the Human Commit Point.
