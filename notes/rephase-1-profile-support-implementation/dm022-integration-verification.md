# DM022 integration verification — C-runtime owner (actual work, not plan-only)

2026-10-31. C-runtime/DM022 integration and verification owner. Exclusive ownership kept:
`scripts/survey_research_authority_v2.py`, `scripts/survey_prearchitecture_acceptance_v2.py`,
`tests/test_dm022*.py`, `tests/dm022_*_fixture_v2.py` — in prepared workcopy ONLY.
Did NOT edit Evidence/Screening/runners/`test_profile_support_upstream_repair_v2.py`.
No new shipping schema/module/family. Read workstream-c.md incl §6, astra review (all),
R4→R5→ROOT§7 map. Prior D draft rejected/archived; none of its guessed
helpers/`assertRaises(Exception)`/unrelated-file/mocked-resolver/same-revision repeat used.

## 1. Owned edits (workcopy, synced to snapshot)

- `tests/dm022_prearchitecture_fixtures_v2.py` — `init_independent_git` now process-scoped
  (`-c user.name/email` + `GIT_AUTHOR/COMMITTER_*` env, no `git config` writes),
  idempotent (existing `.git` → add/commit only), no `--allow-empty`, inert origin,
  no-alternates check kept.
- `tests/test_dm022_prearchitecture_acceptance_v2.py` — `_fixture_commit` process-scoped;
  `_chain_root` git-inits the fixture tree BEFORE first Screening gate (A's prepackage
  runs `verify_state_basis` with in-run HEAD and refuses without resolvable HEAD).
- Both synced byte-identical to snapshot-fixed; `AST_PARSE_OK` on both. No other files
  touched (no A/B/D race edits).

## 2. Real signature verification (executed, no fixture needed)

In snapshot-fixed, `/usr/bin/python3`, `PYTHONDONTWRITEBYTECODE=1` (real import of owned
LOW module; top-level imports unchanged core+schema_gate+stdlib):

- `build_revision_cards_views_from_paths` kwonly `['before_copy_path']` — missing → `TypeError`.
- `accept_revision_evidence_views_from_paths` kwonly `['request_path','before_copy_path']` — enforced.
- `build_versioned_ledger_from_paths` kwonly `['request_path','before_copy_path']` — missing both → `TypeError`.
- `build_versioned_completeness_from_paths` kwonly `['before_copy_path']` — missing → `TypeError`.
- `_verify_adopted_graph_full` exactly `(repo_root, checkpoint_path, checkpoint_sha)`.
- `derive_before_context` exactly 4 positionals.
- HIGH calls real `find_declaration_loss` directly (prepare `:561`, adopt `:1190`); zero
  `BLOCKER(workstream-A)`/`getattr` in owned files; zero real `None,None` (one comment line
  `:2432` only).

## 3. LOW kw-only caller census (read-only search)

- HIGH (`survey_prearchitecture_acceptance_v2.py:651,671,720,730`) forwards all REQUIRED
  keywords already. Agent/renewal callers use unaffected 4-positional check/prove paths.
- Exactly ONE direct test caller omits new keywords:
  `test_profile_support_upstream_repair_v2.py:723` (`build_versioned_ledger_from_paths`
  without `request_path`/`before_copy_path`) — NOT my file; reported, not edited.
- Owned `test_dm022*.py`/`dm022_*_fixture_v2.py` contain ZERO direct calls to the four
  builders (they drive prepare/adopt/prove/check) — no migration needed there; new
  focused tests will pass explicit keywords from real fixture artifacts.

## 4. Executed suites (fixed snapshot, unique raw logs, no overwrites)

Snapshot: `.rephase-1-editorial-runtime/profile-support-dm022-verify-20261031T155554Z/snapshot-fixed`
(769 worktree files = 768 + D new module; independent `.git`, inert origin).
Logs: `notes/rephase-1-profile-support-implementation/dm022-verify-20261031T155554Z/logs/`.

