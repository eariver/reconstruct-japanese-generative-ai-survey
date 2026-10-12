# DM021 promotion/adoption — exact source binding (read-only observation)

2026-10-13 JST, design Co-Worker. Reconstruct at Human commit
`b3feb711d8aeaa5b32e323e94108bba52f89bd3c` (log confirms `b3feb71` on top,
status clean except untracked `notes/rephase-1-dm021-promotion/task.md`).
Candidate source observed at
`/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`.
All observations below are read-only: `rev-parse`, `status --porcelain`,
`diff --cached/--name-only`, file reads, and a stdlib hash/mode comparison.
No scripts run, no fixtures, no imports of application modules, no
restoration, no index/ref/object/network writes.

## 1. Identity observation (sanitized Git env, all rc=0)

Commands used (each prefixed with
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`):

- `git rev-parse HEAD` → `409b292756dd1277b9dfae87679934c0d2ce251c`, rc=0.
- `git rev-parse HEAD^{tree}` → `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, rc=0.
- `git status --porcelain=v1 -uall` → exactly the 13 freeze rows (3M + 10??),
  byte-identical to `freeze-pre.json` `status` field, rc=0.
- `git diff --cached --name-only` → empty (no staged/intent delta), rc=0.
- `git diff --name-only` → the 3 modified paths, rc=0.

A stdlib re-hash of all 13 working-tree files matched `freeze-pre.json`
sha256 + mode (`0o664`) for every path: `ALL_MATCH`.

## 2. Exact 13-file pins (from final `freeze-pre.json`, re-observed equal)

HEAD409 alone excludes this overlay. P1 increment is 3A1M; LF2I 9 preserved.

| Path (candidate-relative) | SHA256 prefix | mode | bytes |
|---|---|---|---|
| `scripts/survey_editorial_correction_proposal_v2.py` (P1 A) | `5d2fde45…` | 0o664 | 110155 |
| `schemas/editorial-correction-proposal-v2.schema.json` (P1 A) | `5623c0d9…` | 0o664 | 3945 |
| `schemas/reader-surface-semantic-review-v2.schema.json` (P1 M) | `e8598239…` | 0o664 | 4219 |
| `tests/test_survey_editorial_correction_proposal_v2.py` (P1 A) | `f581fad0…` | 0o664 | 112708 |
| `scripts/survey_reader_surface_gate_v2.py` (P1 M) | `e7305884…` | 0o664 | 94511 |
| `schemas/reader-surface-gate-v2.schema.json` (P1 M) | `fe4a96f4…` | 0o664 | 6894 |
| `scripts/survey_longform_derivation_v2.py` | `c09c5558…` | 0o664 | 62260 |
| `scripts/survey_longform_generated_v2.py` | `d480e11d…` | 0o664 | 39992 |
| `scripts/survey_longform_semantic_publication_v2.py` | `4d235a38…` | 0o664 | 36224 |
| `schemas/longform-publication-source-manifest-v2.schema.json` | `4dadf873…` | 0o664 | 2720 |
| `schemas/longform-reader-input-v2.schema.json` | `7bae9d2a…` | 0o664 | 10624 |
| `tests/test_survey_longform_derivation_v2.py` | `ce687447…` | 0o664 | 91161 |
| `tests/test_survey_longform_publication_integration_v2.py` | `4a03b564…` | 0o664 | 107757 |

Full SHAs, byte counts and the complete patch pin
(`complete-p1-correction-13path.patch`, 604448B, SHA256
`85e9d9ab3c972a786afb1cf2f941bf4dbcfd4980f2e63d0ad9cf6df3cb55963c`)
are recorded in `outputs/rephase-1-dm021-p1-assessment.md` §2 and the final
freeze files; this unit introduces no new pins. Contract decision
`outputs/rephase-1-dm021-contract-decision.md` is unchanged (SHA
`07e899901f488b256ca846c62b1a1fab3edadc880f34593a38078412aeb3c661`).

## 3. Controller / schema / State callsites (candidate-relative `file:line`)

- Revalidation reason closed set:
  `scripts/survey_agent_control_v2.py:45`
  (`REVALIDATION_REASON_CLASSES = {"REVIEWED_CORE_CHANGE"}`).
  Any editorial adoption under this literal with editorial-only bytes would be
  a false reason; P1 deliberately adds no reason
  (`scripts/survey_editorial_correction_proposal_v2.py:1-23` docstring:
  "No writes, no approval, no reason enum, no State adoption").
- Seven-role admission map (seven checkpoint roles + canonical Reader Gate):
  `scripts/survey_agent_control_v2.py:685-693`.
- Public revalidation entry + truthfulness-relevant guards:
  `scripts/survey_agent_control_v2.py:1773-1798`
  (signature; reason-class membership check `:1789-1790`; nothing-to-supersede
  refusal `:1796-1798`), epoch/lifecycle/Preview/downstream/exception guards
  `:1799-1812`, Architecture-approval provenance `:1813-1822`, prior-checkpoint
  provenance `:1823-1837`, pending-basis binding `:1838-1840`.
- Changed-vs-preserved computation and binding to the checked pending basis:
  `:1844-1886` (no changed artifact ⇒ refuse at `:1875-1876`; row mismatch
  vs pending basis ⇒ refuse at `:1885-1886`).
- Adoption QA (fresh manuscript/bundle/reviews/Gate over the NEW bytes):
  `:1898-1944` (manuscript + quality bundle `:1904-1916`, semantic/visual
  reviews `:1917-1929`, Gate replay `:1930-1940`, all bundle checks PASS
  `:1941-1944`).
- Owned write set + failure semantics (exclusive record create, known-bytes
  State replace, pre/post validation, owner-aware rollback that never deletes
  unknown/foreign bytes): `:1995-2046` establishment through rollback
  (`:2013-2023` pre-mutation rechecks, `:2027-2046` create/verify/replace,
  `:2047-2152` disposition-classified recovery). No global CAS or crash
  atomicity is claimed (`:1559-1567` states the bounded guarantee explicitly).
- State-bound active-record resolution (None when absent; referenced-invalid
  is fail-closed, never fallback):
  `scripts/survey_agent_control_v2.py:1084-1107`.
- Strict public State validator (pending publication is never active State):
  `:348-350`; internal validator with provenance/epoch/checkpoint checks from
  `:353`.
- Preview/Candidate chain (fresh Human Preview only):
  `:1465-1497` — requires `RELEASE_CANDIDATE` + pending Preview (`:1475`),
  canonical Candidate presence + `publication.validate_candidate` (`:1480-1483`),
  writes approval + provenance and revalidates State (`:1484-1496`).

## 4. Gate / review / receipt / readback callsites

- Gate evaluation requires machine-checkable semantic authority; omitting
  semantic review cannot PASS:
  `scripts/survey_reader_surface_gate_v2.py:1234-1260`.
- Gate record validation replays derivation and compares the recorded
  route/receipt binding:
  `scripts/survey_reader_surface_gate_v2.py:1794-1839`
  (replay at `:1832-1837`, mismatch ⇒ refuse at `:1836-1837`).
- Per-manuscript derivation binding with exact reviewed-target and
  semantic-review matching, Longform route at `:1160-1198` (canonical
  `publication/v2/reader-surface-input-v2.json` suffix `:1164-1169`, sibling
  receipt reload `:1173-1175`, reviewed-target `:1178-1179` and review
  `:1180-1181` equality, output-vs-manuscript `:1195-1197`) and Weekly route at
  `:1199-1231` (`reviewed_reader_input` `:1211-1212`, review `:1213-1214`,
  outputs `:1228-1230`).
- Longform receipt construction (pure constructor returning dict with
  `receipt_sha256`): `scripts/survey_longform_generated_v2.py:606-638`.
  Public receipt validator **itself reloads and validates the persisted
  semantic review** (`:665-673`, reload at `:686-693`), pins contract
  (`:681-684`), enforces canonical edition paths (`:721-730`), and replays
  exact canonical FILE bytes plus deterministic outputs (`:735-757`).
- Weekly authored envelope (cover/frontmatter/final-summary only; body lives
  in accepted Draft/Synthesis):
  `scripts/survey_weekly_derivation_v2.py:146-179`;
  Weekly derivation context `:475-570`; Weekly receipt validator at `:726`.
- Longform initial derivation (DRAFT_COMPLETE-only boundary) vs healthy
  readback allowlist (DRAFT_COMPLETE, VALIDATED_DRAFT, RELEASE_CANDIDATE,
  FROZEN, RELEASED; no pending-basis bypass, no manufactured former-State):
  `scripts/survey_longform_derivation_v2.py:1101-1139` vs `:1142-1182`.
- Quality bundle validator: `scripts/survey_quality_v2.py:232`.

## 5. P1 proposal / graph / retention callsites

- Read-only APIs (in-memory only; staged authoring input required; planned
  reader ref prospective):
  `scripts/survey_editorial_correction_proposal_v2.py:1601-1632`
  (`prepare_proposal`), `:1698-1830` (`validate_proposal`, returning only
  `REVIEW_REQUIRED` `:50` / `REVIEW_BOUND_PROPOSAL` `:51`).
- Route allowlist (THEMATIC/LONGFORM_SPECIAL primary, WEEKLY/WEEKLY_MAGAZINE
  envelope-only): `:53-54`, `:345-352`.
- Eligibility (healthy VALIDATED_DRAFT, approved Architecture, pending Preview
  without provenance, pending downstream, inactive exception): `:327-342`.
- Three identities: original checkpoint `:355-377` (exact State-pinned ref,
  identity/producer checks `:365-369`); active-before via State-bound record
  with path-rebind refusal and live-byte agreement `:380-411`
  (`ACTIVE_PATH_REBIND` `:401-402`, drift refusals `:406-409`).
- Derivation routing (Longform readback loader vs Weekly current-State loader)
  and canonical bytes:
  `:431-445` (`load_derivation_for_readback` for Longform, `load_derivation`
  for Weekly), `:448-451`.
- Before-graph with single deterministic COPY/KEEP policy; mutable set =
  effective rows + receipt outputs + receipt + reviewed reader + bundle result
  paths + State + pre-TeX review + publication-authored inputs:
  `:563-606` (policy at `:597-599`).
- Retention plan (KEEP ⇒ `retained_ref`, COPY ⇒ prospective
  `<proposal_dir>/retained/before/<path>`; traversal/alias/overlap/conflict/
  pre-existing-destination refusals; plan only, writes nothing): `:1231-1288`.
- Pipeline bindings over BEFORE bytes (canonical rederivation, no-change
  refusal, upstream equality, receipt/Gate/bundle/pre-TeX validation, graph +
  digests, proposal shape with `PROPOSED` status and no AFTER authority):
  `:1291-1492` (proposal object `:1454-1485`).
- Scope binding to the existing independent review (absent block ⇒
  `REVIEW_REQUIRED`; non-WITHIN / wrong-before / wrong-after / stale-upstream
  / non-PASS substantive check ⇒ refuse): `:1635-1695`.
- Proposal schema strict top-level keys
  (`schema_version proposal_id issue_id research_profile publication_profile
  route status basis proposed retention_plan`):
  `schemas/editorial-correction-proposal-v2.schema.json` (required list).
- Optional scope block (`version decision before_reader_input
  preserved_upstream_sha256 change_summary evidence_locations`; decision ∈
  WITHIN_APPROVED_AUTHORITY / REQUIRES_OWNER_DECISION / REJECT):
  `schemas/reader-surface-semantic-review-v2.schema.json`
  `properties.editorial_correction_scope`.

## 6. Exact modified docs and candidate deltas in THIS unit

None. This design unit writes only the two new files
`notes/rephase-1-dm021-promotion/analysis.md` and (this)
`notes/rephase-1-dm021-promotion/source-binding.md`. No candidate
source/schema/test edits, no fixtures, no test/build execution, no Git
object/index/ref changes, no network/Production/State writes, no intake
refresh. All P1 evidence qualifications (filtered `named_status`, HEAD-inode
apply proof, transient `add -N` erratum, snapshot≠continuous-proof, local-only
config/case/count predicates, lost pre-fix script bytes) remain in force as
stated in the assessment and the mandatory closeout resolutions.
