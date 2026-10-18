# DM021-P3S independent pre-execution source/oracle review (fresh, author-independent)

2026-10-18 UTC. Fresh reviewer, not authors/root. Pre-execution only.
No tests, no imports of candidate modules, no execution of candidate code,
no source/DB/index/network writes. Read-only `Read` over task/contract/
selection/correction/packet plus full read of new3; read-only `sha256sum`/
`stat` of new3 only. No subagents. All existing files preserved; only this
new file created.

## 1. Inputs read

- `notes/rephase-1-dm021-p3s/task.md` (33 lines): 3A/0M, new-copy, real
  fixture/oracle, no old-suite transfer.
- `outputs/rephase-1-dm021-staged-source-contract-decision.md`
  SHA256 `42eb8dbbb1eeda362b264847c80bdbf478b433ab1fe9777e7fe49c8ed9df3472`
  (§§3–7): 3A budget, writer 2× fresh P2V + stable-fact compare, verifier
  retained-only replay, exact 4-file closure, manifest-last, fault taxonomy.
- `notes/rephase-1-dm021-materialization/astra-review-resolution.md` S1–S5:
  scope adapter, 37-closure, manifest/errors, writer call graph/snapshots,
  fixture/oracle budget.
- `notes/rephase-1-dm021-p3s/astra-implementation-selection.md` (concrete
  overrides govern): two APIs, `_SessionScopeReader.safe(value,label)`,
  37-entry S2, lazy-P2V writer-only, W3 decided (P2V digest + canonicalizer +
  renderers, no private pipeline / no public P1 after retention), ownership
  dirfd/fstat, stable original-pin recheck, oracle distinctions (same-inode
  vs new-inode separate; TOOL_DRIFT must reach check; no mock/comment
  coverage; every seam must call API and assert before repair).
- `notes/rephase-1-dm021-p3s/interface-correction.md` §§2–7 (F2–F8 fixes,
  V1–V6, O1–O14 recipes).
- `notes/rephase-1-dm021-p3s/source-implementation/README.md`,
  `coverage-matrix.md`, `preparation-raw.md`: author claims only, not raw
  proof here.

## 2. Candidate identity (summary, not raw proof)

New copy `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`,
read-only hashed here (no candidate import/execution):

- `scripts/survey_editorial_staged_source_v2.py` 77172 B 0o664
  `49a5564371ae57c2ed5925dbe96241f943167e16dd5092218de617df3b0854f0`
- `schemas/editorial-staged-source-manifest-v2.schema.json` 5627 B 0o664
  `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46`
- `tests/test_survey_editorial_staged_source_v2.py` 40738 B 0o664
  `92fcc964838991e8bd6aec4647a88092239dedcfbb0f0aea4a1855a2e930c550`

Sizes/hashes/modes match author README summary. Full reads:
module 1–1316, schema 1–157, test 1–702. Inherited18 not rehashed in this
unit (author `18/18 MATCH` is summary, not raw here); 84 caches not
rehashed. No runtime PASS — unexecuted.

## 3. What correctly matches contract/selection (no blocker)

- APIs: `materialize_staged_source(root,state_path,proposal_path,`
  `retention_manifest_path,scope_review_path)` module 331–334 and
  `verify_staged_source(root,proposal_path,staged_manifest_path)`
  module 977–978. Scope REQUIRED (no `None` default). Correct.
- Scope adapter: `_SessionScopeReader.safe(self,value,label)` module
  184–188, two-arg, backed by actual `session.safe_read(value,label,`
  `"VERIFY","INVALID")`, returns `root/rel`. No live `_Collector` in
  verifier; writer live `_Collector` module 434–437 is current-side only.
  Verifier calls real `p1mod._validate_scope(shim,root_path,scope_ref[path],`
  `proposal,rstate,rprofile)` module 1182 with retained bytes + `reverify`
  module 1189. No fabricated former-State dict, no dummy HEAD/config.
  S1 satisfied in shape.
- Historical chain: verifier V2 module 1066–1157 does actual
  `retention.verify_retention` 1087, SHA compare 1093–1095, typed I1 hops
  `state:authority` COPY 1111–1123 → retained State 1124–1127 →
  `State.profile` → unique KEEP match 1131–1139, labels 1141–1147,
  canonical `expected_dir` 1159–1164. S1/S5 historical layout satisfied
  in shape.
