# DM003-W1 independent implementation review (author-independent, read-only)

Scope: DM003-W1 ONLY. Reviewer did not author code/tests/design; no agents,
no runtime/test/probe execution, no network, no Git ref/checkout/config
changes. Read-only hash/Git/pack/tar inventory only with
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`.
No root/worker/source edits. No full audit, no adoption, whole candidate
remains NOT_READY.

Verdict: **BOUNDED_PASS for W1 only** — narrow approved-Preview agreement
repair is correctly implemented and meaningfully verified within stated
synthetic bounds. No code/test blocker. Qualifications below are
nonblocking for this local unit; they limit what the packet proves and
correct one README overclaim.

## 1. Candidate identity and isolation (verified read-only)

- Parent `222a37e9ee2aa96724a491f2c04c2583a86b9650`,
  tree `dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`,
  parent-of-parent `ff6c67f68e12b3093901248219f2de2872e54d73`.
- Final `e1705b7fed01369767ab9d827c0360117d54aa1f`,
  tree `3d21322587b9e4d3d05d7ae9ef66fbd1d74d3557`,
  parent `222a37e9ee2aa96724a491f2c04c2583a86b9650`,
  branch `codex/dm003w1-preview-agreement`,
  `status --porcelain` clean, origin inert `https://example.invalid/...`,
  shallow `774dd39a951c9ac3818e83dfffd4c7666efb0a20` only,
  no `.git/objects/info/alternates`.
- Original `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z` and restored
  `/tmp/opencode/jgas-dm001019-chainrestore-20261003T150500Z/candidate-partial-b40de60`
  both still at `222a37e`, clean; read-only inputs preserved.
- Reconstruct HEAD `a375eb9c1213b89f66cd5449cca8126fd1c60b7c`; only
  `.gitattributes` modification is root-owned byte-protection for this packet
  plus new untracked W1 evidence. No production source change.
- Own-DB independence: impl `.git/objects` dir inode differs from restore
  `.git/objects` dir inode; impl holds loose `e1/705b7...` commit while
  restore holds `e1705b7` in packs (`packs:4` vs impl `packs:2`); no
  alternates/hardlink sharing observed; both remotes inert.

## 2. Actual diff — exactly the authorized 3 paths

`git diff --stat 222a37e..e1705b7`: 3 files, `331 insertions(+), 1 deletion(-)`.

1. `scripts/survey_agent_control_v2.py` (+4, blob `d11febc`→`d58db79`,
   worktree SHA256 `7974551f870eb78ca38be815bdca8d97bca7e7445b81cc9e2f2d1e8b03e1f416`):
```python
if state.get("human_gates", {}).get("publication_preview") == "approved":
    human = state.get("human_gate_provenance", {}).get("publication_preview")
    if human != authority:
        errors.append("Human Preview and checkpoint approval authorities disagree")
```
Placed inside existing `name == "publication_preview" and wanted == "passed"`
branch after canonical-path/drift/typed-approval checks; equality does not
replace them. Uses exact stage disagreement wording. No wrapper duplication,
no schema/config/new checkpoint names/filesystem scan. Stage file unchanged
(`scripts/survey_stage_validation_v2.py` SHA256
`0f2393dadab72cecba5672b945d2be35e41089e4face5f0e2753b84a6a4b5806`,
same pre/post); profiled wrapper unchanged (`092f1a2d...`).

2. `tests/test_survey_dm003_w1_preview_agreement_v2.py` (new, 323 lines,
   blob `0eb328b1a1ac9d41302e3a229836a3d9273c6bbd`,
   SHA256 `ae42b94a3bad1407207d87a0a2472d109c6cdcd02e2773609699ddf8ce3d366a`):
6 methods, real `agent.validate_agent_state` + real
`profiled.build_profiled_freeze` + real `stage_validation.validate_stage`
+ real `publication` helpers + real `SpecialFixture`/`WeeklyCanonicalFixture`.
No `mock/monkeypatch/patch(/stub/fake` (grep clean); 71 asserts.

