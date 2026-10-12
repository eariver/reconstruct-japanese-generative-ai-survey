# DM021-P1 correction4 final resolution — independent D1/E1 review (read-only)

2026-10-12. Same author-independent reviewer. Read root `astra-review-r4.md`
(D1+E1), latest packet `notes/rephase-1-dm021-p1/evidence-20261012T072355Z-
correction4/` (report/freezes/`run_final.py`/proof/patch), actual candidate
source at `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/
candidate-partial-b40de60` read-only (no code/test rerun, no network, no
commits, no subagents; no OWN-copy probe — no concrete ambiguity required one;
all findings source/log-cited).

## 0. Explicit corrections of old overclaims

- Prior `evidence-20261012T060946Z-correction3/independent-final-resolution.md`
  BOUNDED_PASS claimed full transitive closure. Root R4 proves that claim was
  an overclaim: Discovery acceptance REQUIRED `x_source_intake{path,sha256}`
  and `records[].raw_refs{path,sha256,byte_count}` plus X-manifest locals were
  absent from graph/frozen/retention. That completeness PASS is WITHDRAWN to
  that extent; this resolution re-verifies D1 below.
- Prior runner PASS language for `run_correction.py` (called fail-closed/
  exclusive) was an overclaim: root E1 lists actual script facts —
  existence-then-`w` writes (not O_EXCL), parent freeze Git inherited routing
  with unchecked returncodes, incomplete Python routing rejection, finally
  deletes `__pycache__` BEFORE post-freeze (masking). Prior exact-run evidence
  is preserved but QUALIFIED as non-certified (not fail-closed/exclusive/
  no-cleanup). This resolution verifies the NEW `run_final.py` instead; old36
  (3255s) and older runs stay their own scope, no count transfer.

## 1. FULL pins

- Base HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status exactly 3M10A,
  freeze-pre == freeze-post, `git diff --cached --name-only` empty (no index
  intent this round; R4 `gen_correction_patch.py` is copy-based, `add -N`
  THERE only).
- M gate schema `fe4a96f4` 6894B; M pre-TeX schema `e8598239` 4219B
  (UNCHANGED); M gate script `e7305884` 94511B; A proposal schema `5623c0d9`
  3945B (UNCHANGED); A LF2I manifest `4dadf873`/reader `7bae9d2a`/
  derivation `c09c5558`/generated `d480e11d`/semantic-pub `4d235a38`/
  LF tests `ce687447/4a03b564` stable; A module `5d2fde45` 110155B;
  A test `f581fad0` 112708B — all `0o664`.
- Patch `complete-p1-correction-13path.patch` 604448B SHA256
  `85e9d9ab3c972a786afb1cf2f941bf4dbcfd4980f2e63d0ad9cf6df3cb55963c`,
  13 `diff --git` (header line says "R2" — cosmetic stale label; base
  HEAD/tree correct, content verified by apply proof). `run.exit=exit=0`,
  `proof-apply.exit=exit=0` (empty check out/err). `deps.txt`: Python 3.14.4
  `optimize=0`, jsonschema 4.23.0, pypdf 6.16.2, git 2.53.0.
  `caches-post.json={}` (`PYTHONDONTWRITEBYTECODE=1`, recorded not deleted).
  `runner-meta.json`: argv/cwd/interpreter, `optimize=0`, forced Git3,
  inherited Git/Python rejected (`[]`).
- Run: `Ran 36 tests in 3308.284s OK` (9 P1 + 27 Gate). Proof: byte-copy →
  revert 13 in COPY to clean409 (`status=""`, HEAD409/tree8ce) → `apply
  --check` + `apply` AS SAVED → applied files/modes/status == freeze-pre
  (re-verified). `preserve-prior/` retains correction3 module/test/report/36
  raw; `attempt-1-d1-regex/` + `attempt-2-d1-delta/` preserved with analyses.

## 2. D1 — Discovery/X collectors: FIXED (source-verified)