- S2 closure: `_SHARED_PY` 27 entries module 87–115 (counted 27),
  `_SHARED_SCHEMAS` 5 module 117–123 (incl. self), `_route_code_deps`
  module 126–143 asserts `27+5+3+1+1 == 37`, sorted unique. Proposal+
  retention schemas pinned before validator reread (writer 388–405,
  verifier 1008–1033); route reader DIRECT-USE vs receipt/semantic-pub
  FILE-PIN distinguished (writer 411–414, verifier 1058–1061;
  `_check_runtime_binding` skips semantic pubs 277–279, never imports/
  executes file-pin producers). P2V module pinned writer-side only via
  lazy import 337 (`from ... observer  # noqa`), never in verifier
  closure. No hard-coded SHA versions as runtime truth — pins are
  measured `dep_pins/dep_sizes` 422–425 / 1048–1051 with byte+size
  equality 1052–1057 and `__file__` tripwire 269–308. Cardinality/style
  bound: `STYLE_PATH` in set 138, sized `style_input_ref` schema 126 /
  writer 611–612, staged `style` must byte-equal pinned input (verifier
  1229–1242, `STYLE_MISMATCH` + per-role replay equality). Non-current
  authority: verifier has zero P2V import/call, zero `HEAD==producer_HEAD`
  (producer_head provenance only, writer 615, never compared in
  verifier). Good.
- Writer 2× P2V + stable pins: first `observe_current_authority` 516–522
  with ref match 523–529 + before/upstream 531–535; replay 715–722;
  second `observe_current_authority` 726–730 with ref match 733–739 +
  proposed digest 741–742 + `observed_head==head_pinned` 743–744. No
  full `input_hashes` map equality (only stable refs/digests/HEAD).
  After-readback original-pin checks: `_verify_outputs_and_manifest`
  959–974 (bytes + exact 4-file), FINAL 753–816 (closed inventory 758,
  bytes/sizes 761–763, same-inode identity 777–785, edition delta-only
  800–802, retained/live maps unchanged 805–814, `reverify` 815–816).
  Manifest LAST (emit 3 files 703, manifest 704–705, readback 937–943).
  Ownership: dirfd `mkdir` 658 + open 666 + `fstat` 673 + entry-vs-fd
  683–689 before writes; files `O_CREAT|O_EXCL|O_NOFOLLOW` 876 + `fstat`
  885 + entry bind 903–917 before bytes; fstat-failure preserves
  attempt/error 674–678 / 887–894 and refuses. Primary survives
  secondary via `_attach_close` 244–248 + `_close_session` 251–266
  (never passes `StagedSourceError` as P2R `prior`). Correct shapes;
  tooling/snapshot/ownership detail left to root author-review per task.
- No fake States / no old P1 after capture: writer never calls public
  `validate_proposal` after retention (only `_pin_proposal_layout` 447 +
  P2V); verifier uses `_validate_scope` only. Test helpers use real
  recipes: LF `_complete(_chain())→_state_path→_advance_to_validated_draft`
  `→_authored+narrative delta→prepare/validate→capture→scope` test
  189–211; Weekly `_build_weekly_validated+cover delta` test 214–230;
  `_capture` asserts `RESULT_CAPTURED/VERIFIED` + owned delta test
  233–247; `_make_p3s_source_root` commits all (incl. new3) before
  authority test 96–107 with `UNTRACKED_P3S_SOURCES` 18 incl. new3
  test 38–57. `mock` not imported in test 17–33 (true). No comment-only
  coverage; no dummy-JSON positive fixtures (malformed/duplicate-key
  files are negative tamper inputs only, test 456/485).

## 4. Blockers (must fix before execution credit / acceptance)

### B1 — No actual during-write fault seams; `fsync` absent; O12 mislabels preexisting tamper as fault injection — BLOCKER

- Contract §5/§7 + selection S4 require actual short/zero-write,
  `fsync`/flush failure, close failure, partial/complete-manifest,
  root-create race, ancestor-replace, per-file failure with
  phase/per-file/primary+secondary disposition (`INDETERMINATE_INVOCATION`
  vs `INCOMPLETE`).
- Module 1–1316 contains zero `fsync`/`fdatasync`/`flush` calls.
  `_write_owned_file` 872–946 implements short/zero loop 918–929,
  close-fail 931–935, fstat-fail 885–894, readback-mismatch 941–943,
  but without any `fsync` there is no seam to inject/classify an
  `fsync` failure. Either add the contract `fsync` seam or return an
  exact blocker that durability/`fsync` is out of scope — cannot
  silently claim O12 covers it.
