# Astra P3S initial code draft review R1 — CHANGES_REQUIRED

2026-10-18. Author-side root source review, not independent approval or runtime evidence. Candidate new module49a5564371ae57c2 / schema4fa6172338072258 / test92fcc964838991e8, as identified by the independent pre-execution review. No candidate code/test executed by root. Line numbers below refer to this initial draft. Preserve the draft and original reports before correction. Fixed contract42eb8dbb and implementation selection still govern; only new3 may change.

## R1 — positive-path blockers, separate from missing fault coverage

- Writer415–419 validates the reader SCHEMA document as a reader INSTANCE against itself. Load/check the schema as schema; validate the actual pinned reader later. This is not a positive Longform reader validation.
- Writer471 indexes `session.files[core.DEFAULT_CONFIG]` without ever pinning config in that Session. The separate live Collector's config does not populate this map. Pin actual config raw-safely before reopening validators, match live/Session originals, and use the pinned bytes.
- Writer468 sets the output directory `staged_rel`, but545 overwrites it with the existing reader FILE path. Manifest607, absence635 and subsequent ownership/output paths then use the wrong namespace. Keep distinct immutable output-root and reader-path variables throughout.
- Runtime binding269–308 requires loaded modules to originate at the fixture root; tests import `staged` from the candidate then call it on independently copied roots. Do not weaken runtime binding to make these pass: execute public P3S operations in the actual committed fixture-code subprocess, with durable failures and meaningful assertions. Fresh source before authority remains mandatory.

## R2 — original-boundary guards are missing, not supplied by a later P2V

Contract§5.2–7 requires before-claim and before-manifest checks and final original control/edition/retained equality with exact owned delta. Initial writer633–644 only tests root absence before claim;703–705 emits sources then manifest consecutively without the required pre-manifest original-input/inventory guard. `init_ctrl`, `init_ret`, `init_tree`494–497 are captured but unused. Final796–802 compares only newly added edition names; there is no final full control inventory or retained inventory comparison. `Session.reverify` rechecks known files, not newly planted files/empty dirs. Second P2V's fresh inventory is not the invocation-entry baseline.

Implement reusable checked-boundary comparisons against ORIGINAL bytes/sizes/directory identities and exact admitted owned files/dirs, including original deletions and additions in controls/retention/edition. Recheck original consumed pins/HEAD before root claim, before manifest creation (three source outputs only), and after standalone replay/second P2V. Required dynamic pins must be bound to the original basis. No prefix exemption or newly captured baseline. Add real injected late-control/retained empty-dir/file, pre-write drift and before-manifest drift cases; assert the precise allowed delta before repair.

Second P2V733–744 compares hashes and proposed digest/HEAD only: explicitly compare exact normalized refs (path AND SHA), before/upstream digests and stable facts to first/original basis as selected. First observed HEAD must likewise agree. No whole-map equality.

## R3 — ownership and primary/secondary diagnostics

- Root658–690 compares opened fd vs current entry only after mkdir: this does not establish the identity of the directory created by mkdir if replaced before open. Obtain/check the earliest available entry identity and qualify the unavoidable observation window; check held-root and entry/ancestor identity before each write and all four owned files at completion. Final780–781 explicitly skips manifest identity; remove that exemption. `owned[staged_identity]` must actually be used. Do not claim race-free mkdir identity acquisition.
- `_write_owned_file`944 records ownership only AFTER write/close/readback success. Thus a partial failure omits a created file whose identity was known. Record attempted paths immediately and identity once obtained, then per-file progress/bytes/close/readback state. Root/file open or fstat failures must preserve unknown identity explicitly.
- File close931–935 in `finally` replaces an in-flight primary write error;885–917 silently discard several secondary close errors. Final dir close786–791 can also replace its primary. Preserve primary plus structured secondary diagnostics in every new-module path.
- Manifest failures still use CLAIM/OWNED_PARTIAL until713, including a complete manifest whose close fails. Classify incomplete versus potentially complete/indeterminate accurately. Final `_close_session(..., MATERIALIZED)`825 must not label a failed close as a successful disposition or lose owned diagnostics. No retry/rewrite/cleanup.
- Implement the selected fsync failure seam and short/zero handling without claiming crash/power-loss atomicity. Exercise real API during-write faults (scoped wrappers around actual OS operations are acceptable fault injection, not mock-based replacement of authority/P2V/replay).

