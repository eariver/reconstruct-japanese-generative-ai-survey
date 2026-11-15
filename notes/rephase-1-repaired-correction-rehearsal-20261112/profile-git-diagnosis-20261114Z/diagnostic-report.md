# W34 guarded post-switch refusal — recorded-Profile Git object diagnosis

Scope: `astra-operation-resolution.md` §12 read-only local Git investigation only. Active repo:
`.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`.
No reconstruct Git/Production read, network, object restore, `hash-object -w`, commit/config/State/guard/source write, test, project import, or subagent. Commands used `GIT_NO_LAZY_FETCH=1` and `GIT_TERMINAL_PROMPT=0` with no `GIT_DIR`/`GIT_WORK_TREE`/index/object-directory/alternates/common-dir override. Raw outputs are in this packet.

## 1. Bottom line

The adopt did **not** fail because of a malformed Git batch header, a wrong OID, or a wrong tree entry. The recorded commit `cc1c…` correctly lists the W34 Profile path as blob `155b78cfd588eb9300349e4568ee7065ae498477`; that **blob object is absent from the local partial/promisor object DB**. `git cat-file --batch` therefore returned:

```text
155b78cfd588eb9300349e4568ee7065ae498477 missing
```

The helper at `scripts/survey_research_authority_v2.py:739-740` expects exactly three header tokens and reports any other shape as `recorded-commit batch header mismatch for: <path>`. A `missing` response has two tokens, so the message names a header mismatch although the actual condition is a missing object. The refusal is fail-closed and correct; the wording is the only helper-level defect observed.

An **exact local recovery candidate exists**: `.rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/production-profile.json` hashes to the expected Git blob `155b78cf…` (sha256 `a6e3eb30…`, 2371B). It was not restored or written into any object DB. A second-level contract question remains because that capture is the **baseline** profile, whereas the checkpoint/request/live profile bind a different, amended profile.

## 2. Observed failed state

- HEAD `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`; tree `ed2dc4ddd4a9486ccc9d0944bbd48653199b2485`; shallow `true`; refs only `refs/heads/codex/rephase-candidate-recovery b40de600…`; remote `https://example.invalid/rephase-candidate-recovery.git` (inert).
- Guard `sources/2026-W34/orchestration/v2/acceptance-revision.guard.json` sha256 `ddae0b81…`, nonce `387ee54f65a813f8`, before `d7acd29b…`, expected-after `a8586351…`, work `cc1c…/ed2dc4…`, recorded_at `2026-11-14T06:53:43Z`.
- LIVE State `sources/2026-W34/production-state.json` sha256 `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d` — expected-after class E, lifecycle still `EVIDENCE_REVIEWED`, Human pending, same-record triplet to the R2 checkpoint `73ab28ea…`.
- Checkpoint `…/w34-repaired-20261112-r2/checkpoint/record.json` sha256 `73ab28ea…`, implementation commit `cc1c…`; R2 manifest `867eba96…`/438583B; decision `09b2feae…`/4030B.
- Failure: `postread FULL adopted-graph validation failed (INDETERMINATE): recorded-commit batch header mismatch for: sources/2026-W34/production-profile.json`.

## 3. Exact failure path and helper semantics

The requested symbol `_verify_recorded_epoch` does **not** exist in the selected source. The relevant helper is:

- `scripts/survey_research_authority_v2.py:639-799` — `_verify_own_epoch_commit`.
- Called at line 979 from `_verify_adopted_graph_full`.
- Reached in adopt through `scripts/survey_prearchitecture_acceptance_v2.py:1102` (`write_cleanup_completion -> low._verify_adopted_graph_full`), after State triplet switch and before guard release.
- The helper body is byte-identical between e84 and cc1c (`sha256 207c3a19…`), so this is not a cc1c regression; the first W34 adopt in this runtime newly exercised it.

Relevant behavior:

1. `request.profile_ref["path"]` is added to the needed path set (line 695).
2. `git ls-tree -r <commit> -- <needed>` must contain every needed path as a 100644 blob (lines 696-714).
3. Unique blob OIDs are read in one `git cat-file --batch` call (lines 715-730).
4. Every response header must be exactly three tokens, with the first equal to the requested OID (lines 734-740). A `<oid> missing` line is two tokens and raises “batch header mismatch”.
5. The commit Profile bytes are parsed only for `research_profile`/`publication_profile` names (lines 773-784); Contract8 is recomputed from the **commit's** config and contract files (lines 762-793). The helper does **not** compare the commit Profile sha256 to `request.profile_ref.sha256` (`2a8c3089…`) or to checkpoint `profile.sha256`.