- Test 1–702 contains zero during-write injection (no `os.write`
  short/zero stub, no `os.close`/`os.fstat`/`os.mkdir`/`os.open`
  failure stub, no ancestor-replace, no per-file manifest-failure
  during `materialize`). `coverage-matrix.md:28` O12
  (`truncated manifest; empty subdir; zeroed main.tex`) and test
  597–630 are all **preexisting tamper + `verify_staged_source`**
  (truncated manifest 607–614, empty-subdir 615–620, zeroed `main.tex`
  623–630) — not actual short/zero/fsync/close/fstat/root/ancestor/
  readback faults **during** `materialize`. Same for O11 564–595
  (pre-created dir + post-readback `os.replace` with changed bytes)
  and O13 632–656 (TOOL_DRIFT file-edit + missing scope). The matrix
  claim “actual mid-call drift/ownership/short-zero-write/fsync/close/
  partial/complete-manifest failures” is therefore unproven. Require
  real during-write tests (or honest matrix narrowing + new tests);
  do not accept preexisting-tamper as fault-injection coverage.

### B2 — O10 same-byte new-inode swap oracle is wrong for a read-only verifier — BLOCKER

- Test 552–562 (`swapped.write_bytes(original); os.replace(swapped,`
  `main_tex)` — same bytes, new inode) expects `StagedSourceError`
  `FILE_REPLACED|STABILITY_VIOLATION|OUTPUT_DRIFT|REPLAY_`.
- Verifier 1194–1254 is byte-equality only: replay bytes 1231–1240,
  closed set 1249, self-digest 1251, canonical bytes 1253. It has no
  owned-identity comparison (owned identities exist only in writer
  FINAL 777–785). Same-byte/new-inode therefore still `VERIFIED`;
  the test as written will fail. First subcase 541–551 (in-place `%`
  edit, changed bytes) will correctly refuse, proving the two cases
  are distinct as selection requires — but the second expectation
  must be corrected to expect `VERIFIED` via verifier (or be moved
  to a writer-FINAL `FILE_REPLACED` proof during `materialize`, not
  `verify`). Do not ship the current O10 second assertion.

### B3 — O7/O8/O9/O11 oracle matrix incomplete vs claimed O1–O14 — BLOCKER (add tests or narrow claims)

- O7 433–464 covers missing path, `NEEDS_SCOPE_DETAIL` ordinary,
  `{not json` malformed — but no **stale-upstream** scope variant
  required by correction §7.2-O8/selection (“use pristine/fresh-
  proposal case for current-materializer refusal”). Missing.
- O8 466–490 covers extra-aux → `STAGED_SET_MISMATCH` and
  `{"a":1,"a":2}` duplicate-key → generic error — but no wrong-path
  same-SHA ref, no unknown-field manifest, no unsorted/`code_deps`
  tamper (verifier enforces `CODE_DEPS_MISMATCH` 1043–1045, yet no
  test calls it).
- O9 492–528: alias case 502–510 passes a symlink as
  `scope_review_path` (not staged reader); FIFO case 515–527 covers
  FIFO scope only. No alias staged-reader, no FIFO staged-reader,
  no ancestor-replace. Contract “raw-special-file no-read” + “alias/
  FIFO staged reader” unproven.
- O11 564–595 covers pre-existing root + post-readback changed-byte
  `os.replace`; no drift-before-write / drift-after-helper /
  self-readback-edit **during** `materialize`, no root/file owner
  replacement (fd vs entry), no exact-4-file owned-delta assertion
  after a mid-call fault. These are preexisting-tamper names, not
  actual during-write seams flagged in the task.
- Each claimed seam must actually call the API and assert
  fields/bytes/errors before repair (selection). Add the missing
  methods or explicitly descope them with Astra approval — do not
  count B3 gaps as covered.

### B4 — R1 test refreshes a discarded chain; binding to materialized basis unproven — BLOCKER

- Test 677–696: builds `helper/built/chain,state_path` 680–682,
  commits non-emitted comment 684, runs `_R1_REFRESH_SCRIPT` on that
  old `state_path` 686, then **discards** it and builds a fresh
  `prep = _weekly_prepare(...)` 688 (which internally creates a new
  helper/chain/state test 214–230) and materializes the fresh chain
  689–694. The refresh side-effect on the old State does not bind to
  `prep`’s State/basis. Asserts `out.strip()` nonempty 687 +
  `MATERIALIZED`/`VERIFIED` 694–696 prove only that refresh ran and a
  later unrelated chain staged — not that staging consumed the R1
  basis (no `renderer_commit`/basis-digest/`observed_head` binding
  check to the R1 head 683–685). Rewire to refresh `prep`’s
  `state_path` (or prove the global binding) and assert the basis
  link, else narrow the R1 claim.

## 5. Qualifications (record, not blockers for pre-execution)