## R4 — verifier claims must be compared, retained final closure must be repeated

Verifier1101–1104 compares RETENTION basis/proposed with proposal but never compares STAGED manifest basis/proposed to that proposal. `style_input_ref` is recorded but not validated against fixed style path/hash/size;1241 compares a value to itself. Complete proposal_ref extra IDs (independent Q4), top-level research/publication labels and strict contract identity must agree. Recompute self-digest/canonical bytes AFTER making semantic tamper test cases so earlier digest failure does not masquerade as these checks.

Verifier1255 comment promises staged/retained final inventories, but1258 only inventories staged. Actual P2R verifier runs earlier in its own Session. Pin/check the complete required COPY/KEEP closure in the verifier's own original domain, and repeat retained exact inventory and required consumed pins after scope/rendering. This must not introduce current-State/HEAD/config authority or blanket historical `capture_inputs` equality.

## R5 — test helper correctness and truthful coverage

Independent B1–B4 are accepted as blockers: actual write/close/fsync/fstat/root/ancestor faults, invocation-bound inode change versus fresh same-byte artifact replay, missing semantic/path/dependency/reader special-file cases, and R1 basis of the SAME materialized chain. Add the tests, do not silently descope required contract cases. O1–O14 labels alone are not evidence.

Additional actual test issues:

-456/485 call `Path.write_bytes(..., encoding=...)`, which raises TypeError before API coverage.
-O7 baseline441 predates creating ordinary/malformed input; compare with the fault present, including that input, before cleanup. Other alias/FIFO cases currently compare only after unlink.
-`_snapshot`123–132 reads files blindly, omits directories/types/identities and walk errors; it can follow aliases or block on a FIFO. Use a raw-safe snapshot suitable for the actual oracle and explicit known-injection accounting. Byte equality alone does not prove exact file+directory write window.
-ThreadPoolExecutor515 shutdown waits for a blocked reader even after future timeout. Use a killable/reaped subprocess with saved timeout outcome for no-read cases, and prove special files are refused before ordinary read.
-Fixture copying72–108 must handle actual materialized fixed source deliberately rather than assume every `ls-files` entry is available in this partial/sparse DB. Git return codes must be checked. No network/fake ancestry needed for meaningful independent source fixtures.
-R1 helper165–186 inserts an assignment before a function docstring, not merely a Python comment; check actual indentation and syntax. Use a genuine non-emitted comment and run actual refreshed fixture code, preserving the same State/active receipt chain into proposal/capture/materialization.
-Tighten broad `assertRaises(Exception)` to exact typed refusal/phase/disposition where specified; distinguish earlier guard preemption honestly. Remove redundant external P2V from every positive helper unless a separate coexistence assertion needs it.

## Independent qualifications disposition

Q1 dead bytes-vs-string check and Q2 duplicate verify call: remove/fix. Q3 `.pyc` basename-only tolerance is not path/source binding; narrow or reject that case rather than pretending it proves correspondence. Q4: mandatory equality repair under R4. Q5: exact code dependency set/order is enforced by code, not schema alone. Q6/Q7: R5. Q8: root read actual `survey_production_v2.py:86–105`: file serialization is indent2+newline, object digest is sorted compact JSON. They are intentionally DIFFERENT representations; selected contract specifies `sha256_object(body)` digest, not SHA of pretty file bytes. Current digest helper matches that definition. Retain distinction, no false byte-equality claim.

## Return boundary

Author A: preserve initial new3 and static pins/reports in a new draft-history packet, implement only new3 corrections, create a NEW correction report/coverage matrix/static21. AST/schema inspection allowed without imports/bytecode. No fixture/test/long-run execution yet. Return exact source identity, diff summary, actual method/seam map and any unresolved blockers. Existing18 and84 caches remain fixed.

Tooling independently returned CHANGES_REQUIRED in `verification-tools/independent-tooling-preexecution-review.md`; author B repairs in new filenames. Root must read corrected code/tools before selecting execution. No runtime acceptance, no candidate/reconstruct commit or push.