| Run | Result | Cause |
|---|---|---|
| A2 weekly positive (`a2-weekly1-*`) | ERROR | A-gate State-basis mismatch (see §5) |
| A2 full module (`a2-baseline-*`) | 25 tests, errors≈24 | same |
| c1 trio (`c1` quick run) | 14 tests, 3 errors | same |
| b-ordinary-consumers (`b-consumers-*`) | 23 tests, 10 errors | same |
| presence controls (`presence-*`) | 3 tests, 3 errors | same |
| depth+presence combined | 31 tests, 2 failures + 28 errors | same + `timeout`-wrapper self-trip of depth duplicate-guard (harness artifact; without wrapper no trip) |
| 8-file batch | TIMEOUT 600s, no result | heavy suites (lifecycle/guard); recorded not-run, no duplicate rerun |

All errors share ONE traceback root: `survey_screening_v2.py:751
resolve_prepackage_root_effective → core.verify_state_basis → ValueError:
implementation commit differs from authoritative state`. No HIGH/LOW operation body
reached; no operation PASS/FAIL beyond the gate is claimed.

## 5. Blocker returned to root (cross-owned, NOT race-edited)

A's `resolve_prepackage_root_effective:750` calls `core.repository_commit_sha(repo_root)`
(real HEAD) instead of threading `prepare_package`'s passed `IMPLEMENTATION_SHA`.
The whole fixture contract (`init_profile`/`make_screening`/`make_evidence`/… in
`test_survey_evidence_v2.py`, hardcoded `IMPLEMENTATION_SHA = "4"*40`) builds State with
the fake SHA while the new gate demands real HEAD. Before my fix: "cannot resolve
commit" (no git); after early-init fix: "commit differs" (fake vs real). Either way EVERY
chain-building suite fails at the first Screening gate — including suites never touched
by D. Fixture-side adaptation would require editing helper `test_survey_evidence_v2.py`
(not in C/D ownership) or silent State rewrites (dishonest). REQUIRED: A threads the
caller's SHA through the prepackage helper (as every other prepare path does), or root
explicitly authorizes + assigns real-HEAD fixture migration. Until then: HIGH/LOW DIRECT
+ true-DERIVED R≠E operation, Profile/path mismatches, retention substitution,
second-`revision_id` repeat, downstream consumer/readback/CURRENT proof are BLOCKED —
attempting them now would test nothing. No fake evidence manufactured.

## 6. Not run / not claimed

- New focused DM022 module (DIRECT + DERIVED R≠E multi-DID/source/parentOID, mismatches,
  repeat with second id, consumer/readback, CURRENT vs own-epoch) — unwritten while the
  chain gate blocks; will use real fixture builders + exact error predicates + no-write
  inventories, never D-draft patterns.
- Heavy suites (`full_lifecycle`, `normal_writer_late_guard`, `b_late_prepublish`,
  `g71_g76`, `lifecycle`, closure/history) — not run (timeout proportions); no counts summed.
- No PDF builds (proportionate need only; explicit TinyTeX verified earlier).
- RETRO: stays ordinary upstream only; no schema expansion attempted.

## 7. Source pins / process state

- C: `survey_research_authority_v2.py` 212084B `546bbad1…` (3644 lines, §6 corrected);
  `survey_prearchitecture_acceptance_v2.py` 92741B `388c8994…` (1526 lines).
  A: screening `45e93e76…`, evidence `174c04cf…`; B: runner `5a6280ac…` — integrated.
- Env: `/usr/bin/python3` 3.14.4, `PYTHONDONTWRITEBYTECODE=1` all runs; no installs,
  network, Production, intake, rebaseline, Human readback, reconstruct git ops.
  No candidate/snapshot commits; fixture temp trees auto-cleaned; raw logs outside temps
  (cleanup cannot erase only proof). Synthetic labels honest (`SYNTHETIC_FIXTURE_*`).
- Earlier failed drafts/runs preserved (rejected-D archive + `a2-baseline` setup-failure
  raw); counts qualified per-run above, never summed.

WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN retained. No independent
approval, no whole-ready claimed. Awaiting root disposition on §5 before operation evidence.

## 8. Root disposition compliance + focused positives (2026-10-31, second return)