- Q1 Dead empty-check module 631–632:
  `if core.sha256_bytes(manifest_bytes) == b"":` never fires
  (`sha256_*` returns 64-hex str, not `b""`). Should be
  `if not manifest_bytes`. Ineffective but harmless (schema 619 +
  equality 623–629 still gate). Fix or remove.
- Q2 Duplicate post-write check module 708–709 calls
  `_verify_outputs_and_manifest(...)` twice with identical args.
  Redundant (likely truncation-repair artifact per
  `preparation-raw.md:90–96`); no semantic harm, but clean up or
  justify.
- Q3 `RUNTIME_BINDING` pyc tolerance module 292–294 accepts a
  `__pycache__` `.pyc` path without proving pyc↔source correspondence
  (later compares expected source bytes 299–308, so tripwire still
  holds). Disclose as tripwire limit, not hotpatch proof (author
  README already notes tripwire; keep the note).
- Q4 Verifier `proposal_ref` check module 1021–1024 compares only
  `path/sha256`, not the extra `proposal_id/issue_id/research_`
  `publication_profile` carried in schema 30–42 / writer 594–598.
  Drift in those ID fields alone would not refuse. Either compare
  them or record as schema-strictness gap (proposal/basis equality
  1101–1104 partially covers, but not the ref copy).
- Q5 Schema `code_deps` schema 127–131 enforces only `minItems:1` +
  `sized_ref`; sorted/unique/exact-37 is enforced only in code
  (writer 627, verifier 1043–1045) with `CODE_DEPS_MISMATCH`. Acceptable
  per selection (verifier refuses before replay), but do not cite the
  schema alone as the sortedness guard.
- Q6 Generic exception assertions weaken oracles: O3 333
  (`assertRaises(Exception)` for P1 destination-conflict), O10 first
  547 (generic), O11 second 591 (generic), O12 truncated/zeroed 610/626
  (generic). They prove refusal + no-write, but not the typed
  `code/phase/disposition`. Tighten to `assertRaisesRegex` with the
  specified codes where contract names them (O4 stale, O6a
  `TOOL_DRIFT`, O14 `STAGED_ROOT_EXISTS` already do).
- Q7 Test `_materialize` 263–280 performs an outer
  `observe_current_authority` 266–268 before `materialize`. That outer
  P2V is not the writer’s authority (writer still does two fresh
  516/726); it only adds cost and a pre-assertion. Must never be cited
  as one of the writer’s “2 P2V scopes.”
- Q8 `manifest_digest` construction module 209–212 uses
  `core.sha256_object(body)` while file bytes use
  `_canonical_json_bytes` 191–206 + `core.json_bytes`. Internal
  writer/verifier consistency holds (both use `_manifest_digest`),
  but equivalence to “`sha256_object` of canonical bytes minus digest”
  depends on `core.sha256_object` canonicalization, not re-verified
  here (no core read in this unit). Root author-review should confirm
  `core.sha256_object` vs `core.json_bytes` canonical equivalence.

## 6. Verdict

No runtime PASS (unexecuted, by design). Source shapes for S1 (adapter),
S2 (37/route, sorted, file-pin/style bound, lazy-P2V, no verifier
Collector/P2V/HEAD-compare), S3 (17-required strict schema, 8-key
`contract_identity`, manifest-last, `INDETERMINATE` vs `INCOMPLETE`,
primary-preserved closes), S4 (current-root-first, 2× fresh P2V,
stable-fact compare, no full-map equality, exclusive dirfd/O_EXCL/
fstat/entry binds, original-pin FINAL) and S5 (real LF/Weekly/R1
recipes, commit-before-authority, no mock, no fake State, no public P1
after capture) are present as static shapes.

Blocked for execution credit/acceptance on B1 (missing during-write
short/zero/fsync/close/fstat/root/ancestor/readback + no `fsync` seam),
B2 (O10 same-byte swap expects verifier refusal it cannot produce),
B3 (O7 stale-upstream / O8 wrong-path/unknown-field/unsorted-deps /
O9 reader-alias+reader-FIFO+ancestor / O11 mid-call/ownership gaps),
B4 (R1 refresh target ≠ materialized chain). Qualifications Q1–Q8 must
travel with the code. Root separately author-reviews writer/snapshot/
ownership and verification-tooling per task; this review does not
cover those.

*Method: `Read` of task/contract/S1–S5/selection/correction/README/*
*coverage/preparation + full `Read` of module 1316 / schema 157 / test*
*702; read-only `sha256sum`+`stat` of new3 only. No candidate imports,*
*no test runs, no Git/DB/index/network writes.*
