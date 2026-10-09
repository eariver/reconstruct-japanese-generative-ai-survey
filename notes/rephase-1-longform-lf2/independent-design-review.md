# LF-2 independent design review (design only, no code/test acceptance)

2026-10-09. Author-independent scoped DESIGN reviewer, separate from root
contract author and General proposal author. No source edits, fixtures, tests,
builds, network, refs, commits, or subagents. Read-only verification used
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file` with all
Git-root routing overrides unset. This review covers the SELECTED contract
scope only; implementation (LF-2I) acceptance is explicitly out of scope.

## 1. Identities verified read-only

- Composite `/tmp/opencode/jgas-lf2-design-20261009T113013Z`: HEAD
  `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, parent
  `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`; status exactly the 3 LF-1
  untracked files; overlay hashes runtime `233e8655…0744cf7`, schema
  `7bae9d2a…43`, test `ce687447…913` (all re-hashed, match).
  Fetch AND push origins inert `https://example.invalid/...`.
- Reconstruct checkout HEAD `b11c2d0b28d49c0df560273a7f49f7e6739aee85` observed
  (packet untracked only). Preparation claims corroborated by
  `current-verification.log` (all 7 overrides absent, zero shared objects,
  DST nlink==1); its stated non-retroactive scope is accepted, not extended.

## 2. Reviewed documents (sha256)

- `outputs/rephase-1-longform-lf2-contract-decision.md` `4795a586…36d6`
- `notes/rephase-1-longform-lf2/task.md` `b900cca3…bbf5b93`
- `notes/rephase-1-longform-lf2/design-proposal.md` `23b2e4dc…ed4bf3`
- `notes/rephase-1-longform-lf2/astra-design-feedback.md` `7cbc8867…53fdcc2`
- `notes/rephase-1-longform-lf2/design-correction.md` `042d0491…150729`
- `evidence-20261009T113013Z/preparation-qualification.md` `89828b49…0af939`

Contract precedence ("choices below govern conflicting proposal wording",
contract L5) is the binding tiebreak throughout §3.

## 3. Confirmations (spot-checked against DST bytes)

- C1 Directive: legacy consumer `run_..._base.py:133-135`, LF-1 lexists
  refusal `derivation:988-993` both confirmed. Restricted directive-absent
  route needing no blanket Human bind/migrate/defer decision is coherent;
  legacy check/writer untouched, directive-bearing-edition block retained.
- C2 Caller: bridge `_advance_stage:365-407` (validate→reviews→checkpoint→
  advance), `validate_stage:601-647`, `build_stage_checkpoint:1267-1329`
  confirmed; registry gap `handlers:452-479` correctly NOT repaired; no
  executed-route claim. Correct.
- C3 Two-pass: review loader `:884-1045` signature/semantics (SEMANTIC_
  EDITORIAL-only, digest, drift, PASS rules), Weekly two-pass model
  `:70-153`, refuse-existing `:135-137`, tool-guard-before-writes `:116-124`
  all confirmed. Pass1/pass2 windows and no-silent-pass1-upgrade are closed.
- C4 Scanner/schema/admission: Weekly-only `_derivation:1086-1118`,
  DIRECT_PRIMARY preserved `:1082-1085`, Gate schema only two arms
  `:160-185`, scanner fallback gaps `:787-863` vs LF-1 nested fields all
  confirmed. Both runtime AND schema Longform arms required — correctly set.
- C5 Digests: file-SHA vs canonical-object-hash distinction matches Weekly
  `build_receipt:634-666` and review digest `:926-931`. Correctly separated.
- C6 Readback/provenance: LF-1 `load_derivation` has no `pending_basis`
  param (vs Weekly `:475-500`); historical-State-SHA-as-provenance plus
  mandatory current validation is the right boundary; pending/changed-Core
  refusal with per-operation documentation is honest, not a gap.
- C7 Fidelity: numbered-section authority + starred-heading exclusion
  (`fidelity:106-118`), renderer numbered `\section` per package, manuscript
  `reader_locations` obligations confirmed; type/identity-only fixture claim
  with stop-on-blocker is correctly bounded, no auto semantic approval.
- C8 Budgets/oracles: path table A/M/R labels, LF-1-Gate-schema corrections,
  uncommitted-composite guard vs synthetic committed fixtures, and
  prospective-only oracles with no performed-test claims are all sound.
  Preparation-qualification limits (guard omissions, 689-files units,
  attempt-1 handling) are preserved, not papered over.

## 4. Findings

- F1 (Major, resolved-by-precedence): contract §4 REQUIRES receipt replay to
  reload+validate the persisted review AND Gate to reload it, explicitly
  rejecting correction §6's "preserves that split" (receipt does not reload,
  Gate does). A worker reading correction §6 normatively would diverge.
  Resolution: contract governs; LF-2I task must cite contract §4 verbatim
  and annotate correction §6 as superseded on this point. No design rework.
- F2 (Minor editorial): correction §6 heading "five distinct digests"
  enumerates six items (a)-(f). Resolution: fix count or merge (e)/(f) in a
  correction addendum; LF-2I uses contract §4 digest definitions.
- F3 (Minor clarity): contract §6 oracle item 4's "If a later-state fixture
  is unavailable, return the precise unsupported scope" is the correct
  feasibility guard for FROZEN/RELEASED readback; carry it as an explicit
  LF-2I stop condition rather than an implicit fallback.

No generic CAS/crash-atomicity, universal-parser, old-suite, or new-Human-gate
demands are added: contract already refuses global CAS claims, scopes the
scanner to defined reader-schema display strings, limits tests to affected
paths, and requires no new Human decision for the restricted route.

## 5. Verdict

**DESIGN_BOUNDED_PASS** — selected contract is coherent, source-grounded,
and review-gated end to end (reader-only → persisted review → serializer →
receipt → generated Gate → both admissions → healthy readback), with F1
resolved by stated contract precedence and F2/F3 as non-blocking conditions
for the LF-2I task. No implementation/test acceptance implied.

Design unit closes at Human Commit Point. Next: LF-2I implementation on the
preserved 409+LF1 independent copy after exact identity check, incorporating
F1–F3 conditions. No candidate commit authorized.
