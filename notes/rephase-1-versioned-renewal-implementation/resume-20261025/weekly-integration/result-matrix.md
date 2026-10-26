# Weekly integration — result matrix (FIXED 736 INPUT, Weekly only)

HumanHEAD `f84fcf5` (clean except packet, verified at start). Selected contract `478f0051` incl §11, ROOT `7d7d5a45` §6 binding. FIXED INPUT READONLY `.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work` (736 intended, manifest `resume-20261025/final-integration-input.json` SHA `e4401779008a62481c7946ebdf033e54d95521e59718778402961e8dcbf5a6f1`, all-file pin `d7d7f6df...`). H `70bcdbb...`, S `20f63eaf...`, HIGH `9a0469ef...`, PUB `90d90738...`, Reader `098a2c82...` (all verified via dst-hash-intended, 736/736 bytes identical, see warmup).

No candidate/INPUT/other-route edits. Only NEW independently cloned fixture DB + WEEKLY harness/evidence. No ordinary candidate/reconstruct commit/network/old-runner exec/cleanup/cache-purge/git-reset/clean. Fresh Python process after EVERY tool commit (subprocess CLI, no stale imports). Unique UTC dirs + raw `*-exit.txt`/`*-stdout.txt`/`*-stderr.txt`/`commands.log`/source identity each milestone.

## Fixture provenance chain

- Bootstrap READONLY genuine old R3: `.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly` HEAD `721a04d85532d7855f3e54cc411f5847c787726e` (721 files, old E uncommitted 127+2 ignored incl PDF/log, real 5-page PDF `0684697f...` 61239B, r1 `65246288...` VALIDATED_DRAFT).
- Clone byte-independent: `.rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly` via `git clone --no-hardlinks`, remote inert `https://example.invalid/versioned-renewal-weekly-integration.git`, own absolute gitdir, no `objects/info/alternates`, `nlink==1`, `dev:ino` disjoint from BOOT (0 overlap), no inherited `GIT_*`, E copy exact 129 files SHA `E_HASH_UNCHANGED` (see `setup-20261025T052132Z/e-hash-boot.txt` vs `e-hash-verify.txt`).
- Overlay EXACT 736 INPUT filenames/modes (`dst-hash-intended-stdout.txt` 736 lines, SHA `d7d7f6df...`), `OVERLAY_BYTES_OK`, bridge `0o775`, SOURCE-only `git add` 47 paths (32M+15A? 47 staged, overlap with E 0), E remains untracked. G1 commit `85eac6f4e2c042c45603552a729770683982c7be` (parent `721a04d`, ancestor OK, HIGH `9a0469ef...` 202862B, tree `025a0673...`). See `setup-20261025T052132Z/commands.log`.
- G2 `cec67e5` (eligible Core+style comment, style `a4bd135a...` 6654B vs old `035645ca...`, HIGH unchanged `9a04...`, tool `survey_weekly_derivation_v2.py` comment). G3 `1a0d587` (impl-only H comment, broken syntax preserved) + fix `e8bf1b9` (docstring, parse OK). G4 `296c460` (impl-only S comment). Artifact `b2644a1` (G1→G2) + `6141dad` (G4→now, readback only). Current HEAD `6141dad65f985f246cd6cbd766d1afbf250ab296`, tree `594da22644b562639b8740629b49c082bec69da5`, ancestry `721a04d→85eac6f→b2644a1→cec67e5→1a0d587→e8bf1b9→296c460→6141dad` (all `merge-base --is-ancestor` 0). Status untracked-only E + `sources/` + `surveys/` (129 E files, no staged). No candidate/INPUT mutation. Code changes NONE to shared candidate/INPUT (fixture-only tool commits as ordered).

## Warmup (Python3.14.4, TeX local, JSON schema, PDF)

- `setup-20261025T052132Z/warmup-20261025T052132Z/warmup.json` exit 0: HIGH/H/S/PUB/Reader all `match true`, import root `.../renewal-weekly/...` OK, recipe markers `$pdf_mode/$lualatex/$biber/$max_repeat` true, TeX `lualatex/biber/latexmk` rc 0 (TeX Live 2026, `/tmp/opencode/jgas-texlive-20261019T133205Z/...`), `jsonschema 4.23.0`, `pypdf` OK, old PDF 5 pages 61239B, State VALIDATED_DRAFT r1 `65246288...`.

