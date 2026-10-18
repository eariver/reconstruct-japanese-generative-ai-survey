# DM021-P3S independent final supplement — corrections + packaging PROOF (fresh, author-independent)

2026-10-18 UTC. Fresh reviewer, not candidate/test/tool author, not root reviewer.
No delegation. This file is the ONLY new write; `independent-final-review.md`
is preserved byte-for-byte. Readonly only: `Read` + `sha256sum`/`stat`/
`git rev-parse`/`status` (sanitized env). No runtime imports/tests/fixtures/
DB/index/network/Git writes.

## 0. Honest read scope (corrects §0/footer contradiction)

Prior §0 said “full actual frozen new3” while footer said “targeted inherited
helper reads”; both overstate test coverage. Actual this unit + prior unit:

- Module `survey_editorial_staged_source_v2.py` 2095 lines: read fully in 5
  `Read` windows (1–400, 401–800, 801–1200, 1201–1600, 1601–2096) at frozen
  R11 bytes. Schema 157 lines: read fully. These support S1–S5 line cites.
- Test `test_..._staged_source_v2.py` 2622 lines: NOT read line-by-line.
  Method census via `ast.parse` (26 `test_*`, 23 helpers + 4 script constants,
  total 49 funcs), embedded scripts via literal-eval + `ast.parse` (all 4 OK),
  plus targeted `Read`/grep of O12b (`OWNED_PARTIAL` assert), fault-script
  `fired`/`observer_calls` counts, and R1/O10/O9 oracle regions. Prior “full
  new3” claim is withdrawn; test verdict rests on AST census + targeted reads
  + runtime raw, not a full-test line audit.
- Batch raw: ALL 8 packets’ `batch-*.record.txt`/`launch.*`/`run_p3s_b3.stdout`/
  `stderr`/`stage-done`/`pre`/`post` read (counts/durations/rc below). Durable
  `fixture-raw/child.*` NOT exhaustively read: sampled R9-D O9/O10/O11b/c/e/f,
  R9-E R1 allowlist stderr, R10-F R1 snapshot stderr, R11-G summary only. Prior
  “durable child JSON/script/error refs” implies exhaustive review — corrected
  to sampled child raw + full batch-level raw.
- Inherited helpers: spot-read callsites only (P1/P2R/P2V/renderers/gate/core),
  hashes inherited from P2V/P2R packets, not rehashed here.
- Packaging GEN+PROOF read fully (hashes, stage-done, freezes, terminal-note,
  console exits). No PROOF inference from GEN.

## 1. Corrections to prior review (explicit)

1. **§1 L65 cache84 / static21 / TB1.** Wrong: “Inherited18 18/18 + 84 caches
   84/84 per R11 `static21.json`” and “authority is P2V TB1 proof.”
   Correct: `static21.json` holds exactly 21 source entries (18 inherited + 3
   new), zero cache entries. Cache84 authority is the separate recorded guard
   `notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/cache-inventory-static.json`
   (`provenance` + `files` 84 entries), NOT rehashed here; P2V TB1 is historical
   cache-byte proof at old pins, not current-cache-byte proof. Distinction:
   §2 below reports (a) my actual readonly rehash of active 21 (21/21) and
   (b) recorded-guard comparison applied-21 vs static21 (0 mismatches) + PROOF
   “active 21 match static + 84 caches” as tool-observed guard — only (a) is my
   rehash; cache bytes rely on the recorded P2R inventory, disclosed as such.

2. **§4 L162 O12b disposition.** Wrong: “Tests assert typed code/phase not the
   disposition string for O12b.” Correct: O12b explicitly asserts both:
   `assertEqual(outcome.get("phase"),"CLAIM")` +
   `assertEqual(outcome.get("disposition"),"OWNED_PARTIAL")` per fault
   (targeted read `test_o12b...` 1927–1952). The standing qualification remains
   (CLAIM uses `OWNED_PARTIAL` where contract text names `INCOMPLETE`), but it
   is an asserted exact behavior, not an unasserted label. SET-completeness is
   still proven by FINAL inventory, not the label alone.

