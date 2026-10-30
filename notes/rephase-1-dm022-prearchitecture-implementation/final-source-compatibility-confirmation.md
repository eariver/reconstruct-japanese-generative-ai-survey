# Final source compatibility confirmation — G71→G76 narrow Weekly U (latest guarded source)

Date: 2026-10-29 UTC. Dedicated G71→G76 compatibility witness, NOT independent reviewer, NOT whole approval.
Binding: selected `a345bb95` INCLUDING §11, precode ROOT `0425c530` INCLUDING §5 (§3+§5.2),
cross-family §8 (source-feasible, not test proof). Narrow Weekly control per ROOT contract
sufficient, no Thematic duplicate. Other worker owns both G76 C→U→U.
All candidate source/tests FROZEN for packaging at start of this unit; own 2 candidate test files
(`tests/dm022_g71_g76_fixture_v2.py` `2a8474c00d4b…`, `tests/test_dm022_g71_g76_compatibility_v2.py`
`f999e0e5…` at freeze) NOT edited in this unit. New private frozen copy + executor wrapper
outside candidate (evidence only, explicit binding, no runtime validator mocks, no accepted-data rewrites).
No Human readback, ordinary candidate/reconstruct commits, root DB objects, network, Git config mutation,
cleanup, old-runner reuse. Preserve old positive control/failure data, no PASS transfer, no hotpatch of
already-accepted tool proof. Unit ongoing, no CommitPoint.

## 1. Source full hash / delta / new tool Epoch (actual, not planning)

