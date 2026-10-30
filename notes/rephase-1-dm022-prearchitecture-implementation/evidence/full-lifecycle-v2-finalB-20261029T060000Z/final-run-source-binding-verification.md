# Final-run source binding verification — DM022 FinalB CUU (data-only, no runtime)

Date: 2026-10-30 UTC (read-only verification).
Scope: resolve author FinalB inconsistent durable `162124Z` source guess.
Method: data-only file reads + `sha256` byte hashing + read-only `git rev-parse/log/ls-tree/cat-file/status` inside private/durable/fixture copies ONLY. No test execution, no imports, no builds, no source edits, no Human-commit readback, no Git mutation, no network, no ordinary Commit/Push. Existing reports untouched. No independent semantic approval.

## 1. Delivery identity (FINAL)

- Packet: `notes/rephase-1-dm022-prearchitecture-implementation/source-packaging/final-20261029T152913Z/`
- `complete-dm022-manifest.json`: SHA256 `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa` / 185422B. Verified by re-hash.
- `complete-dm022-prearchitecture-409.patch`: SHA256 `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b7260` / 4931836B.
- Intended files: **768** = 689 tracked-at-HEAD + 79 untracked new (per `source-disposition.md`).
- Delta vs actual409 (`409b292756dd1277b9dfae87679934c0d2ce251c` / tree `8ce36998…`): **133 = 54M + 79A**. Supersedes `52M79A131` premise.
- Disposition pins (full SHA, verified against manifest `files` map): HIGH `f8af03cc5d58af1057ea26d9cef0eb87b1fd71118ddf63a2186e24da9bc1e751` / 88603B; LOW `2aef837faaa549b9eab3f1a03696b5a44ef63ff63316cad817842c2110554fb` / 155892B; agent `d801feb679c99d2ed8e52b83ed5aca5253ad695ea69eef90feb2e6727dacfe88` / 199521B; human `101792ad8070607e3f735ddf6e0f6d60f0b3c77afeaab85347cc87e5bee246b6` / 74902B; orch `491888fe2d089edb1bef8a8cfa5bad942438148f9b630ac4cf18610a27a26b76` / 61147B; bridge `2fd8a6a24569333ce3a1ecabd4779fa19dc84ba4f79be6d380f47422e8a1f9ec` / 25617B; pub `705bcee32557a634c229acbbb58c42d8b34babd90d331f442c158ed59a67482d` / 155658B; release `b9433b9efeca0275c3cd6f8cf77fce0942eaa3208e44df65187f6fcfbee18296` / 14505B; refresh `dd01fa01c974486690c9da9701b9ca7040371f6c4d10cb1aa9840126865b551e` / 96623B (prefix `dd01`, not `01`); ed `3a8721569d3cb1512501699ecf78d7c7e3679120cfb9b06504fa1471bfdee722` / 275939B; H `a9de2c97eb40e358cd06b59cedacc78f3880fab18bd6e6b281ca9e2f578156d9` / 315610B; S `b139f493f791cdcd2e3e2a298e97d92b379f62dff95a14c7412ecd63da2217ca` / 144597B; own_test `e41df24f2509a22321f306aeb59e9e1b0034be4babb06af13bb9d392f52ef3b3` / 280014B.

Expected 8-prefix set from task (`HIGH f8af03cc`, `LOW 2aef`, `agent d801`, `human 1017`, `orch 4918`, `bridge 2fd8`, `pub 705`, `release b943`, `refresh dd01`, `ed 3a87`, `H a9`, `S b139`) all match delivery full SHA above. `refreshed01` in task text is read as `dd01fa01…`; no `01…` or `ed3a87…` file exists in delivery (verified: `ed3a87` zero hits; `01`-prefix files are only `accept_special_freeze_issue_only.py` / `revise_special_half_year…`, not refresh).

## 2. Terminal two-route CUU — actual executed root

