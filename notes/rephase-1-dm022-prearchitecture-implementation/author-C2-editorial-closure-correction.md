# Author C2 — editorial closure generation-awareness (Attempt7 blocker)

2026-10-28 UTC. Owner C2 (replacement). Scope ONLY C2 paths+tests per
coordination: `scripts/survey_editorial_publication_v2.py` (closure only) +
new `tests/test_survey_dm022_c2_editorial_closure_v2.py`. No A/B/C1 edits.
No ordinary commit/Gitconfig/readback/network/Production/cleanup/old-runner.
`apply_patch` only. Tests ONLY NEW private frozen copy; no live-candidate
tests. All owners idle for freeze except B just returned (now idle).
No Commit Point; root unit ongoing.

Binding: Attempt7 `whole-lifecycle-witness-progress.md` §§Attempt7/BLOCKER,
R4/R5 finite families G67/G71/G76 as narrowed by R6/ROOT, C1
`author-C1-epoch-presence-correction.md` (H `a9de2c97…` presence-fixed,
S `b139…` unchanged, stage `a1b97759…` pinned), C1
`_route_code_deps(route,family)` literal 63/70 + `_derive_current_family_from_disk`,
`_derive_tool_generation`/`_normalize_generation`, contract a345bb95 §11,
ROOT 0425c530 §5, R6 role map. P1/P2R/P2V 9/25/14 green preserved from prior
C2 run (no R1 faking, before-graph preserved); NOT rerun here (long burn).
Actual `prepare_publication` long witness will rerun longitudinally.

## 1. Blocker (foreign, C2-owned, NOT patched by witness)

Attempt7 `P1→P2R→P2V→P3S green → editorial prepare` fails verbatim:

`CLOSURE_SHAPE: editorial closure expected 63, got 70`
(`survey_editorial_publication_v2.py:2163`, `_editorial_closure_rows`).

Route deps are generation-aware (C1 P3S G71 63 / G76 70); count predicate
hardcoded G71. Current disk is G76 (config pipeline 76 + 7 renewal + 7 DM022),
so prepare builds 70 but expects 63. Blocks editorial
prepare→reviews→finalize→activate→VERSIONED_ACTIVE → renewal U/C (+ normal
release) → G71→G76 control. Renewal `BASIS_ENTRY_INELIGIBLE` without prior
VERSIONED_ACTIVE is EXPECTED correct entry behavior (not a bug).

## 2. Fix (C2 editorial publication only, actual API/frame)

### 2a. CURRENT prepare — derive, never hardcode

New `_derive_current_editorial_family(repo)` calls existing C1 H
`_derive_current_family_from_disk(repo,"editorial closure current family")`
(exact config/schema/member/module predicate, pinned H `a9de2c97…`,
S `b139…`, stage `a1b97759…`). Rejects `G67`/unknown (editorial needs
G71/G76 only; G67 50 not editorial). No hardcoded G76, no `len in (63,70)`
blanket.

`_editorial_closure_rows(repo,route,family=None)`:
- `family is None` → CURRENT via above; explicit `family` allowed for
  OWN-epoch control/tests.
- `family` must be `G71`/`G76`, else `UNSUPPORTED_GENERATION`.
- `expected = _staged_mod._route_code_deps(route,family)` (C1 literal
  63/70 already; no reimplementation).
- Full checks, no dropcheck/globalreplace:
  expected literal has no duplicates (`len==len(set)`),
  `len(expected)==_want` where `_want=63 if G71 else 70` (family-specific,
  not blanket `len in (63,70)`),
  sorted-unique pin via `_safe`+`_read_bytes_bounded` (no laundering/FIFO),
  `os.lstat` regular + no exec bits (`0o111==0`, i.e. 100644 family),
  SHA==current bytes, `path==name`, no duplicates, `len(rows)==_want`.

### 2b. Historical validation — OWN epoch, never forces current70