Disposition (`astra-implementation-review.md` §§43–56) applied as ordered; §§1–7 above
preserved as first-return history except where explicitly corrected here.

- **Batch archive:** `dm022-verify-20261031T155554Z/batch-archive.md` (new) with exact raw
  counts: A2 25t/errors26, weekly1 1/1, b-consumers 23/10, presence 3/3, depth+presence
  31t/failures2+errors28, c1-trio terminal-observed 14/3 (no raw file, NOT rerun),
  8-file batch **INCOMPLETE/TIMEOUT** (600s kill, no log — corrected from "not-run").
  Depth duplicate-guard trip classified as harness preemption (`timeout`-wrapper
  self-match; avoided without wrapper). All setup errors share the §5 gate traceback.
- **caller723 withdrawn:** the keyword-less invocation was a deliberate `TypeError`
  oracle in the rejected D draft, already replaced — NOT a missing shipping caller.
  Missing mandated keywords in a negative oracle is not a migration defect.
- **No A threading:** fixtures migrated to real committed synthetic source BEFORE
  initialize (no fake SHA, no State rewrites of accepted data). Shared helper
  `test_survey_evidence_v2.py` (ordinary owner, still fake-SHA at check time) NOT
  race-edited; new tests replicate its builder sequence with the real HEAD in owned
  `tests/test_dm022_c_direct_operation_v2.py` (standalone class, no suite bloat).
- **Correct facade:** EVIDENCE_REVIEWED State verified via strict
  `agent.validate_agent_state` inside reused A2 `_make_evidence_reviewed_state`
  (existing agent facade, not a mock; bare-verifier attestations untouched).
- **B2 untouched:** no ordinary3/5, residual-union, empty-dimension, or LOW new-policy
  edits anywhere (awaiting reviewer/root discrimination).

**Focused positives EXECUTED** (snapshot-fixed, `/usr/bin/python3`,
`PYTHONDONTWRITEBYTECODE=1`, unique raws `c-both-routes3-*`, exit 0):

- `test_c_direct_weekly_prepare_adopt_readback` — prepare → ADOPTED (guard released) →
  PREARCH readback (triplet) → detached checker `[]`. **ok.**
- `test_c_thematic_direct_prepare_adopt_readback` — same chain on THEMATIC
  (profile-specific views annotations) → ADOPTED → readback → checker `[]`, plus pure
  `find_declaration_loss` oracles both directions (identical-carrier `[]`;
  wrong-parent-only `[("derived-source","O-DERIVED-1")]` despite global OID equality).
  **ok.** `Ran 2 tests … OK` (3.073s).

**Finding returned (request-level R!=E):** a `REFERENCE_EXPANSION` row with raw parent
`target-source` fails Discovery normalization (`local:`/`external:` namespace
required); with `local:target-source` it passes normalization but A's raw string-array
loss compare cannot match it. Namespaced-vs-raw parent linkage needs an A/root ruling
before a request-level R!=E positive is meaningful — recorded, not hacked.

**Pending (exact):** second-`revision_id` repeat + guard/no-overwrite, targeted negatives
(COPY Profile/path mismatch, corrupted `discovery_ref` before first COPY, retention
substitution, tampered Contract8), downstream consumer/readback + CURRENT-vs-own-epoch
proof, heavy suites (full_lifecycle/guard/b_prepublish/g71/lifecycle/closure/history).
Common shared-helper migration (ordinary owner) still pending for old suites; C's own
path no longer depends on it. New test pin: `test_dm022_c_direct_operation_v2.py`
(synced workcopy→snapshot; see `c-both-routes3` raw for bytes).

## 9. Selected scope complete on fresh snapshot (2026-10-31, third return)

Snapshot: `.rephase-1-editorial-runtime/profile-support-dm022-verify-20261031T194049Z/snapshot-fixed`
(770 worktree files; independent `.git`, inert origin; synced from latest workcopy AFTER
ordinary-helper + A/B corrections). All runs `/usr/bin/python3`,
`PYTHONDONTWRITEBYTECODE=1`, unique raws under `dm022-verify-20261031T194049Z/logs/`.
No counts summed across batches; each line below is its own exact run.

