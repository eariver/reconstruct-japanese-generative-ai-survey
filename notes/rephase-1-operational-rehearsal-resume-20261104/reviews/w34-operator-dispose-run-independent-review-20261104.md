# Independent source review — W34 dispose+run wrapper (source-only, NO execution)

**Role:** New independent reviewer. NOT author/operator, NOT Astra/root, NOT Sol/Luna/Human.

**Bounds:** Source/data-only, no active/project runtime imports/execution/tests, no network/Production/reconstruct Git (`git -C .` never used)/readback, no subagents. `Read` + `sha256sum` + stdlib `json` text inspection only. Wrapper/launcher/checks NOT executed. Active source read only at `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`. Packet captures as DATA. Creates only NEW review files. No removal/retry authority.

**Files reviewed (programmatic full SHAs):**
- Wrapper `w34-operator-dispose-run-20261104.py` `68253077b0f10a3bd17b9c1ecce23e459c06489397ff7641c9be07396d5ae7bd` 43406B
- Launcher `w34-dispose-run-launcher-20261104.sh` `eaac10f7f7f0b8ec1a3559ec42ab048343e3c6c1115a810223fa8a13b2ca4076` 1079B
- Checks `w34-dispose-run-checks-20261104.py` `284edbe6fa81f9e1272862895907c85e35c344478142ec356b2d029716d0041c` + raw 19/19 PASS (counts/READY/archival only — NOT destruction proof, see §5)
- Manifest UNCHANGED `cede7e467406b25763b9090484b31e34dc771a6c85a81e52bd19025a9db02590` 991185B 1781f/80d + 428/425; READY `473bf85bf33b9f8adaf33d0f7c588bea6bbcbe5bd7e3bd33b4772788d6788200` 5360B preflight-only 409/409; input r2 `1ea56297…` 1580317B; supp `ce6f977a…` 389414B; r6 helper `2c6f1aeb…` (verified-before-import); SP READY `c7cd05a8…` + SP DISPOSE `cf26a23c…` (snapshot only)
- Prior actual preflight `retention-W34-20261104T235848Z/` baseline 1781+1=1782 (1 NEW `interactive-evidence-w34-r2-20261104T235848Z.json` `1ea56297…`), State `7e6a50c2…` CAND, source e84 `e84a82ac…`/hist `48082356…`
- Actual e84 defs (read, not imported): `run_evidence_v2_interactive.py:560 run(repo,state,input,supp?)->dict{evidence_result_count,completeness_status}`, `survey_evidence_v2.py:523 validate_evidence_authority_supplement(repo,supp,impl,*,expected_issue/source/discovery/screening,screening_acceptance,discs)->dict`, `:1956 validate_evidence_acceptance(repo,ev_path,impl)->tuple`, `:2528 validate_edition_views_acceptance(repo,profile,ev,views,impl)->dict`, `:2770 validate_materiality_ledger(ledger,repo,profile,discovery,screening,ev,views,impl)->None`, `survey_completeness_v2.py:265 validate_profile_completeness(result,repo,profile,discovery,screening,ev,views,ledger,impl)->list`

## 1. Scope correct (exact2 + once + effective439 + SP snapshot)

- Exact2 owned CAND: `materiality-ledger-v2.json 76ac53f9…` 186202B + `profile-completeness-v2.json 93dbefae…` 71532B, both `0o664/nlink1` per manifest. P2 O_EXCL packet backups + readback + live-verified 64-char State SHA + UTC + old/new path/SHA/bytes/mode linkage; no rename onto names. P3 ledger gate (State+1782+771+manifest/READY+backups) → unlink ledger ONLY → absent+not-symlink + retained copy re-verified + State SHA64. P4 completeness gate (State+1781 ledger-absent-expected/completeness-present+pins+backups) → unlink completeness ONLY → both absent (1780) + retained copy re-verified. P5 1780 + old accepted byte-identical + State CAND unchanged. Matches required `1782->1781->1780`.
- ONE `rn.run(repo,state_path,staged_input_abs,supplement_abs)` (owns facade, no outer facade), result `evidence_result_count==409` else STOP. Post-run `ledger rows==439/effective`, `obligations==3`, `overall_status==LIMITED`, `ev 409/views 409` from files. Modes: staged + archived `interactive-evidence.json` `0o664`, others recorded umask (`0o666&~umask`), O_EXCL copies stay `0664`. No Raw/supplement change; ONLY staged r2 input consumed (1 NEW, no new Raw/supp; `new_rels len==1` enforced).
- EFFECTIVE 439 path (not root 369): `validate_materiality_ledger(ledger_doc,repo,profile,effective_path,screening_acc,ev,views,live)` + `validate_profile_completeness(comp_doc,repo,profile,effective_path,screening_acc,ev,views,ledger_path,live)` with `ctx[effective_path]` (439) from `resolve_effective->{root_records 369,records 439}`. Correct. Accepted root is `discovery-v2.jsonl` 369 lines (via `discovery-accepted`), event `event-discovery-v2.jsonl` 439 lines; effective distinct. No SP root 369 for ledger.
- Shared-repo SP preserved (snapshot only, no SP invoke): `retention-SP-…/READY c7cd05a8…` + `retention-SP-dispose-…/DISPOSE_RUN cf26a23c…` still present checked. Does NOT require SP old-state ledger — only current completed products snapshot. Correct per instruction.
- Actual dir/file names match live old accepted: `evidence/v2/accepted` + `bf208f96…` (+`tasks/results`) and `evidence/v2/views/accepted` + `f744e46b…` (+`views`); top NEW `evidence-accepted.json/package.json/interactive-evidence.json/interactive-audit.json` + `edition-views-accepted.json`; field names (`result_count/results/view_set_sha256/views/evidence_sha256/authority_supplement/interactive_input/overall_status/obligations/rows`) match live old JSON. No invented transport/schema/module.