- Private exec preserved: `.rephase-1-editorial-runtime/dm022-full-lifecycle-finalB-20261029T060000Z/` (has `.git`, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, worktree M = DM022 overlay, status shows expected modified files).
- Wrapper: `evidence/full-lifecycle-v2-finalB-20261029T060000Z/final-cuu-wrapper.py` (171 lines). Retention-ONLY patch: `TemporaryDirectory.cleanup` patched to `copytree` C renewal dirs + reviews dirs (excl `.git`/`__pycache__`), writes `exact-original-target-paths.json` with PDF/trio/proof/manifest hashes. No runtime patch, no accepted-metadata rebind, no editorial-as-C copy.
- Raw:
  - `dm022-finalB-wrapper-raw.txt` exit 1: `ModuleNotFoundError: No module named 'tests'` (first attempt wrong CWD, preserved, not a runtime blocker).
  - `dm022-finalB-wrapper-raw2.txt` exit 0: `test_weekly_renewal_c_u_u_release … ok` (preserved `tmpktizrd34`), `test_thematic_renewal_c_u_u_release … ok` (preserved `tmpr06nq3yv`), `Ran 2 tests in 2000.510s OK`.
  - `dm022-durable-finalB-raw.txt` exit 0: `Ran 1 test in 878.762s OK` (separate durable 1-test, not counted as FinalB CUU).
  - Exits: `exit-finalB-wrapper.txt:1`, `exit-finalB-wrapper2.txt:0`, `exit-durable-finalB.txt:0`.
- Wrapper pins (both runs, `pins-wrapper-20261029T153125Z.json` pid 1445939 and `pins-wrapper-20261029T153146Z.json` / `wrapper-result-20261029T153146Z.json` pid 1448460): `frozen=.rephase-1-editorial-runtime/dm022-full-lifecycle-finalB-20261029T060000Z`, `HEAD=409b292…`, `B2_agent=d801feb679c99d2e`, `A_HIGH=f8af03cc5d58af10`, `B_human=101792ad8070607e`, `B_orch=491888fe2d089edb`, `B_bridge=2fd8a6a24569333c`, `C2_pub=705bcee32557a634`, `C2_release=b9433b9efeca0275`, `LOW=2aef837faaa549b9`, `own_test=e41df24f2509a223`, `runtime=3.14.4`. 8-prefix equality holds, but verification below uses full SHA, not prefixes alone.
- Private exec vs delivery (byte `sha256`, read-only):
  - FinalB: **768/768 MATCH, 0 missing, 0 diff**.
  - Finalsrc (`.rephase-1-editorial-runtime/dm022-g71-g76-finalsrc-20261029T152924Z/`, HEAD `409b292…`): **768/768 MATCH, 0 missing, 0 diff**.
  - 13 role files (HIGH/LOW/agent/human/orch/bridge/pub/release/refresh/ed/H/S/own_test) all MATCH delivery in both execs (full SHA, §1).
  - No old-module imports, no missing runtime in either exec. `b650` appears in neither exec nor delivery.

## 3. Retained C proof — CURRENT closure vs DELIVERY (not report 8-prefixes)

- Preserved dirs: `c-visual-tmpktizrd34-20261029T153146Z/renewal-c/ren-weekly-cuu-c-v2/` (PDF `a5584e2b…` 67729B) and `c-visual-tmpr06nq3yv-20261029T153146Z/renewal-c/ren-thematic-cuu-c-v2/` (PDF `f2f9fc7f…` 85830B). Each has `renewal-source-proof.json`, `renewal-basis.json`, `validated-source-manifest.json`, `build-record.json`, `publication-candidate/set`, `reader-manuscript/gate`, `quality-bundle`, `staged-source/{main.tex,references.bib,jgaisurvey.sty}`, `retained/before`, `renewal-c-reviews/`.
- Stored CURRENT closures compared row-by-row to delivery manifest full SHA:
  - Weekly `renewal-source-proof.json:dependency_closure`: **70/70 MATCH, 0 mismatch**.
  - Weekly `validated-source-manifest.json:current_tools.closure`: **70/70 MATCH** (repo_commit `e1028f69…`, temp fixture commit, gone — see §5).
  - Thematic `renewal-source-proof.json:dependency_closure`: **70/70 MATCH**.
  - Thematic `validated-source-manifest.json:current_tools.closure`: **70/70 MATCH** (repo_commit `d8120949…`, temp fixture commit, gone).
  - Total checked: 280 rows, 0 mismatches. Includes all implicit tools/schemas: 39 `scripts/*` rows (incl `survey_agent_control d801`, `survey_prearchitecture_acceptance f8af`, `survey_research_authority 2aef`, `survey_publication 705b`, `survey_editorial_publication 3a87`, `history a9de`, `source b139`, plus architecture/completeness/discovery/drafting/evidence/handlers/longform/quality/reader/schema/screening/stage/versioned/weekly/x etc.), `config/survey-production-v2.json 95fe3c28…`, `.latexmkrc 18199fd8…`, 30 `schemas/*` (incl 5 `dm022-*`, editorial, publication, reader, quality, discovery, renewal, weekly sets). Full list in data JSON.
  - Drivers NOT in closure (by design, not a diff): `survey_human_gate 1017`, `survey_orchestrator 4918`, `survey_core_execution_bridge 2fd8`, `survey_release_checkpoint b943`, `survey_weekly_mechanical_refresh dd01` — these are execution entry/driver files, proven via private-exec 768/768 equality (§2), not via 70-row renewal closure.