- **C module 4/4 OK** (`c-four-tests3`, exit 0, 8.914s; re-confirmed in `final-c-a2`
  combined 29/29): Weekly DIRECT prepare→ADOPTED→PREARCH readback→checker `[]`;
  THEMATIC same + loss oracles; DERIVED R!=E (root `[target-source]` vs effective
  carrying `derived-source`) + NEW-ID second correction ADOPTED + resolver PREARCH +
  resume; negatives N1 (profile SHA refusal, zero rev-dir writes) / N2 (tampered COPY
  SHA refusal, bytes restored) / N3a (pre-adopt double-prepare dir guard) / N3b
  (post-adopt reuse stale refusal, zero new files). Intermediate failures preserved
  (`c-derived2` namespace, `c-four-tests` identity-order, `c-neg2` unadopted-checker,
  `c-neg3` adopted-request rewrite — each fixed by the exact predicate, no mocks).
- **A2 full 25/25 OK** (`final-c-a2` with C module: `Ran 29 tests … OK`, 44.323s).
- **Affected 37/37 OK** (`affected-c1-b3`, exit 0, 100.559s): c1 family_closure (fresh
  CURRENT G76 closure on changed bytes, same memberships map — not counts-alone),
  presence, research_graph, b-ordinary-consumers (history/normal-consumer/late seams).
  Two leftover fake-SHAs migrated in owned files (b-consumers wrapper + full_lifecycle
  ledger → actual HEAD); line-504 stale-input oracle left deliberate (still refuses).
  Fixture identity migrated in owned helpers (prearchitecture/lifecycle/c1/g71:
  process-scoped `-c`/env, idempotent, no `git config`, never empty).
- **Signatures** (unchanged C bytes `546bbad1`/`388c8994`): 4 LOW REQUIRED kw-only
  `TypeError` proof, adopted 3-arg, derive_before 4-pos, zero BLOCKER/getattr, zero
  real `None,None`, HIGH direct loss calls — from prior run, still binding.
- **DERIVED per disposition** (no normalizer abuse, no runtime change): root BASE +
  named OID → root acceptance (DCP); E holds ONLY the expansion child (raw parent
  refs, same source identity, obligation subset — expansion contract exact);
  SCP/request flow E. Prior namespace-conflation finding withdrawn as fixture error.
- **B1/B2 withdrawn** per independent §8: no ordinary3/5/residual/empty-dim/LOW-gate
  edits made. B0/B3 ordinary-fixed tests healthy (affected run green).
- **Not run:** heavy full_lifecycle/guard/b_prepublish/g71 suites (old INCOMPLETE/TIMEOUT
  stands; test_20 lifecycle witness passed inside b-consumers), full Selection /
  Architecture runs (consumer proof via resolver+readback+checker proportionate),
  RealPDF builds (no new findings requiring them; inherited limited scope not
  transferred).
- **Pins (workcopy):** C-direct-test 25186B `cd80c293…`; A2 86675B `322a600e…`;
  b-consumers 47594B `cad603cc…`; full_lifecycle 280038B `b736baa7…`;
  fixtures prearch 3873B `769f1820…`/lifecycle 4717B `f8c8f822…`/c1 4782B
  `059fdf24…`/g71 5918B `43d4d414…`; C runtime unchanged `546bbad1`/`388c8994`.
- **Live process state:** no test processes running at closeout. No candidate/snapshot
  commits; fixture temps auto-cleaned; raws outside temps. No reconstruct git ops,
  network, Production, intake, rebaseline, or Human readback.

Genuine operation evidence delivered for the selected scope. Unresolved: heavy-suite +
  full Selection/Architecture + RealPDF runs above (explicit, not hidden).

## 10. Extended boundary: binding negatives, report controls, consumers (2026-10-31, fourth return)

