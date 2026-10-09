# LF-1 independent implementation/evidence review — CHANGES_REQUIRED

2026-10-09. Fresh author-independent reviewer, not prior workers/root. Read-only
static review + read-only identity checks only. No unittest rerun, no old-runner
invocation, no new content copy needed (no unresolved probe requiring one), no
network, no commits/refs/branches/config in candidate/source/reconstruct, no
fixture mutations. Whole candidate NOT_READY, step4/B3 OPEN, canonical audit
unstarted. No canonical/shipping/production PASS. STOP at Commit Point.

## 1. Identity (independently verified read-only)

- Fixed basis HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (DST rev-parse HEAD/tree match).
- Overlay exactly 3 `??` (status + `diff --name-only HEAD` empty), zero tracked mods.
- Hashes match packet: runtime
  `abd50864e5065d7d69a6c3ccc13d01915be4654aee4aedeac1eb60f9aa33987f`,
  schema `71156a53b776a82928519b0a3f821cf40bd4279550e0bc4973c7ed27394e588b`,
  tests `d4ab5361c7741d10dbe5986bf1f62b85a21646a8e220641469e6395389ba2ca6`.
- DST remote inert `https://example.invalid/rephase-candidate-recovery.git`,
  no `.git/objects/info/alternates`, all six `GIT_*` overrides unset.
- Original source `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` HEAD 409, clean.
- Patch `overlay.patch` (147323 B, new-file `a/`/`b/`) apply proof in
  `verify-apply.log` accepted: fresh `cp -a` copy, HEAD/tree verified, inert
  origin, no alternates, `git apply --check`/`apply` exit 0, post-apply exactly
  three `??`, zero tracked mods, three SHA match. No test repeat for packaging
  (disclosed, accepted for packaging only).

## 2. What passes on final identity (bounded)

- R1 runner: `run-corrected.sh` is fail-closed (absent-log-only, pinned
  HEAD/tree/3 hashes/exact 3-path predicate, zero tracked mods, 6 GIT vars,
  interpreter/version/caller+child cwd/argv/filtered env/inert origin/protocol,
  `cd DST`, numeric exit, finally postguard, `exit CHILD_EXIT`). Proofs:
  wrong-HEAD refuses exit 2 before child (inner log absent); failing child exit 1
  with postguard (final hash). Raw `run-final-batch.log` (6 OK, 562.904s),
  `run-unsupported/heldback/tamper.log` (1 OK each, ~64-73s), all pre/post
  guards clean, exits 0. Limit: per-run DST isolation (alternates/hardlinks)
  relies on preparation + verify-copy; accepted narrowly, not re-asserted.
- R2 archive: `_validate_archive_authorization` enforces exact package count+set,
  duplicate package, exact spec-vs-Result non-CLAIM_BOUNDARY block sets, per-block
  + deck `citation_refs.refs` exact-one for EVERY assigned DID. Five negatives
  (extra/duplicate package, extra/duplicate block, cross-package archive-only
  DID2) + healthy/repair controls + selected-only `{DID1}`/`{DID1,DID2}` all in
  final batch. PASS.
- R4 runner nonreader: `REQUIRED_RUNNER` removed, non-empty-string envelope,
  Profile defines route; runner/review-ref-only changes retain bytes with
  differing `authored_refs`; schema carries no runner/provenance. Final proof. PASS.
- R6 scanner + selected-only + additional: read-only
  `surface_gate.scan_reader_text_lines` BLOCKING/UNRESOLVED refusal before local
  checks; global container/card integrity for EVERY Matrix row then selected-only
  eligibility with fail-closed `missing`; untrimmed URL validated before trim;
  `deepcopy(VISIBLE_TEXT)`; pre-read `_safe_card_path` + `_safe` + `validate_*`
  containment; process-scoped fixture identity. Pure/table/archive code + final
  logs support this. PASS for proved paths. Unselected-HOLD narrower scope is
  disclosed, not invented. Accepted limit.

## 3. Blocking findings (no fix applied)

**B1 — schema/module citation-key mismatch (blocking).** Schema
`$defs/citation_key` pattern `^[A-Za-z][A-Za-z0-9:_-]*$` forbids `.`, but module
`_CITATION_KEY` `^[A-Za-z][A-Za-z0-9:._-]*$` allows `.` and `_bib_key` preserves
dots (`paper.v1-D001` → `sp001paper.v1d001`, runtime:274-278, test:1111-1112,
1342). DID subset allows dots (module `_DISCOVERY_ID`, schema `discovery_id`).
A dotted-DID projection would fail schema validation. Selection requires dots
preserved, so schema must gain `.`. One-char fix + affected rerun required.

**B2 — 17/26 test methods lack final-hash proof (blocking).** File has 26
methods; final raw proves only 9 (batch 6 + unsupported/heldback/tamper).
Unproved on final hash: reordered-normalize, two-package kicker/bib order,
Unknown-org fallback, unknown-DID, duplicate-note, primary-URL-mismatch,
access-ambiguity, unsafe-URL end-to-end, missing-package-row, directive
file/symlink, earlier-lifecycle, state-escape, symlinked-ancestor, mechanical
(redundant w/ runner-reref), no-writer explicit names, needs_more (justified
upstream-only exclusion). Selection §4 explicitly requires directive presence,
unsupported lifecycle/Profile, path aliases/escapes, mechanical stability,
Unknown fallback, reordered-normalize, omission/duplicate/membership/hash/URL/
ambiguity. Code inspection shows implementations present, but old-hash
superseded logs do NOT transfer (test hash changed). Either run the missing
contract-required methods on final identity with `run-corrected.sh` logs, or
get Astra to narrow scope AND trim the test file (new hash + rerun). Table-21
sampling (one mutation per category, not every field e.g. anchors/scope_notes/
labels/paragraphs/qwen/deepseek/kimi) is accepted as bounded only once B1-B2
close; note as limit, not separate blocker.

## 4. Verdict

**CHANGES_REQUIRED** for B1 (schema dot) + B2 (final proof for missing
contract-required methods). No new HEAD/commit/LF-2. Prior packets preserved;
this file is the only addition. No probe artifacts (none created).