3. **§7 L276 / L284 counts.** Wrong: “O12b–f rerun (6)” and “R11 reran only
   R1 + 6 affected + O11d.” Correct: O12b–f is FIVE methods
   (O12b, O12c, O12d, O12e, O12f); affected6 = O11d + those five; R11-G ran
   SEVEN total (R1 + O11d + O12b–f five), 7/7 ok 5634.188s. “6” is withdrawn.

4. **§7 L282 func counts.** Wrong: “48/49 identical R10→R11.” Correct per
   `correction-report-r11.md` + my AST check (49 total funcs): all 49 funcs
   IDENTICAL R10→R11; only 1 of 4 script constants changed
   (`_R1_FIXTURE_PREPARE_SCRIPT` 3473→3388, `5f469984…`→`11da8e5f…`);
   other 3 constants identical. R9→R10 remains 9 changed nodes (6 methods +
   R1 helper + fault script + class aggregate) as reported.

5. **§7 L302–304 R1 failure order.** Wrong order (snapshot defect listed before
   allowlist). Correct: R9-E R1 failed BEFORE refresh — `MechanicalRefreshError:
   unsupported control/criteria/schema change outside weekly_derivation.py`
   (child stderr `p3s-fixture-code-_awqasgu`, fixture changed refresh impl
   itself vs `ALLOWED_CHANGED_PATH`); R10-F R1 failed AFTER successful refresh —
   fixture oracle defects (snap0 taken BEFORE `_stage_authoring_before_prepare`
   then prepare, falsely attributing staging to prepare; plus P1 file-only
   `_snapshot` vs expected directory delta, second guaranteed mismatch in
   `p3s-fixture-code-nwfqxli6` line 28–32/60–61). R11 repair (stage-then-snapshot
   + fixture `_p3s_snapshot` + real `TestCase`) addresses the R10-F oracle.

6. **§7 L244 “each passed once.”** Wrong: O11d and O12b–f each have TWO recorded
   passes (R9 pins + R11 rerun). Correct: each of the 26 has a recorded
   successful run at its pin (§4 table with repeats noted); 7 methods have two
   passes due to the warranted R11 affected rerun. No method lacks a pass; no
   “exactly once” claim.

7. **§10 L364 packaging PROOF OPEN.** Superseded: PROOF was pending at prior
   write; it is now selected AND executed (§2). Overall full promotion/DM021
   remains OPEN (adoption/reason/State/Candidate/Gate/PDF never selected), but
   P3S complete21 GEN + independent clean409 apply PROOF is COMPLETE. Do not
   cite PROOF as promotion acceptance.

8. **“26 real fault oracles.”** Wrong phrasing (prior §§6/9). Correct: 26
   behavioral methods = 2 positives (O1/O2) + coexistence/probe (O3) +
   drift/compat probes (O4/O5) + TOOL_DRIFT/KEEP (O6a/O6b) + scope/tamper/
   alias (O7/O8/O9) + same-inode/ownership/midcall/late/final faults
   (O10/O11/O11b–f) + during-write/fsync/manifest/fstat/combined (O12a–f) +
   no-write/existing-root (O13/O14) + genuine-owner R1. Only a subset are
   during-write fault-injection cases.

9. **“Every replacement after earliest [stat] detected.”** Overclaim (prior
   §§5/8/9). Correct: checked-boundary detection only — replacements after
   the earliest post-mkdir entry stat are detected by open-fstat/entry bind
   before each write + FINAL rebind; the mkdir→earliest-stat interval is an
   explicitly qualified blind window (module 1015–1023), and no continuous
   race proof or post-final-injection guarantee is claimed.

## 2. Packaging PROOF — now read (corrects prior pending)