## Step1 — bootstrap U (G1, REUSE_TARGETS) + controls — SUCCESS

Dir `step1-20261025T052508Z`, all `*-exit.txt` 0 unless noted REFUSE (expected 2):

- `s1-prepare-u1` 0 (`high-u1-weekly`, REUSE_TARGETS, basis `f49f34...`? Actually `94c663...`? See stdout).
- `s1-qa-u1` 0 (fresh QA, synthetic fixture labels, exact current bytes, 3 checks).
- `s1-finalize-u1` 0 (`REUSED_TARGETS`, set `180de57d...`, receipt, bundle, gate, candidate).
- `s1-validate-set` 0, `s1-validate-receipt` 0 (CURRENT).
- `s1-activate-u1` 0 (`ACTIVATED r2`, record `sources/.../publication-surface-revalidation-r2.json`, observed new, reason truthful Core-change, executor weekly-integration-step1).
- `s1-history-u1` 0 (`HISTORICAL_IDENTITY_VERIFIED` 2 refs EDITORIAL+U1, `schema_pointer ""`, FILE SHAs).
- `s1-live-state` 0 (strict LIVE `agent.validate_agent_state` PASS on same bytes, no pending).
- Old receipt stale note: old editorial receipt `6bce5aa7...` tool epoch `721a04d` vs current `85eac6f`, HIST passes, CURRENT stale expected (recorded, not re-probed with old tools).
- Artifact-only `b2644a1` descendant control PASS: `s1-art-commit` 0, `s1-history-after-artifact` 0 (readback only, same r2, no new renewal reason).
- `s1-activate-already` 0 (`ALREADY_ACTIVE r2`, readonly canonical path, no new record, strict CURRENT set validate/readback).
- `s1-activate-alias-refuse` 2 (`HIGH_PATH` REFUSED_PRE_WRITE `renewal publication set must be repository-relative: './sources/...'`, NOT ALREADY_ACTIVE).
- `s1-prepare-state-alias-refuse` 2 (`HIGH_PATH` REFUSED_PRE_WRITE `Production State must be repository-relative: './sources/...'`).
- `s1-activate-empty-reason-refuse` 2 (`ARGS` REFUSED_PRE_WRITE truthful Core-change reason required).
- `s1-finalize-wrong-qa-refuse` 1 (traceback `BASIS_DIGEST_MISMATCH: LIVE State must equal fresh before_state` – State already r2, old basis expects r1; still REFUSED, no write, preserved).

Step1 verdict: SUCCESS (bootstrap U + HIST+CURRENT + LIVE + artifact readback + ALREADY_ACTIVE + alias/style/reason/wrong-target controls as required; wrong-QA refused albeit via State-moved code 1, still no-write).

## Step2 — G2 genuine Core+style, old T pass, U refuse, fresh C real build — SUCCESS (C) + expected U REFUSE

- G2 commit `cec67e5` (see `g2-commit-20261025T060000Z/commands.log`): style `a4bd135a...` changed, contract/schemas unchanged, HIGH `9a04...` same (tool epoch moves via `survey_weekly_derivation_v2.py` + style).
- Old style T pass: step1 U1 PASS at `85eac6f` (old style `035645...`) without editing old authority (preserved).
- U reuse attempt `high-u2-weekly` (prior r2, new G2 tools, old trio):
  - `s2-u-prepare-refuse` 0 (prepare succeeds, REUSE request).
  - `s2-u-qa` 0 (fresh QA on old trio).
  - `s2-u-finalize-refuse` 2 (`PROOF REUSE_TARGET_MISMATCH` `current style template changed vs retained trio.style (U keeps old style refuses; fresh C allowed; not merely closure-contains-new-style while U keeps old)`). Keeps failed U root inert (`high-u2-weekly/` basis retained, no activation, no deletion, new ID for C).
