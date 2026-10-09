# LF-1 preimplementation design/blocker gate review (author-independent)

2026-10-09. Fresh scoped reviewer, separate from Astra/root and earlier
General authors. Design/blocker check only: no implementation/tests/
fixtures/network/refs, no commits, no subagents, no unread-corpus intake.
Not canonical audit or implementation acceptance. Whole candidate NOT_READY,
step4/B3 OPEN, canonical audit unstarted. Stop at Human Commit Point.

## 1. Reviewed documents (exact sha256)

- decision `outputs/rephase-1-special-support-contract-decision.md`
  `796c65fca59f5a2461aca82065d0448e12410d1d3c341c2d2ab8ac2e7942e9b9`
- LF-1 `notes/rephase-1-longform-lf1/task.md`
  `21db424d261c500f860912af1e5556fb8830722e2aba6b17de4d227caf5eb6eb`
- Astra feedback `notes/rephase-1-longform-lf1/astra-design-feedback.md`
  `3f55fb265da8c22da57421f0ce226f2361d20fa7cd9ad26b685cbbedc1204a2c`
- proposal `evidence-20261009T001653Z/design-proposal.md` (733 lines)
  `4860669aad6b4135cd252050a873aebe8e3628ba0707c3a567ebfae98437a289`
- correction `evidence-20261009T001653Z/design-correction.md`
  `6717328c0248e3c5e1c282b69a0d0db2c8522d8fa4d9c4e0ffddf901d47290d3`
- qualification `evidence-20261009T001653Z/preparation-qualification.md`
  `e29f3b72732e9a3bddc9c8114c995cbb180f01bd6ecb018b62cc2a5a92fb8085`
- `current-verify.sh` `e491dc4fa0c6b1f1ab60423fda1474a062036d279da4f04a4e273b3dc0ae3568`
- `current-verification.log` `be24d02eb844761fde5399cc16fdfeb84554897cfb8e169db67c3fa71be62798`
- `commands.txt` `ffb8258047d10480e2958921537e83488e6093b21f1dee2669b4cfb088a3cd30`
- contract `astra-review-resolution.md`
  `e1ed71f4f97810848d200ea4f7a523fcdc76213e451aaf2d3799afce4e9bd24b`

## 2. Method and read-only identity

Env `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`,
all `GIT_DIR/WORK_TREE/CEILING/COMMON` unset, no fetch/checkout/ref writes.
This review verified NOW (read-only `rev-parse/status/remote/ls/config`):

- SRC `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` and DST
  `/tmp/opencode/jgas-lf1-design-20261009T001653Z`: HEAD
  `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, parent
  `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`, both
  `status --porcelain=v1 --untracked-files=all` empty.
- Both origin `https://example.invalid/rephase-candidate-recovery.git` inert,
  `--is-shallow-repository true`, no `objects/info/alternates` (ls exit 2),
  no `extensions.partialClone`, no root overrides.
Source reads only via `Read/Glob/Grep` on DST (byte-identical basis);
`python3 -c` used only for document hashes, not candidate execution.

## 3. Directive/final-summary gate (core question)

Correction §1 is NOT a silent exemption. It preserves the substantive
obligation and honestly scopes the procedural gap to LF-2:

- Substantive placement is retained as format constant from selected
  contract §4: `final_summary` mandatory, end-order before references.
  Existing encoding verified: heading `この号の総括` + `>=3` paras at
  `run_semantic_publication_v2_interactive_base.py:114-116`, render order
  `:101-103`, manifest placement `:202`. LF-1 enforcing this constant
  invents no authority; the contract already mandates it.
- Bound carriage carries no placement semantics. `derive_draft_package`
  copies `profile/publication_extensions` verbatim
  (`survey_drafting_v2_base.py:365-366`); preservation is validated
  (`survey_draft_profile_v2.py:22-43`, `survey_handlers_v2.py:334-350`,
  `survey_stage_validation_v2.py:448-450`). Schema free-object permits
  carriage; it does not authorize a placement obligation. The
  "extension directives" docstring (`survey_draft_profile_v2.py:5-8`) is a
  different Architecture→Package mechanism, not the editorial JSON file.
- Legacy file is an unbound sidecar. Sole consumer
  `run_..._base.py:133-135` (`core.load_json`, exact-one-row placement
  check); after-the-fact manifest `:202`; no producer/schema/validator/
  checkpoint artifact (grep `post-architecture-directives` in `scripts`
  yields only `:133`; `schemas/*directive*` none); absent from Human-gate
  inputs (`config/survey-production-v2.json:218-226`) and from approval
  binding (`survey_drafting_v2_base.py:105-134` binds only
  architecture/summary/attention). `docs/special-human-gates.md:13-23,41-54`
  preserves Architecture/exception authority; extension allowance alone is
  not authority. Search bound correctly qualified to AVAILABLE partial 409
  worktree (shallow; unmaterialized history unsearched) — no universal
  absence claim. No `UNPROVED`-as-accepted flag invented.
- Precise unresolved relationship stated: legacy publisher still
  hard-requires the sidecar (`:133-135` SystemExit), so LF-1 reader output
  cannot satisfy that publisher without a demonstrated bound producer or a
  Human-authorized publisher change. That blocks LF-2, not LF-1 projection.

No existing bound Architecture/directive route gives placement authority
to the synthetic fixture. No new Human substantive policy is needed for
LF-1 (placement already fixed by selected contract); Human publisher
authority (bind-file vs migrate-publisher vs defer, i.e. D1/D2/D3
equivalent) is required before LF-2 only.