Snapshot unchanged (`.../profile-support-dm022-verify-20261031T194049Z/snapshot-fixed`).
No broad matrices; only focused singles after setup green. B1/B2 withdrawn honored
(zero ordinary-policy/LOW-gate edits). No whole-PASS claimed; root → final independent
review/packaging next.

**Ready exact test IDs** (all in `tests/test_dm022_c_direct_operation_v2.py`,
workcopy 35636B `ac44154f…`, PLUS `test_dm022_prearchitecture_acceptance_v2.py`
87215B `bdf10930…` with root/materialize overrides + HEAD ledger fix):

- `Dm022CDirectOperationTests.test_c_direct_weekly_prepare_adopt_readback`
- `Dm022CDirectOperationTests.test_c_thematic_direct_prepare_adopt_readback`
- `Dm022CDirectOperationTests.test_c_derived_weekly_true_r_not_equal_e`
  (+ NEW-ID second correction ADOPTED, resolver PREARCH, resume)
- `Dm022CDirectOperationTests.test_c_negatives_profile_copy_retention_refuse_no_write`
  (N1 profile-SHA + zero rev-dir writes; N2 COPY-SHA checker refusal, bytes restored)
- `Dm022CDirectOperationTests.test_c_binding_negatives_beyond_file_sha`
  (N4 alt-Profile path mismatch; N5 canonical State-path mismatch; N6 discovery_ref
  path→profile-file resolve mismatch; N7 ghost-DID record refusal; N8 manifest
  retention_snapshot substitution → prove refuses; N9 tool_shas substitution →
  adopt refuses with State unswitched — CURRENT proof enforced, not silent)
- `Dm022CDirectOperationTests.test_c_report_positive_control_extra_rows_pass`
  (extra valid NamedRef + non-CORE DETERMINISTIC review through strict agent
  validation → full adopt/readback/checker green; predicates not over-tight)
- `Dm022FullLifecycleWitnessTests.test_weekly_dm022_to_selection_stage`
  (post-adoption 7-slot regeneration + SELECTION_COMPLETE advance, 24.9s)
- `Dm022FullLifecycleWitnessTests.test_weekly_present_old_seven_slots_retain_clear_regenerate`
  (old-7 retain → adopt clears → new regen, 20.6s)
- `Dm022FullLifecycleWitnessTests.test_weekly_draft_synthesis_reader`
  (generated draft+reader consumer on revised graph, 36.2s)

**Exact results (per-run raws under `dm022-verify-20261031T194049Z/logs/`):**
`c-full` 6/6 OK (12.96s); `a2-full2` 25/25 OK (37.07s); `affected-c1-b3` 37/37 OK
(100.56s, incl. CURRENT G76 closure); `consumer-selection`, `consumer-sevenslot`,
`consumer-draft` each 1/1 OK. Intermediate failures preserved
(`c-derived2` namespace, `c-four-tests` identity-order, `c-neg2` unadopted-checker,
`c-neg3` adopted-request rewrite, DERIVED reuse/identity/invention predicates).
Unittest writes results to stderr (all `*-stdout.txt` empty by framework design, not
evidence loss); `*-stderr.txt` hold REAL full outputs; `*-exit.txt` numeric exits;
`c-bindings-meta`/`c-full-meta`/`a2-full2-meta` hold command/PID/date/env/pwd.
No transcript reconstruction, no overwritten files.

**CURRENT proof tied to code bytes:** N9 (tampered `tool_pins.tool_shas` → adopt
refuses, State unswitched) + every adopt re-verifying contract/tools against live
files + closure run on changed bytes. Literal membership alone not claimed as proof.

**Real-build determination:** Selection regeneration + draft synthesis verify
generation on current bytes without TeX; no PDF-dependent finding arose, so NO real
PDF run executed and no inherited PDF transfer claimed.

**Retained critical artifacts** (ignored runtime + manifest, never root Git DB):
`.../profile-support-dm022-verify-20261031T194049Z/retained/rev-c-derived-1/`
— revision-manifest.json, record.json, supersession-report.json,
proposed-graph-proof.json, state-before.json (COPY), request + decision JSON,
`manifest.json` (per-file SHA256/bytes/mode + route/script binding).

