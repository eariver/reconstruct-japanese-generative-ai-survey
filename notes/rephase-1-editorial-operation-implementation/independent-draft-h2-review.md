# Independent pre-execution H2 code review — CHANGES_REQUIRED (H-owned only)

Fresh author-independent reviewer. Readonly. No imports, no tests, no build,
no network, no Git mutation. DST only
`/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`.
L/C files were **not audited** (parallel correction in progress); L/C symbols
below are API-frozen reads only to check H call compatibility, per brief.
H2 author claims in `notes/rephase-1-editorial-operation-implementation/correction-h2/H2-report.md`
are treated as claims only; all findings below are from real paths.

Governing read:

- `outputs/rephase-1-editorial-operation-contract-decision.md` d880f53e (191 lines, §§1–10).
- `notes/rephase-1-editorial-operation-implementation/astra-implementation-selection.md` (§§1–5).
- `notes/rephase-1-editorial-operation-implementation/astra-draft-review-r1.md` (7 H items + L/C integration).
- `notes/rephase-1-editorial-operation-implementation/correction-h2/H2-report.md` (151 lines, claims only).
- `notes/rephase-1-editorial-operation-implementation/correction-h2/history/README.md` + H1 bytes preserved (not re-reviewed for correctness).
- `notes/rephase-1-editorial-operation-implementation/independent-draft-lc-review.md` read only to avoid duplicating L/C audit; no L/C re-finding repeated here except where H call compatibility requires it.
- `notes/rephase-1-editorial-operation-implementation/implementation-map-20261020.md` §§1–16 for interface context only.

Exact H read coverage (DST unless noted):

- `scripts/survey_editorial_publication_v2.py:1–2862` (all, H2 `b86983cb` 2862 lines).
- `schemas/editorial-publication-source-manifest-v2.schema.json:1–92` (all).
- `schemas/editorial-publication-build-record-v2.schema.json:1–94` (all).
- `schemas/editorial-manuscript-spec-v2.schema.json:1–67` (all).
- `schemas/editorial-toolchain-spec-v2.schema.json:1–27` (all).
- `scripts/survey_reader_publication_v2.py:165–414` (editorial branch + builder) and `:412–761` (`validate_manuscript_manifest`, review builders/validators).
- `scripts/survey_reader_surface_gate_v2.py:1140–1389` (`_derivation_for_manuscript` editorial branch), `:1390–1689` (evaluate tail), `:1689–1898` (`_inspect_gate_record` + validator), `:1891–2010` (validator), `:462–541` (`_resolve_repo_path`/`_rel`/`_safe_file`).
- `scripts/survey_weekly_derivation_v2.py:1–787` (all, closure 22 + receipt/derivation context).
- `scripts/survey_longform_generated_v2.py:1–99` (closure 27 head only; body not audited).
- `scripts/survey_schema_v2.py:1–81` (all, helper semantics for temp-outside analysis).
- `scripts/survey_reader_publication_v2.py:1–140` (`_rel`/`_safe_file` containment).
- `scripts/survey_publication_v2.py:34–103` (`_rel`/`_safe_file`/`_write_immutable`) — API-frozen only.
- `schemas/publication-surface-revalidation.schema.json:1–246` (all) — frozen read only to check H record shape; L runtime not audited.
- API-frozen def-line + minimal signature reads only (no body audit): `survey_quality_v2.py:132–261`, `survey_publication_v2.py:668–767`, `survey_editorial_current_authority_v2.py:101–190`, `survey_editorial_staged_source_v2.py:1724–1753`, `survey_publication_set_v2.py:337–431,823–1002` (chain normalize, anchor head, selection frozen keys), `survey_agent_control_v2.py` def lines for `_exclusive_create_record_bytes`/`_atomic_replace_state_bytes`/`validate_agent_state` via grep.
- Grep-only (readonly, no execution): `shutil.rmtree`/`core.write_json`/`_build_only`/`staged_refs`/fictional L names/`shell=True`/`O_EXCL`/`mkdtemp`/closure counts in H module; def lines for builder APIs above.