- Fresh C `high-c1-weekly` (prior r2, RENDER_TARGETS, toolchain `lualatex-biber-lualatex` local `/tmp/.../lualatex`, recipe `.latexmkrc` markers OK, TMPDIR workspace-local `.../tmp-tex`):
  - `s2-c-prepare` 0, `s2-c-targets` 0 (REAL TL2026 build, disposable `mkdtemp`, 4 cmds, PDF 5 pages, SHA `8fb8aca78a28...` vs old `0684697f...` different, trio style `a4bd...` changed, primary `1e3b22...` same, bibliography same – actual changed trio, not same-trio metadata).
  - `s2-c-reviews-qa` 1 (harness NameError `issue_id`, reviews already built `semantic 5586B/visual 2073B` with `renewal_source_proof_ref`, preserved).
  - Resume `s2-c-qa-only` 0 (QA-only, 3 checks, synthetic fixture, no genuine approval), `s2-c-finalize-resume2` 0 (`NEW_TARGETS`, set `.../high-c1-weekly/publication-set.json`, build-record `EXECUTED_BUILD` BEFORE receipt, 3 outputs `publication-pdf/build-log/pdf-digest`, no companions sidecar, full set match), `s2-c-activate-resume2` 0 (`ACTIVATED r3`, record `.../publication-surface-revalidation-r3.json`), `s2-c-history-resume2` 0 (`HISTORICAL_IDENTITY_VERIFIED` 3 refs EDITORIAL+U1+C1, `schema_pointer ""`).
  - Build-record variant `EXECUTED_BUILD`, outputs 3, receipt binds build-record (receipt cannot precede record – per contract §11.1, verified via finalize order).

Step2 verdict: SUCCESS (U refuse oracle + C real build + new postrender reviews/QA + finalize/activate + history; failed U inert preserved).

## Step3 — G3/G4 impl-only, repeat U→U (C→U→U) — SUCCESS

- G3 `1a0d587` (H comment, syntax fail preserved) + fix `e8bf1b9` (parse OK), style unchanged `a4bd...`. G4 `296c460` (S comment), style unchanged.
- G3 U `high-u2b-weekly` (prior r3 C1, REUSE_TARGETS, G3 epoch `e8bf1b9`):
  - `s3-g3-u-prepare` 0 (after fix; initial 1 due to G3 syntax `SyntaxError: invalid character '—'` at `history_v2.py:188`, fixed via new commit, no reset/clean).
  - `s3-g3-u-qa` 0, `s3-g3-u-finalize` 0 (`REUSED_TARGETS`), `s3-g3-u-activate` 0 (`ACTIVATED r4`), `s3-g3-u-history` 0 (4 refs EDITORIAL+U1+C1+U2b), old C targets unchanged `True` (6 files SHA equal).
- G4 U `high-u3-weekly` (prior r4, REUSE_TARGETS, G4 epoch `296c460`):
  - `s3-g4-u-*` all 0 (`REUSED_TARGETS`, `ACTIVATED r5`, history 5 refs EDITORIAL+U1+C1+U2b+U3, `HISTORICAL_IDENTITY_VERIFIED`, `schema_pointer ""`).
  - Stored C proof older ancestor: U3 new tool proof CURRENT (G4 `296c460`) + old proof HIST (C1 `bd2e39a4...` from G2, older than immediate prior r4), exact unchanged old C targets byte paths (`main.tex 1e3b..., refs faea..., style a4bd..., build PDF 8fb8...`), both new activation (r4/r5), bounded chain + CURRENT readback.
- Artifact-only `6141dad` (docs note, no Core change) after G4: `s3-artifact-readback` 0 (`HISTORICAL_IDENTITY_VERIFIED` r5, readback only, not new renewal reason).

Step3 verdict: SUCCESS (actual `C→U→U` with `C(r3)→U2b(r4)→U3(r5)`, repeat with new tool epochs, artifact readback only).

## Step4 — renewal→editorial at latest prePreview (r5 VALIDATED_DRAFT) — INCOMPLETE (product blocker, not harness waiver)

