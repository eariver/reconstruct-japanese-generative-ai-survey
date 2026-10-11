# DM-021 P1 — author-independent design review

2026-10-10. Fresh DESIGN reviewer: no authorship, no root/General/Explore participation,
no subagents. Read-only design review only. No code/tests/fixtures/build executed,
no source content reads, no refs/commits/copies, no network/Issue/corpus intake.
Authors' docs untouched. Canonical audit unstarted; whole NOT_READY; baseline 774.
Stop at design Human Commit Point.

## 1. Documents reviewed (FULL SHA256)

- decision `outputs/rephase-1-dm021-contract-decision.md` (114 lines):
  `07e899901f488b256ca846c62b1a1fab3edadc880f34593a38078412aeb3c661`
- task `notes/rephase-1-dm021-contract/task.md` (24 lines):
  `78b20234103cf3799d877e3567512fecd5539dff3d905bd5da9b2d32c9b89eba`
- analysis `notes/rephase-1-dm021-contract/analysis.md` (234 lines):
  `fe62ca589ed5fde8ecd14f303d16b988369f952a089ddc231c2f0679a260a8c6`
- astra-feedback `notes/rephase-1-dm021-contract/astra-feedback.md` (21 lines):
  `410dc94027255f387ef23209398d6924dc99e189c86327650e4df025fc5f7304`
- correction `notes/rephase-1-dm021-contract/correction-and-boundary.md` (165 lines):
  `1a8c61f2f4848a90e477dcde0f18129e7262a9d7f7913d01335d65e1251d2845`
- source-binding `notes/rephase-1-dm021-contract/source-binding.md` (52 lines):
  `846e2a24dd87553c6739035cb42dc4cd097aad5d65717c2036e73dbc3a6cc6ee`
- disposition `notes/rephase-1-dm021-intake/astra-disposition.md` (24 lines):
  `f8b38ce06b3a6ed0a8b42a6944004b9cd1790a265f3cf2bbe48991ffa8e5e2c7`

## 2. Source identity (read-only, limits disclosed)

