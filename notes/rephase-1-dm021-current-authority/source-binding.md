# DM021 retained-aware current-authority — exact source binding (read-only observation)

2026-10-14. Design Co-Worker (General), design-only unit. Reconstruct at Human
commit `620c3ef727db4e633c887f20940268ae53d61540`. Candidate source observed at
`/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`.
All observations below are read-only: `rev-parse`, `status --porcelain`,
`diff --cached/--name-only`, `diff --name-only`, file reads via Read/Grep, and
stdlib byte/hash/mode comparison (no candidate-module imports, no cache
execution, no test/suite runs, no copies/restores, no fixture construction, no
DB/index/ref/commit/network/intake/Production writes). New documentation only
in this packet (`analysis.md` + this file). No code/schema/test/source edits.

## 1. Identity observation (sanitized Git env, all rc=0)

Commands (each prefixed with
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`),
run in candidate dir, all rc=0 (direct capture, not summary):

- `git rev-parse HEAD` → `409b292756dd1277b9dfae87679934c0d2ce251c`, rc=0.
- `git rev-parse HEAD^{tree}` → `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, rc=0.
- `git status --porcelain=v1 -uall` → 100 rows total, rc=0:
  16 source rows (3M+13A) + 84 `__pycache__` rows. Full output captured to
  transient scratch (not persisted as evidence); counts and set equality below
  are direct observations.
- `git diff --cached --name-only` → empty (no staged/intent delta), rc=0.
- `git diff --name-only` → exactly 3 modified paths, rc=0:
  `schemas/reader-surface-gate-v2.schema.json`,
  `schemas/reader-surface-semantic-review-v2.schema.json`,
  `scripts/survey_reader_surface_gate_v2.py`.

Reconstruct HEAD (read-only, rc=0): `620c3ef727db4e633c887f20940268ae53d61540`;
`git status --porcelain=v1 -uall` shows only untracked
`notes/rephase-1-dm021-current-authority/task.md` (task input, preexisting).
No other reconstruct writes.

## 2. Exact 16-file pins (direct re-observation, ALL_MATCH)

Compared working-tree bytes/mode/size against static
`notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/expected16-correction2c.json`
via stdlib `hashlib.sha256` + `os.stat` (read-only, no imports of candidate
modules). All 16 match hash+bytes+mode (`0o664`):

| Path | SHA256 | bytes | mode |
|---|---|---|---|
| `schemas/editorial-correction-proposal-v2.schema.json` | `5623c0d9…` (full `5623c0d92e3dfc5415e1ab73c73b3d5f1b147f265f2255469cede2ec333a4607`) | 3945 | 0o664 |
| `schemas/editorial-retention-manifest-v2.schema.json` | `347e5499…` | 5618 | 0o664 |
| `schemas/longform-publication-source-manifest-v2.schema.json` | `4dadf873…` | 2720 | 0o664 |
| `schemas/longform-reader-input-v2.schema.json` | `7bae9d2a…` | 10624 | 0o664 |
| `schemas/reader-surface-gate-v2.schema.json` | `fe4a96f4…` | 6894 | 0o664 |
| `schemas/reader-surface-semantic-review-v2.schema.json` | `e8598239…` | 4219 | 0o664 |
| `scripts/survey_editorial_correction_proposal_v2.py` | `5d2fde45…` | 110155 | 0o664 |
| `scripts/survey_editorial_retention_v2.py` | `3833b14a…` | 122231 | 0o664 |
| `scripts/survey_longform_derivation_v2.py` | `c09c5558…` | 62260 | 0o664 |
| `scripts/survey_longform_generated_v2.py` | `d480e11d…` | 39992 | 0o664 |
| `scripts/survey_longform_semantic_publication_v2.py` | `4d235a38…` | 36224 | 0o664 |
| `scripts/survey_reader_surface_gate_v2.py` | `e7305884…` | 94511 | 0o664 |
| `tests/test_survey_editorial_correction_proposal_v2.py` | `f581fad0…` | 112708 | 0o664 |
| `tests/test_survey_editorial_retention_v2.py` | `4155baab…` | 93733 | 0o664 |
| `tests/test_survey_longform_derivation_v2.py` | `ce687447…` | 91161 | 0o664 |
| `tests/test_survey_longform_publication_integration_v2.py` | `4a03b564…` | 107757 | 0o664 |

Full SHAs/bytes in `expected16-correction2c.json` (82 lines, read). P1-13 subset
equals `inherited13-static-freeze.json` pins per independent-final-resolution
§2 (cited, not re-derived here). P2R module `3833b14a`/test `4155baab`/schema
`347e5499` match final Astra closeout §1. HEAD409 alone does not contain this
overlay. Complete16 patch `5b79218e…` (830622B) and P1 full13 patch `85e9d9ab…`
are cited from durable packets, not rehashed here. No new HEAD/commit.

## 3. Exact 84-cache accounting (preserved, not executed)

Static inventory `cache-inventory-static.json` (dict with `provenance` +
`files` dict, 84 entries, all `0o664`): provenance states “candidate live
status at correction2b authoring; regular non-alias only”.

Direct observation:

- Status cache rows (`__pycache__` substring): 84. Status source rows: 16.
  Total 100. Matches final v9 “16 source +84 preknown cache rows”.
- Static 84 keys vs status 84 cache paths (`[3:]` stripped): sets equal
  (`static==status`, both diffs empty) via stdlib set comparison (read-only).
- Caches preserved in active tree (not cleaned to make status pass). No cache
  bytes read, hashed, or executed in this unit; modes/sizes not re-observed
  byte-wise here. Inherited v9 pre/post pins (`run_p2r_correction_v9.pre/post.json`
  with full sha/size/mode detail, `pre==post`) remain the byte authority for
  caches. No `PYTHONPYCACHEPREFIX` manipulation, no bytecode writes, no imports.

This accounting is direct path-set observation, honestly labeled as such (not a
persisted raw-proof file). No exclusive observation packet created; none needed.

## 4. Fixed contracts read (no edits)

- P1 contract `outputs/rephase-1-dm021-contract-decision.md` (SHA
  `07e899901f488b256ca846c62b1a1fab3edadc880f34593a38078412aeb3c661`,
  cited from durable packet; file read, not rehashed here).
- P2R contract `outputs/rephase-1-dm021-retention-contract-decision.md` (SHA
  `194fd7dea0bfef7e9605fc7ed34a2e90a7f0ab63428333c1dec48b605949370e`,
  file read).
- P2R assessment §4 (`outputs/rephase-1-dm021-p2r-assessment.md:51-62`) and
  mandatory qualifications read: `astra-closeout-resolution.md` (37 lines, esp.
  §2 late-plant/inode/proof-logger limits) and `independent-final-resolution.md`
  §§1–10 (esp. §10 late-plant + proof-logger narrowing, E-1 1818-line erratum).
  No broader canonical audit or runtime/adoption PASS inferred.

## 5. P1 callsites (candidate-relative `file:line`, read-only)

`scripts/survey_editorial_correction_proposal_v2.py` (1830 lines, `5d2fde45`):

- Docstring/no-write contract `:1-23`; `PROPOSAL_FILES`/`RESULT_REQUIRED`/
  `RESULT_BOUND` `:44-51`; routes `:53-54`; frozen prefixes `:56-76`.
- `_Collector` raw-first pins + `reverify` (HEAD/config/stability):
  `:87-103` init (HEAD pin, config via `safe`), `:107-179` `safe`/`pinned`
  (lexical→alias→resolve→regular→read, `STABILITY_VIOLATION` on re-read
  mismatch), `:191-233` `reverify` (ancestor-alias + bytes + HEAD + config).
- `_tree_map` full edition-tree byte map (root-anchored, alias/FIFO refusal,
  `.git` excluded): `:267-318`.
- `_eligibility` (VALIDATED_DRAFT/approved Architecture/pending Preview-no-
  provenance/pending downstream/inactive exception): `:327-342`.
- `_original_checkpoint` (State-pinned validation ref, exact path/sha,
  identity/producer, 7-row shape): `:355-377`.
- `_active_effective` (State-bound revalidation via
  `resolve_active_publication_revalidation`, `ACTIVE_PATH_REBIND` `:401-402`,
  superseded/preserved drift `:406-409`, ORIGINAAL fallback when no record):
  `:380-411`.
- `_load_profile` (State-bound Profile path/sha, issue binding): `:414-428`;
  `_derive` (Longform `load_derivation_for_readback` vs Weekly `load_derivation`,
  archive pin): `:431-445`; `_canonical` `:448-451`.
- Graph policy (mutable⇒COPY else KEEP, mutable set incl. effective rows/receipt
  outputs/receipt/reviewed reader/bundle/State/pre-TeX/authored inputs):
  `:563-606` (policy `:597-599`); bundle/manuscript Profile exact binding
  `:491-514`.
- `_retention_plan` (KEEP⇒`retained_ref`, COPY⇒prospective
  `<proposal_dir>/retained/before/<path>`, traversal/alias/overlap/conflict/
  absent-required refusals `:1231-1288`, esp. dest-absent `:1278-1284`).
- `_pipeline` full before bindings (State/config/canonical-State `:1291-1321`,
  proposal-dir/authoring-staged `:1323-1343`, original/active `:1344-1349`,
  manuscript/Gate/receipt routing `:1351-1384`, before/proposed derivation +
  `NO_EDITORIAL_CHANGE` `:1386-1391`, receipt/Gate/bundle/pre-TeX `:1393-1430`,
  graph+digests+retention `:1431-1438`, tree/reverify `:1439-1442`, proposal
  object `:1454-1485`): `:1291-1492`.
- `_validated_state_profile_for_tree` strict State/Profile authority before broad
  walk (C4): `:1536-1569`.
- `_final_full_receipt_recheck` actual full receipt predicate (not contract-only,
  C3) + stability: `:1572-1598`.
- `prepare_proposal` (in-memory only, staged authoring required, schema +
  final recheck + tree): `:1601-1632`.
- `_validate_scope` (existing review loader + `EDITORIAL_CORRECTION_SCOPE_V1`
  before/after/upstream/substantive checks, absent block⇒`REVIEW_REQUIRED`):
  `:1635-1695`.
- `validate_proposal` (rederive from FILE bytes, all-field equality except
  nonempty description, staged-bytes equality, scope, final recheck, return
  supplied UNCHANGED + `input_hashes`/`measured`): `:1698-1830`.

Schemas: proposal `schemas/editorial-correction-proposal-v2.schema.json`
(112 lines, strict keys, `PROPOSED`, KEEP/COPY XOR); review scope block
`schemas/reader-surface-semantic-review-v2.schema.json:93-124`
(`EDITORIAL_CORRECTION_SCOPE_V1`, WITHIN/REQUIRES/REJECT, before/upstream/
summary/evidence + substantive `EDITORIAL_CORRECTION_SCOPE` PASS).

## 6. P2R callsites (candidate-relative, read-only)

`scripts/survey_editorial_retention_v2.py` (2080 lines, `3833b14a`):

- Docstring (P1-before-writes-only, standalone verifier never calls P1/Git/HEAD):
  `:1-29`; schemas/paths/results `:43-49`; canonical order lists `:51-62`.
- `_Session` dirfd/no-follow safe reads, entry-vs-fd binding, `FILE_REPLACED`,
  `reverify`, `_close_all` with primary-preserving secondary accounting
  (S2): `:240-439` (esp. `_close_all` `:243-278`, `_open_dir_chain` `:285-353`,
  `safe_read` `:369-431` with close-after-read `:418-421`).
- `_retained_expected_sets` exact file+dir closure (late file/empty-dir refusal):
  `:829-848`.
- `capture_retention` (HEAD pin `:880`, narrow pins `:882-918`, retained-root
  existence refusal `:934-945`, schema `:947-954`, HEAD-before-P1 `:956-957`,
  P1 call under sanitized env `:959-967`, `input_hashes` recheck `:977-985`,
  control/edition snapshots `:988-1010`, preflight `:1012-1092`, exclusive claim
  + ancestor pins `:1094-1112`, COPY/manifest fstat/write/close `:1262-1280`/
  `:1306-1319`/`1488-1553`, pre-manifest finalization `:1347-1422`, manifest-last
  `:1424-1553`, post-verify with standalone `verify_retention` + P1-hash/HEAD/dep/
  control/edition/retained/original-byte/ownership binding `:1561-1687`,
  `reverify`+close before `RETAINED_SET_CAPTURED`): `:851-~1700`
  (return `:1695`).
- `verify_retention` (no P1/Git/HEAD, lexical/raw checks, schema, header/basis/
  proposed equalities `:1764-1777`, ordered plan projection `:1778-1826`, I1
  State-authority COPY→retained State→Profile→KEEP chain `:1827-1843`,
  provisional dest mapping `:1844-1860`, retained State/Profile reads + label
  agreement `:1860-1900`, canonical dir/manifest `:1901-1915`, dest recomputation
  `:1916-1925`, inventory + COPY/KEEP rehash + staged refs `:1926-1988`,
  `capture_inputs` historical-observation scope `:1989-2019` with mandatory P2R
  deps `:2017-2019`, canonical-bytes `:2041-2042`, final re-inventory
  `:2043-2056`, reverify+close before `RETAINED_SET_VERIFIED` `:2056-2066`):
  `:1731-2080` (return `:2062-2066`).
- Manifest schema `schemas/editorial-retention-manifest-v2.schema.json`
  (149 lines, `2.0-rc1` + `EDITORIAL_RETENTION_V1`/`CAPTURED`, proposal_ref/
  basis/proposed/rows/`capture_inputs`, COPY `retained_sha256`/`retained_byte_count`
  required equal to source row).

## 7. Controller / R1 / Longform / Weekly epoch guards (read-only)

- `scripts/survey_agent_control_v2.py`: reason closed set `:45`
  (`REVIEWED_CORE_CHANGE` only); 7-role admission `:685-693`; public
  `revalidate_publication_surface` `:1773-1798` (reason check `:1789-1790`,
  nothing-to-supersede `:1796-1798`, VALIDATED_DRAFT/approved/pending/inactive
  guards `:1799-1812`, Architecture provenance `:1813-1822`, prior checkpoint
  `:1823-1837`, pending basis `:1838-1840`, changed-vs-preserved `:1844-1886`,
  QA `:1898-1944`, owned writes/rollback `:1995-2152`); `validate_agent_state`
  strict `:348-350`; `resolve_active_publication_revalidation` `:1084-1107`;
  `approve_publication_preview` (fresh Preview only) `:1465-1497`.
- Longform: `load_derivation` (DRAFT_COMPLETE-only) `:1101-1139` vs
  `load_derivation_for_readback` (allowlist DRAFT_COMPLETE/VALIDATED_DRAFT/
  RELEASE_CANDIDATE/FROZEN/RELEASED, no pending bypass/manufactured State)
  `:1142-1182`; receipt `validate_receipt` (itself reloads review `:665-673`,
  pins contract `:681-684`, canonical paths `:721-730`, replay `:735-757`).
- Weekly: `load_derivation` (`:475-570`, pending-basis fallback `:481-487`
  without editorial authority, strict State `:487-489`); receipt `:726`.
- R1 predecessor relevance: P1 `active_revalidation_ref` may be non-null after
  real R1(s); `_active_effective` binds it with live-byte agreement and path-
  rebind refusal. P2V must preserve this distinction (see `analysis.md` §3);
  no new R1 code read beyond this binding in this unit.

## 8. Method / attribution

Direct commands only (sec. 1–3); file/line citations via Read/Grep (no imports,
no execution). Counts/timings below are cited from persisted P1/P2R raw (not
re-executed): P1 final 36 (9P1+27Gate); P2R final 25/7936.817s + affected2 +
optimized1; proof v7 `APPLY_PROOF_OK`. All P1/P2R evidence qualifications
(filtered status, HEAD-inode proof, transient `add -N` erratum, snapshot≠
continuous proof, late-plant/proof-logger narrowing, 1818-line erratum) remain
in force. This binding is a summary of direct observations (sec. 1–3 are direct
capture; secs. 5–7 are file-read citations, not rerun proof). No raw packet
persisted beyond these two docs.