- Latest prePreview: State `VALIDATED_DRAFT`, `next_action stage:publication-candidate`, provenance `r5 278bded5...`, HEAD `6141dad` (G4 tools + artifact, tool bytes same as G4).
- Monotonic `recorded_at`: `prev_max r5 2026-10-25T05:36:08Z` + `wallclock` → synthetic `2026-10-25T06:02:15Z` (see `step4-*/recorded-at.json`), avoids longform run55 chronology bad.
- Changed-reader staging: `wk-ed-renew-1` (2 paragraphs, invalid, preserved as failure), `wk-ed-renew-2` (synthesis paragraph missing? Actually 3 paragraphs but missing exact synthesis? Preserved as failure), `wk-ed-renew-3` (headline/deck changed + 3 paragraphs incl exact synthesis `The accepted source authors describe the tested method.`, valid Weekly envelope edit, no fake Core-as-editorial).
- P1 `prepare_proposal` on `wk-ed-renew-3` (fresh subprocess, 1200s timeout, no faulthandler-only PASS):
  - `s4-stage-authoring` 0 (canonical `core.json_bytes` write).
  - `s4-p1-prepare` 1 (`ProposalError DERIVATION_REFUSED` → first `Weekly final summary must contain at least three...`/`must preserve exact approved synthesis...` for invalid `wk-ed-renew-1/2`, then `RECEIPT_KIND_UNKNOWN: generated receipt kind unknown: 'VERSIONED_RENEWAL_SOURCE_V1'` for valid `wk-ed-renew-3`).
  - Exact blocker: file `scripts/survey_editorial_correction_proposal_v2.py`, function `_dispatch_generated_receipt:113-152`, predicate `RECEIPT_KIND_UNKNOWN` for `VERSIONED_RENEWAL_SOURCE_V1` (active U3 receipt `VERSIONED_RENEWAL_SOURCE_V1/WEEKLY_GENERATED_V2` with `authoring_refs` + `reviewed_reader_ref` valid, but dispatcher only handles `EDITORIAL_PUBLICATION_SOURCE_V1` + old canonical, returns None otherwise – fails closed). Caller `_pipeline_data:1753` (`dispatched = _dispatch_generated_receipt(...)`) cannot proceed to renewal→editorial derivation. Oracle: public `P1.prepare_proposal(root,state,authoring,proposal_id,change)` on r5-active prior with changed-reader (Weekly envelope edit, synthesis preserved).
  - No timeout (immediate refusal, not `Timeout (0:03:00)!`), no blind rerun, no source relaxation. Preserved partials `wk-ed-renew-1/2/3/authoring-input.json` (no edit/delete, new id per attempt).
- Required P1→P2R→scope→P2V→P3S63→prepare→reviews/finalize/activate, new old-format EDITORIAL63 history (no hardcoded OLD50), legitimate current State (no rewinds/fakes), canonical R1 after versioned refused proof: OPEN (blocked at P1 routing, no further stages attempted).

Step4 verdict: INCOMPLETE (real code blocker, Root to assign owner – likely P1 routing team, not S F3/H nor B1-B3; relates to `remaining-route-failures.md` §2 run47/49 `RECEIPT_REF_SHAPE` pre-G5/G6 gap, now surfaced as `RECEIPT_KIND_UNKNOWN` for renewal kind in dispatcher; FIXED INPUT includes G6 `authoring_refs` key but not dispatcher renewal branch).

## Step5 — normal DIRECT Candidate/stage→synthetic Preview/Freeze/Release on r5 U3 — PARTIAL (stage+Preview SUCCESS, Freeze blocker)