NOT read/executed: L `survey_publication_set_v2.py` body, agent body, stage/production/freeze/config/orchestrator/handoff/human-gate/workflows, P1/P2V/P3S bodies beyond cited API lines, R1/wrappers, full Longform body, full Gate scan body. No whole-candidate audit, no execution, no fixture, no approval.

Verdict: **CHANGES_REQUIRED** — H2 fixes all 7 R1 scaffolds to real code, but two
load-bearing defects make actual initial/revised smoke impossible (§§1–2).
Remaining §§3–4 are correctness gaps that weaken (not block) smoke on healthy
inputs. §5 is generic TOCTOU/discipline, explicitly non-blocking for smoke.
No bounded source approval; no whole-implementation-done claim; synthetic vs
genuine not conflated (H never synthesizes PASS; supplied reviews still require
real execution to prove genuine).

## 1. Smoke blocker — build-record `argv` shape (prepare cannot succeed)

`scripts/survey_editorial_publication_v2.py:905–933` builds `cmds` as
`list[list[str]]` (4 commands for `lualatex-biber-lualatex`, 1 for
`latexmk-lualatex`). `:1071` returns `"argv": cmds`. `:1408` stores
`"toolchain": {"executable":…, "versions":…, "argv": build["argv"], "env":…}`.
`schemas/editorial-publication-build-record-v2.schema.json:51–56` requires
`"argv": {"type":"array","items":{"type":"string"}}`. `:1420` calls
`schema_gate.validate_instance(build_base, repo / BUILD_RECORD_SCHEMA)`.
A list-of-lists fails `items.type:string`. Prepare therefore fails closed at
`BUILD_RECORD_SCHEMA` after already writing build3/manuscript/receipt,
never returning `prepared_paths`. This is not a generic disclaimer; every
`prepare_publication` invocation with either fixed recipe hits it.

H2 report §2.6 claims “digest includes input/output refs excludes only self”
and §5 claims focused checks pass, but no focused check validates the build
record instance against its schema (report lists `py_compile`, lexical,
exclusive-write, closure, argv-token presence — not a build-record
`validate_instance`). Real-path inspection, not report claim, controls.

## 2. Smoke blocker — Gate temp-outside-repo fails its own validator (finalize cannot succeed)

H finalize `:1667` creates `tmp_gate = Path(mkdtemp(prefix="editorial-gate-")) / …`
outside the repo (system temp, deliberately outside publication inventory).
`:1669–1676` calls `gate.evaluate_reader_surface_gate(…, output_path=tmp_gate)`.
`survey_reader_surface_gate_v2.py:1689–1690` writes via `core.write_json`
with no containment check, so the write succeeds. `:1680` then calls
`gate.validate_reader_surface_gate(repo, tmp_gate, …)`.
`:1695–1713` (`_inspect_gate_record`) calls `_safe_file(repo_root, path, …)`.
`:481–485` (`_safe_file`) → `:462–473` (`_resolve_repo_path`) resolves and
requires `relative_to(root)`; `/tmp/…` raises “escapes repository root”.
Finalize therefore raises `GATE_INVALID` with temp preserved on every
invocation, never reaching exclusive transfer `:1692` or Candidate/seal.

Contrast (why only Gate blocks): manuscript temp `:1268` + `reader.validate_manuscript_manifest`
(`survey_reader_publication_v2.py:413–449`) loads via `schema_gate.load_and_validate_json`
(`survey_schema_v2.py:71–81`, no repo containment on the manifest path itself;
containment applies only to its refs, which are inside) — passes outside.
Quality `validate_bundle` (`survey_quality_v2.py:232…`, schema-gate load only)
and publication `validate_candidate` (`survey_publication_v2.py:749…`, schema-gate
load only) likewise impose no containment on the bundle/candidate path itself.
Only Gate inspects its own path via `_safe_file`. H’s uniform
“system temp + validate + exclusive transfer” pattern (correct for
manuscript/quality/candidate, and correctly avoids review-target rebinding
since all refs stay repo-relative) is incompatible with the existing Gate
validator. No new design is proposed here; root must choose between a
repo-contained staging location outside the publication inventory or a
concrete safe-builder extension — H currently does neither for Gate.