**Owned fixture migrations this round:** A2 `_prepare_and_decide` extra_obligations
forwarding, `_materialize…(discovery_path?)`, `_make_evidence_reviewed_state(…,
root_acceptance?, extra_dcp_…?)`; b-consumers + full_lifecycle HEAD ledger/wrapper;
lifecycle/c1/g71 fixture identity (process-scoped, idempotent); line-504 stale
oracle left deliberate. Shared helper `ed0155cd` untouched. C runtime bytes
unchanged (`546bbad1`/`388c8994`).

**Live process state:** none (ps clean at closeout). No candidate/snapshot commits,
network, Production, intake, rebaseline, Human readback, or reconstruct git ops.

## 11. Test-only oracle/retention correction (2026-10-31, fifth return; no runtime change)

Per final independent §3.1 + root last section. Only
`tests/test_dm022_c_direct_operation_v2.py` changed: 35636B `ac44154f…` →
42156B `6ffde575a21b3748147fda3f662d7934a78c5082a062a4f174519d4902aee585`
(7 methods; initial pin preserved in review/packaging history). Runtime pins
re-verified UNCHANGED (`546bbad1`/`388c8994`/`f0f28954`/`36b7b583`/`5a6280ac`/
`ed0155cd`); snapshot stays 770 files. No runtime-changed assurance claimed.

- **Retention:** hardcoded workspace writer removed. Extra preservation runs ONLY
  under explicit `PROFILE_SUPPORT_RETAIN_ROOT` (normalized, jailed, fresh
  `mkdtemp` per-run dir, exclusive `xb` files/manifest; without it the test is
  an ordinary temp run). Proven once via harness dir
  (`retain-harness/rev-c-derived-1-vbkutpyw/`, 7 files + manifest, exit 0).
  Existing `retained/rev-c-derived-1/` bytes preserved + annotated
  observation-only/latest-unknown-run (`ANNOTATION-observation-only.md`), NOT
  earlier-run proof; nothing deleted.
- **Exact predicates** (discovered via focused probes, pinned by execution):
  N1/N4/N5/N6 `AcceptanceError` full texts (profile SHA drift / Profile
  path-SHA match / canonical LIVE State path / discovery_ref resolve);
  N7 RAW `ResearchAuthorityError` ghost-DID text with owned-partial window
  (rev dir + candidate + COPY exist; NO checkpoint/proof dirs; canonical State
  SHA unchanged; honest late-failure label, no universal-prewrite promise);
  N3a dir-guard startswith; N3b exact staleness text; N2 checker single-error
  assertEqual + pre-restore inventory; N8 schema-valid `present`-flag flip on
  the STORED manifest (finally-restored) → checker
  `adopted graph FULL validation failed: checkpoint retention_plan inventory
  row != stored manifest snapshot for slot: candidate-matrix-v2.json`
  (sidecar-manifest + unknown-key variants recorded as failed shapes);
  N9a relabelled stored-request integrity
  (`manifest request SHA drift: …/request-rev-c-bind-n9.json`); N9b REAL
  fixture tool-bytes drift post-prepare → adopt refuses
  `tool SHAs drift since prepare (refuse; NEW attempt required)` with State
  unswitched (no authority rebinding). All negatives carry full SHA/mode/dir/
  symlink inventories (new `_sha_tree` helper); ordinary 3/5/LOW7 untouched.
- **Focused runs** (new unique dir `dm022-narrow-20261031T201738Z/logs/`, real
  direct captures + PID/env/exit/pins; unchanged positives NOT rerun):
  `c-narrow` 3/4 → `c-integrity4` 1/1 → `c-changed-rest` 3/3 →
  `c-retain-env` 1/1, all exit 0. Probe scripts live outside the workspace
  (`/tmp/opencode/c-probe-narrow[2].py`); probe outputs are evidence raws.
- **Gaps before broadening:** heavy lifecycle/guard suites, full Selection /
  Architecture beyond selected consumers, RealPDF (unchanged); request-level
  R!=E namespace ruling (prior finding) stands.