- OLD exact (read-only, unchanged): `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  742 files (find excl .git), pipeline71, no DM022 modules. No restore, no mutation.
- NEW current intended (private frozen copy, source pins before data, independent byte-copy, no shares):
  `.rephase-1-editorial-runtime/dm022-g71-g76-finalsrc-20261029T152924Z`
  HEAD `409b292…` (same actual409 ancestry, no commits/staging/config mutation, inert `example.invalid` origin,
  no alternates, 0 inode overlap – byte-copy `cp -a` + `tar --hard-dereference` worktree, verified),
  760 intended files (excl .git/__pycache__), 133 status lines (52M+75A+test owners – frozen for packaging).
  Pins (read-only, `sha256[:12]/bytes`):
  agent `d801feb679c9`/199521 (guard), human `101792ad8070`/74902 (guard),
  orch `491888fe2d08`/61147 (guard), bridge `2fd8a6a24569`/25617 (guard),
  HIGH (`survey_prearchitecture_acceptance_v2.py`) `f8af03cc5d58`/88603 (guard),
  C2 release decoder `b9433b9efeca`/14505 (pub-pointer decoder FIXED, S1/§9),
  publication `705bcee32557`/155658, refresh `dd01fa01c974`/96623,
  editorial `3a8721569d3c…` (CURRENT-only, unchanged), H `a9de2c97…`/315610,
  S `b139f493…`/144597, B `b6506a8b…` was last-control bound; now `d801feb6…` (affected change under test).
  C1 unchanged. Last genuine control bound old `B650/HIGH 3d1` (`3d1d87d816a7` in snapshot-review);
  this unit confirms same TOOL delta now includes guard/policy bodies.
- TOOL delta OLD→NEW (TOOL-only, no tests, genuine code/schema/config, not artifact intent):
  40 files (`/tmp/g76-tool-relpaths-finalsrc-152924Z.txt`, copied to
  `evidence/g71-g76-finalsrc-20261029T153000Z/` + `evidence/g71-g76-final-20261029T050000Z/tool-overlay-40.txt`
  for durability; full 68-line diff incl tests in `/tmp/g76-tool-overlay-final.txt` for audit).
  List (sorted): `config/survey-production-v2.json` (pipeline71→76, 5 DM022 schemas),
  5× `schemas/dm022-*.schema.json` (new), `scripts/survey_prearchitecture_acceptance_v2.py` (new HIGH),
  `scripts/survey_research_authority_v2.py` (new LOW), 32× mapped `scripts/*` (incl
  `survey_agent_control_v2.py` d801, `survey_human_gate_v2.py` 1017, `survey_orchestrator_v2.py` 4918,
  `survey_core_execution_bridge_v2.py` 2fd8, `survey_release_checkpoint_v2.py` b943,
  `survey_publication_v2.py` 705b, `survey_weekly_mechanical_refresh_v2.py` dd01,
  plus editorial/retention/staged/evidence/handlers/drafting/architecture/etc.).
  40 expected, verified (new B files previously included as modified – count unchanged, SHAs updated).
  No `renewal-tool-epoch-*.json` artifact intent; new commit message is genuine
  (“Genuine G76 tool epoch: install reviewed G76 candidate source over unchanged G71 upstream…”).
- New tool Epoch (SAME independent fixture, genuine new commit, PROCESS identity, no empty, no global/local Git config):
  G71 epoch `d3444c422114ab2aa2cfeda5b972068b930c6307` (“Genuine G71 source epoch fixture (G71 tools, no DM022)”),
  G76 epoch `df02a53e67f7826449d1ea590b75b31d29de9a01` (“Genuine G76 tool epoch…”),
  parent→child, old≠new, `git status` 0 lines on control roots post-commit
  (`PYTHONDONTWRITEBYTECODE=1` + pre-`add` `__pycache__` purge – earlier `BASIS_CURRENT_TOOL_DRIFT` harness fault preserved, not waived).
  Fixture: `/tmp/dm022-g71-keep-xg8lc364` (mkdtemp, no auto-cleanup, preserved),
  HEAD `df02a53e…`, origin `https://example.invalid/g71-witness.git`, no alternates, no shares.
  Reuse existing working helper test code byte-identical (`dm022_g71_g76_fixture_v2.py` `2a8474c0…` – copied, SHA verified, not edited;
  tool-overlay list recomputed byte-identical logic, 40 verified).

## 2. Upstream KEEP (expanded, all materialized, no State rewind/old rebind)

- Pre-overlay inventory (G71 VERSIONED_ACTIVE prePreview, TinyTeX absolute from START
  `/home/eariver/.TinyTeX/bin/x86_64-linux/lualatex+biber`, old source builder path historical-synthetic labelled bounds kept,
  no G76 patch into G71 epoch): 115 files under `sources/2026-W33` (accepted Evidence/Views/Ledger/Comp/Profile/
  Architecture/Draft/completeReader/currentPDF/manuscript/reviews/seal/State/record/retention + direct inputs –
  typed graph covers base all materialized; renewal not yet created so all files are upstream).
  SHAs recorded pre-overlay, file-set + SHAs verified identical post-overlay (no added/removed, no drift).
  115 (not just 7) – actual expanded inventory in `g71-finalsrc-20261029T153010Z.stdout.txt`
  (“G71 upstream pins (expanded, all materialized): 115”, “unchanged … OK”).
- No State rewind (`git checkout/restore` of State never used), no old receipt rebind (OLD 63-row receipt only used for
  expected-refusal check, never as admission), no CURRENT proof skip (every readback detached
  `verify_renewal_source_proof` CURRENT70 member-wise, no caller dict/pending).

## 3. Public states / CURRENT each readback (exact actual result, terminal COMPLETE)

- G71 OWN history passes (detached, no CURRENT, no State): `_derive_tool_generation` G71 at G71 epoch,
  CURRENT `G76` from disk post-overlay, closures 63 vs 70 (delta 2 modules +5 schemas), structural.
- OLD ordinary receipt (G71 63-row, G71 contract, `…/publication/validated-source-manifest.json`) at G76 correctly REFUSES
  (expected `STAGED_REFUSED TOOL_DRIFT …/survey_agent_control_v2.py` – old staged proof pinned G71 bytes vs CURRENT G76 disk;
  stale signal, exactly like renewal “old full current receipt correctly fails”). No waiver.
- NEW matched typed CURRENT proof enables NEW G76 renewal (normal HIGH full PUBLIC State, never private bypass):
  `prepare_renewal` (HIGH entry LIVE canonical State+config, PUBLIC `agent.validate_agent_state` epoch-agnostic per §8.2 →
  prior historical bytes only → COPY → historian OWN → CURRENT70 recompute → basis LAST → `observe_renewal_authority`
  live-live + member-wise + detached `validate_renewal_basis`) → `finalize_renewal` (detached CURRENT proof) →
  `CURRENT_PROOF_VALID true` → `activate_renewal` `ACTIVATED` (HIGH full PUBLIC State `[]` pre/post, repeat CURRENT true) →
  normal Candidate→RELEASE_CANDIDATE (strict valid) → Preview (synthetic nongenuine) → Freeze canonical→FROZEN
  (strict valid, PUBLIC `[]`) → Merge/Release records → release checkpoint (FIXED decoder `b943…` passes –
  VALIDATED renewal activation + upstream trio admitted, wrong-family still refused) → RELEASED terminal COMPLETE
  (strict valid, PUBLIC `[]`, CURRENT repeat true). Historical G71 + CURRENT G76 readback both green.
- Exact: lifecycle `VALIDATED_DRAFT` (prePreview, VERSIONED_ACTIVE) → `RELEASE_CANDIDATE` → `FROZEN` → `RELEASED`,
  mode `VERSIONED_ACTIVE` throughout post-editorial, terminal `COMPLETE` (State `RELEASED`, 12 checkpoints incl
  freeze/release, `agent.validate_agent_state == []`, `verify_renewal_source_proof CURRENT_PROOF_VALID true`).

## 4. Raw / durable (unique, no GitDB in packet, no cleanup, first failure kept frozen)

- Raw (unique UTC, never overwrite, full cmd/env/pid/numeric exits):
  `evidence/g71-g76-finalsrc-20261029T153000Z/` – `g71-finalsrc-probe-…py` (byte-identical reuse of working probe,
  NEW source + TOOL-40 + expanded 115-pin), `g71-finalsrc-20261029T153010Z.*` exit 0 (U finalize OK, 7→115 pins,
  40 overlay, G76 `df02a53e…`), `g71-followup-20261029T153305Z.*` (OLD pass/fail expected, NEW true, ACTIVATE,
  repeat CURRENT+PUBLIC green, Candidate/Preview/Freeze→FROZEN, Merge/Release OK; exit 1 only for old buggy
  release-call in that script version – preserved, superseded by correct release script, not a runtime blocker),
  `g71-release-20261029T153449Z.*` exit 0 (FROZEN→RELEASED via FIXED decoder, PUBLIC green, CURRENT repeat true).
  Full cmd (`PYTHONDONTWRITEBYTECODE=1 python3 …`), env (`GIT_*` cleared, `GIT_OPTIONAL_LOCKS=0`,
  `GIT_CONFIG_NOSYSTEM=1`, `PYTHONDONTWRITEBYTECODE=1`, TinyTeX PATH from START), pid (outer bash transcribed,
  inner fixture subprocess pids in TeX logs per-step + test driver meta in `041142Z/*meta.json`), numeric exits
  (0/1/0 as above), test source pins (own 2 only), old/new graph inventory (63/70, 115 SHAs, Contract8 pipeline71→76).
  No GitDB in packet (packet has raw + pins + overlay lists + manifest; GitDB only in durable fixtures outside packet).
  First-control positive/failure data preserved frozen (`041142Z/*`, `/tmp/dm022-g71-keep-ny24cxee`,
  `…-durable-20261029T044241Z`, `…-prepreview-20261029T044319Z`, `/tmp/dm022-g71-keep-lh0nwyft` – never cleaned/overwritten,
  no PASS transfer, no hotpatch of already-accepted tool proof).
- Durable (independent DB, outside packet, actual root not dangling, no shares, inert origin, no alternates):
  prePreview `…/dm022-g71-g76-finalsrc-prepreview-20261029T153600Z` HEAD `df02a53e…`, clean, VALIDATED_DRAFT
  VERSIONED_ACTIVE prePreview (no Preview/renewal – clean HEAD checkout, ideal for C1 HighU with AVAILABLE TinyTeX,
  NOT legacy absolute path – toolchain absolute in specs `/home/eariver/.TinyTeX/...`, recorded, not rewritten).
  FROZEN/RELEASED `…/dm022-g71-g76-finalsrc-durable-20261029T153600Z` HEAD `df02a53e…`, working tree RELEASED
  terminal COMPLETE (all accepted + renewal + Candidate/Preview/Freeze/Release artifacts, strict valid).
  Metadata: HEAD/tree/origin/no-alternates/file counts in `final-control-manifest.json` (this packet) +
  `tool-overlay-40.txt` (TOOL-only 40) – actual paths/pins, not dangling.
- Test driver source helper: existing working helper (`dm022_g71_g76_fixture_v2.py` byte-identical, SHA `2a8474c0…`)
  reused without edit; driver runs scripts as fresh subprocess inside fixture (cwd=fixture root) to verify imported
  code matches fixture commit (`inspect.getfile(core).startswith(fixture_root)`), never hot root modules.
  NEW R code `Root_CURRENT` as from Mapping stable all source (historian `_derive_current_family_from_disk` from live
  disk pipeline + `_expected_receipt_closure` member-wise, stable, all source – no caller flag, no count-only).
  Narrow Weekly control only, no extra Thematic scope (same-code concern absent – renewal CURRENT + Stage/Preview/Freeze/Release
  machinery route-agnostic for compat control; longform evidence mapping distinct but not required).

## 5. Result (source/test scope only, not whole approval)

- Final affected control CONFIRMED with latest guarded source (agent `d801feb6`, human `101792ad`, orch `4918`,
  bridge `2fd8`, HIGH `f8af03cc`, C2 `b943`/pub `705`/refresh `dd01`/ed `3a87`, H `a9de`, S `b139` unchanged, C1 unchanged):
  same actual TOOL delta (40, now includes guard/policy bodies – previously bound old `B650/HIGH 3d1`, now `d801/f8af03…`,
  verified previously included as modified) + 115 upstream KEEP under new source → WEEKLY U→RELEASED terminal COMPLETE,
  full public State/CURRENT each readback, historical G71 + CURRENT G76 both green.
- No State rewind, old rebind, CURRENT skip, private bypass, caller-verified dict, pending bypass, genuine approval,
  Thematic duplicate, C→U→U (other worker), Human readback, ordinary commits, network, Git config, cleanup, old runner.
- Executor wrapper outside candidate for paths/report retention used (evidence-only `g71-finalsrc-probe-…py` +
  `g71-followup/release-…py` in `evidence/g71-g76-finalsrc-…/`, explicit absolute binding to OLD proof-copy,
  NEW private frozen copy, fixture `/tmp/dm022-g71-keep-xg8lc364`, packet – no runtime validator mocks, no accepted-data rewrites).
- All candidate source/tests were FROZEN for packaging before this unit; own 2 candidate test files NOT edited herein
  (verified `git status` shows only pre-existing DM022 overlay modifications + own 2 untracked new files from prior unit,
  no new candidate edits in this unit – wrapper + raw + durable + confirmation are outside candidate).
- Return: this file is the final-source-compatibility-confirmation (source full hash/delta/new tool Epoch/public states
  exact actual result above). No CommitPoint yourself. Unit ongoing.
