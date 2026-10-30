# DM022 C1 correction (root REJECTED → corrected, NO test run, NO Commit Point)

2026-10-28. C1 owner corrects assigned files only with apply_patch (Edit/Write).
First integrated return preserved; root `astra-r1-source-review.md` REJECTED is
authority; no Commit Point (root whole unit ongoing). Old returns preserved
(`author-C1-return.md` historic, not edited). No Human commit/readback, no
ordinary commits/config writes beyond owned `config/survey-production-v2.json`
(pipeline 76 already, unchanged here), no network/old-runner/cleanup. No tests
run on shared candidate while A2/B/C2 edit; AST own files only (no imports/cache).

## 1. Root findings addressed (C1 scope only)

- **C1 `_is_prearch_record` used `reason_class` (wrong).** Fixed to strict
  schema `reason` (`PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` +
  `REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`). Publication kinds keep
  `reason_class`; PREARCH has no `reason_class` (discriminators return False).
  `_record_kind` refuses PREARCH as `DM022_WRONG_FAMILY` (never CANONICAL,
  no auto-upgrade). Helper `make_prearch_record` fixed to `reason`.

- **Longform derivation docstring-only (no accepted-graph propagation).**
  Wired FULL LOW detached research proof in `survey_longform_derivation_v2.py`
  + `survey_weekly_derivation_v2.py` (C1 owned, no PREARCH publication branch):
  path-reloading `resolve_research_authority(root, state_path)` (never State
  dict, never agent/State/HIGH/guard) → `{family, checkpoint, artifacts(parsed),
  lineage}`. When PREARCH: verify kind/reason/operation/boundary/checkpoints,
  4 NamedRefs exact, artifacts parsed (4 keys), lineage triplet+paths,
  `artifact_refs` 4 NamedRefs. Upstream `evidence/materiality/completeness`
  via LOW parsed artifacts + live re-hash (no TOCTOU permit); all other
  checkpoints via agent (historical+current). Split preserved (operational State
  via `agent.validate_agent_state` separate from detached upstream; no recursion).
  Positive G76 proceeds; wrong-role publication use refuses in agent/B/C2, not
  blanket-refused here. Function-local LOW import (no preload/cycle).

- **Hist accepted graph: newCP/report/proof/schema ownership + ownEpoch pins.**
  Added `verify_prearch_accepted_graph(repo_root, record_path, epoch, label)`:
  OWN-epoch `git show` (never live/HEAD/State/agent), strict kind/reason/
  operation/boundary/checkpoints/4 NamedRefs/lineage (research supersedes
  separate, never publication)/sole `DM022_SUPERSESSION_PROOF`/SELF/
  revision_root ownership/request/report/proof/decision under revision_root/
  pipeline G76 at epoch. Publication `_record_kind`/`supersedes` remains ONLY
  LEGACY|EDITORIAL|VERSIONED (PREARCH refused; no PREARCH arm added – R5
  overbroad revoked by R6/ROOT).

- **ALL generation callers handle G67/G71/G76.** `_normalize_generation`
  (OLD→G67, NEW→G71 historical compat only, never wrong binding). Added
  `_derive_current_family_from_disk` (current pipeline + live 7+7 existence,
  never hardcoded). `survey_versioned_renewal_source_v2._expected_closure_names`
  requires explicit family; `verify_renewal_source_proof` derives CURRENT via
  disk (not hardcoded G76). `survey_versioned_renewal_v2` OBSERVE+PREPARE derive
  CURRENT via disk. Old proofs use OWN epoch derived family. Historical
  `_expected_staged_code_deps` default OLD→G67 preserved for compat.

- **Registry: installed report hash sync.** Installed
  `dm022-preadoption-report-v2.schema.json` is `10238a1a…` (path
  `schema-proposals/`→`schemas/` by A), proposal `21369608…` preserved as
  historical. `_KNOWN_SCHEMA_SHAS` report entry now both. Added
  `_require_owned_schema_fingerprint(repo_root, schema_path)` (live bytes SHA
  must be known; proposal alone never authorizes runtime). Other 4 installed
  == proposal (verified sha256sum). Old known sets preserved.

- **P3S/weekly/longform actual module closure (R4/R5 literal, not count-only).**
  Weekly/Longform: added `_verify_actual_import_closure` (AST own file, actual
  `scripts.*` imports ⊆ G71/G76 literal; extra → expansion return, never silent
  omit; counts alone never authorize) called from `current_closure`. Staged:
  already AST + set equality; updated CURRENT to G76 (70) with explicit
  G71/G76 families. All compare R4/R5 literal sets member-wise + actual files
  exist + actual imports, not len-only.

- **Narrow G71→G76 SAME upstream authority (no generic dict).** Delta check
  (`G76-G71==2+5`) is necessary but NOT sufficient; code comments + tests state
  SAME research/Profile/Architecture/Draft/reader authority must be verified
  separately via full U/C proofs (affected/unaffected, obligations, lineage)
  elsewhere (HIGH adoption). No claim that set difference alone proves sameness.

- **Strict LOW API + consumer split + positive G76.** Resolver
  `(repo_root, state_path)->{family,checkpoint,artifacts(parsed),lineage}`
  and checker
  `(repo_root,checkpoint_path,report_path,before_copy_path)->list[str]` used
  with exact signatures (function-local LOW, no caller-dict authority, no
  exception-swallowing, no duck-typing). Derivations use resolver (read-only
  consumers); checker with before_copy is HIGH adoption (not derivations –
  derivations lack retention context; split documented). No blanket refusal:
  PREARCH upstream with valid proof proceeds to rendering.