- `supported_contract` pipeline `3adfbda2…`, quality `b5b955d5…`, research `666f8a06…` (weekly) / `0f575e6d…` (thematic), publication `99adff93…` (weekly) / `a6859559…` (thematic). `supported_source_bindings` schema SHAs (e.g. `editorial-manuscript-spec 043ce8a5…`, `editorial-correction-proposal 5623c0d9…`, `build-record b7c82476…`, `publication-set 7beebcef…`, `source-manifest 494a1d15…`, `retention 347e5499…`, `reader-surface-semantic e8598239…`) all match delivery schemas.
- `exact-original-target-paths.json` per route records PDF/trio/proof/manifest paths + SHA + bytes (weekly trio `b0437b09…`/`4c832136…`/`035645ca…`, thematic trio `f394b247…`/`594e229e…`/`035645ca…`).

## 4. Raw fixture-bound subprocess / import-path scope (exact)

- Wrapper `sys.path.insert(0, REPO_ROOT)` where `REPO_ROOT=CWD` (must be new private freeze). Test `REPO_ROOT=Path(__file__).resolve().parents[1]` (single `__file__` in test file, line 46). No `module.__file__` dump, no `RuntimeBinding` log, no `inspect.getfile(core).startswith(fixture_root)` assertion in FinalB raw (`grep __file__|RuntimeBinding|inspect.getfile` over FinalB evidence returns only wrapper/test boilerplate, no per-import path log). G71 probe pattern (`inspect.getfile(core).startswith(fixture_root)`) exists only in `g71-finalsrc-probe`/`g71-final-probe`, not in FinalB CUU raw.
- Therefore: live import-path proof is NOT directly logged in FinalB raw. Binding rests on (a) wrapper pins (8 prefixes + HEAD + pid + run_stamp), (b) retained C CURRENT closures 70/70 vs delivery (§3), (c) preserved private-exec 768/768 vs delivery (§2) with `REPO_ROOT=CWD` insertion, (d) preserved PDFs/build trio with hashes. This is content-equality binding, not logged-loader binding.
- Temp fixture DBs ` /tmp/tmpktizrd34`, `/tmp/tmpr06nq3yv` gone (verified absent; `TemporaryDirectory` cleanup after retention copy). Do NOT claim their Git objects exist. Retained proof `retained/before/sources/*/production-state.json` + `renewal-basis/before_state_ref` preserve pre-state bytes, but not live DB objects. `validated-source-manifest.current_tools.repository_commit_sha` (`e1028f69…` weekly, `d8120949…` thematic) refer to gone temp fixture commits — metadata-only, not verified, not used as binding.
- Preserved Git objects that ARE claimed (read-only verified): private FinalB `.git` HEAD `409b292…`; finalsrc `.git` HEAD `409b292…`; durable 162124Z fixture DBs HEADs `bf9e7e5a…`/`4456769f…`/`1e95441f…`/`f1bd3768…` (see §5); finalsrc keep `/tmp/dm022-g71-keep-xg8lc364` HEAD `df02a53e…` (still present, see §6). No other Git objects claimed.

## 5. Durable `162124Z` — actual fields + B650/D801 + HIGH 3d1/f8 (objective, no TIME arithmetic)

