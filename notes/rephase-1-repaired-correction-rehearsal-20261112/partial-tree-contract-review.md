# Partial-tree contract review — `write-tree --missing-ok` for artifact-only epoch (read-only)

Scope: root §15 + `artifact-epoch-20261114T123542Z-execution-report.md` (captured failure only) + `git write-tree --help` doc. Separate agent tests fixture; this review declares no method success before experiment. No active Git write/runtime/test/network/Production/reconstruct-readback/subagents; no source changes.

## 1. Failure preserved

- Index staged EXACT 2: `sources/2026-W34/production-profile.json` (`2a8…`/`c2990d4f…`), `sources/SP-efficient-llm-2026/production-profile.json` (`aff05…`/`9251f487…`); HEAD still `cc1c7fd1…`, no new tree/HEAD.
- Normal `commit` refused: `invalid object 100644 b797783c401a3d7b5dbdfcb2ef63d7b1d6295740 for 'sources/2026-W34/architecture-review-attention-v2.json'` ×2 + `Error building trees`. Cause is pre-existing index entry for unrelated missing blob (inherited 26k partial-DB gap), not the 2 staged Profiles. Index kept staged per STOP; no reset/hydration/amend/retry.

## 2. Contract question

`git write-tree --missing-ok` per local doc “disables check that objects referenced exist”. Narrow use here would be: preserve every unchanged old-tree OID ref (including missing `b797…` absence-preserved), update only the 2 staged Profile entries, then normal `commit` (parent `cc1c`, hooks run, process identity). This does NOT forge ancestry (parent stays `cc1c`), drop tracked history (all other entries byte-identical), or hydrate globally — IF constrained below.

Separate requirements:

- **Tool-commit data requirement (strict):** `_verify_own_epoch_commit` + `_verify_adopted_graph_full` need all ~90 needed objects (contract files + mapped codeset + request Profile) actually readable via `cat-file --batch` (3-token exact). `W34 155b78cf…` now present after §13 fill; new-epoch SP check will need `c2990d4f…` + `9251f487…` + all config/schema/tool blobs present. `--missing-ok` must NOT mask a missing needed object; needed-set readability stays strict, no memory/in-memory override.
- **Global hydration (not required):** unrelated missing blobs (e.g. `b797…`, other 26k) need not be present for the artifact epoch or for W34 `cc1c` own-epoch readback; tree may reference them absent-preserved under partial/promisor model with lazy-fetch disabled.

So `--missing-ok` is contract-consistent ONLY as tree-construction tolerance for unrelated absent objects, not as proof bypass.

## 3. Narrow acceptance conditions (active operation, if root authorizes after fixture evidence)

1. Index diff is EXACT 2 paths above, nothing else staged/unstaged for commit; `diff --cached` names verified.
2. New tree: all other entries identical to `ed2dc4…` (same mode/OID/path); only the 2 Profile OIDs change to `c2990d4f…`/`9251f487…`; old missing OIDs (incl `b797…`) preserved as refs, not dropped/substituted.
3. Commit: parent exactly `cc1c…`, normal hooks (no bypass/empty/amend/config/HOME change), process-scoped identity, message records artifact-only scope.
4. Unchanged: source773 `a7e40c…`, States `a858…`/`180db8c3…`, CPs `73ab28ea…`/`1233b1f6…`, W34 `cc1c`-anchored readback (`PREARCH/triplet true/completion true`) re-verified after.
5. Needed-object reads for new epoch verified actually readable locally (not merely tree-present); no `--missing-ok` reliance for needed set.

## 4. If method fails

STOP, preserve index/raw. Return to root before any broader fetch/full restore. No empty-root commit, subset tree, forged IDs, `commit-tree` substitute, hook bypass, broad hydration, reconstruct/Production access, or automatic retry.
