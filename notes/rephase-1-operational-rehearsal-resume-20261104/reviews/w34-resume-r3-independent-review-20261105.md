# Independent source review — W34 resume r3 (source-only, NO execution)

**Role:** New independent reviewer. NOT author/operator, NOT Astra/root, NOT Sol/Luna/Human. Preserves r1/r2 reviews untouched.

**Bounds:** Source/data-only, no active/project runtime imports/execution/tests/writes, no network/Production/reconstruct Git/readback, no subagents. `Read` + `sha256sum` + AST/text inspection only. Wrapper/launcher/checks NOT executed. Active source read only at e84 candidate-work. Creates only NEW r3 review files.

**Files (programmatic full SHAs):**
- Wrapper r3 `w34-operator-resume-r3-20261105.py` `9072acff864a718ba24f1c31dd29176686f25fc73ec428107b18a53fdcf42f43` 44856B
- Launcher r3 `w34-resume-launcher-r3-20261105.sh` `c25008bb736aeb00aeac73c53b572c7c0e88c5f66e0d6410b2e94c282ea18398` 1074B
- Manifest UNCHANGED `w34-resume-expected-manifest-20261105.json` `13a3871067bedaa03c6208d31ac6a99ef4d3ea59d6abc2df58d6ae716cd6a1de` 807341B 1780f/80d; input r3 `15e87eef…` 409; preflight READY `473bf85b…`; supp `ce6f977a…`; r6 `2c6f1aeb…`; dispo-r3 `48be5879…` (stdlib import verified, disposal never executed)
- Oracle r3 `15bceeda…` + raw 6/6 PASS (helper scope only — D3/fixture/counts, NOT run proof, see §4)
- Actual e84 defs (read, not imported): `_build_card_core(task,meta,package,record,runner,source_authorities)`, `_validate_card_core(card,task,task_sha,package,get_sources)`, `rn.run(repo,state,input,supp?)->{evidence_result_count,completeness_status}`, `D3._check_post_run_layout(repo,src,base_plus1,base_dirs,staged_new,old_ledger,old_comp,old_ev_names,old_view_names,409,input_rel,sha,supp_rel,sha,439,3,LIMITED,umask)`, validators with EFFECTIVE439

## 1. R2 NameErrors fixed + Root adaptation (no regressions)

R2 full branch called bare `_derive_old_accepted_dirs` (undefined) + bare `LEDGER_REL/COMP_REL` (undefined) → `NameError` before post-layout. R3 defines `LEDGER_REL/COMP_REL` module globals + `_derive_old_accepted_dirs_resume` (ORIGINAL pinned `cede7e46…` hash-verified, frozen `w34_tree_full` + accepted pin parents, returns DIR NAMES per D3 join convention, never calls D3 derive which requires `w34_tree_full` resume lacks, never fakes `accepted_evidence_dirs` defaults). Diff r2→r3 = docstring + LEDGER/COMP/BACKUP consts + derive + pre-READY guards + post-run adaptation + terminal pins only; destructive guards (`2 unlinks` — none here, `1 rn.run`), card-core 409, facade, SP anchors, umask, journals otherwise identical. No new network/Production/Git, no top-level project imports (`sys.path/from scripts` only inside `stage_resume` after fail-closed gate), no `os.unlink`/`write_json` State writes.

## 2. Manifest coherence + post-layout wiring (real fields, no defaults)