The helper was reproduced without importing the project: the exact needed path list (90 paths, 85 unique objects) reads `84 present / 1 missing`, batch exit `0`. The only missing entry is the W34 Profile. Raw: `needed-ls-tree.raw.txt`, `needed-batch-stdout.raw.bin`, `needed-batch-parsed.json`, `cat-file-*`.

## 4. Recorded vs live Profile

| Item | Git blob OID | sha256 | bytes |
|---|---|---|---|
| Recorded commit tree (`cc1c`, also `774`, `409b292`, `480`, `e84`, `b40`) | `155b78cfd588eb9300349e4568ee7065ae498477` | `a6e3eb3006dde95da008876486cbfc7fdce75f507f7efcd6b0fcaba5e154b21a` | 2371 |
| Local object availability | **missing** (`cat-file -e` exit 1; `-t` exit 128) | — | — |
| Live worktree | `c2990d4fcb81f71a6afac0b14bf93c5b2d9ebb5e` | `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1` | 2371 |
| Index / HEAD entry | `155b78cf…` | (recorded) | 2371 |

`git status` shows `M sources/2026-W34/production-profile.json`. The live file was already modified before setup and intentionally preserved (setup report: `M`, material diff `UNCHANGED-OK 2a8c3089 vs 2a8c3089`). The only byte differences between the exact baseline capture and the live file are the embedded contract hashes:

```text
-pipeline_contract_sha256 e6ae2637fe2e… -> 3adfbda22131…
-quality_contract_sha256   3a36dceaaae9… -> b5b955d524fb…
```

Because the helper uses only profile names and recomputes Contract8 from the commit config/contract files, restoring the baseline blob would satisfy the mechanical check even though the recorded commit's Profile bytes are not the adopted live Profile bytes. That is the precise contract question for root; it is not resolved by the missing-object diagnosis alone.

## 5. Source of the missing dependency

- The runtime is a shallow/promisor partial DB copied from the b40 recovery material. Every reachable commit tree (`774`, `409b292`, `480`, `e84`, `cc1c`, `b40`) references the same baseline Profile blob `155b78cf…`.
- The baseline blob was never materialized in the copied object DB. The b40 archive contains the partial DB plus materialized files, but **no** `sources/2026-W34/production-profile.json` file and no object with this OID (the active `b40` DB also fails `cat-file -e`).
- The worktree Profile is a separate amended file (`2a8c3089`/`c2990d4f`), modified before the setup commit. Setup installed the exact 773 source/test files and committed only six intended paths; its material check hashed the amended Profile but did not test recorded-commit Profile object reachability. The setup review's “partial-DB failure properly qualified” note concerns other paths and did not cover this blob.
- Therefore the immediate cause is the pre-existing partial-clone object gap, surfaced by the recorded-commit own-epoch proof on the first W34 adopt — not a bad OID, bad tree entry, or cc1c source change.

## 6. Exact local recovery candidate

Found and verified read-only:

```text
/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-inputs/
  774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/production-profile.json
```

- sha256 `a6e3eb3006dde95da008876486cbfc7fdce75f507f7efcd6b0fcaba5e154b21a`
- Git blob `155b78cfd588eb9300349e4568ee7065ae498477`
- 2371 bytes — **exact expected OID and bytes**

Provenance:

- `notes/rephase-1-contract/inputs.json` records exactly this path, sha256, blob, and byte count at fixed `774dd39a…`.
- `notes/phase-4f/inputs.json` and `notes/rephase-1/evidence.json` record the same identity.
- `.rephase-1-inputs/774dd…/tree.json` entry: `mode 100644`, `type blob`, `sha 155b78cf…`, `size 2371`.
- `notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z/material-sufficiency.md` says this capture was reused and verified as blob `155b78cf…`, 2371B.

No other exact copy was found: 544 local Git DBs (542 under `.rephase-1-editorial-runtime` plus 2 under `.rephase-1-inputs`/`.phase-5-inputs`) have zero hits for `155b78cf…`; `/tmp/opencode` has no Git DB; the b40 tar lacks the file; all runtime Profile-named copies (four runtimes plus the pre-stage snapshot) are the live amended blob `c2990d4f…`, which must **not** be substituted. The `.rephase-1-inputs/774dd…` capture itself is a plain worktree/tree.json snapshot with no `.git`.