- Dir `step5-20261025T061246Z`, `s5-lifecycle` 1 (overall), State pinned True (no mutation, Preview synthetic).
- Stage + synthetic Preview SUCCESS (no traceback for `stage.validate_stage`/`build_preview_approval`/`validate_preview_approval`; failure is later at Freeze).
- Freeze blocker: `ValueError: renewal checkpoint wrapper evidence artifact materiality-ledger not allowed (exact producer map)` at `scripts/survey_publication_v2.py:684 _prepare_freeze_inputs` (function `_prepare_freeze_inputs`, predicate exact producer map for renewal checkpoint wrappers).
  - Exact: `_FIXED_PRODUCERS["evidence"]={"evidence-acceptance","edition-views-acceptance"}` vs actual shared wrapper `sources/.../checkpoints/CANDIDATES_NORMALIZED.json` artifacts `[edition-views-acceptance, evidence-acceptance, materiality-ledger, profile-completeness]` (used for evidence+materiality+completeness, all same SHA). Evidence wrapper contains `materiality-ledger` → refused. Similarly materiality wrapper would contain extra artifacts.
  - Oracle: public `stage.validate_stage` + `pubmod.build_preview_approval (synthetic, NO genuine Human approval)` + `pubmod.build_freeze` on `high-u3-weekly` seal (VERSIONED_ACTIVE r5, proof `...`, Candidate `...`, QA/Gate, PDF 5 pages `8fb8...`).
  - Synthetic reviews explicit fixtures, content NO-GO retained (no genuine approval, Production semantic NO-GO).
- Freeze proof snapshot guards, exact new Candidate State/QA/Gate/typed proof bindings, whole public statuses/readbacks/paths/file SHA/PDF pages: OPEN beyond stage/Preview (blocked at Freeze).

Step5 verdict: PARTIAL (stage + synthetic Preview PASS, Freeze REFUSED, no State mutation).

## Remaining fault/resume, affected regressions, independent review

- Here public no-write alias/style/reason/wrong-target controls + ALREADY_ACTIVE enough (step1). Explicit failure/resume (IO/close/fsync/replace/postread/foreign-inode/32/33/cycle/anchor) + affected regressions (original routes/R1 slow incl R1×2 anchor/DM004 `7/7` + publication/quality/gate/stage/pubset/revalidation/freeze/staged) + independent final implementation review remain OPEN for separate worker (per task: “After positive remaining fault/resume more separate worker”).
- Whole unit NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Production semantic NO-GO on synthetic editions; fixture reviews synthetic, never genuine approval.

## Raw exits summary (all `*-exit.txt` 0 unless noted)

- Setup: `clone-0`0, `remote-0`0, `cfg-*`0, `head-pre`0, `noalternates`0, `add-736`0, `commit-g1`0, `warmup`0.
- Step1: prepare/finalize/activate/history/validate-set/validate-receipt/live-state/artifact-readback 0; already 0 (`ALREADY_ACTIVE`); alias/state-alias/empty-reason 2 (REFUSED); wrong-qa 1 (REFUSED).
- Step2: U prepare/qa 0, U finalize 2 (`REUSE_TARGET_MISMATCH`); C prepare/targets/qa-only/finalize/activate/history 0 (after harness NameError 1 fixed via QA-only resume, no deletion).
- Step3: G3 prepare 1 (G3 syntax `SyntaxError`, fixed via new commit), then prepare/qa/finalize/activate/history 0 (r4), G4 prepare/qa/finalize/activate/history 0 (r5), artifact-readback 0.
- Step4: stage-authoring 0, P1 prepare 1 (`RECEIPT_KIND_UNKNOWN`, blocker).
- Step5: lifecycle 1 (`materiality-ledger not allowed`, blocker; stage+Preview passed before Freeze).

## Provenance (no whole-unit PASS, no CommitPoint)

- Current fixture HEAD `6141dad65f985f246cd6cbd766d1afbf250ab296`, tree `594da22644b562639b8740629b49c082bec69da5`, manifest chain `721a04d→85eac6f(G1)→b2644a1(artifact)→cec67e5(G2)→1a0d587(G3 broken)→e8bf1b9(G3 fix)→296c460(G4)→6141dad(artifact)`, active `r5 278bded5...` (U3), State VALIDATED_DRAFT, old renewal proof fresh (C1 `bd2e39...` older ancestor, U3 CURRENT).
- Code changes NONE to shared candidate/INPUT (fixture-only SOURCE commits as ordered, E uncommitted, no reconstruct commit).
- This is NOT whole-unit/independent PASS/CommitPoint. Root to review and coordinate fixes (P1 dispatcher renewal branch, Freeze shared-wrapper producer map).