## 3. Correctness gaps (weaken, do not block healthy-input smoke)

### 3.1 Receipt does not rederive via ordinary route loaders

`validate_editorial_receipt:481–734` implements strict State
(`agent.validate_agent_state:522`), proposal/staged/retention/scope pinning
(`:528–572`), NEW authoring vs `proposal.proposed.authoring_input_ref`
(`:579–580`), unchanged accepted Draft via `basis.generated_receipt_ref →
drafting-authored-archive` path+sha (`:583–606`), validation-checkpoint vs
State (`:611–613`), reviewed-reader vs `proposed_reader_ref` (`:615–620`),
early scope `reviewed_surface` + `editorial_correction_scope V1/WITHIN`
+ `before_reader == basis.active_reader_input_ref` (`:622–640`), P3S proof
`RETAINED_SET_VERIFIED` with `proposal_ref/staged_manifest_ref/observed_refs`
(`:643–650`), staged `outputs=={main,bibliography,style}` with explicit
`main→primary` mapping (`:653–675`), closure exact 22/27 set/path/SHA/contract/
ancestor (`:677–730`), no before-State equality (`:731–733`). No caller
delegation — R1 §H2 fixed.

Missing vs contract §4.1: no call to Weekly/Longform `load_derivation` to
rederive the proposed reader from NEW authoring + unchanged Draft and compare
canonical reader FILE bytes plus all rendered output bytes. H checks ref
equality and staged proof, not independent route-loader replay. On healthy
inputs smoke passes, but a swapped NEW-authoring/old-reader pair with
consistent proposal refs would not be caught at receipt layer (seal layer
`:1887–1895` checks manuscript-vs-staged, not receipt-vs-rederived-reader).
Flagged as strictness gap, not smoke blocker.

### 3.2 Activation omits explicit retained-COPY check

`activate_publication:2290–2296` checks
`basis_state_ref.path==state_rel` and `sha==sha(current State)` (proposal
basis vs current). It never loads the P2R retained COPY bytes and compares
to `before_state_ref`, nor checks retained Profile (P2R KEEP) against bound
proposal/State. `_require_scope_bound` (P2V fresh) and `_verify_staged` (P3S
historical) are called at both prewrite boundaries (`:2283`, `:2493`,
`:2518`), and `validate_prepared_set` + `selection_before` are called, but
none of those is an explicit “retained COPY == before_state_ref” assertion
in H. Retained-before vs fresh-current agreement for
`supersedes`/before-Candidate/digest is therefore delegated to L
`validate_activation_record`/`resolve_publication_selection` (which LC review
already flags as table-only). H is correct to stay read-only on L, but the
contract §4.3 line 85 + §5 line 100 equality (“must equal bound proposal basis
+ P2R retained COPY; supersedes/before-Candidate/digest must agree with both
retained-before and fresh current-before”) has no H-side pin. Healthy-input
smoke passes; swapped-retained-COPY passes.

### 3.3 Digest exact-seven not enforced by H before calling L

`:2377–2384` strips `effective7_before` to `{path,sha256}` and calls
`setmod.before_active_digest`. H never checks
`set(effective7)==PUBLICATION_ROLES_7` / `len==7` first. L
`before_active_digest:162–195` (per LC §1.2) also does not enforce seven.
Wrong-shape digests are self-consistent. Healthy 7-row smoke passes; 6/8-row
inputs produce a digest that later compares equal to a similarly malformed
stored digest. Same class as LC §1.2; H must not rely on L to add it.

### 3.4 Ambient env merged despite “no ambient merge” comment