3. `tests/test_survey_dm001_019_freeze_equivalence_v2.py` (single authorized
oracle, blob `be394ef`→`25a7881`,
SHA256 `7d4d0004aab8e190dcc79bb3916e4ff4c4abc5d500799c4c564098924ec574b9`):
only `test_w4_wrapper_negatives_leave_no_outputs` assertion changed from
`"approval authority drift"` to
`"Human Preview and checkpoint approval authorities disagree"` with
DM003-W1 comment; no-write assert preserved. Initial failure retained in
`run-04`.

## 3. Test oracle and byte assertions (from patch, not re-execution)

- S3 repaired split: separately authored rival via
  `build_preview_approval` for same C1, asserts distinct `approval_id` and
  same `publication_candidate_sha256` (not a copy); Human ref swapped to
  rival, checkpoint stays A1; `validate_agent_state` contains DISAGREE;
  actual wrapper raises `ValueError(DISAGREE)` before writes; State bytes
  stable; Freeze/Manifest absent; full `_inventory` no added/removed/
  modified; stage still raises DISAGREE and writes no report. Proves
  pre-write rejection, preserves backstop.
- Null/path-only/hash-only: null → DISAGREE; copied same-byte alternate
  path (same SHA, different path) → DISAGREE; same path different SHA →
  DISAGREE. AND required; copy distinguished from separately authored A2.
- Equality insufficient: both-equal stale SHA → `drift`, NOT DISAGREE;
  both-equal noncanonical rival → `not canonical`, NOT DISAGREE; malformed
  Human extra key → schema rejection (`invalid before Freeze`), no new
  structural oracle. Existing checks preserved.
- Healthy: Special and Weekly approved agree → State `[]`, wrapper BUILDs
  exactly the 2 expected files with no other diff, manifest validates;
  Special follows `_special_advance_to_frozen` to FROZEN PASS and State
  stays `[]`. No full Retrospective claim.
- Pending/inert: fresh Special pending `[]`; RC Weekly pending `[]`; inert
  typed file alone leaves State `[]`; wrapper still rejects with existing
  `approved Publication Preview` gate (not DISAGREE), no writes, State
  bytes stable. Healthy pending State valid, not rejected — matches
  implementation-task correction.
- Fixture no-write proofs are regular-file inventories under the two owned
  roots (`fix.src`, `fix.survey` / `ROOT`), plus State-byte equality and
  output-absent asserts. Not whole-filesystem attestation (disclosed).

## 4. Schema vs duplication; other consumers; pending basis

- Schema `validate_instance` runs at function entry; malformed Human shape
  returns schema error before the new gate — no duplicate structural
  subsystem created. Null is schema-valid but `None != authority-dict`
  yields DISAGREE, as tasked. Non-dict checkpoint authority would yield
  both the existing lacks-provenance error and DISAGREE; harmless additive,
  existing errors retained.
- Gate scoped to `human_gates.publication_preview == "approved"`; pending
  (`pending` forbids any Preview provenance) unaffected. `_pending_conditions`
  and revalidation admission untouched.
- Shared `_validate_agent_state` is consumed by wrapper
  (`_safe_state_profile`), stage entry, weekly/refresh, human-gate and
  execution paths (grep confirms); placing the gate there gives one
  invariant to all State consumers, as tasked. Wrapper still loads the
  Human-side ref after validation, so the earlier gate is the correct
  pre-write boundary. Stage `human != checkpoint` guard retained.

## 5. Runs — 6+16+2=24 finals, initial failures retained

- Finals (post-commit `e1705b7`): `run-06` 6/6 OK (83.545s),
  `run-07` 16/16 OK (106.713s), `run-08` 2/2 OK (74.036s) = 24 methods.
- Pre-commit: `run-02` 6/6 OK, `run-03` 16/16 OK, `run-04` 2-run 1 FAIL
  (W4 oracle, full traceback retained), `run-05` 1/1 retry OK after
  authorized oracle update. `run-01` 5 ok + 1 ERROR retained verbatim
  (pending-fixture built inert approval before candidate existed; corrected
  to RC-advanced Weekly pattern, no validator weakening).