- **Test helpers: 2+5 in corresponding existing helpers (not new-only).**
  Updated C1-owned existing helpers (ownership, disjoint):
  `test_survey_editorial_staged_source_v2.py` CURRENT 63→G76 70 + 2+5 list;
  `test_versioned_renewal_history_phase_h.py` CURRENT NEW→G76, historical
  OLD→G67 (+G71 explicit); `test_versioned_renewal_source_phase_s.py`
  `_closure_names` + proof closure derive CURRENT via disk (not hardcoded NEW);
  `test_versioned_renewal_history_author_h_20261025.py` assert G71 (not NEW).
  New helper `dm022_c1_fixture_helpers_v2.py` retains explicit 2+5 lists.
  Did NOT edit non-C1 helpers (e.g., `test_group_c_editorial_consumers_v2.py`
  35/22 check – C2/B owned; our `_SHARED_PY` stays G71 35 for compat, G76 via
  `_SHARED_PY_G76` 37 for CURRENT – cross-owner coordination via root if needed).

- **Family tests run actual fixtures + public verifiers (not dicts/counts).**
  Rewrote `test_dm022_c1_family_closure_v2.py` /
  `test_dm022_c1_research_graph_v2.py` to: actual files exist + AST + R4/R5
  literal sets + owned fingerprint (`_require_owned_schema_fingerprint`) +
  independent Git DBs with real epochs calling public verifiers
  (`_derive_tool_generation`, `verify_prearch_accepted_graph`,
  `load_typed_checkpoint_record`, `is_prearchitecture_record`,
  `_record_kind`) on real files/epochs (refusal with expected code still proves
  epoch use). No `reason_class` manufactured PREARCH; strict `reason` files.
  Private frozen copy from saved R1 with ONLY C1 overlay for pure family runs
  is test design (own fixture DB/raw logs/pins); no application against
  changing shared candidate (tests NOT run here).

## 2. Full written paths (apply_patch, C1 only)

Source (candidate-work):

- `scripts/survey_versioned_renewal_history_v2.py`: `reason` fix,
  `_KNOWN_SCHEMA_SHAS` report both hashes, `_require_owned_schema_fingerprint`,
  `_derive_current_family_from_disk`, `verify_prearch_accepted_graph`
- `scripts/survey_versioned_renewal_source_v2.py`: explicit family,
  `_derive_current_family`, CURRENT via disk (not hardcoded G76)
- `scripts/survey_versioned_renewal_v2.py`: OBSERVE+PREPARE CURRENT via disk
- `scripts/survey_weekly_derivation_v2.py`: FULL LOW upstream + AST closure
- `scripts/survey_longform_derivation_v2.py`: FULL LOW upstream (replaces docstring-only)
- `scripts/survey_longform_generated_v2.py`: AST closure
- `scripts/survey_editorial_staged_source_v2.py`: (prior G76 already; no new change here beyond existing)
- `config/survey-production-v2.json`: unchanged (76 already)

Tests (C1 owned):

- `tests/dm022_c1_fixture_helpers_v2.py`: `reason` fix
- `tests/test_dm022_c1_family_closure_v2.py`: rewritten (files+AST+owned fingerprint+own-epoch public verifiers)
- `tests/test_dm022_c1_research_graph_v2.py`: rewritten (real files+public LOW/history verifiers+own-epoch)
- `tests/test_survey_editorial_staged_source_v2.py`: 63→70 + 2+5
- `tests/test_versioned_renewal_history_phase_h.py`: NEW→G76 CURRENT, OLD→G67 (+G71)
- `tests/test_versioned_renewal_source_phase_s.py`: derive CURRENT via disk
- `tests/test_versioned_renewal_history_author_h_20261025.py`: assert G71

Packet: `notes/rephase-1-dm022-prearchitecture-implementation/author-C1-correction.md` (this file; old returns preserved).

## 3. Verification (explicit: NOT run)

- `ast.parse` own files (no imports/cache): OK (history/source/renewal/weekly/
  longform/staged + helpers/tests). Config pipeline 76.
- Tests NOT executed (shared-candidate discipline while A2/B/C2 edit; no fixed
  snapshot env). No PASS, no count transfer, no fake pending/hash-only/schema-auto.
- No workspace `git status/diff/log`, no ordinary commit/push, no fixture objects
  in reconstruct, no network/restore/old-runner/cleanup.

## 4. Exact unresolved predicates (honest, return to root before broadening)

- Full 70-file own-epoch fixtures at real G76 epoch calling
  `verify_prearch_accepted_graph` + `verify_closure_at_commit` +
  `verify_renewal_source_proof` end-to-end (requires fixed snapshot with complete
  G76 source + independent Git DBs + raw logs/pins; minimal fixtures here refuse
  with expected codes, proving epoch use but not full positive).
- Positive G76 upstream rendering via LOW in longform/weekly with real G76
  accepted graph (requires A2 LOW + B agent PREARCH branches + fixed snapshot;
  code allows positive path, not yet witnessed).
- Cross-owner `test_group_c_editorial_consumers_v2.py` 35/22 expectation vs G76
  37/27 CURRENT (C1 preserves `_SHARED_PY==35` compat; CURRENT via `_G76`;
  needs root coordination if C2/B expect update).
- A2 LOW/HIGH replacement ongoing: checker `before_copy` path derivation for
  derivations (derivations use resolver; HIGH adoption owns checker+retention –
  split documented, root confirmation pending if checker required in consumers).
- Implementation report SHA sync done (10238a1a… current + 21369608… historical);
  runtime owned-fingerprint enforcement added but full CURRENT schema-vs-disk
  verification across all paths needs fixed-snapshot witness.

No map contradiction beyond above; if any required reader/closure/contract
contradiction found later, return exact root before broadening. Do NOT stop at
Human Commit Point (root whole unit ongoing).
