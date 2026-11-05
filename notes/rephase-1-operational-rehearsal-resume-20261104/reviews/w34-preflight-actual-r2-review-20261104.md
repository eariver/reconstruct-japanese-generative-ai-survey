# Independent actual-run review — one authorized W34 r2 preflight (source/data-only, no execution)

**Role:** New independent reviewer. NOT author/operator, NOT Astra/root, NOT Sol/Luna/Human.

**Bounds:** Source/data-only, no active execution, no project imports, no reconstruct Git (`git -C .` never used), no network/Production, no subagents. `Read` + `sha256sum` + stdlib `json` inspection only. Invocation/READY/raw/packet/active files read as DATA. No operation launched here. No removal/retry authority.

**One authorized run reviewed:**
- Invocation `w34-preflight-invocation-20261104T235848Z.json` `c493d72ff97b675c155c3a44e9eaf8f4532a584bd291575eddb71ee50fadf0eb` exit 0, `2026-11-04T23:59:06Z-23:59:32Z`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_DIR/WORK_TREE/INDEX/OBJECT` null, isolated e84 only, no reconstruct Git/network/Production.
- Tool `w34-operator-preflight-r2-20261104.py` `0898d6bc3b24c8e89dc3286037ac659fe818704cbd6effafea694e5ad617ce68` 25129B; manifest `cede7e467406b25763b9090484b31e34dc771a6c85a81e52bd19025a9db02590` 991185B; input r2 `1ea562977534b55d3bbf2f89492411e89e22be09bc5667a450da6bf5ede2fbed` 1580317B; SP helper `2c6f1aebfae91d95ed1f10e2cae6db6e8665e653d3ec5ecd881e988cab56d664`.
- Stdout `c96f8a6066d0daf1bf71f55b4e6596dfc3806930443750fb80d1c1c831a9bd7c` `{"stage":"preflight-only","exit":0,"tasks":409,"records":409}`; stderr empty `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Retention `retention-W34-20261104T235848Z/` packet-local: `READY.json` `473bf85bf33b9f8adaf33d0f7c588bea6bbcbe5bd7e3bd33b4772788d6788200`, `journal.json` `a8eb0c024977018c8c81e10cc0f89dea74f63764512b5da79187633b7e25e94a`, `pkg-w34-r2-20261104T235848Z/package.json` `0ec312b4b66435ee09c34f982b39bf126710edb2c853d6b2915733a7fe25652c` + 409 tasks.

## 1. READY 409 + staged ONLY 1 NEW (existing 428/425 unchanged)

- READY: `ready true/preflight-only/no_removal/no_retry`, manifest `cede7e46…`, live `e84a82aca000c990597ea8cf60f548e2ff187bd1` vs historical `48082356…`, `new_input w34-r2-20261104T235848Z` rel `sources/2026-W34/evidence/proposed-input/interactive-evidence-w34-r2-20261104T235848Z.json` 1580317B `1ea56297…` mode `0o664`, supplement reused `ce6f977a…` 389414B, `state_sha 7e6a50c2…`, `task_count 409/input_records 409`, `retained_pkg_dir pkg-w34-r2-20261104T235848Z`, `package_json_sha 0ec312b4…`, journal `phase1 pass/stage-input/package+validate-input 409/409/finish-authority-phase pass`.
- Staged active file bytes identical to packet r2 (`sha256sum` live staged `1ea56297…` == packet `1ea56297…`, 1580317B). Live `proposed-input/` contains exactly 2 files: original `interactive-evidence.json` (preserved) + 1 NEW `interactive-evidence-w34-r2-20261104T235848Z.json`. No overwrite of `bf208f96…/f744e46b…`.
- Live W34 tree 1782f/80d = baseline 1781f/80d +1; extra set exactly the 1 NEW input, 0 missing. Old runs/Ledger/Completeness untouched.
- Supplement active `ce6f977a…` 428 sources / 425 distinct Raw (parsed, not token), hash matches manifest + READY. No new supplement staged. Package `authority_supplement{path,sha256=ce6f977a…}` + `basis{state/discovery/profile/screening paths+SHAs}` + 409 tasks (`evidence_task_id/path/sha256/discovery_ids/authority_supplement_source_ids`).
- No `FAILURE.json` in retention; stdout exit 0, stderr empty. No removal/retry executed.

