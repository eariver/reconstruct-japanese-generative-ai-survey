# LF-2I preparation plan (THIS CALL ONLY, no code)

2026-10-10. Source verified read-only; implementation STOPPED pending root DM021
applicability disposition. No candidate/test/fixture execution this call.

## 1. Composite identity (actual observation, design copy)
- `/tmp/opencode/jgas-lf2-design-20261009T113013Z`: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`.
- Untracked-only overlay (3 paths): derivation `233e8655…0744cf7`, reader schema
  `7bae9d2a…bd0643`, test `ce687447…913` — all match LF-1 pins and LF1 copy.
- `status --porcelain`: only those 3 `??`; no dirty tracked bytes.
- Origin inert `https://example.invalid/rephase-candidate-recovery.git`; no
  `objects/info/alternates`; no `*.lock`; shallow=true with `.promisor` (inherited
  partial, not lazy-fetch routing: no `extensions.partialClone`).
- Inode sharing LF2-vs-LF1: `comm` over `find .git/objects -printf %i` empty; sample
  pack device/inodes distinct. No copies/reruns needed; reuse copy if held.
- Runtime (no candidate run): `/usr/bin/python3` 3.14.4, `jsonschema` import ok;
  pinned venv path exists (not executed). Reconstruct HEAD `a4dc0fd` clean except
  untracked intake dirs.

## 2. Exact A/M budget (contract s6, no extras selected)
- A: `scripts/survey_longform_semantic_publication_v2.py` (thin 2-pass CLI),
  `scripts/survey_longform_generated_v2.py` (pure render/receipt/replay),
  `schemas/longform-publication-source-manifest-v2.schema.json`,
  `tests/test_survey_longform_publication_integration_v2.py`.
- M (only on demonstrated gap): `scripts/survey_longform_derivation_v2.py`
  (default vs `load_derivation_for_readback` allowlist), `scripts/survey_reader_surface_gate_v2.py`
  (Longform scan + receipt branch), `schemas/reader-surface-gate-v2.schema.json`
  (generated arm), `config/survey-production-v2.json` (contract registration only).
- Read/reuse, no edit by default: `survey_stage_validation_v2`,
  `survey_agent_control_v2` (`_PendingPublicationBasis`, checkpoint/advance),
  `survey_core_execution_bridge_v2._advance_stage:365-407`, Weekly derivation receipt
  pattern (`route/status/basis/refs/tools/outputs/self-digest`), `contract_identity`,
  `implementation_control_roots`, semantic-review + reader-input schemas, `jgaisurvey.sty`.
  Renderer `render_article_draft_tex._render_tex` is reference inventory, not drop-in.

## 3. Closure to freeze before first run (from actual imports/call graph)
LF-1 derivation + new helper/entry + pure-render/preflight helpers actually used +
`survey_drafting_citation_refs_v2` + `survey_bibliography_access_provenance_v2` +
`render_article_draft_tex` (named use only) + both reader schemas + new receipt schema +
shared Gate/runtime/schema + semantic-review schema + literal style bytes + repo
`implementation_control_roots` + configured `contract_files` equality/ancestry.
Declare/register new receipt/reader contracts where `contract_identity` requires.

## 4. Fixture/execution strategy (synthetic committed fixtures, independent DBs only)
Real accepted Thematic chain -> pass1 reader-only -> persisted
`load_and_validate_reader_surface_semantic_review(require_pass=True)` -> pass2
same-input main/bib/style/archive/receipt -> independent `validate_receipt`
(review reload) + Gate create/revalidate (`LONGFORM_GENERATED_V1` /
`LONGFORM_MAIN_BIB_STYLE`, same review SHA) -> DRAFT_COMPLETE->VALIDATED_DRAFT->
RELEASE_CANDIDATE admissions via existing stage/bridge callers -> healthy
FROZEN/RELEASED readback via allowlist loader (no publisher call). Negatives:
stale/missing/wrong-path/non-PASS/VISUAL/legacy review, directive presence incl
dangling symlink, alias/undeclared-input, pre-existing partials, tampered
reader/main/bib/style/closure/accepted-source, wrong-issue manuscript at both sites.
Reading source is NOT fixture proof. Later-state infeasibility -> STOP with blocker.

## 5. Asserting runner design (to build before verification)
Capture runtime/argv/cwd/env/base + all source hashes; assert pre AND
finally-post identity/allowed-delta (drift fails even if child passes);
exclusive (`O_EXCL`) logs, never overwrite; direct child-exit capture (no
tee-mask), timeout with partial stdout/stderr preserved; no hidden repair before
immediate no-write inventories; committed-tool guard must refuse uncommitted basis.
Affected Weekly/direct-primary + LF-1 default-loader controls only; no auto full suite.

## 6. Boundary
No extra path needed beyond s2 pending caller-gap proof. STOP here; next is LF-2I
implementation only after Astra DM021 disposition. No commit/branch/push authorized.