## 2. Object shapes/signatures/context vars verified (defs, not names)

- `validate_evidence_authority_supplement(repo,supp_abs,live,expected_issue_id=ISSUE,expected_source_root=(repo/SRC).resolve(),expected_discovery_path=effective_path,expected_screening_acceptance_path=screening_acc, screening_acceptance=real_acc,discoveries=real_disc)` — arity/kw-only/shapes match def 523.
- `validate_evidence_package_basis(repo,pkg_path,package,live)` + retained 409-task `package.json` basis check — matches 1203.
- `rn.run(repo,state_path,staged_input,supp)` — matches `run(repo_root,state_path,input_path,supplement_manifest_path?)->dict`. Return `evidence_result_count/completeness_status` checked (matches `run` tail 899-903).
- Post-run `validate_evidence_acceptance(repo,ev_acc,live)->tuple`, `validate_edition_views_acceptance(repo,profile,ev,views,live)->dict`, `validate_materiality_ledger(...)`, `validate_profile_completeness(...)->list` (empty == pass) — all match defs with effective 439 + screening/evidence/views/ledger paths. `task_source` helpers not needed post-run (package already validated pre-removal).
- Archive binding: `audit.interactive_input{path==new_ev/interactive-evidence.json,sha256==staged_sha}` + archived bytes `sha==staged_sha` + `package.authority_supplement{path,sha}==existing supp` — enforced in `_check_post_run_layout` (580-589). Staged `==r2 packet` bytes already proven in preflight actual.
- Context vars: `live_impl, state_path, screening_acc_path, effective_path, disc_recs/root_recs, real_acc/disc, pkg_path/package, supplement_abs/staged_input_abs, umask/umask_file_mode` threaded correctly; no verified-dict fabrication, no global bypass. `current_stage_basis_override` owns each validation phase; `rn.run` owns its own facade.
- Permitted write-set fully enumerated: packet `retention-manifest.json/DISPOSE_RUN.json/journal.json/FAILURE.json + 2 backups` (O_EXCL, packet-contained, `DIRECTLY under packet` + `_require_absent_under`), active `2 unlinks + rn.run NEW dirs/files` only. Post-run layout rejects unexpected writes, symlink/special, mode/nlink drift, dir-set drift. No auto-restore/retry, no new checkpoints, no policy bypass.

## 3. Concrete blockers — NOT DISPOSE_AND_RETRY_READY

**B1 definite failure — invented accepted-dir fields:** `_check_post_run_layout` call passes `[d for d in manifest[original_authority].get(accepted_evidence_dirs,[])]` + same for views (lines 436-437). Manifest has NO such keys (verified: top keys lack them, text search false). `.get→[]` → `old_ev/old_view={}`. Baseline has 1 old ev dir `bf208f96…` + 1 old view dir `f744e46b…` (from `w34_tree_full` 8 dirs). Post-run `new_ev/new_view` detection (`startswith+depth==len(ev_root.split)+not in old`) will count old+new =2 → `len(new)!=1` → `expected exactly 1 NEW accepted dir` failure even on correct run. Must bind real old dirs (e.g. derive `bf208…/f744…` from `w34_tree_full` or accepted pins), not invented `.get default []`.

**B2 source rigor gap — no after-import re-hash:** P0 pins 10 modules + 771 BEFORE `sys.path.insert` + imports, but never re-hashes after import nor refuses `__pycache__` (unlike preflight r2 `_bind_roots_after_import`). Source could drift across import undetected before destructive unlinks. Must add pre/post hash compare + `__pycache__` refuse for destructive operation.

**B3 State strictness regression:** `_strict_w34_state_and_ready` uses `json.loads(...)` (line 195), not `R6._strict_json` duplicate-key strict (preflight r2 uses strict). Weaker State parsing for destructive gates. Must use strict JSON (duplicate-key refuse) for State.

Fix B1-B3 + independent re-review before any authorize. No other invented paths/fields found; backup/mode/StateSHA64/umask/retention/validator paths otherwise sound.

## 4. 19 checks scope (NOT destruction proof)

`w34-dispose-run-checks-20261104.py` 19/19 PASS covers DERIVED `369/439/439` from live files, invalid `368/438` + token-string refusal, `root369≠ledger439` (effective required), READY shape/manifest/input/supp/tasks, staged-live match, retained 409, archival `staged==r2` + mismatch refusal. No unlink, no `rn.run`, no new-dir/mode/State/layout validation. Counts/READY only — NOT actual-destruction proof. Must not be cited as dispose/run authority.

## 5. Verdict

**NOT DISPOSE_AND_RETRY_READY (source-only blockers B1-B3).** Wrapper `68253077…`, launcher `eaac10f7…`, checks `284edbe6…` valid as reviewed, but B1 guarantees post-run failure, B2/B3 insufficient rigor for irreversible `1782->1781->1780` + once-run. Preserve preflight actual `READY 473bf85b…` (still valid, no removal/retry executed here). No semantic approval, no `EVIDENCE_REVIEWED`/Selection/Architecture, no SP touch.

**NEW review path:** `reviews/w34-operator-dispose-run-independent-review-20261104.md` + `w34-operator-dispose-run-independent-findings-20261104.json` (this addendum). Human Commit Point — stop; do NOT execute until B1-B3 fixed + re-reviewed + separate Root dispose+run auth.

Attribution: Independent reviewer. No execution/network/Production/reconstructGit/project imports/subagents.
