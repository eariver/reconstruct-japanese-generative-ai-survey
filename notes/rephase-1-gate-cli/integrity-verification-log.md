# Gate CLI successor — independent integrity verification log

- Recorded: **2026-09-27T18:44:55+09:00** (revised after root evidence review), author identity **General independent reviewer** (not Sol/Luna/Astra; no model-identity claim). Predominantly read-only inspection; one disclosed worktree-HEAD movement deviation — see §Deviations.
- Scope of head: successor `e4c82692abee6acedbba07815b0d74ccefb80a7e`, tree `bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`, parent `6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`; total diff from B `c04f32ad46109403e8a63faaa8394a90ee6b869c`.
- Fixture: `/tmp/jgas-rephase-gate-cli` (independent DB, inert origin `https://example.invalid/...`). No code/tests run. No commits/objects/refs created; no network/production/Actions. `git checkout` was used twice (worktree movement at `c04f32a`, then restored) — disclosed in §Deviations.

## Git identity (WSL db)

```
HEAD=e4c82692abee6acedbba07815b0d74ccefb80a7e
TREE=bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e
PARENT=6d87edd28a1be8893ca2ab67fed6e32e54b0de6c
branch=codex/rephase-1-gate-cli
status: ?? scripts/__pycache__/  ?? tests/__pycache__/   (tracked tree clean)
```

`git diff --name-status c04f32a e4c8269`:
```
M  scripts/survey_reader_surface_gate_v2.py
A  tests/test_survey_gate_cli_persisted_review_v2.py
```
`git diff --name-status 6d87edd e4c8269`:
```
M  tests/test_survey_gate_cli_persisted_review_v2.py
```

## Runtime blob identity (B vs 6d87edd vs e4c8269)

```
c04f32a:scripts/survey_reader_surface_gate_v2.py = 927ef1130b3e64f1ed3726ae3324cca28d82e875
6d87edd:scripts/survey_reader_surface_gate_v2.py = ea1eb652ab49eb479e17318712d84c318bfaf475
e4c8269:scripts/survey_reader_surface_gate_v2.py = ea1eb652ab49eb479e17318712d84c318bfaf475
```
=> runtime bytes identical between 6d87edd and e4c8269; only the test module differs (test-only successor).

Committed-blob sha256/size vs `candidate.json`:
```
scripts/survey_reader_surface_gate_v2.py
  git blob ea1eb652ab49eb479e17318712d84c318bfaf475
  sha256 78f136a0902617506ff572263b3bb08f97c7c1184c54dbe9735866fa0f4769b4  (candidate 78f136a0…: MATCH)
  bytes  84430  (candidate: MATCH)
tests/test_survey_gate_cli_persisted_review_v2.py
  git blob c839a2fef18f22ebe7bf347c8090a2dac74080e0
  sha256 1bf1451f494bbf0788d54894b4be572fb4c33e953b55dfb237ed41cc6f7cfa86  (candidate 1bf1451f…: MATCH)
  bytes  30300  (candidate: MATCH)
```

## Packet artifact identity (/mnt/d/.../notes/rephase-1-gate-cli)

```
increment-gate-cli.patch  sha256 29b7f187417df5f7524087c25a4f0931d4906ba3ffd502104baa59e8cd3cb726  34507 bytes   (candidate: MATCH)
changed-files/scripts/survey_reader_surface_gate_v2.py          sha256 78f136a0…6fa0f4769b4   (candidate: MATCH)
changed-files/tests/test_survey_gate_cli_persisted_review_v2.py sha256 1bf1451f…1cc6f7cfa86  (candidate: MATCH)
logs/candidate-relevant-tests-e4c8269.log  sha256 20831ed90e656e886443df9ee2cf71dc75393cca38fb7aab9a586746d8c672d6  (candidate: MATCH)
logs/candidate-relevant-tests-e4c8269.exit = "0\n"   (candidate exit 0: MATCH)
```
`setup/16-make-final-candidate-artifacts.sh` additionally re-verifies each disk copy with
`git hash-object` against the committed blob; its raw log `logs/16-...log` reports
`FINAL_ARTIFACTS_OK`, `SUBTEST_BLOCKS=16`, `RUNTIME_UNCHANGED_VS_6d87edd=yes`, `LOG_EXIT=0`.

Patch applicability: `git apply --check --stat` of `increment-gate-cli.patch` produced the
exact expected stat (2 files, 706 insertions, 12 deletions). **Caveat:** `--stat` per
`git apply --help` "Instead of applying the patch, output diffstat for the input. Turns
off 'apply'." So this invocation **did not apply** the patch and is **not** an
independent clean-baseline application proof; it is a display-only dry check. The scoped
review relies on the exact blob/sha256 diff verification above.

## Final raw test log binding

