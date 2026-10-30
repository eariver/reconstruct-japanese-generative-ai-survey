# Independent cross-family boundary review — C2 editorial closure vs selected G71→G76 control

2026-10-28 UTC. Independent SOURCE analysis only. No code/test/network/Git mutation/Human readback.
No whole approval. Other authors idle. Uses fixed report pins, no edits to other files.

## 0. Authority order and pins (fixed, not re-certified)

- Selected DM022 contract `outputs/rephase-1-dm022-prearchitecture-contract-decision.md`
  INCLUDING §11, SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`/31351B.
- DM022 precode ROOT `notes/rephase-1-dm022-prearchitecture-precode/astra-precode-gate-resolution.md`
  INCLUDING §5, full SHA256 `0425c5300c9c7211e4468d3b842c4e3af1acb9f5bf1eba00e90f7ba72ef44a5a`/13788B.
  §§1–4 snapshot `56b66880…` is not full-file hash.
- Prior renewal contract `478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf`,
  renewal precode ROOT full SHA256 `7d7d5a4552eb7a1abcbafa79d8f358ff10ec96e885b55f09f271766b136cab57`
  (§2 strict LIVE State + §6 schema-pointer erratum).
- Final93 source: actual409/tree8ce +93paths40M53A/742, DIRECT patch
  `f898d33bfe6904fd29063d5a1ff462588d11f227f5aab6a3a2d505614941da2a`/3423014B,
  proof-copy `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  (same-path original cited below).