`_run_disposable_build:943–950`: comment `:942` says “no ambient
`os.environ` merge”, but `:944–946` copies every `ALLOWED_ENV_KEYS` present
in `os.environ` into `allowed_env`, then overlays spec env `:947–950`.
Toolchain spec env is allowlisted (`_validate_toolchain_spec:777–788`,
correctly refuses `GIT_*`/`PATH`/`PYTHONPATH`/`LD_LIBRARY_PATH`, newline/NUL),
and executed `env=allowed_env` (`:996`) correctly excludes `PATH`/`GIT_*`.
But ambient `TEXMFHOME/TEXMFVAR/TEXMFCONFIG/SOURCE_DATE_EPOCH/TZ/LANG/LC_ALL`
still influences the disposable build. Clean-env smoke passes; ambient-injected
TeX inputs are not refused. R1 §H6 “merges ambient despite allowlist” is
only half-fixed (unallowlisted ambient removed; allowlisted ambient kept).

### 3.5 Spec argv validated but not executed/recorded

`_validate_toolchain_spec:765–775` allowlists every spec `argv` token and
refuses `-e`/`-shell-escape`/`-output-directory`/shell metachars — correct.
`_run_disposable_build:904–940` then ignores spec `argv` and executes fixed
`cmds` per recipe (allowlisted at `:937–940`). Build record stores executed
`cmds` (`:1071`, `:1408`), not spec `argv`. Spec `argv` is therefore dead
config: any allowlisted spec passes regardless of whether it equals the fixed
recipe. Healthy smoke passes; mismatched spec-vs-executed is undetected.
Selection §4 requires “argv must match fixed recipe allowlist” — H enforces
allowlist on both, but not equality. Not a smoke blocker.

### 3.6 Activation ordering + depth + unused import

- `activate_publication:2385–2441` derives anchor/seq/collision before the
  read-only `ALREADY_ACTIVE` check (`:2423–2441`). On an already-active State,
  anchor/seq work can fail before the cheap pointer-equality short-circuit.
  Initial-activation smoke unaffected; same-set re-activation does redundant
  work that can mask `ALREADY_ACTIVE`.
- `_build_anchor_chain:2115` loops `range(32+1)` (33 links) before
  `CHAIN_DEPTH`; contract bounds total chain at 32. L `derive_canonical_anchor`
  enforces its own bound, so healthy short chains pass; 33-link input is
  accepted one link too far at H layer.
- `survey_editorial_publication_v2.py:21` imports `shutil`, never used
  (grep finds only the import; no `shutil.rmtree` — R1 §H6 “no rmtree”
  holds). Dead import only; no deletion behavior.
- `_next_record_seq:2196–2221` lists via `iterdir` + `lstat` (symlink-safe),
  enforces no-leading-zeros and strictly increasing, allows gaps (max+1).
  Gap tolerance matches “strictly increasing, no dup” (not “contiguous”);
  noted for root awareness, not a defect.

### 3.7 Reader/Gate narrow slices — pass with one note

- Reader `_validate_manifest_semantics:218–269`: canonical rule verbatim when
  `editorial_source is None` (`:219–221`); editorial branch requires exact
  `{proposal_ref,staged_manifest_ref}` (`:226–231`), actual
  `verify_staged_source` with `RETAINED_SET_VERIFIED` + ref equality
  (`:237–247`), staged `outputs=={main,bibliography,style}` with explicit
  `main→primary` (`:253–264`), bib/style exact (`:265–269`). No `staged_refs`
  alias (grep: only comments). Existing DIRECT/WEEKLY/LONGFORM paths untouched.
  Source-proof entry calls P3S only, never seal/activation — callgraph holds.
- Gate `_derivation_for_manuscript:1159–1251`: editorial branch first, P3S proof
  (`:1173–1181`), receipt at `P/publication/validated-source-manifest.json`
  (`:1183–1194`), exact early-scope binding `reviewed_surface_path ==
  scope_ref.path` (`:1201–1205`), scope `reviewed_surface == receipt
  reviewed_reader_input` + `editorial_correction_scope V1/WITHIN` (`:1215–1222`),
  staged `main→primary` + manuscript trio (`:1225–1249`). Existing three
  branches verbatim after (`:1252–1328`). Never substitutes postrender
  semantic record — holds.