- Saved patch `gen-complete21/complete-p3s-21path.patch`
  SHA256 `e449d029c8775ee28ee610f224997a57b0cd68664194c6720a6038ce9a3012fa`,
  1233670 B (matches `.sha256`; `gen.console.exit 0`; GEN `stage-done`
  `copy_rc 0`, `copy_git_regular 134/dirs 96`, inert `example.invalid` remote).
- PROOF `proof-apply21/` (`proof.console.exit 0`): tool stdout
  `saved patch sha256=... bytes=1233670 (matches hash manifest)`,
  `active HEAD detached`, `active 21 match static manifest + 84 caches +
  HEAD/tree/index pinned`, `copy completeness verified`,
  `copy caches removed files=84 (disposable only)`, `copy is clean409;
  applying EXACT saved patch`, `APPLY_PROOF_OK head=409b292... files=21
  patch=e449d029...`, `PROOF secondary=[] elapsed_s=0.46`.
  `proof_apply21_b3.exit 0`, `terminal-note` no primary/secondary/interrupt.
  Freezes: clean `proof-freeze-clean-b2.json` (HEAD 409b292/tree 8ce36998,
  empty status/index, 18 `new_absent`, 3 `modified_match_head`, 84
  `caches_removed`) and applied `proof-freeze-applied-b2.json` (same HEAD/tree,
  105-row status, `files` 21 exact).
- My readonly verification (allowed hashes/status, no writes): active 21
  `sha256+bytes+mode` rehashed vs R11 `static21.json` → 21/21 match (scripted
  `hashlib+stat`, `ok 21/21`); applied-21 `files` vs `static21.json` →
  0 mismatches (all21 byte+mode+size+sha); active HEAD `409b292`, status 105
  rows confirmed; apply copy `/tmp/opencode/jgas-p3s-final-20261018T154812Z/proof-apply21-clean409-copy`
  exists. Cache84 NOT rehashed by me; reliance is the recorded P2R
  `cache-inventory-static.json` (84 entries) + PROOF’s before-removal census
  and 84-removed accounting — disclosed, not my byte proof.
- Scope: GEN applies DIRECTLY to clean409 (no layered patches/archive/fake
  root/network); PROOF byte-copies actual409, declares overlay reversion +
  disposable cache removal, proves clean409 first (new_absent 18 + modified 3),
  applies SAVED patch, checks exact21 + all-entry isolation + current-copy
  mapping. This is patch/apply proof only — not a test rerun, not adoption.

## 3. R11 bounded-source conclusion — explicitly assessed

Question: is the final R11 bounded-source conclusion supported by QUALIFIED
scoped26 with exact shared-helper/script correspondence and no full26 run?

Yes, within stated bounds; no new full suite needed for symmetry (and none run).

- Runtime control unchanged since R5: module `7059166e` + schema `4fa61723`
  byte-identical across R5→R11 (every batch PRE static21 check); all runtime
  behavior deltas are test-only.
- Shared-helper/script correspondence: R5→R6 O1/O2 + 24 helpers identical;
  R8→R9 48/49 identical (only O8 changed); R9→R10 9 nodes changed (6 fault
  methods + R1 helper + `_P3S_FAULT_SCRIPT` observer wrapper + class);
  R10→R11 49/49 funcs identical, 1/4 constants changed (R1 prepare script).
  Fault-script wrapper change (R10) correctly forced the warranted affected6
  rerun (R11-G 7/7 ok); other fault-using passes stay pin-bound, no silent
  transfer. Prior successes’ bodies that did not change remain
  body-identical to their passing pins; methods that changed were rerun at new
  pins (or, for O4/O7/O8 single-change cases, at their corrected pins in
  R7/R8/R9-D).