- Module `1124-1215`: finds pinned `upstream:discovery-acceptance` nodes
  (checkpoint-bound, not receipt-prefix iteration). Per acceptance:
  `discovery_path/sha256` → `upstream:discovery-raw-jsonl` KEEP+frozen;
  REQUIRED `x_source_intake{path,sha256}` (exact 2-key shape, never URL) →
  `upstream:x-source-intake` KEEP+frozen; X-manifest typed locals via
  schema/validator conventions (no new intake, no generic follow):
  `production_profile{path,sha256}` → `upstream:x-production-profile`
  (frozen; unions with State profile if same path/sha),
  `runs[].task{path,sha256}` → `upstream:x-task:<run_id>` (frozen),
  `runs[].result.raw{path,sha256,byte_count}` → `upstream:x-raw:<run_id>`
  (frozen, `len==byte_count` bound `1189-1190`); `records[].raw_refs[]
  {path,sha256,byte_count}` (REQUIRED minItems, explicit) →
  `upstream:discovery-raw:<did>` (frozen, SHA+size bound `1211-1212`).
  `source_locator` (URL), drive paths, policy/series literals, historical SHAs
  deliberately NOT followed (provenance only, `1126,1195`). Missing/
  unclassified → `DISCOVERY_*/X_*` stop, never omit. All literal refs are
  `col.pinned` SHA (+size) checks, not name-prefix claims. No tool/prompt/
  control refs in these fixtures' manifests (all X locals research here) —
  distinction recorded in code comment, none omitted.
- Frozen/retention: new roles all `upstream:*` → frozen via existing
  `_frozen_member_kinds`; all KEEP (not in mutable set) with `retained_ref`;
  correct research/raw KEEP+frozen vs operational distinction.
- Oracle (independent): `_assert_transitives_expected_set` extended
  (`test:759-792`) derives expected JSONL/x-manifest/profile/tasks/raws/
  raw_refs IN TEST via independent `core.load_json` of actual acceptance/
  manifest (explicit fields, never P1 nodes/receipt list/URLs), asserts EACH
  KEEP+frozen/retention with sizes; wrappers operational excluded; pub/QA/
  State/receipt/candidate excluded; stale completeness sibling still NOT
  adopted. D1 outside-tree raw (`raw/source.json` outside source/survey roots)
  proves tree-walk insufficient (path-prefix check `1627`).
- Seam phase classification (required note): worker report calls it
  "mutated BEFORE validate-with-scope" — ACCURATE. Test
  `d1-outside-raw-scope:1608-1672` snapshots clean, mutates outside raw,
  asserts injected delta ONLY raw, then calls `validate_proposal(..., scope)`
  and expects refusal (`DISCOVERY|RAW|REF_DRIFT|SIZE|RECHECK|RECEIPT|
  DERIVATION`). This is PRE-CALL staleness (fault injected before the P1
  call), fail-closed EARLY in `_pipeline` rederivation (discovery validator
  `DERIVATION_REFUSED`) or at D1 pin/size/final-recheck — NOT a late-in-call
  concurrent mutation after scope. No-cleanup-masking proven (mutated-vs-post
  identical, HEAD/status unchanged beyond injected, explicit restore). Late-
  in-call stability remains covered by C3 late-helper seams + `reverify()`;
  existing collector final checks DO include raw deps (pinned raw files under
  `reverify()` + full receipt recheck). Classification recorded, not a defect.

## 3. E1 — NEW runner: FIXED (source-verified)

- `run_final.py` (252 lines, NEW, old `run_correction.py` untouched):
  rejects `GIT_*`/`PYTHONPATH`/`PYTHONHOME`/`optimize!=0` BEFORE any candidate
  Git (`125-133`); parent freeze Git sanitized forced-3 with EVERY rc checked
  (`72-97`); exclusive `open(x)`/O_EXCL for EVERY log (`55-61,137-165,
  175,195-227,235`); records argv/cwd/interpreter/env + forced Git
  (`runner-meta.json`); compares all13 hashes/modes/named-status(13 rows,
  caches ignored)/base pre AND finally-post (`179-187,238-243`); timeout 5400s
  (prior 3255s basis) with partial preservation (`209-218`); NEVER
  deletes/repairs source/cache before comparison — records caches separately
  (`list_caches`, `caches-post.json`, `229`); child unittest env sanitized
  forced-3 (`193`). Prior script facts (E1) fixed; prior evidence
  preserved/qualified, not certified. PASS. Report §E1 accurate.

## 4. Scope/limits (not blanket PASS)

- Bounded preparatory validator only (`REVIEW_REQUIRED/REVIEW_BOUND_PROPOSAL`);
  retention plan != retained bytes; whole NOT_READY, DM021 OPEN; no genuine
  publication/proposal adoption or full-historical retention proof. Verdict
  covers D1/E1 at pins §1 with 36-method + apply-proof scope only.

## 5. Verdict: BOUNDED_PASS (correction4, D1+E1)

D1 finite typed collection (SHA/size/frozen/operational, no URL/string
following, independent oracle + outside-tree + stale-sibling proof) and E1
exclusive runner (explicit errors, full routing/optimize/O_EXCL/returncode/
no-cleanup discipline, 36/3308s + AS-SAVED apply proof) verified in actual
source/logs. Old graph-completeness/runner overclaims explicitly corrected
(§0). Stop at Human Commit Point; Commit/Push Human-owned.