- Note: both branches pass `repo_root / ref.path` (Path) to
  `verify_staged_source`, while H `_verify_staged:465` passes lexical `str`
  rels. P3S signature `(root: str|Path, proposal_path: str|Path,
  staged_manifest_path: str|Path)` accepts both — compatible, no blocker.

## 4. Passes (R1 defects actually fixed on real paths)

- No fictional L writers: grep finds `activate_selection`/`write_activation_record`/
  `resume_activation_record`/`verify_activation_history` only in comments/docstrings
  (`:2244–2245`, `:2727`); code constructs the exact 17-key branch2 record
  (`:2468–2486`, matching `publication-surface-revalidation.schema.json:169–187`
  required list) and uses existing agent `_exclusive_create_record_bytes:1864`
  / `_atomic_replace_state_bytes:1926` via function-local import with
  `hasattr` fail-closed (`:2507–2508`, `:2690–2691`), never `hasattr` fallback
  to invented behavior. `hasattr` uses that remain (`:414`,`:458`,`:519`,
  `:1577`,`:2258`) all raise `*_MISSING` with “need concrete helper to root”,
  no silent fallback.
- `_safe` raw-first lexical (`_lexical_rel:112–126` rejects absolute/backslash/
  `..`/`.`/empty before resolve) + `core.repo_local_path` + held-ancestor
  `lstat` walk refusing symlink/FIFO/socket/non-dir (`_safe:159–181`) + leaf
  `lstat` refusing symlink/FIFO/socket (`:192–195`). Bounded reads via
  `O_RDONLY|O_NOFOLLOW` + short-read loop (`_read_bytes_bounded:217–247`).
  R1 §H4 laundering fixed at H layer (L/C alias discipline remains L/C-owned,
  not re-audited here).
- Exclusive writers: `_exclusive_write_bytes:249–352` uses
  `O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW`, no prior exists-check trusted, no
  tmp+rename, short-write loop/fsync/`fstat` identity/seek+same-fd readback
  (`:321–341`), never unlinks owned partial/unknown (`:343–346`).
  `_exclusive_write_json:355–375` adds canonical bytes + final pin re-read.
  Build3 transfer `:1165–1175` does pinned-bytes exclusive + readback (no glob
  CAS). Own-temp cleanup only on identity+bytes match
  (`:1306–1313`,`:1633–1640`,`:1696–1703`,`:1746–1753`); no foreign deletion;
  no `shutil.rmtree` in H module. Primary+secondary preserved (see §6).
- Build trio exact: `_run_disposable_build:839–844` requires
  `{main,bibliography,style}` (NOT primary, no `staged_refs`); verifier shape
  `RETAINED_SET_VERIFIED` + `proposal_ref`/`staged_manifest_ref`/`observed_refs`
  (`validate_editorial_receipt:644–650`); explicit `main→primary` mapping
  (`:656–665`, prepare `:1330–1371`, seal `:1887–1895`, Gate `:1230–1234`).
- Toolchain: absolute exe + `lstat` regular (not symlink) + companion in same
  bin dir (`_validate_toolchain_spec:753–762`, `_run_disposable_build:855–861,
  :912–919`); fixed exact argv per recipe + allowlist (`:769–775`,`:937–940`,
  `ALLOWED_ARGV_TOKENS:67–78` excludes `-e`); env allowlist
  (`ALLOWED_ENV_KEYS:79–87`,`:777–788`); recipe `.latexmkrc` pinned before/after
  (`:864–867`,`:1052–1057`) and recorded as `recipe_ref` (`:1401`); source
  inputs pinned pre/post (`:869–878`,`:1044–1050`); real exe/companion
  `--version` recorded where available (`:881–898`); log predicates + `pypdf`
  strict `>=1` page gate (`:1015–1042`, finalize `:1577–1584` with no
  `else 1` fallback); failed root + full raw (1 MB each, `:999–1011`, no
  `[-4000:]` truncation, tmp path in error, no `rmtree`).