`logs/candidate-relevant-tests-e4c8269.log` header (runtime-derived, not hardcoded):
```
COMMAND=/tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v \
  tests.test_survey_reader_surface_gate_v2 tests.test_survey_gate_cli_persisted_review_v2
CWD=/tmp/jgas-rephase-gate-cli
HEAD=e4c82692abee6acedbba07815b0d74ccefb80a7e
TREE=bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e
PARENT=6d87edd28a1be8893ca2ab67fed6e32e54b0de6c
python=3.12.14
Ran 32 tests in 65.075s
OK
```
32 OK methods = 27 unchanged Gate methods + 5 dedicated CLI methods; no skips recorded;
numeric exit file = 0. 16 `subTest(` blocks, 18 executed subcases (one 3-way loop).

## Antecedent archive identity (attempts/6d87edd)

```
changed-files/scripts/survey_reader_surface_gate_v2.py          sha256 78f136a0…  (identical runtime)
changed-files/tests/test_survey_gate_cli_persisted_review_v2.py sha256 d5bd97f51847d6229d475dd0abc810ed6c5fe5925d579713c2972720d3eacc5f  (≠ successor)
increment-gate-cli.patch                                        sha256 f8593bdd410cd9c09ec9787dfe28e385734d0b9f7aded726cd614db38f961b1d
candidate-relevant-tests-6d87edd.log: HEAD=6d87edd… TREE=777c65e9… exit=0
```

## Isolation evidence (setup/02, logs/04)

Independent byte copy, `NO_ALTERNATES`, no `GIT_*` overrides, `.git` symlinks empty,
in-destination hardlinks (>1) empty, cross-DB inode intersection empty
(7037 vs 7037), inert origin, shallow boundary `774dd39a…` pinned; promisor
"missing blob" set inherited (not a copy defect).

## Deviations from strict read-only (disclosed)

This verification was **not** pristine read-only. The fixture worktree HEAD was moved:

- Command A (session clock ~18:40:46):
  `cd /tmp/jgas-rephase-gate-cli && git checkout -q c04f32a 2>/dev/null; git checkout -q codex/rephase-1-gate-cli 2>/dev/null; git apply --check --stat notes/.../increment-gate-cli.patch 2>&1 | tail -20`
  (the path used was the /mnt/d packet path; the initial relative path attempt failed and was not the one that produced the stat).
- Command B (session clock ~18:44:40):
  `cd /tmp/jgas-rephase-gate-cli && git checkout -q c04f32a 2>&1 | head; git apply --check --stat /mnt/d/.../increment-gate-cli.patch; echo APPLY_CHECK_EXIT=$?; git checkout -q codex/rephase-1-gate-cli; git rev-parse HEAD`
  → `APPLY_CHECK_EXIT=0` (rendered once as PowerShell `True`), final `HEAD=e4c82692abee6acedbba07815b0d74ccefb80a7e`.

Effect: the fixture worktree detached at `c04f32a`, then re-attached to
`codex/rephase-1-gate-cli`. **No ref was created/deleted/repointed; no commit or object
was created by the reviewer; no test was run.** The `git apply` calls never mutated the
worktree because `--stat` turns off apply.

Reflog and refs observed after the fact (read-only), consistent with the above:

```
e4c8269 HEAD@{2026-09-27 18:44:40 +0900}: checkout: moving from c04f32ad... to codex/rephase-1-gate-cli
c04f32a HEAD@{2026-09-27 18:44:40 +0900}: checkout: moving from codex/rephase-1-gate-cli to c04f32a
e4c8269 HEAD@{2026-09-27 18:40:46 +0900}: checkout: moving from c04f32ad... to codex/rephase-1-gate-cli
c04f32a HEAD@{2026-09-27 18:40:46 +0900}: checkout: moving from codex/rephase-1-gate-cli to c04f32a
e4c8269 HEAD@{2026-09-27 18:35:43 +0900}: commit: Correct Gate CLI tests: exact-manuscript binding, findings separation, oracles
6d87edd HEAD@{2026-09-27 18:25:33 +0900}: commit: Route persisted reader-surface review admission through strict Gate loader
```

Current identity/status (read-only, unchanged refs):
```
HEAD=e4c82692abee6acedbba07815b0d74ccefb80a7e
HEAD symbolic-ref = refs/heads/codex/rephase-1-gate-cli
status: ?? scripts/__pycache__/  ?? tests/__pycache__/   (tracked clean)
refs/heads/codex/rephase-1-gate-cli         e4c82692abee6acedbba07815b0d74ccefb80a7e
refs/heads/codex/rephase-1-increment-a      1a9649129d1745fed0b98db46ef15f014407e6fc
refs/heads/codex/rephase-1-increment-b      c04f32ad46109403e8a63faaa8394a90ee6b869c
refs/heads/codex/rephase-application-r2     d38f023ce200619f7f49ce17a348755f05e0e021
refs/heads/codex/rephase-freeze-b1b2        bf32edf98ba8f605169d7188bbc764de74ee4f6e
refs/heads/codex/rephase-r2-original        46472e41e353de56685e737fc91e85fcc2005312
```

No new mutations were performed to reconstruct this evidence; the reflog/refs above are
the actual post-hoc read-only observations.

No test or code was executed during this verification.