- File: `evidence/full-lifecycle-v2-fixture-manifests/durable-versioned-20261029T162124Z/durable-fixture-manifest.json` (`recorded_at 162124Z`, `schema_version 2.0-rc1`, `producer General whole-lifecycle witness`, `candidate_HEAD 409b292…`).
- `source_pins`: `B_agent b6506a8b334408bc99c5baff655afe0e5719817aa89bf4efd40429153b5f2638`, `C2_editorial 3a8721569d3cb151…`, `C2_publication 705bcee32557a634…`, `C2_refresh dd01fa01c9744866…`, `C2_release_decoder b9433b9efeca0275…`, `H_history a9de2c97eb40e358…`, `S_source b139f493f791cdcd…`. No HIGH/LOW/human/orch/bridge pins in this manifest version.
- Objective file-SHA test:
  - `b6506a8b…` matches NOTHING in delivery 768 (verified scan). Delivery agent is `d801feb6…` / 199521B. Per `independent-evidence-ledger` / `independent-final-operation-review`, `b650` = 195749B pre-B2 snapshot (`60aaaee` 764f era, agent `b650`, HIGH `3d1d87d8` 88792B), superseded by B2 rollback `d801` (199521B) + HIGH `f8af03cc` (88603B). Wall-clock order (`162124Z` vs `180000Z`) is NOT used as evidence; byte equality is.
  - `C2_editorial/pub/refresh/release/H/S` all MATCH delivery full SHA (§1). So 6/7 durable source_pins match delivery; **1/7 (`B_agent`) is OLD stencil**.
  - HIGH `3d1d87d816a712bc9822d071ba4e6f5bd7b051e44884efbb9ae8aca22621dd9` (old, 88792B, in `review-source-manifest 60aaaee`, `late-guards`, `full-lifecycle-v2-final-20261029T053058Z` C proofs) vs `f8af03cc…` (new, 88603B, delivery + FinalB exec + closures). `3d1` matches nothing in final delivery except as historical record; classify OLD.
- Actual durable worktree bytes CONTRADICT the stale manifest pin (read-only):
  - `dm022-durable-validated-prepreview-weekly-20261029T162124Z`: git HEAD `bf9e7e5a…` (matches manifest), worktree `scripts/survey_agent_control_v2.py d801…` / 199521B, `HIGH f8af…` / 88603B; `git cat-file -p HEAD:scripts/survey_agent_control_v2.py | sha256sum` = `d801feb6…`, `ls-tree HEAD` blob `77479f2b…`.
  - `dm022-durable-versioned-active-prepreview-weekly-20261029T162124Z`: HEAD `4456769f…` (matches), files `d801`/`f8af`.
  - Thematic pair: HEADs `1e95441f…`/`f1bd3768…` (match manifest), files `d801`/`f8af`.
  - Hence durable fixtures on disk bind NEW code, while `durable-fixture-manifest.json:source_pins.B_agent=b650` is stale metadata. **Classify `b650`/`3d1` as OLD, not final-code proof. Do NOT use manifest pins alone.**
- Durable PDFs/sets/heads/trees/state_shas in manifest (`weekly validated 97b3bf6e…` 68035B, `weekly editorial df8b9c82…` 68270B, `thematic initial 1507436d…` 85152B, `thematic editorial d19144e1…` 86156B, heads `bf9e…`/`4456…`/`1e95…`/`f1bd…`, trees `e3067b97…`/`ad275952…`) are metadata-only here (PDF bytes not re-hashed in this verifier; heads verified via `rev-parse`, worktree agent/HIGH re-hashed, full PDF re-hash out of scope and not claimed).

## 6. G71 finalsrc — 40 TOOL + 115 KEEP, 760 vs 768, followup exit1 vs release exit0