- Current candidate: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
  (HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`/tree`8ce36998…` + DM022 overlay).
  H `a9de2c97eb40…`/315610B, S `b139f493f791…`/144597B, stage `a1b97759c36174bb86567952f86729e5d06d4727a9fa0d26afa452cc085a5573`
  per C2 report (fixed pins, not re-hashed here).
- C2 overlay under review: `scripts/survey_editorial_publication_v2.py`
  `21ebf43d5d889057d3ae60f4b14e6ddd403920e1ba37059422c07b756242af26`,
  new test `tests/test_survey_dm022_c2_editorial_closure_v2.py`
  `6ef68f49688b25db29a06b86bd88b4a2b809f04b9ff1d68094f5eaa81e76f4a9`,
  actor return `notes/rephase-1-dm022-prearchitecture-implementation/author-C2-editorial-closure-correction.md`.

## 1. Finding: C2 `validate_editorial_receipt` is a weakened LIVE admission function

### 1a. Exact weakened lines (candidate-work `survey_editorial_publication_v2.py`)

- `782`: `def validate_editorial_receipt(root, receipt_path, state_path)` — public docstring:
  "Public editorial receipt … Implements the full public contract independently".
- `800–848`: retains strict State bytes + `_require_canonical_current_state` + public
  `agent.validate_agent_state(repo,cfg,state)` — this part is correct and MUST stay.
- `1218–1230`: derives `_own_fam` from `tools.repository_commit_sha` via
  `_derive_own_editorial_family`, derives `_cur_fam_for_val` via
  `_derive_current_editorial_family`, **with fallback**:
  `except EditorialError: _cur_fam_for_val = _own_fam`
  with comment "If CURRENT derive fails … fall back to OWN … CURRENT proof still
  required in prepare path." This fallback hides indeterminate CURRENT inside the
  LIVE validator itself.
- `1236–1265`: `expected` set is OWN literal (`_route_code_deps(route,_own_fam)`,
  `_own_want=63/70`); per-row SHA checked vs OWN commit blob (`git show commit:name`);
  CURRENT-bytes equality (`_read_bytes_bounded`) executed **ONLY when `_own==_cur`**
  (`1266–1272`).
- `1276–1287`: `contract==current_contract` enforced **ONLY when `_own==_cur`**;
  else `pass` with comment "Do NOT force CURRENT".
- `1306–1331`: filtered canonical subset is OWN-family (`_canonical_closure_names_for_family`);
  `_verify_head_bytes` / `verify_tool_basis` (both commit+HEAD, control roots, contract,
  dirty/untracked, closure vs both bases) executed **ONLY when `_own==_cur`**
  (`1312–1320`); else OWN-blob-only loop (`1321–1331`), comment "never forces CURRENT 36/41".
- `1334–1342`: extra rows checked vs commit blob always, vs CURRENT bytes only via the
  earlier OWN==CURRENT branch. Net: when OWN(G71)!=CURRENT(G76), **no CURRENT bytes,
  no CURRENT contract, no HEAD control-root check** occurs in this function.

### 1b. This function is LIVE admission, not historian-only

Exact callgraph in same file + H wrapper:

- `2361` (`finalize_publication`, pre-seal): `receipt = validate_editorial_receipt(repo, receipt_rel_f, state_rel_f)`.
- `2654` (seal write boundary): same re-validation "at final boundary (exact bytes)".
- `2952` (`validate_seal`): "full public receipt validation (strict State, tool closure,
  P3S proof, scope, replay)" → `validate_editorial_receipt(repo, receipt_rel, state_rel)`.
- `4247` (CLI): `out = validate_editorial_receipt(root, args.receipt, args.state)`.
- `survey_editorial_correction_proposal_v2.py:240` (H dispatch for
  `EDITORIAL_PUBLICATION_SOURCE_V1`) and `:2394` (H recheck `col.rel(receipt_abs)`,
  `col.rel(state_abs)`): both delegate to `_edpub.validate_editorial_receipt`.

H `verify_activation_history` (`4134–4176`) is the separate historical classifier
(INERT/HISTORICAL, "no current eligibility claim") and does NOT call this function.
Therefore the OWN-fallback path directly gates mutating downstream
(prepare/finalize/seal) and State-bound admission. Calling it "historical OWN
consistency proof" does not change its operational role.

**Verdict: unselected stale/public admission.** A G71 63-row receipt with G71 contract
passes at G76 disk without any CURRENT 70 proof. This is exactly what selected
§10 forbids ("New caller flags/verified dictionaries, skipped predicates … are not
allowed") and what renewal ROOT §2 forbids ("Do not change those current predicates
to history checks merely to make `validate_agent_state` pass").

### 1c. Final93 original at same path proves always-CURRENT

Proof-copy `survey_editorial_publication_v2.py` `def validate_editorial_receipt`
(same function, offset ~39264):

- `expected_closure = _editorial_closure_rows(repo, generator_route)` — no family
  parameter; CURRENT derived from disk only.
- Every row: `SHA==current bytes` for **both** `got` and `exp`
  (`CLOSURE_DRIFT`); message "must equal expected union 63".
- `tools["contract"] != current_contract` → `CONTRACT_MISMATCH` **unconditionally**.
- `_canonical_closure_names(generator_route)` CURRENT-only, then
  `_verify_head_bytes` / `verify_tool_basis` **unconditionally** (commit+HEAD).
- Comment: "Real old initial receipts 22/27 remain valid via existing route helpers;
  no old-epoch migration" — i.e. old *initial* Weekly/Longform receipts use route
  helpers, not this editorial validator. There was never a G71-OWN branch in the
  LIVE editorial validator at final93. C2's branch is new behavior, not preservation.

## 2. Selected control that C2 contradicts

- **ROOT 0425 §3**: "Admission still independently requires all existing
  publication-renewal proofs … Full current publication proof continues to check
  current tools on every readback. This is necessary for later same-contract G76
  renewal and is not a stale-proof waiver." And: "Historical research checkpoint/report
  checks bind recorded source epochs and retained bytes. Current consumers validate
  the exact active content under current supported rules."
- **ROOT 0425 §5.1(2)**: classification read precedes role admission; referenced-authority
  consumption follows; "G76 is the supported research family; the original creation
  window is proved from retained operation context, **never reimposed on later LIVE
  readback**."
- **Selected a345 §11.2**: "Readback of the adopted checkpoint is not restricted to
  that current lifecycle. Normal forward transitions … must continue to validate and
  consume it while its original operation context is verified from retained
  before-State/lineage." + "Historical/detached proof remains State-nonrecursive;
  current operational eligibility and guard checks remain high-side. The agent's normal
  public strict State validator must retain its full existing predicates with a precise
  new-kind branch, not a current-pinned `production.verify_state_basis` substitute."
- **Renewal ROOT 7d §2 predicate table + recursion boundary**: public
  `agent.validate_agent_state` on exact LIVE bytes + canonical path + prePreview/Exception
  allowed **only** in high invocation/normal State consumers, **never** in history,
  accepted-authority content assembly, `validate_renewal_basis`, or
  `verify_renewal_source_proof`. Low projection proves identity/structure only;
  "The high renewal entry may admit a historically intact predecessor whose old full
  current receipt correctly fails. Normal stage/Preview/Freeze/Release must still call
  the Candidate/Gate/current detached proof validators … and they refuse stale current
  tools."

Correct pattern already implemented for renewal in candidate HIGH
(`survey_versioned_renewal_v2.py`):

- `_observe_renewal_entry:622–805` — LIVE canonical State+config pins, schema,
  `_profile_and_source`, canonical path, `_require_renewal_entry_window`,
  public `agent.validate_agent_state`, zero-delta rechecks, prior history via typed
  historian, current commit/contract as INFO pins.
- `observe_renewal_authority:876–960` — basis CURRENT epoch must equal fresh
  `_derive_current_family_from_disk` + `_expected_receipt_closure` member-wise
  recompute (`BASIS_CURRENT_TOOL_DRIFT` on any drift).
- `_validate_before_renewal_receipt` (editorial `714–736`) — strict kind-aware gate:
  `validate_renewal_receipt` fully validated public context, detached CURRENT proof,
  fully reloads basis/proof/build + Layer-B HIST+CURRENT closure/contract, exact
  `VERSIONED_RENEWAL_SOURCE_V1` kind, route equality, no `.get(a)/.get(b)` fallback,
  no raw kind/digest rewrite. C2 preserved this branch correctly; the weakness is
  only in the *editorial own-closure* branch that follows it.

Narrow G71→G76 mechanical compat per ROOT §3/R6 is therefore: **same authority,
normal renewal full CURRENT proof, unchanged upstream as compatibility control** —
not family-name migration, not old-closure admission. C2 inverts it: old closure
admitted as LIVE.

## 3. HIGH prepare/bootstrap chronology (why fallback cannot live in validate)

- `prepare_publication` builds CURRENT: `2007 receipt_closure = _editorial_closure_rows(repo, generator_route)`
  with `family=None` → `_derive_current_editorial_family` (disk, `2183–2197`);
  `2014 current_contract = core.contract_identity(...)` CURRENT; `2002–2006` renewal
  route binding via strict `_validate_before_renewal_receipt`; plus genuine
  current-before `_require_scope_bound` (P2V `observe_current_authority`, `644–691`),
  `_verify_staged` (P3S historical proof, `694–711`), `_dm022_require_ready` guard,
  disposable build + exclusive transfer + post-build re-proof.
- `finalize/seal` then re-validates via `validate_editorial_receipt` at `2361/2654/2952`.
  If that validator accepts OWN!=CURRENT without CURRENT proof, prepare (CURRENT 70)
  and validate (OWN 63 accepted) diverge: a stale G71 receipt seals at G76.
- Renewal HIGH chronology challenge noted in task ("HIGH_observe publicState before
  basis"): `_observe_renewal_entry` validates LIVE State *before* basis capture, then
  `observe_renewal_authority` rechecks `basis.current_tool_epoch == CURRENT disk
  recompute`. CURRENT proof is **recomputed at consumption time**, never carried by
  the old receipt. Editorial cross-family must do the same: at finalize/seal, reload
  CURRENT 70 + CURRENT contract + HEAD verification fresh; do not trust embedded
  `tools.closure/contract/commit`.
- `verify_activation_history` (`4134+`) shows the correct home for OWN-only checks:
  detached, no State eligibility claim, caller must use `resolve_publication_selection`
  with State for current-active. C2's OWN branch belongs there (or a new detached
  `verify_editorial_history_own_epoch`), never in `validate_editorial_receipt`.

## 4. G67→G71 bootstrap: how existing source already handled it (no assumption)

- Renewal historian (`survey_versioned_renewal_history_v2.py`): `_derive_tool_generation`
  (`1606+`: G67 OLD67 67 / G71 NEW71 71=OLD67+4new / G76 NEWDM76 76=NEW71+5dm022 via
  exact pipeline+files+modes, no files-only classification),
  `_derive_current_family_from_disk` (`1731+`: CURRENT from live disk, never hardcoded
  G76), `_normalize_generation` (`1529+`: OLD==G67/NEW==G71, G76 no alias),
  `_expected_receipt_closure` 50/63/70 OWN-vs-CURRENT separation. Staged
  `_route_code_deps(route,family)` in candidate is the new G71/G76 editorial analogue
  (final93 had `_route_code_deps(route)` CURRENT-63-only).
- G67→G71 never weakened a LIVE validator: final93 editorial stayed CURRENT-63-only;
  old receipts correctly failed CURRENT proof while historian admitted predecessor
  structurally (renewal ROOT §2: "may admit a historically intact predecessor whose
  old full current receipt correctly fails"). C2 breaks this by merging historian
  logic into the LIVE function.
- Do NOT treat earlier C2 green (run-01 G76 70 + explicit G71 63 control +
  malformed/missing/extra, run-02 release 9, run-03 C2-consumers 17) as LIVE
  cross-family proof: those prove `_editorial_closure_rows` construction + OWN-set
  equality + negative refusals in a frozen copy, not that a G71 receipt is eligible
  for seal/State admission at G76. Longitudinal Attempt7 prepare→…→G71→G76 control
  remains unrun per C2 §5.

## 5. Smallest mapped repair (no new design, no waiver)

**Remove the fallback and the OWN!=CURRENT skip branches from the LIVE function.
Restore CURRENT-only operational semantics (final93 shape + family-aware CURRENT 70).
Relocate OWN checks to a detached historical validator that no operational caller uses.**

Concrete map (file/line refs are candidate-work `survey_editorial_publication_v2.py`):

1. Delete fallback `1225–1230`: if `_derive_current_editorial_family` raises,
   raise (fail-closed `CLOSURE_FAMILY`/`UNSUPPORTED_MIGRATION`). Never
   `_cur_fam_for_val = _own_fam`. Indeterminate CURRENT must refuse LIVE admission.
2. In `validate_editorial_receipt`, derive `expected` from **CURRENT** only:
   `_cur = _derive_current_editorial_family(repo)`;
   `_expected_tuple = _staged_val._route_code_deps(generator_route, _cur)`;
   `_want = 63 if _cur=="G71" else 70`. Require `got set == CURRENT set`
   (keep `CLOSURE_SET` but with CURRENT names in message).
3. For every row: require **both** `git show commit:name == got sha` (ancestry pin)
   **and** `_read_bytes_bounded CURRENT bytes == got sha` (as final93 did with
   `cur_bytes vs got vs exp`). Delete `if _own==_cur` gate around `1266–1272`.
   Keep per-row `path==name`, dup refusal.
4. Require `tools["contract"] == current_contract` **unconditionally**
   (delete `1276–1287` else-pass). Keep stage `a1b977…` note as comment only.
5. Require `_verify_head_bytes` / `verify_tool_basis` on CURRENT-canonical filtered
   subset **unconditionally** (delete `1312–1331` else-OWN loop). Filtered set must be
   `_canonical_closure_names_for_family(route,_cur)` or CURRENT wrapper — never OWN
   when CURRENT differs. Keep ancestor + `cat-file -e` + `merge-base --is-ancestor`
   checks.
6. Keep untouched: strict State bytes/schema, `_require_canonical_current_state`,
   public `agent.validate_agent_state` + error propagation (`800–848`), proposal/staged/
   scope/P3S proof/route-loader replay (`849–1210`), renewal strict branch
   (`714–756`, `945–954`), `_validate_before_renewal_receipt` route equality,
   no caller-verified dict, no pending/verified-dict bypass, no `production.verify_state_basis`.
7. Move OWN-epoch logic to a **new detached function** (e.g.
   `verify_editorial_receipt_history_own_epoch(repo, receipt_path)` — no `state_path`,
   no `agent.validate_agent_state`, no `_require_canonical_current_state`, no admission):
   derive OWN from commit, check OWN set vs OWN blobs + OWN canonical subset vs OWN
   blobs only, return historical classification. Operational callers (`2361/2654/2952/
   4247`, H `:240/:2394`) MUST NOT call it. H recheck at `:2394` stays on LIVE
   `validate_editorial_receipt`. Document that G71 receipts at G76 correctly FAIL LIVE
   validation; history path proves OWN consistency for audit/lineage only.
8. No change to `prepare` CURRENT construction (`2007/2014`) except ensure it never
   passes explicit `family` other than CURRENT (call with `family=None`).

This repair is constructible without new interface/proof propagation: it restores the
selected map (ROOT §3 full CURRENT proof every readback + renewal §2 LIVE/HISTORY
separation + a345 §11.2 historical-vs-operational split). The G71→G76 control then is:
historian validates G71 OWN detached → fresh G76 prepare builds CURRENT 70 with full
proof → LIVE admission accepts only G76 CURRENT → renewal U/C + normal release.
A G71 editorial receipt consumed operationally at G76 refuses (correct stale refusal),
exactly like renewal's "old full current receipt correctly fails."

**Forbidden alternatives (do NOT apply):** generic `pending`/`verified_dict` admission,
`try CURRENT except pass with OWN`, skipping `validate_editorial_receipt` at
finalize/seal, removing `agent.validate_agent_state` or canonical-State checks,
substituting `production.verify_state_basis`, or normalizing renewal `authoring_refs`
into old `authored_refs` shape. Each violates contract §10 / ROOT §§2–3.

## 6. NOT_READY condition (return to Astra before code if triggered)

If General/Astra requires that a G71 63-row receipt with G71 contract be **admitted
as LIVE** at G76 disk (seal/activate/normal release) without a fresh G76 CURRENT
70 receipt — i.e. cross-family operational reuse without fully reloaded matching
typed CURRENT proof — the selected map cannot construct it. That would need a new
typed migration/proof-propagation interface (explicit G71→G76 renewal/migration
receipt carrying both OWN lineage and fresh CURRENT recompute, with new schema,
closure, and consumer map). No such interface is in R3/R4/R5/R6/ROOT or contract §11.

In that case: flag **NOT_READY contract return to Astra** with source-grounded options:

- (A) Strict (selected, recommended): keep §5 repair; G71 LIVE admission refuses;
  compatibility via fresh G76 prepare + historian OWN readback. No contract change.
- (B) New migration contract: return to contract selection (A1-vs-A2 analogue per
  a345 §9/§11.4) to design/version a new typed G71→G76 editorial migration with full
  CURRENT proof propagation, new schema/closure/callgraph, and new witness scope.
  Do not implement as a silent validator fallback.
- (C) Partially guarded A1 is rejected per a345 §11.4: "If any required predicate or
  normal writer cannot be included without weakening it, return the exact blocker and
  revise A1 versus A2; do not implement a partially guarded operation."

Current C2 as written is (C) and must not proceed to longitudinal witness until §5
is applied and re-reviewed. Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN`
preserved. No Production, no W40, no genuine approval.

## 7. Exact re-review checklist for the repair

- `validate_editorial_receipt` contains no `_own_fam` variable, no
  `_cur_fam_for_val = _own_fam` fallback, no `if _own==_cur` gates around bytes/
  contract/head checks; `grep -n "_own_fam\|_cur_fam_for_val" survey_editorial_publication_v2.py`
  empty in that function.
- G76 CURRENT weekly/longform full70 + G71 CURRENT-when-disk-is-G71 control still green;
  tampered/missing/extra/dup/`path!=name`/drift/contract-mismatch/HEAD-drift all refuse.
- Historical G71 receipt at G76 disk: LIVE `validate_editorial_receipt` refuses
  (`CLOSURE_SET`/`CLOSURE_DRIFT`/`CONTRACT_MISMATCH`/HEAD check), detached history
  validator reports OWN-consistent. Both behaviors evidenced, not just one.
- Callgraph unchanged: `2361/2654/2952/4247` + H `240/2394` all invoke LIVE validator;
  no operational caller invokes detached history validator.
- `agent.validate_agent_state` + canonical-State + P3S proof + scope + replay branches
  byte-identical except the closure/contract/head CURRENT restoration.

*End of independent review (pre-append). Source-read only; no runtime/import/test/build/fixture/network/ordinary Commit/Push.*

## 8. Appendix — exact feasibility chronology (root-accepted finding, 2026-10-28 follow-up)

Root accepts §1 finding and requests CURRENT restoration. Open question from §5:
"hist OWN + fresh G76 prepare + CURRENT admission, no new interface" — is that
actually runnable given HIGH chronology (`prepare_renewal → _observe_renewal_entry →
PUBLIC `agent.validate_agent_state`` happens BEFORE basis/source-proof creation)?
If an active G71 editorial receipt refuses at G76, what existing call sequence builds
the first fresh G76 proof without faking old State or waiving a current predicate?
Source-only answer below. Frozen final93 proof-copy pins are authoritative for
HIGH/agent/source (stable); candidate C2 file may be mid-restore, so no candidate
line numbers are relied on here. No prior-green PASS is transferred; mechanisms are
stated as source-read, not as reused test results.

### 8.1 Frozen HIGH chronology (exact, no waiver in the sequence)

File: proof-copy `scripts/survey_versioned_renewal_v2.py` (frozen final93).

1. `prepare_renewal:1068–1105` — entry FIRST: `entry = _observe_renewal_entry(repo,
   state_path)` at `1105`, before any renewal directory claim (`1114–1135`),
   before COPY (`1138–1143`), before history revalidation (`1145–1153`), before
   basis LAST (`1266–1310`) and before post-capture `observe_renewal_authority`
   (`1321`) + detached `srcmod.validate_renewal_basis` (`1326`). Docstring: "Exclusive
   capture: entry -> COPY claim + inventory -> basis LAST + recheck."
2. `_observe_renewal_entry:619–805` — LIVE canonical State+config pins through strict
   no-follow bytes (`642–658`), State schema pin (`660–668`), live Profile binding
   (`670–673`), canonical State-path derivation P1-1575-rule (`674–707`), pure
   prePreview/Exception window (`_require_renewal_entry_window`, P1 414–429 predicates),
   then PUBLIC `agent.validate_agent_state(repo,cfg,state)` on those same LIVE bytes
   with no pending argument + zero-delta rechecks, then prior versioned history via
   typed historian (`verify_versioned_history` on `prior_record_ref`), then current
   commit/contract recorded as INFO pins only ("never compared to state.contract here;
   that equality lives in the forbidden `production.verify_state_basis`").
   Explicit bans: never calls `production.verify_state_basis`, checkpoint resolvers,
   Reader/Gate/Candidate/seal/full receipt/P1/P2R/P3S.
3. `_load_prior_graph:1013–1065` — prior seal + prior receipt reloaded as TYPED
   HISTORICAL DATA ONLY: seal bytes vs `prior_set_ref` SHA (`1022–1026`), receipt bytes
   vs seal `source-receipt` role SHA (`1041–1044`), proposal bytes vs receipt
   `proposal_ref` SHA (`1055–1058`). **No call to `validate_renewal_receipt`,
   no call to `validate_editorial_receipt`, no CURRENT closure/contract check.**
   Returns seal/receipt docs + derived proposal namespace. The old receipt's CURRENT
   validity is never consulted during prepare.
4. CURRENT construction `1191–1200`: `expected_names =
   hist._expected_receipt_closure(entry["generator_route"], "NEW")`, then every name
   re-read from CURRENT disk into `closure_rows` with live SHA. `basis.current_tool_epoch
   = {repository_commit_sha: entry current_commit, contract: entry current_contract,
   closure: closure_rows}` (`1294–1296`). Post-capture `observe_renewal_authority
   :876–960` rechecks `basis.current_tool_epoch == CURRENT disk recompute` member-wise
   (`BASIS_CURRENT_TOOL_DRIFT` on any drift) plus live-live State equality and
   retained-COPY equality.
5. `validate_renewal_receipt:2472–2518` — DETACHED (takes only `receipt_path`, no
   `state_path`, never calls `agent.validate_agent_state`): schema + self-digest +
   basis/proof/build live-SHA pins, then bound `srcmod.verify_renewal_source_proof`
   readback. `verify_renewal_source_proof` (source `survey_versioned_renewal_source_v2.py
   :1408–1537`) is documented "Layer-B full detached verifier (still NO State, EVERY
   readback … Never calls agent/State/Reader/Gate/Candidate/seal/P1/P2R/P3S/full
   receipt/observer)": recomputes CURRENT closure member-wise vs live disk, contract
   vs supported, schemas vs disk, HIST verdict for prior chain. Returns descriptive
   proof, not permission.
6. Editorial prepare (frozen `survey_editorial_publication_v2.py:1631–1910`) NEVER calls
   `validate_editorial_receipt` on the old receipt. It calls `_require_scope_bound`
   (P2V fresh current-before, `:611+`), `_verify_staged` (P3S historical proof),
   builds CURRENT `receipt_closure = _editorial_closure_rows(repo, generator_route)`
   (`1897`) + CURRENT `contract_identity` (`1904`), and only reads the before receipt
   for (a) byte-drift pin, (b) draft-archive/arch path+SHA location. The sole CURRENT
   gate on a before receipt is `_validate_before_renewal_receipt:681–703` and ONLY when
   `gen_kind == VERSIONED_RENEWAL_SOURCE_V1` (then full detached CURRENT renewal proof
   is required). Old-initial and old-editorial before kinds take the unchanged
   old-kind branch with no CURRENT renewal check. `validate_editorial_receipt` runs
   only on the NEW receipt at finalize (`2432`), seal readback, `validate_seal`, CLI,
   and H recheck — all post-build.

Net: **no step in fresh prepare consumes the old G71 editorial/renewal receipt as a
LIVE permission token.** Stale-refusal of the old receipt at G76 therefore cannot
block fresh prepare. The feared circularity ("must pass CURRENT to build CURRENT")
does not exist in this callgraph.

### 8.2 Why LIVE `agent.validate` still passes across G71→G76 (no fake, no waiver)

Per renewal ROOT 7d §2 predicate table, `agent.validate_agent_state` checks State
schema, Profile binding, lifecycle, legacy bytes, checkpoint set/provenance discipline,
stage producer/schema/Profile/recorded-core/review/artifact identity **with historical
`expected_contract` derived internally from that exact record** (not caller overrides),
history lifecycle/instants, Architecture Human provenance, Preview discipline,
derived control fields. It does NOT check editorial/renewal tool closure, CURRENT
contract equality, or CURRENT disk membership. CURRENT-ness is added OUTSIDE the agent
validator by HIGH (`current_commit/current_contract` INFO pins → CURRENT recompute →
`observe_renewal_authority` member-wise equality) and by the detached source proof.
Hence installing G76 (2 modules + 5 schemas, new pipeline/Contract8) does not by
itself fail LIVE State validation for an intact G71-pointing State; the State's own
graph is epoch-agnostic by selected design, and HIGH carries the epoch delta
separately. No synthetic old lifecycle State, no caller-verified dict, no pending
bypass, no `production.verify_state_basis` is involved at any step above.

### 8.3 G67→G71 bootstrap — exact mechanism, no assumed green

Frozen historian `survey_versioned_renewal_history_v2.py`:

- `_derive_tool_generation:1304+` — OLD50 vs NEW63 from ACTUAL OWN recorded epoch:
  owned-epoch config mode/content (pipeline OLD67 vs NEW71 exact), 7 new-file
  presence+`100644` modes via `git show epoch:path`, Contract8 recomputed at OWN epoch
  (pure, NUL framing, no old code). Presence-with-wrong-config REJECTS; partial set
  refuses UNKNOWN. Never a caller flag, never a count-only check.
- `_expected_receipt_closure:1263+` / `_expected_staged_code_deps:1280+` — OLD (30py+
  14schemas+route3+staged1+style1+recipe1 = 50) vs NEW (OLD + 2 family py + 3 new py +
  4 new schemas + 4 family schemas = 63), exact sorted membership.
- First-renewal bootstrap order was therefore: LIVE State passes agent validation
  (epoch-agnostic) → historian admits OLD predecessor structurally (OWN-epoch) while
  its old full CURRENT receipt correctly fails NEW proof → HIGH builds fresh NEW63
  CURRENT basis/proof → detached Layer-B validates CURRENT on every readback →
  normal validators accept only NEW. G67 editorial receipts were never admitted as
  LIVE at NEW disk; the final93 editorial validator stayed CURRENT-63-only with the
  comment "Real old initial receipts 22/27 remain valid via existing route helpers;
  no old-epoch migration."

The candidate DM022 historian extends the identical finite pattern to G67/G71/G76
(`_derive_tool_generation` OWN-epoch, `_derive_current_family_from_disk` CURRENT from
live disk, 50/63/70 closures). Whether any prior green run exercised a TRUE old code
epoch is NOT relied on here; the feasibility claim rests on the source-read callgraph
above, and the G71→G76 control must still be witnessed fresh (Attempt7 longitudinal
run unrun).

### 8.4 Direct answer: smallest existing API sequence for first fresh G76 proof

Precondition: G76 tree installed (candidate 70 files present, modes correct, config
pipeline 76 + Contract8 + 5 schemas registered); LIVE State intact at its G71
checkpoint graph; no State/content edits.

1. HIGH `prepare_renewal(root, state_path, new_renewal_id, intent, manuscript_spec,
   toolchain_or_None, executor)` → internally `_observe_renewal_entry` (LIVE State +
   PUBLIC agent.validate, epoch-agnostic) → `_load_prior_graph` (old seal/receipt bytes
   only) → COPY claim → historian `verify_versioned_history` (OWN-epoch structural) →
   CURRENT 70 closure recompute from disk → basis LAST → `observe_renewal_authority`
   (live-live + CURRENT member-wise) → detached `validate_renewal_basis`. Breaks no
   invariant: old G71 receipt bytes are inputs to lineage/location only, never to a
   CURRENT predicate.
2. Build/prove/finalize/activate renewal per selected U/C routes (detached
   `verify_renewal_source_proof` on every readback; `validate_renewal_receipt`
   detached CURRENT). Result: fresh G76 `VERSIONED_RENEWAL_SOURCE_V1` receipt with
   CURRENT 70 closure + CURRENT contract.
3. Editorial `prepare_publication(root, state, proposal, staged_manifest, ...)` with
   `proposal.basis.generated_receipt_ref` pointing at the FRESH G76 renewal receipt →
   `_validate_before_renewal_receipt` passes (detached CURRENT, route equality) →
   CURRENT 70 editorial `receipt_closure` + CURRENT contract → disposable build →
   exclusive transfer → NEW `EDITORIAL_PUBLICATION_SOURCE_V1` receipt.
4. `finalize_publication` / seal / `validate_seal` invoke RESTORED CURRENT-only
   `validate_editorial_receipt` on the NEW G76 receipt: CURRENT set, CURRENT bytes,
   CURRENT contract, `_verify_head_bytes`/`verify_tool_basis` (commit+HEAD). Passes
   without any OWN fallback because the receipt IS current.
5. G71→G76 compatibility control per ROOT §5.2: the same unchanged-upstream renewal
   at G76 (steps 1–2 with identical research inputs) is the control; the G76 upstream
   correction then follows steps 1–4. Old G71 receipts remain HISTORICAL_VALID via the
   detached history path (`verify_activation_history`-class, no State, no admission)
   and correctly FAIL the restored LIVE validators — that refusal IS the control
   signal, not a failure to be repaired by fallback.

`verify_renewal_source_proof` does NOT build the basis before eligibility (it validates
basis+proof detached, no State); basis construction stays in HIGH `prepare_renewal`
AFTER `_observe_renewal_entry`. No new API is needed for this ordering: the existing
triplet (HIGH LIVE entry + detached basis validation + detached CURRENT source proof)
already spans pre-admission. A new typed pre-admission proof/interface is required
ONLY for the unselected behavior in §8.5.

### 8.5 Final feasibility: CONFIRMED constructible (strict option); genuine contradiction iff LIVE reuse demanded

- **CONFIRM: §5 repair is constructible with existing selected interfaces. No new
  module/schema/API/proof-propagation is needed** to restore CURRENT-only
  `validate_editorial_receipt` + detached OWN history + fresh-G76-prepare ordering
  above. Permitted scope is respected throughout: full public LIVE State validator
  preserved (`agent.validate_agent_state` untouched, canonical path + prePreview window
  intact); H historical stays nonrecursive (no State, no `agent.validate`, no HIGH);
  current source proof reads paths fully (bounded `_read_bytes_bounded` + live re-hash,
  never a caller-verified dict); no implicit new State pointer, acceptance reason, or
  generic pending. Do NOT say "fresh prepare" as a slogan: the five concrete calls in
  §8.4 are the feasibility proof, each breaking no invariant per §§8.1–8.2.
- **Genuine precode-map contradiction exists if and only if** the required witness
  demands operational LIVE admission of a G71 63-row/G71-contract receipt AT G76 disk
  (seal/activate/normal release consuming old closure as current authority) — i.e.
  cross-family receipt REUSE rather than cross-family renewal CONTROL. That behavior
  has no interface in R3/R4/R5/R6/ROOT or contract §11 (which select A1
  retain/clear + guarded regeneration + fresh CURRENT proof, and explicitly reject
  hash-only/reason-only admission, caller-verified dicts, skipped predicates, and
  partially guarded A1 per §11.4). If ROOT requires that reuse, flag NOT_READY contract
  return to Astra with §6 options unchanged: (A) strict refuse-stale + fresh prepare
  (selected, recommended, constructible now); (B) new typed G71→G76 editorial migration
  contract with full CURRENT proof propagation (new schema/closure/callgraph/witness,
  pre-code map + readiness review BEFORE code); (C) partially guarded operation is
  rejected — current C2 text is (C) until §5 lands and §7 re-review passes.
- Real blocker until then: C2 LIVE validator text (`_own_fam` branch + CURRENT-failure
  fallback + OWN!=CURRENT skips). G76 same-family positive work continues independently;
  longitudinal G71→G76 control must run only after CURRENT restoration + independent
  re-review. Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN`, no
  Production/W40/genuine approval, ordinary Commit/Push Human-owned.