- Prepared set: `validate_prepared_set:1940–2103` requires schema (no fallback,
  `:1955–1960`), exact 15 roles + SHA/bytes + no-dup (`:1969–1984`), staged-vs-build
  inventory (`:1985–1996`), full receipt (`:1998–2003`), actual manuscript
  (`:2011–2013`), bundle + external result pins (`:2021–2031`), supplied reviews
  with PASS (`:2033–2042`, never synthesized), Gate editorial derivation
  (`:2044–2055`), Candidate (`:2057–2065`), build record digest
  (`:2067–2088`), State/Profile/refs agreement (`:2091–2101`). No public
  `_build_only` param (grep: docstring mention only). Valid inert set needs no
  active pointer, all current proofs apply — matches contract §6.
- Activation/State: record 17 keys + `REVIEWED_EDITORIAL_CORRECTION`/
  `VALIDATED_DRAFT` + `supersedes` common edge + `canonical_anchor` via
  `_build_anchor_chain` + `derive_canonical_anchor` + `before_active_digest`
  from selection `effective7`/`candidate_ref` (`:2320–2396`); seq via
  `publication-surface-revalidation-rN.json` + `lstat` no-leading-zeros
  (`_next_record_seq:2155–2226`); ordinary-activate collision refusal
  (`:2408–2415`); P2V fresh at both prewrite boundaries (`:2283`,`:2493`,
  `:2518`); State still-old rechecked before record (`:2495–2500`) and before
  replace (`:2524–2529`); sole mutation `publication_revalidation_provenance`
  (`:2532–2538`, no canonical rewrite); guarded replace via agent writer
  (`:2540`); post-replace strict selection + record + set + agent State before
  success (`:2548–2584`); `ALREADY_ACTIVE` read-only with full strict State +
  full set (`:2431–2441`, resume `:2642–2653`); orphan resume revalidates
  current-before + record bytes + P2V + still-old before install (`resume_activation:
  2589–2695`); `INDETERMINATE` preserves (`:2656–2658`); close/postreplace
  observed `old`/`new`/`unknown` + primary+secondary, never deletes record
  (`:2551–2584`,`:2697–2719`).
- Callgraph: H top-level imports only stdlib + `core` + `schema_gate`
  (`:18–31`), no import-time execution. Source-proof entry
  (`_verify_staged:450–467`, Reader `:237–247`, Gate `:1173–1181`) calls P3S
  historical only, never P2V/seal/activation. Receipt (`:481–734`) calls strict
  State + P3S, never Gate. Gate editorial branch loads the receipt file for
  ref comparison (`:1188–1194`), never calls H `validate_editorial_receipt`
  — no State→Gate→receipt cycle. P2V (`_require_scope_bound:402–447`) is
  before-eligibility at prepare/finalize-prewrite/activate-prewrite only
  (`prepare:1120,1142`; `finalize:1508,1767`; `activate:2283,2493,2518`;
  `resume:2671`), never receipt replay after activation. P2V call passes
  5 positional args matching frozen
  `observe_current_authority(root,state,proposal,manifest,scope=None,receipt_kind=None)`
  with `retention_rel` as manifest and `None` receipt_kind (editorial allowed;
  `WEEKLY`/`LONGFORM` refused inside P2V) — no `receipt_kind` invention.
- Schemas: receipt 16 keys + `outputs=={primary,bibliography,style}` +
  `current_tools=={commit,contract,closure}` (`source-manifest:7–68`); build
  record 13 keys + `declared_inputs=={primary,bibliography,style}` +
  `outputs=={pdf,log,digest}` (`build-record:7–70`); manuscript-spec FULFILLED-only
  (`manuscript-spec:22–51`); toolchain-spec 8 keys (`toolchain-spec:7–26`).
  All `additionalProperties:false`. No shape change was needed — H2 report §1
  “no schema shape change” holds on real paths.