- Source: `final-source-compatibility-confirmation.md` (G71→G76 narrow Weekly U) + `evidence/g71-g76-finalsrc-20261029T153000Z/` + private `dm022-g71-g76-finalsrc-20261029T152924Z/` (768/768 vs delivery, §2) + keep `/tmp/dm022-g71-keep-xg8lc364` (still present, HEAD `df02a53e67f7826449d1ea590b75b31d29de9a01`, parent G71 `d3444c422114…`, files `d801`/`f8af`, `status 0` at commit per stdout).
- TOOL overlay: `tool-overlay-40.txt` 40 files (1 config +5 `dm022-*` schemas +2 new modules +32 mapped scripts, list in data JSON). Verified **40/40 MATCH delivery** in both FinalB and finalsrc execs; `missing_in_delivery=[]`. Full 40 list includes `config/survey-production-v2.json`, 5 `schemas/dm022-*`, `survey_prearchitecture_acceptance`, `survey_research_authority`, `survey_agent_control d801`, `human 1017`, `orch 4918`, `bridge 2fd8`, `release b943`, `publication 705b`, `refresh dd01`, plus editorial/retention/staged/evidence/handlers/drafting/architecture etc.
- 760 vs 768: confirmation text says `760 intended files` for finalsrc freeze; actual preserved finalsrc worktree counts **768** (excl `.git`/`__pycache__`/`*.pyc`), identical to delivery 768. The 8-file gap is tests-only bookkeeping in prose, not a runtime gap — all 40 TOOL + all 768 delivery files match (§2). Omission is therefore not a problem, stated as qualified prose drift, not a blocker.
- KEEP 115: `g71-finalsrc-20261029T153010Z.stdout.txt` records `G71 upstream pins (expanded, all materialized): 115` and `G71 upstream unchanged after G76 overlay … OK`, `G76 epoch df02a53e…`, `G71 closure 63 → G76 70 delta 7`. Keep fixture `/tmp/dm022-g71-keep-xg8lc364` still exists with HEAD `df02…`, so epoch commit is preserved here (unlike FinalB temp DBs). The 115 per-file SHAs themselves live only in that stdout + probe memory, not re-hashed here (fixture still on disk but full 115 re-inventory out of data-only scope and not claimed beyond stdout record).
- Exits: `g71-finalsrc-20261029T153010Z.exit 0` (U finalize OK, 7 paths), `g71-followup-20261029T153305Z.exit 1` (OLD script wrong release-checkpoint args — harness bug, core `ACTIVATE` + `Candidate→RELEASE_CANDIDATE→Preview→Freeze→FROZEN` + `Merge/Release OK` verified before failure, preserved), `g71-release-20261029T153449Z.exit 0` (`FROZEN→RELEASED` via FIXED decoder `b943`, `PUBLIC` green, `CURRENT` repeat true, `KEEP … lifecycle=RELEASED`). Exit 1 is qualified intermediate, superseded by correct release script — recorded as qualified, not masked, not a runtime blocker.

## 7. Binding verdict — which runtime binds the successful terminal run

- Successful terminal run = `dm022-finalB-wrapper-raw2.txt` (2 tests, 2000.510s, exit 0) from private exec `dm022-full-lifecycle-finalB-20261029T060000Z`.
- That exec binds, by preserved bytes (no conditional):
  - 768/768 vs delivery (§2), incl all 13 roles full SHA (§1).
  - 40/40 TOOL vs delivery (§6).
  - Retained C closures 70/70 ×4 vs delivery (§3).
- Durable `162124Z` manifest does NOT bind the terminal run for `B_agent` (stale `b650`); its 6 other pins do match, and its on-disk durable worktrees DO bind NEW (`d801`/`f8af` + HEADs match manifest). Use worktree bytes + FinalB exec bytes, never manifest pins alone.
- All roots available are DURABLE source metadata only in the sense of §4–§6 limits: no rebaseline, no data repin, no edits performed here.

## 8. Essential-gap assessment (blocking vs qualified)

- BLOCKING if relied on alone: `durable-fixture-manifest.json:source_pins.B_agent=b650` + any `HIGH=3d1` record — stale, must not be cited as final-code proof. Resolved by preserved NEW bytes (§2/`§5 worktrees), so terminal-run binding itself is NOT blocked, but pins-alone citation IS blocked.
- Qualified (not blocking, explicitly limited): (a) no logged `module.__file__`/`RuntimeBinding` paths in FinalB raw — import binding is content-equality + `sys.path` insertion, not logged-loader proof; (b) FinalB temp fixture Git objects gone — `repository_commit_sha e1028/d812` metadata-only; (c) 115 KEEP SHAs stdout-only (though keep `xg8lc364` HEAD `df02` preserved); (d) durable PDF bytes not re-hashed here; (e) 760-prose vs 768-actual tests count drift (§6); (f) first wrapper exit 1 (CWD fault) + G71 followup exit 1 (old-script args) preserved as qualified intermediates, superseded by exit-0 runs, not masked.
- No new Git mutation, no network, no Human readback performed. No files edited except this verification pair.

## 9. Outputs

- This file + `final-run-source-binding-verification.json` (counts, full SHA tables, 40 TOOL list, 70-row closure summary, mismatch arrays — all empty except durable `B_agent` stale).
- All other packets/reports untouched.