- Affected 16 are exactly the tasked selection: agent_control 5, stage 3,
  freeze_boundary 8; plus DM001-selected 2. No full-56/R1/Weekly rerun;
  old PASS not transferred (disclosed).
- Logs contain actual unittest streams with `Ran`/`OK`/`FAILED`, not mere
  headers; assertions are byte-level (State bytes, inventories, absent
  outputs), not tautological post-read comparisons.

## 6. Guards, pack and restore — verified with one proof gap

- Guard scripts are correct: `guard.sh` expects pre-commit `222a37e`/
  `dbabeed...`/`ff6c67f` + pinned control/profiled/stage SHAs and exactly
  the 2-then-3 intended paths; `guard-final.sh` expects `e1705b7`/
  `3d21322...`/`222a37e`, fully clean, 5 pinned SHAs.
- Gap (nonblocking qualification): saved `run-02..run-08` logs contain
  only unittest output, no per-run guard invocations/outputs; only
  `run-01` header notes a guard OK. Manifest `test_runs` records log SHAs
  and `Ran`/`OK` but no guard transcripts. README claim “each with fresh
  per-run HEAD/tree/source guards” is therefore unverified from the packet
  alone. Mitigation: manifest final HEAD/tree/parent/clean + source SHAs
  all re-verified read-only here (impl and restore both clean at `e1705b7`/
  `3d21322...`, worktree SHAs match, `ls-tree` modes/blobs match), and
  pre-commit parent pinned by diff. Bounded binding holds; do not rerun
  green suites to decorate this.
- New pack `w1-222-to-e1705b7.pack`: SHA256
  `97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9`,
  57,856 bytes, `verify-pack` 7 objects (1 commit + 3 trees + 3 blobs),
  `ok`. Old inputs re-hashed: b40 tar `faf6792f...`, 20-pack `2c2a8e6f...`.
- Restore `/tmp/opencode/jgas-dm003w1-restore-20261004T073938Z/candidate-partial-b40de60`:
  actual HEAD `e1705b7`, tree `3d21322...`, branch `dm003w1-final`, clean,
  shallow `774dd39...` only, chain `e1705b7→222a37e→ff6c67f→490414c→b40de60→774dd39a`,
  inert remote, all 3 file mode/blob/worktree bytes match impl
  (`d58db79`, `25a7881`, `0eb328b`, all `100644`). `run-09` log itself is
  minimal (pack-verify sections empty); binding relies on manifest +
  independent re-read above. No safe generic restore-script certification,
  no full-history claim (26,309 missing blobs inherited, runtime unbundled).

## 7. README wording correction

Packet `README.md` “No shipping change here” is misleading if read as “no
source changed”: the isolated candidate changed (`222a37e`→`e1705b7`, 3
paths). Correct statement: Production/reconstruct shipping unchanged;
change lives only in the independent `jgas-dm003w1-impl` DB and its
offline restore. Ordinary reconstruct Commit/Push remains Human-owned.

## 8. Limits (no adoption, no full audit)

Single synthetic Special/Weekly scope; no all-profile/real-publication/
real-Human inference. Per-module (not per-test) guards; inventories under
owned roots only. FROZEN compat shown for one Special path; no full
Retrospective flow. Stage backstop kept, not removed. Whole candidate
NOT_READY; step4/B3 OPEN; canonical seven-point audit unstarted.

## 9. Disposition

- Blockers: none. Code gate, test oracles, byte proofs, single authorized
  W4 update, pack/restore binding and isolation all check out within W1
  scope.
- Nonblocking qualifications: (a) per-run guard transcripts absent —
  final binding independently corroborated, do not rerun; (b) README “No
  shipping change” needs the isolated-vs-Production clarification;
  (c) `run-09` minimal, restore proof via manifest + re-read;
  (d) all disclosed partial-DB/runtime/scope limits above.
- **BOUNDED_PASS for DM003-W1 only.** No full audit, no adoption, no
  transfer of old 56/R1 PASS, no generic DM-003 resolver.