- Closures: `_editorial_closure_rows:1438–1470` enforces sorted-unique,
  `path==name`, SHA==current bytes, exact `22`/`27` (`:1463–1465`).
  `survey_weekly_derivation_v2.py:28–51` is 22, `survey_longform_generated_v2.py:
  53–80` is 27 (Gate overlap excluded) — matches selection §3
  (Weekly 8∪14, Longform 14∪13). P3S 50 and `contract_files` registration are
  C-owned, not re-audited here. Closure contradiction (selection 22/27/50 vs
  map-resolution 8/14/37+12) is a root decision, not an H code defect; H
  follows selection.

## 5. Generic TOCTOU / non-blockers (disclosed, do not gate smoke)

Single-writer/operator assumption is explicit in H errors
(`REFUSED_PRE_WRITE`/`PRESERVED_INCOMPLETE`/`EXPLICIT_RECOVERY`); no
multi-file atomicity/globalCAS/power-loss claim — matches contract §7.
Remaining windows are disclosed, not waived: `_check_file`→`open` TOCTOU
closed by `O_NOFOLLOW` open failure (not by lease); FIFO swap after `lstat`
could block `O_RDONLY` (no `O_NONBLOCK`) — healthy fixtures have no
adversarial swap; `_exclusive_write_bytes` `mkdir(parents,exist_ok)` traverses
before its post-mkdir ancestor walk — healthy `P/publication` parents are
pre-checked via `_safe`/`lstat`. These are the standard “boundary guards are
not atomic CAS” qualification, already required to be explicit + fault-tested
at integration. They do not make initial/revised smoke impossible and must
not be cited to waive §§1–2.

## 6. Controls, hash discipline, genuine vs synthetic

- Every record/State write/close/late-readback failure in H carries
  `code:[phase/disposition] detail` via `EditorialError` (`:99–109`), with
  `observed old/new/unknown` on the activation paths (`:2551–2584`,
  `:2697–2720`) and `record inert at …; observed old` on pre-replace P2V/State
  failures (`:2518–2529`). CLI maps all failures to exit 2 with stdout JSON
  only (`main:2777–2858`). Primary+secondary reporting is actual (secondary
  list joined at `:2584`,`:2719`), not a comment.
- No expected-hash blessing: `_exclusive_write_bytes:340–341` compares
  same-fd readback bytes to the passed `data` bytes (not to a caller hash);
  final pin `:369` re-reads file bytes vs `data`; build3 `:1171–1175`,
  manuscript `:1297–1303`, bundle/candidate/Gate temps all compare temp bytes
  vs transferred bytes. Digests (`receipt_sha256:1373`, `build_sha256:1417`,
  `set_sha256:1790`) hash the canonical object excluding itself, verified by
  recomputation on read (`:497`,`:1963`,`:2081`).
- Synthetic vs genuine: H never generates semantic/visual PASS. `prepare`
  ends before reviews (`:1424`); `finalize:1641–1653,2033–2042` requires
  persisted supplied reviews with `decision==PASS` (and `status` PASSED/PASS
  where present) via actual `validate_review_record`, then Gate editorial
  derivation + Candidate via actual builders. No agent-generated genuine Human
  approval is claimed; production semantic NO-GO remains for root to enforce
  with real-PDF inspection. H2 report §7 “no authority execution claimed”
  holds.

## 7. Precise return

**CHANGES_REQUIRED** before any long authority/build run or combined-source
freeze that includes H:

1. Fix build-record `argv` shape (§1) — prepare smoke impossible until the
   recorded `argv` validates against `editorial-publication-build-record-v2.schema.json`.
2. Fix Gate temp-outside validation (§2) — finalize smoke impossible until the
   Gate staging location passes `validate_reader_surface_gate` without
   rebinding review targets into the publication inventory.

Then address §3.1–§3.6 in H (receipt rederivation, retained-COPY pin,
digest seven, ambient env, spec-vs-executed argv, activation ordering/depth)
before integration execution. §5 needs no H code change for smoke; preserve
its disclosure into fault tests.

Do not author code or alternative design in response. Do not re-review L/C.
Read scope above is the entire basis; no whole-audit, implementation-acceptance,
or production-adoption claim is made. Await H correction, then combined-code
root review before targeted real execution.

(End of review — readonly H-owned only; L/C API-frozen reads only as cited.)