This candidate was identified, not restored. `git hash-object -w`, object-store copy, State/guard edits, and a retry remain unauthorized by §12.

## 7. Normal resume predicates — why resume cannot pass

`resume_revision` delegates to `resume_bound_attempt`:

- Current class is **E** (expected-after `a858…`), guard present.
- Resume verifies guard planned checkpoint sha `73ab…` and retention rows against the manifest, then executes `write_checkpoint_as_planned -> clear_remaining_exact_slots -> write_cleanup_completion -> release_guard`.
- `write_cleanup_completion` reloads LIVE State and calls `low._verify_adopted_graph_full` at line 1102, which calls `_verify_own_epoch_commit` at line 979 and hits the same missing blob.
- If the guard were absent, `require_completion_consistent` also calls `_verify_adopted_graph_full` (line 1018) and fails the same way. Readback `resolve_research_authority` calls it at line 1073 and also fails.

So no normal resume/readback/ALREADY_ACTIVE path can succeed while `155b78cf…` is absent. A new prepare/adopt at the same recorded commit would fail at the same own-epoch check; only exact object restoration or a new source epoch/expected-head can change the outcome.

## 8. SP risk (separate gap)

The SP prepared candidate is **not** object-recoverable in the same sense:

- `sources/SP-efficient-llm-2026/production-profile.json` is absent from the `cc1c`, `e84`, `480`, and `b40` trees, absent from the index, and has zero `git log --all --` entries. The SP worktree has **2,523 untracked files** under that directory.
- SP prepared manifest pins implementation `cc1c…`; its request and State bind Profile `aff05fd5…`/13748B (Git blob `9251f487…`), but no commit contains that path.
- SP adopt would therefore fail, before any batch read, at `recorded-commit tree lacks required path: sources/SP-efficient-llm-2026/production-profile.json` (`survey_research_authority_v2.py:709-711`), unless a new source commit includes the SP tree.
- The authorized c8 capture (`notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z/DATA.production-profile.json`) is blob `37be89b9…`, sha256 `22f2e822…`, 13748B, and differs from the live SP Profile only in `pipeline_contract_sha256` (`ee897962… -> 3adfbda2…`). Neither SP blob exists in any probed local Git DB, and commit `c8d0ecc1…` is not present locally.

SP therefore needs a root decision on (a) a source commit/epoch that contains the SP tree and (b) whether the live amended SP Profile or the authorized c8 capture is authoritative. It cannot be fixed by restoring the W34 object.

## 9. Conclusion

- **Missing dependency:** baseline fixed-774 W34 Profile blob `155b78cfd588eb9300349e4568ee7065ae498477` is absent from the local partial/promisor object DB; the commit tree and expected OID are correct.
- **Exact local recovery:** only `.rephase-1-inputs/774dd39a…/sources/2026-W34/production-profile.json` matches the expected Git blob/sha256/bytes. It is a verified capture, not a fake equivalent. Do not use live profile `c2990d4f…`.
- **Before recovery:** resolve whether the recorded commit may carry the baseline Profile (old embedded contract hashes) while the checkpoint/request bind the amended live Profile. The helper checks names and commit-derived Contract8 only; that is a root/contract decision.
- **SP risk:** independent missing-tree/source-epoch gap; SP adopt is blocked even if W34 recovers.
- No object restore, commit, config, State, guard, source edit, resume, readback, adopt, test, import, or network action was performed.

## 10. Packet raw inventory

- `needed-paths.txt`, `needed-ls-tree.raw.txt`, `needed-batch-stdout.raw.bin`, `needed-batch-stderr.raw.txt`, `needed-batch-exit.txt`, `needed-batch-parsed.json`
- `cat-file-type.*`, `cat-file-exists.*`, `cat-file-batch-check.*`
- `repo-identity.raw.txt`, `refs.raw.txt`, `remotes-config.raw.txt`, `git-version.raw.txt`
- `tree-profile-entries.raw.txt`, `index-profile-entries.raw.txt`, `status-profile-summary.raw.txt`
- `profile-oids.raw.json`, `w34-profile-copies.raw.txt`
- `expected-capture-tree-entry.json`, `expected-vs-live-w34-profile.diff.txt`
- `c8-sp-capture-manifest-entry.json`, `c8-sp-vs-live-sp-profile.diff.txt`
- `diagnostic-machine.json`