- Resume manifest lacks `w34_tree_full` (has `w34_tree_current` 1780/80); D3 derive requires full — r3 never calls it. Old dirs from ORIGINAL `cede7e46…` (hash-checked live, 1+1 `bf208…/f744…` + pin-parent cross-check), DIR NAMES to match `D3._check_post_run_layout` (`{ev_root}/{d}` join). Discovered from real frozen dirs + accepted pins, P1 asserted + pre-run re-derived equality gate. No invented defaults.
- Baseline 1780 excludes old2 (CONTINUE ABSENT, absent verified pre/post). D3 unadapted expects old2 in baseline for regen compare (`exp_old None` fail — proven by r3 oracle fixture). R3 supplies obs-only `_obs_old2` from PINNED backups (`76ac…/93db…` bytes/mode/nlink, no claim originals exist live) + `base 1780+new input`; D3 preserved loop skips old2 rels, regen check `live sha != backup sha` proves regeneration, `mode==umask/nlink1`. No fake files.
- Call matches D3 signature exactly (17 args, `old_ev/view_names`, `409/input_rel/sha/supp_rel/sha/439/3/LIMITED/umask`). Field payload coherent: `baseline=w34_tree_current` + NEW, `old2=backups_pinned`, `old dirs=orig w34_tree_full names`, validators `effective_path (439)/screening_acc/ev/views/ledger` + `archive path+sha==staged` + `supp==ce6f…` + `umask`. Terminal post pins AFTER validators: source771 + State + old baseline inputs/supp + manifest SAME hash + new Ledger/Completeness post-SHA + strict State resume, before `journal.json` terminal record. READY (`preflight-journal.json` + `READY.json` O_EXCL distinct) vs final `journal.json` distinct paths; failure logger absolutizes packet path (`rdn=normpath(absolute)`, PACKET containment, `O_EXCL|O_NOFOLLOW 0664`, `error[:4000]+partials` unmasked, numeric 2).

## 3. Card-core 409 + single run (no publish, semantic later)

SAME `_build_card_core(task,meta,package,by_id[did],runner,_auth)` / `_validate_card_core(card,task,meta[sha256],package,lambda)` ALL409 real tasks (exact target sets, `363/38/8` preserved; oracle proves r3 0 mismatch, tamper detected pre-write). `private _finish_authority_phase` under current facade; retained `card-{did}.json` actual `core.json_bytes` packet-local (NOT publish, no view-shape claim). Input/task binding via real `validate_screening/_resolve/_capture/_discovery/_merge` + `validate_interactive_input(...,discovery_records=439/root=369)`. No `os.unlink`, no restore, no State/CP/Human/source/schema writes. ONE `rn.run(repo,state_path,new_input_abs,supp)` only after full preflight + pre-READY + pre-run rechecks; outputs semantic read comes later (this review claims NO semantic PASS).

## 4. Oracle 6/6 scope (NOT run proof)

`d3_pinned_import`, `unadapted_fails_resume_shape` (real D3 + resume-shaped fixture MUST fail), `adapted_passes_with_obs_old2` (439 rows/2 tasks bindings), `r2_failclosed_and_schema10`, `real_R369_E439`, `r3_packet_15e87eef` — stdlib file/fixture/AST only, no project runtime/Git. Helper scope, NOT actual destruction/runner proof. Do NOT cite as run authority.

## 5. Verdict

**RESUME_AND_RUN_READY (source-only, single bounded FULL resume).** Wrapper r3 `9072acff…`, launcher `c25008bb…` valid: B1/B2 fixed, manifest coherence + post-layout adaptation + terminal pins correct, no invented defaults, no regressions, no redundant gates. Preserves r1/r2 + preflight-actual. No semantic PASS, no `EVIDENCE_REVIEWED`/Selection/SP mutation.

**Authorized-next (ONE bounded Root auth AFTER this review, NOT now):** Run `w34-resume-launcher-r3-20261105.sh` with NEW packet retention + manifest `13a38710…` + tool `9072acff…` externally recorded (tool self-checks `__file__`), NEW `w34-r3-*` input ID. `--prepare-only` stops at READY; without it same invocation continues full guard+run. STOPS at `journal.json`/`run-complete` or first `FAILURE.json` (preserve partials, no restore/retry). Human Commit Point — stop.

Attribution: Independent reviewer. No execution/network/Production/reconstructGit/project imports/subagents.