## 4. Other LF-1 feasibility checks

- Producer/checkpoint chain (proposed, not demonstrated — correct):
  `stage_validation.validate_stage` + `agent.build_stage_checkpoint`
  (`survey_agent_control_v2.py:1267`) + `advance_with_checkpoint` (`:1332`)
  with `approve_architecture` (`:1393`), increment-B pattern, ending AT
  DRAFT_COMPLETE (draft passed, validation pending). Hard limit disclosed:
  DRAFT_COMPLETE outputs (`survey_stage_validation_v2.py:66-74,464-521`)
  have no LONGFORM_SPECIAL producer; config requires
  `stage:reader-publication-validation` (`survey-production-v2.json:330-333`)
  with no registry entry (`survey_handlers_v2.py:452-479` lacks it).
  LF-2 scope, not LF-1 fabrication. No schema-only dicts as acceptance.
- Input-only contract exact: `load_derivation` read-only via §2.2 loaders,
  `build_longform_reader_input` pure, `validate_*` schema-gate, no legacy
  writer import, no `main/bib/sty` writes, no Gate/PASS, no CLI, no shared
  lifecycle/admission change. Refusals include exact-one refs, duplicate
  note, key collisions, unsafe URL, forbidden patterns. Lifecycle via
  `core.LIFECYCLE.index` + required `next_action`, not lexical compare.
  `explicit_source_id=None` always (no sidecar fallback from
  `survey_bibliography_access_provenance_v2.py:154-167` / base `:175-178`);
  equal-ts follows resolver `:109-111`, different-ts refuses, no min/max
  (`:59-60`). Matches decision §5 and feedback item 5.
- Constants complete: technical-note labels `Chronology:/Technical
  points:/Limitation / attribution:/Primary URL:` (`survey_longform_...py:106-116`,
  `\url{}` without escape `:116`); style defaults OBSERVED
  (`templates/survey/jgaisurvey.sty:60-73`: title lacks `Special`, descriptor
  Weekly default) so Longform values are explicit overrides, Weekly
  `VISIBLE_TEXT` not reused where it differs; `cross_table_header` ordered
  ARRAY (wrapper `:138`); single `edition_descriptor` in `visible_text`;
  `toc_title` left as future selected string, not class default — needs
  Astra pick before implementation (see §6).
- Bytes/provenance separation: `provenance` deleted from file, in-memory
  mechanical context only; `as_of_source` moved out; ONE file algorithm
  `core.write_json` (`survey_production_v2.py:86-92`) with digest
  `sha256_file` (`:99-100`); `sha256_object` (`:103-105`) comparator only.
  Safe subset single-DID/card/primary-subject/canonical-URL/card-sources-only
  with VERIFIED/PARTIAL eligibility preserved.
- Oracles: mutate authoring/accepted inputs then reproject (never edit IR
  bytes); stability retains all accepted bindings while varying mechanical
  context only; raw-Draft-only mutation without hash update correctly ruled
  INVALID; no-write = full recursive inventory + `git status` BEFORE
  cleanup, no hidden repair. Matches feedback item 6.

## 5. Evidence qualification

- `commands.txt` is abbreviated reconstruction (line 22 placeholder
  `find <SRC|DST>`, line 23 aggregated pseudo-command, no per-command
  exit/env transcript). Preserved as-is, not replayable. Honestly
  qualified by correction §7 and qualification record.
- `current-verify.sh/log` verify CURRENT bytes only. Script echoes exits
  without `set -e`/assertions (`diff` exit 1, `ls` exit 2 expected) — it is
  observations, not fail-closed proof. It cannot retroactively certify
  copy-time guards. Proposal intact (733 lines) confirmed.
- Single `.git/index` `diff -r -q` difference attributed to stat-cache
  refresh by read-only `status` is plausible but UNPROVED under
  `GIT_OPTIONAL_LOCKS=0`; refs/objects/worktree otherwise identical per
  logs and this reviewer's HEAD/tree/status checks. Same-device (dev 45)
  distinct inodes, nlink 1, zero shared inodes: isolation rests on
  no-hardlink/no-alternates, not separate media. Full history stays limited.

## 6. Verdict

**LF1_DESIGN_READY** — source-only projector design is feasible under
explicit input-only scope; **LF-2 publisher/receipt/Gate integration is
BLOCKED** on missing bound file authority/producer.

Minimum resolution before any implementation (Astra records, no code yet):
1. Record LF-1-only scope: enforce format constant (heading/`>=3`/END
   order), never read `editorial/post-architecture-directives-v2.json` in
   LF-1, make no publisher/Gate claim; legacy file check is an LF-2
   migration item. This applies selected-contract §4, not new authority.
2. Select `toc_title` disposition (reviewed constant vs disclosed build
   dependency), confirm single-descriptor placement and exact closure list;
   no shared-helper/Weekly-closure change without analysis.
3. Human Commit Point; LF-2 needs publisher-authority decision plus real
   DRAFT_COMPLETE producer/handler, receipt/Gate, serializer proofs.
4. Editorial: correction §5 `whitepsace` → `whitespace` (non-blocking).

Blocks LF-1: only an actually unconstructible accepted fixture at
implementation time (to be proved; never fabricate State). Blocks LF-2
only: sidecar-file satisfaction, artifact producer/handler, receipt/Gate
replay, serializer escaping/closure, later-state readback, IRI handling.