New `_derive_own_editorial_family(repo,commit,label)` calls H
`_derive_tool_generation(repo,commit,…)` + `_normalize_generation`
(OLD==G67/NEW==G71/G76 alias, G76 no alias). Rejects non-G71/G76.

Validation (`_validate…` receipt path):
- Derive `_own_fam` from `tools.repository_commit_sha` (OWN epoch),
  `_cur_fam` from disk (CURRENT, fallback to OWN if disk derive fails).
- `expected = _route_code_deps(route,_own_fam)`; `len==63/70` family-specific.
- `got` set must equal OWN expected exact (missing/extra with family in
  message, not hardcoded 63). `path==name` enforced.
- Each row SHA must equal OWN epoch blob (`git show commit:name`);
  CURRENT-bytes equality (`_read_bytes_bounded`) checked ONLY when
  `_own==_cur` (fresh CURRENT receipts). Historical G71 stays OWN-epoch.
- Contract: `tools.contract==current_contract` enforced ONLY when
  `_own==_cur`; historical G71 (pipeline 71) vs CURRENT G76 (pipeline 76)
  mismatch is expected, NOT forced. Stage `a1b977…` identical across
  generations, pinned via H registry.
- Canonical: new `_canonical_closure_names_for_family(route,family)`
  (G71 29/34 vs G76 36/41, never CURRENT-only). Old
  `_canonical_closure_names(route)` kept as CURRENT wrapper for backward
  compat. Validation filters with OWN canonical, checks size OWN-specific.
  CURRENT receipts (`_own==_cur`) use existing `_verify_head_bytes` /
  `verify_tool_basis` (both commit+HEAD); historical uses OWN-commit-blob
  checks only (never forces CURRENT 36/41).

### 2c. Audit — all C2 63/66/29/34 hardcodes

`grep` all 12 C2 scripts for enforced `len==63/70/29/34/36/41`:
- ONLY enforced 63 was `survey_editorial_publication_v2.py:2162`
  (prepare) + messages `union 63`/`expected 63` (1212/1231/1941/2161) — ALL
  fixed to family-aware (`_want`, OWN/CURRENT in messages).
- `survey_publication_v2.py:512` comment `63 rows` is comment-only (no
  enforcement; iterates list, no `len==63`); left, not an unrelated-contract
  change.
- No enforced `66`/`29`/`34`/`36`/`41` in C2 runtime (weekly `29/36`,
  longform `34/41` are C1-owned `CURRENT_CLOSURE` + `_CANON_*_G71/G76`;
  C2 calls them via family-aware helper, never hardcodes).
- `_canonical_closure_names` CURRENT-only wrapper preserved; new
  `_for_family` used for OWN validation. No `len in (63,70)` blanket,
  no dropcheck, no globalreplace anywhere C2.

## 3. Source pins (frozen for this correction)