- Qualified scoped26 (§4 table as corrected): each method has a recorded pass
  at a known pin with saved stdout/stderr/stage-done/pre/post; 7 have two
  passes (O11d/O12b–f at R9 + R11). There is deliberately NO single full26
  invocation and NO claim that old passes transfer to R11. If symmetric
  full26-at-R11 were demanded, that would be a new selection with real cost
  (~sum of batch durations, P2V×2 per materialize) and is NOT justified to
  reprove unchanged bodies/pins; the affected rerun already covers the only
  shared-wrapper change. Symmetry alone is not a blocker.
- Gaps checked, none blocking: no inherited18 change, no S2 extension needed,
  no new authority, no unproved seam (every required seam fired with
  `fired`/`observer_calls` + exact code/phase/disposition + fault-present
  no-write/owned-delta before repair in raw). If a future audit finds an
  actual uncovered seam or body drift I missed, that is a blocker to return —
  I waive nothing; I report no such blocker at R11 bytes + read raw.

## 4. Corrected verdict / scope / qualifications

**BOUNDED PASS (corrected) — actual frozen R11 source + QUALIFIED scoped26 +
complete21 GEN/PROOF.**

- Source: R11 `7059166e`/`4fa61723`/`a3bb0f23` satisfies S1–S5 at cited lines
  (prior §§2–6 stand subject to §1 corrections); no concrete code blocker.
- Evidence: 26 behavioral methods each with a recorded successful run at its
  pin (7 with two passes); R11-G proves R1 + affected6 (O11d + O12b–f five) at
  final pins. Explicitly NOT a full26 run, NOT a transfer. First-B2 0-test
  failure + all intermediate failures preserved with honest oracles, no
  retroactive clean run.
- Current proof scope: complete21 patch `e449d029…` 1233670 B GEN complete +
  independent clean409 apply PROOF complete (21/21 byte/mode/size vs R11
  static21 by my rehash + recorded applied freeze; HEAD/tree/index/detached/
  inert/all-entry guards; 84-cache handling via recorded P2R inventory).
  Overall DM021/full promotion/adoption/State/Gate/Candidate/PDF remains OPEN;
  staged `VERIFIED` is byte-consistency + deterministic replay only.
- Standing qualifications: disposition label (`OWNED_PARTIAL` asserted, vs
  contract `INCOMPLETE` text), schema-vs-code sortedness, tripwire≠hotpatch,
  mkdir→earliest blind window + checked-boundary-only detection, no
  CAS/atomicity/no-drift, exact-run tooling only, synthetic≠genuine approval,
  Weekly canonicalizer disclosure, sampled (not exhaustive) child-raw review,
  cache bytes via recorded inventory/TB1 history (not my rehash).
- Stop at Human Commit Point. No candidate/reconstruct commit/push, no live
  replacement, no adoption/authority inference. No broader audit claimed.

*Method: `Read` of prior review + GEN/PROOF raw/freezes/terminal/source guards
+ R11 static21 + P2R cache inventory + targeted active-21 rehash (`hashlib`/
`stat`) + targeted O12b/R1-child reads + AST counts; no imports/tests/fixtures/
DB/index/network/Git writes. Only this supplement created.*

## 5. Mandatory bookkeeping addendum (overrides §1-item6 / §2-status / §3-seam / O12b-FINAL wording; verdict stands corrected)

Preserves all paragraphs above; where this §5 conflicts, this §5 governs.

1. **Two-pass count.** Supplement §1-item6 (L81–85), §3 (L160–162), verdict
   (L182–183) wrongly say “7 methods have two passes.” Correct: **SIX methods
   have two recorded passes = O11d + O12b–f five** (R9 pins + R11-G rerun for
   the warranted R10 shared-wrapper change). **R1 passed only at R11-G** (R9-E
   and R10-F R1 failed as preserved; no earlier R1 pass). Total distinct
   remains 26; methods with repeats = 6, not 7.