Worktree `/tmp/opencode/jgas-lf2-design-20261009T113013Z`, env
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`,
no git root overrides, no fetch/writes. Observed:
HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
`log -1` parent-Side subject matches DM-004 cleanup.
`diff --name-status HEAD`: exactly 2M
(`schemas/reader-surface-gate-v2.schema.json`,
`scripts/survey_reader_surface_gate_v2.py`).
`status --porcelain=v1`: same 2M + 7 untracked LF-2I source paths +
`__pycache__` caches (disclosed, not authority). Total 2M+7A as claimed.
No file contents read; 9-file hashes NOT re-hashed here — adopted from
source-binding §6/task pins (publisher4d235a38/test4a03b564/helperd480e11d/
derivationc09c5558/Gatee7305884 + manifest remainder).
LF-2I 43+2 method bounds cited, not re-executed/transferred.
Reconstruct HEAD `c50be33a…` as reported, not re-verified here.

## 3. Selected scope (what PASS covers, what it does not)

PASS covers ONLY: DM021-P1 read-only before-graph / proposed-reader /
retention-plan validator + optional strict `editorial_correction_scope` block
in the EXISTING semantic-review schema. No reason enum, no live writer,
no State adoption, no promotion, no DM-021 fix, no rebaseline.

## 4. Findings

| # | Check | Severity | Result / precise resolution |
|---|---|---|---|
| F1 | ChatGPT operates / Humans gate twice, no new gate/role | PASS | §5 selects placement A inside existing review; assessor = existing ChatGPT reviewer; Architecture/Preview/exception intact; "no new Gate" is structural (no new step), not renaming. |
| F2 | Corrected PASS alone insufficient; exact old/new/upstream relation | PASS | §5 requires PASS + `WITHIN_APPROVED_AUTHORITY` + exact before/after/upstream bindings + substantive scope check; bare PASS/reason/name insufficient. |
| F3 | Optional block backward-compatible; no self-approval | PASS | Ordinary records valid without block; block required only for `REVIEW_BOUND_PROPOSAL`; §5 forbids P1 generating the review PASS/block; machine checks ≠ independence proof. Enforcement is an implementation condition (§6). |
| F4 | Original vs active-before vs proposed-after | PASS | Three-identity table + no-recency-inference + referenced-invalid = stop; `prior_sha256` stays original; effective map via superseded.new + preserved. |
| F5 | 7 rows ≠ closure; real edge validation, no generic resolver | PASS | 7 = validation-6 + Gate; reader/archive/receipt/bib/style/Candidate via manuscript/Gate/receipt/bundle edges; actual validators; conflicts/unknown/dup/unresolvable = stop; dedup preserves logical edges. Exact enumeration/dedup text is the explicit NEXT General return (§6), not a missing contract. |
| F6 | Unknown Candidate inert, not owned | PASS | Optional observed/unadopted; validator + exact agreement else stop; bytes in retention set, no adoption/overwrite; stale filename ≠ ownership. Correctly read-only for P1. |
| F7 | KEEP_IMMUTABLE vs COPY_BEFORE_REPLACEMENT; immutable refs | PASS | Typed rows with role/path/hash/byte-count; deterministic `retained/before/…` destinations; no omitted deps/unknown inputs; no self-retention of plan/review; plan validity ≠ byte existence/authorization. |
| F8 | Missing/race/metadata-vs-content/nonreader distinction | PASS | Alias/traversal/noncanonical refusal; FILE-bytes-must-differ; same-byte metadata → explicit refusal (not R1 routing); drift reported without writes; staleness ≠ semantic change. Read-only TOCTOU note is inherent, non-blocking (no writes claimed atomic). |
| F9 | Longform prose vs Weekly frozen body + closing constraint | PASS | Longform (+`longform_revision`) is primary fixture; Weekly envelope-only; no Draft body/deck override, bib rewrite, or patch language; real loaders, no pending/fake State. Resolves feedback-4 honestly. |
| F10 | Healthy VALIDATED loaders derive proposal; no bypass | PASS | Longform readback loader + authored input; Weekly current-state loader; no manufactured DRAFT_COMPLETE/pending basis; P1 persists nothing. Exact loader-reuse proof is interface-return condition (§6). |
| F11 | No path-rebind-by-SHA; staged review never becomes live review | PASS | Explicit shortcut refusal; staged-path review; promotion (later design) = copy + digest re-verify; canonical-path rules intact; correction-§5 ambiguity superseded. Core anti-authority clause present. |
| F12 | Acyclic DAG; no plan→review→plan cycle | PASS | proposal(old+proposed digests only) → review(proposed path+SHA) → future receipt/Gate → future adoption; scope block carries no proposal/Gate/receipt refs; validator output is `REVIEW_REQUIRED`/`REVIEW_BOUND_PROPOSAL`, never a semantic PASS/Gate/revalidation record. |
| F13 | Budget/producer/consumer clarity; feasibility stop real | PASS | 2A+2M paths named; rest read-only; extra-path/loader gap returns to Astra; no four-file promise override. Creator/assessor/consumer split (§4–§5) sufficient for design; exact ownership text pinned at interface return. |
| F14 | Epochs: new-edition witness vs old migration; R1 nonregression | NOTE (non-blocking) | New synthetic edition witness; no TS-003 migration; mixed-epoch stop; same-Core = control/contract equality-ancestry. "Harmless artifact-only commits" needs an exact allowlist at interface return — default remains stop, so design PASS stands. |
| F15 | No generic resolver/override engine/dashboard/duplicated review | PASS | Actual rederivation/schema checks; no text overrides; affected-checks only; no framework claims. |
| F16 | Canonical reader bytes / upstream-digest / token rules | NOTE (non-blocking) | Exact canonicalization, preserved-upstream digest construction, `proposal_id` token rule belong to the NEXT General interface/fixture return (§6). Contract correctly requires exact byte/digest comparison now; absence is deferred precision, not a design hole. |

No FAIL-grade (blocking) gap found. Nothing forces full-writer design now.

## 5. Explicitly NEXT (not missing contract)

General pre-implementation return per decision §7: exact before-graph
enumeration/dedup rules, schema/API shape (incl. canonical bytes, upstream
digest, token rule, harmless-artifact allowlist), real accepted-fixture plan
(not mocks). Later promotion order (Weekly-subset vs Longform-first) and
promotion/adoption design stay unselected — correctly out of P1.

## 6. Verdict: DESIGN_BOUNDED_PASS

P1 + optional scope block is feasible against the pinned source with no hidden
authority: roles preserved, no new Human gate, PASS-insufficiency closed,
identities/edges/retention acyclic, rebind shortcut refused, output unadopted,
budget/stops real, epochs/regressions bounded.

Necessary conditions before code: (1) General interface/fixture return above;
(2) implement only the 2A+2M paths, return to Astra on any extra-path/loader
gap; (3) no enum/writes/adoption/promotion inside P1; no self-generated PASS;
(4) genuine synthetic scope PASS via existing review loader; type/identity
fixtures ≠ semantic/publication acceptance; (5) DM-021 stays OPEN; whole
NOT_READY, step4/B3 OPEN, audit unstarted; no candidate commit without explicit
authorization. Stop at Human Commit Point.