- Candidate HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce36998…`, inert `example.invalid`, no alternates/commondir.
  H `a9de2c97eb40…`/315610B, S `b139f493f791…`/144597B,
  stage `a1b97759c36174bb86567952f86729e5d06d4727a9fa0d26afa452cc085a5573`.
- C2 overlay (candidate==exec, byte-identical):
  `scripts/survey_editorial_publication_v2.py`
  `21ebf43d5d889057d3ae60f4b14e6ddd403920e1ba37059422c07b756242af26`
  `tests/test_survey_dm022_c2_editorial_closure_v2.py` (new, 4 tests)
  `6ef68f49688b25db29a06b86bd88b4a2b809f04b9ff1d68094f5eaa81e76f4a9`
- Frozen exec: `…/c2-editorial-closure-20261028T223346Z/exec/` 760 files
  (759 + new test; 758 + longitudinal 2 + new 1 + C1/B returns),
  83 git files, 0 `(dev,ino)` overlap vs candidate objects (57/57),
  0 `__pycache__` PRE/POST, no `GIT_*` env, process-scoped fixture identity,
  no global config, no `git clean/reset`, no fixture deletion.
  Runtime `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`,
  `python -m unittest` only, `PYTHONDONTWRITEBYTECODE=1`, per-run `unset GIT_*`.

## 4. Tests — NEW frozen copy ONLY, unique RAW, no live tests

Evidence: `notes/…/evidence/c2-editorial-closure-20261028T223346Z/`
(`run-01…run-03`, each `header.txt`+`stdout-stderr-raw.txt`+`exit-code.txt`).
Prior `c2-release-fixture-…`, `c1-presence-…`, full-lifecycle dirs preserved,
never overwritten.

| Run | Selection | Ran | OK | FAIL | ERR | Skip | Exit | Time | Raw SHA256 |
|-----|-----------|-----|----|------|-----|------|------|------|------------|
| 01 | `tests.test_survey_dm022_c2_editorial_closure_v2` (G76 weekly70 + longform70 + G71 63/29/34/36/41 control + malformed/missing/extra) | 4 | 4 | 0 | 0 | 0 | 0 | 1.079s | `f5ba36ba…` |
| 02 | `tests.test_survey_release_checkpoint_v2` (narrow-gate regression) | 9 | 9 | 0 | 0 | 0 | 0 | 0.314s | `eb3e83d0…` |
| 03 | `tests.test_survey_dm022_c2_consumers_v2` (C2 17) | 17 | 17 | 0 | 0 | 0 | 0 | 40.730s | `a69657a0…` |

0 skipped everywhere (no skip-as-PASS). POST 760 files, 0 pycache (clean,
unlike prior 43-pyc diagnostic contamination, now avoided by env-var-only
diagnostics; not cleaned, simply absent).

Targeted unit proves (actual APIs, real G76 disk + explicit G71):
- CURRENT G76 weekly/longform full70: exact names == C1 `70`, no dups,
  `path==name`, regular non-exec modes, SHA==current bytes.
- G71 historical OWN control: explicit `family="G71"` returns 63 exact;
  canonical OWN `29/34` vs CURRENT `36/41` (`29<36`, `34<41`).
- Malformed/missing/extra refuse: bogus route/family, invalid staged family,
  empty repo (no config/files), tampered set (missing/extra/dup) and
  `path!=name` all refuse (never PASS). Full `prepare_publication`
  (TinyTeX, real P1→P2V→P3S chain, PDFs, synthetic reviews) NOT run here —
  longitudinal Attempt7 will rerun after this fix.

External-review scope: synthetic exact-new-PDF reviews later are explicitly
nongenuine; they cannot create genuine PASS runtime. No genuine approval,
no Production, no W40.

P1/P2R/P2V 9/25/14 green from prior C2 `c2-release-fixture-…` run preserved
(no R1 faking, before-graph intact); NOT reburned here (359+842+650s).
Our editorial change does not touch P1/P2R/P2V helpers; release + C2-consumers
re-green above proves no regression in C2 narrow gates.

## 5. Remaining (honest, root unit ongoing)

- Longitudinal Attempt7 `prepare_publication` long witness (real revised
  reader scope, P1→P2R→P2V→P3S→editorial prepare→reviews→finalize→activate→
  VERSIONED_ACTIVE → renewal U/C → normal release → G71→G76 control, both
  routes, REAL TinyTeX PDFs, retained manifests, synthetic nongenuine gates):
  unblocked by this fix, NOT run here; awaits longitudinal rerun.
- THEMATIC editorial/draft, renewal dual-epoch (genuine G71 old + G76 new
  commits + current proof), independent implementation review, Profile/
  quality/audit/adoption/savings: OPEN. Whole `NOT_READY/step4B3OPEN/
  audit unstarted/DM021+022OPEN` preserved.
- No new family/schema introduced; G67 remains unsupported for editorial
  (50, `UNSUPPORTED_GENERATION`); narrow G71→G76 mechanical compat ONLY.

Stop: no Commit Point taken. Ordinary Commit/Push Human-owned.