2. **Applied-freeze status.** Supplement §2 (L124–125) wrongly says applied
   `proof-freeze-applied-b2.json` has “105-row status.” Re-read actual freeze:
   `status` holds **21 rows** (3M + 18A source-only: 3 modified tracked +
   18 new source; `files` 21 exact; `index` empty). The “105” is the *active
   source-tree* census (21 source + 84 caches) seen in active `PRE/POST` and
   batch records, NOT the applied disposable copy — its 84 caches were
   declared removed (`caches_removed 84` in clean freeze; applied copy has no
   `__pycache__`). No source/applied confusion: active-105 vs applied-21.

3. **Rehash distinction (no live-apply rehash claimed).** My independent
   readonly rehash covers **active 21 only** (21/21 `sha256+bytes+mode` vs R11
   `static21.json`, `ok 21/21`). The applied-21 comparison (0 mismatches) is a
   **recorded-guard comparison** (`proof-freeze-applied-b2.json:files` vs
   `static21.json`), plus the tool’s `APPLY_PROOF_OK files=21` and clean-409
   preconditions — NOT my independent rehash of the live apply copy at
   `/tmp/opencode/jgas-p3s-final-20261018T154812Z/proof-apply21-clean409-copy`
   (exists, not rehashed by me). Per root resolution, the distinction stands:
   active-21 = my rehash; applied-21 = recorded freeze + tool proof, disclosed
   as such.

4. **Seam-firing scope narrowed.** Supplement §3 (L168–173) blanket “every
   required seam fired / no unproved seam” exceeds my targeted-test + sampled
   child-raw review and is withdrawn. Correct bounded finding: **no blocking
   defect identified in the inspected source (full module + full schema + AST
   census + targeted O12b/fault/R1 reads) and sampled evidence (all batch
   stderr/stage-done/pre/post + sampled R9-D/R9-E/R10-F child stderr/stdout +
   GEN/PROOF freezes/terminal).** Scope is the actually represented
   assertions/guarded outcomes I read — not an exhaustive fault-matrix
   certification. A future audit finding an uncovered seam/body drift I did
   not read is a blocker to return, not a waived case.

5. **O12b `OWNED_PARTIAL` / exact partials / FINAL wording.** Prior review §4
   (L160–165) and supplement §1-item2 (L53–56) phrase “SET-completeness proven
   by FINAL inventory” is wrong for failed invocations (CLAIM-phase faults
   never reach FINAL). Correct per targeted O12b read (`test_o12b...`, no
   `FINAL` in method; 3× `_assert_no_write_except` + `new_entries ==
   expected_new` + `owned_files` progress asserts): O12b proves exact owned
   partials via **test-level snapshot** (`_snapshot` before vs after with fault
   present) + **structured `owned` diagnostics** (`bytes_written`/`fsync`/
   `close`/`readback` states), not via module FINAL. FINAL-inventory closure
   applies to **successful completions** (and post-repair verifier checks);
   failed-fault SET scope is proven by the specific post-fault test
   inventories. Disposition `OWNED_PARTIAL` at CLAIM remains the asserted exact
   behavior (code+phase+disposition all asserted), with the standing
   contract-text (`INCOMPLETE`) label variance disclosed, not a semantic pass.

**Corrected verdict (standing): BOUNDED reviewed source + QUALIFIED scoped26,
no generic certification or full audit.** Frozen R11 module `7059166e` + schema
`4fa61723` + test `a3bb0f23` satisfy S1–S5 in inspected shape; 26 distinct
methods each with a recorded pass at its pin (SIX with two passes: O11d +
O12b–f five; R1 only R11); complete21 GEN `e449d029…` 1233670 B + clean409
apply PROOF read (applied-21 recorded 0 mismatches; active-21 my 21/21 rehash;
cache84 via recorded P2R inventory). Full promotion/DM021 remain OPEN; staged
`VERIFIED` is byte-consistency + replay only. Stop at Human Commit Point; no
commit/push/adoption inference.