## 2. Old State/Profile/CP/Human/Ledger/Completeness/accepted + source 771 same

- Live State `7e6a50c2…` == manifest, `CANDIDATES_NORMALIZED`, impl `48082356…`, machine evidence/materiality/completeness pending, cp null, human pending/pending + provenance null/null. Profile `2a8c3089…`, Ledger `76ac53f9…`, Completeness `93dbefae…` all match manifest pins.
- Authority DCP/accepted/SCP/event all match manifest: `dcp_jsonl discovery-v2.jsonl e176326f…` 963155B, `dcp_accepted discovery-accepted-v2.json 255fb12d…` 377589B, `scp_accepted screening-accepted.json b9d963d8…` 543880B, `scp_event event-discovery-v2.jsonl 0a23be47…` 1335444B. Accepted `bf208f96… evidence-accepted.json 450b508c…` preserved (sample). Checkpoints `DISCOVERY_COLLECTED/ISSUE_INITIALIZED` pinned. Source 771 per invocation `770 ok +1 known test d486 vs 7b862305, 0 missing` + terminal intended recheck in wrapper (no drift → READY).
- SP19 preserved: `retention-SP-20261104T162747Z/READY.json` `c7cd05a888106b2cdf0f4e984fb22412678a8ff792deda1ad7ff94e3b31e7643` exists 12270B, no SP invoke in this run.

## 3. Real validator call path (from wrapper source + READY journal, not re-execution)

Wrapper r2 `0898…` calls real public APIs inside `current_stage_basis_override`: `disc.validate_acceptance→repo_local_path→resolve_active→resolve_effective→validate_screening_acceptance→prepare_evidence_package→validate_screening_acceptance→_resolve_phase_supplement_context→_capture_phase_pins→_discovery_task_sources/_merge→validate_interactive_input→_finish_authority_phase(revalidate_owner=validate_evidence_package_basis)`. Journal `package+validate-input tasks 409/records 409/runner Muse Spark` + `finish-authority-phase pass` confirms full input/supplement facades ran with real `run_ctx[entries]` (not dummy). No caller verified-dict, no third validator, no `run()` retry. Source `0898…` pin verified before import per invocation.

## 4. Correction — rootpath mislabel in prior r2 addendum

Prior r2 review §0 mislabels `root_path` as `screening/input/event-discovery-v2.jsonl` 439 lines. Correct:
- Accepted root = `discovery/discovery-v2.jsonl` 963155B 369 lines (via `discovery-accepted-v2.json{discovery_path,record_count 369}`), single-JSON parse fails (JSONL), 369 records.
- Event input = `screening/input/event-discovery-v2.jsonl` 1335444B 439 lines, single-JSON parse fails, 439 lines.
- Effective = `resolve_effective->{root_records 369, records 439}` distinct (DIRECT or DERIVED_EXPANSION both return both keys); r2 enforces `len(root)==369/len(disc)==439` + screening `record_count/decisions==439`. R1 defect remains certain failure (`_strict_json` on 369-line JSONL), but file identity is accepted-root 369, not event 439. Both JSONLs fail single-JSON; distinction matters for authority (accepted root vs effective expansion). Prior verdict logic unchanged, file label corrected here.

## 5. Verdict

**ACTUAL_PREFLIGHT_VALID narrow (preflight-only, STOPS at READY).** One authorized run `20261104T235848Z` valid: exact pins (tool `0898…`, manifest `cede7e46…`, input `1ea56297…`, supp `ce6f977a…`, READY `473bf85b…`, package `0ec312b4…`), 409/409, ONLY 1 NEW staged, 428/425 reused unchanged, all old State/Profile/CP/Human/Ledger/Completeness/accepted + 771 same, SP19 preserved, real validator path. No semantic PASS, no Selection/Architecture/Draft/PDF/R4, no adoption/savings, no removal/retry authority. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN.

**NEW actual review path:** `reviews/w34-preflight-actual-r2-review-20261104.md` + `w34-preflight-actual-r2-findings-20261104.json` (this addendum). Human Commit Point — stop.

Attribution: Independent reviewer. No execution, no readback/network/Production/project imports/subagents.
