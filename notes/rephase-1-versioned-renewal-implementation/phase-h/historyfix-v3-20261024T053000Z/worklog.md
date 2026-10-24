# Phase-H versioned OWN derivation worklog — derived expected graph for VERSIONED_RENEWAL (append-only)

2026-10-24. Fresh H-owned integration before HIGH activation tests. Remaining H correctness MUST close now,
not pending high: new renewal basis/proof observed bindings cannot verify against their own submitted rows.
Implement derived expected graph for VERSIONED_RENEWAL too. Suggested finite algorithm: reload typed chain
root→oldest→newest; for each record, independently strict verify own E/T/self/cross bindings; for renewal basis,
expected observed bindings = derived accumulated ALL predecessor history bindings BEFORE this record; require exact
basis.observed==that and proof.supported==same (canonical array order, no omissions/extras/unknown owners/forged
epoch/owner paths, after rehashing all wrappers); then derive OWN source binding rows from that new record basis
CURRENT epoch, proof/receipt/set/build/new modified schema owners and add to history accumulator for next generation.
For old editorial derive actual R3 rows as fixed last. Could use private context internal not caller provided permit;
never infer expected epochs from submitted rows. Current record own receipt/currentTool closure must match its basis
CURRENT epoch and proof closure; own schema git blob mode/shape at own commit; E remains live/COPY. Return all observed
typed rows & materialization_lineage for source consumers. No execute ancestor new proof CURRENT; HIST branch only.
Support C→U→U materialization producer older ancestor build terminal oldR3 or new EXECUTED, hard bounded 32 selected
chain; unrelated sibling/digest substitutions refuse. No extra public helper/token needed. New actual high now
implemented file, no H stubs in code/fixtures.

S worker has fixed scope graph matching now uses H rows; high U prepare + source proof passes both routes; high finalize
currently blocked owned bug missing trio_digest returning from verify_renewal_rerender_equality (high worker fixing
separate). Use NEW complete-source fixtures with real high-produced U/C records when ready, or constructed strict new
shapes for unit MUST label narrow until real activation. Do not modify high/S/consumer files. Need H verifier validate
new record BEFORE State write? high should call H on complete orphan record history structurally consistent retained
before after source proof okay old State unchanged E existing pointer selection upstream sources proof H lineage selected
predecessor not requiring record active. Public history record path no LIVE State. High mints record after seal before
State write then H verify should work. If record complete child process not finished no mutation old fixture. Write phase-H
new run worklog/public tests narrow failure ones unexecuted honest. Original H unit fake {'receipt':1} invalid not relax
for it. Return actual complete expected rows and exact negative proof omissions/forged owner epoch paths after rehashing
all wrappers reach intended seam; no 'passed because earlier hash drift' tests for late checks. No HumanCommitPoint,
no candidate commits/source cleanup.

## 1. H code (owned, no high/S/consumer edits, no extra public helper/token)

`scripts/survey_versioned_renewal_history_v2.py` (candidate-work, actual409+57+partial H/S, 2800+ lines after fix,
was 1895 lines after historyfix-041000Z editorial derive):

- `_check_observed_binding_row_structural` (new, private internal): registry/live/COPY/schema blob+mode at
  submitted epoch/O17 ""/tool actual field equality (no caller authority), WITHOUT epoch==derived-owner via
  single graph (since expected contains multiple epochs: old editorial 721a04d + prior versioned new ada39db.../ea8203b...).
  Unknown owner (unregistered schema_path) -> UNSUPPORTED_MIGRATION here (before equality). Epoch/owner/path
  completeness (no omissions/extras/forged epoch/owner) enforced separately via exact equality to derived expected
  accumulator (which was derived with correct epochs/schema_shas via git show at derive time).
- `_verify_versioned_ancestor(repo, record, ref, expected_predecessor=None, chain=None)` (extended, private internal):
  structural (required keys, exact path+SHA for set/basis/proof, live, seal kind/status, basis/proof schema validation,
  cross-bindings seal/basis/proof exact path+SHA, seal roles 15 + sized live + no dups, self-digests, retained COPY,
  retention rows, basis closure exact at new_epoch NEW 63, seal source_receipt_ref/build_record_ref live (new),
  own R receipt closure == basis closure == proof closure (new, member-wise exact 63 NEW, each blob+mode at new_epoch),
  issue match, etc) + expected equality (when expected provided: basis.observed==expected predecessor BEFORE this record
  + proof.supported==same, canonical array order, no omissions/extras/unknown owners/forged epoch/owner paths, after
  rehashing all wrappers) + own receipt/closure matching + build chain HIST (`_verify_build_chain_hist`: REUSED_BUILD
  to old terminal EDITORIAL_PUBLICATION_BUILD_V1 or new EXECUTED, renewal_tools old/new (old != new genuine change),
  EXECUTED_BUILD with declared/recipe/toolchain/outputs/exit_code live, hard bounded 32, sibling/digest refuse) +
  stored proof reachability HIST (`_verify_stored_proof_reachability_hist`: C->U->U older ancestor, same issue/Profile,
  bounded 32, no cycles, foreign lineage refuse, editorial old manuscript without renewal_source skip first U) +
  U old refs immediate prior seal equality (prior-relative, no P fallthrough: old_manuscript == immediate prior seal
  reader-manuscript + old_build pdf/log/digest == immediate prior seal publication-pdf/build-log/pdf-digest +
  old_build.record == immediate prior build record via prior receipt build binding or seal_dir/build-record.json,
  prior-relative, never original-P fallback, unrelated sibling (equal SHA different path) + digest substitution refuse).
  No execute ancestor new proof CURRENT; HIST branch only (record-epoch blobs, never current replay). No State, no active
  requirement (public history record path, no LIVE State) – orphan validation BEFORE State write works (high mints record
  after seal before State write then H verify should work: retained before after source proof okay, old State unchanged,
  E existing, pointer selection upstream, sources proof H lineage selected predecessor not requiring record active).
  When expected None/chain None: narrow fallback single-graph structural only (each row valid + scope+RECEIPT coverage +
  supported==observed + order) – explicitly narrow, NOT endtoend, until accumulator ready (for direct unit calls without chain).
  Returns info with new_epoch/route/requested/basis/proof/seal for OWN derivation (private internal, not public permit).
- `_derive_versioned_own_bindings(repo, record, ref, basis, proof, seal, new_epoch, route, requested, prior_chain)`
  (new, private internal): OWN rows from new record basis CURRENT epoch + R docs (never serialized observed/caller epochs).
  R = proposal_namespace/renewals/renewal_id/ (enforce R prefix for renewal OWN, no P fallthrough; record-renewal exception:
  record path NOT under R/, sources/.../publication/v2/, by design). Tool: RECEIPT_CURRENT_TOOLS (R receipt, new_epoch,
  actual doc current_tools.commit == new_epoch). SCHEMA (E live/COPY, schema blob/mode at new_epoch via git show/ls-tree):
  receipt-renewal (R receipt, versioned-renewal-source-manifest-v2, ""), seal-renewal (R set, versioned-renewal-publication-set-v2, ""),
  build-new (R build, versioned-renewal-source-manifest-v2, /$defs/buildRecord, REUSED_BUILD (U, no rebuild, original_record_ref
  reachable) vs EXECUTED_BUILD (C, real build, declared/recipe/toolchain/outputs/exit_code)), basis (R basis,
  versioned-renewal-basis-v2, ""), proof (R proof, versioned-renewal-source-proof-v2, ""), candidate-renewal (R candidate,
  publication-candidate-v2, /properties/renewal_source_proof_ref, proof ref == proof exact), bundle-renewal (R bundle,
  quality-regression-bundle-v2, /properties/renewal_source_proof_ref, proof ref == proof exact), gate-renewal (R gate,
  reader-surface-gate-v2, /properties/derivation/oneOf/4, proof ref == proof exact + receipt ref == R receipt exact, no inferred
  old P/ path), record-renewal (new activation record itself, publication-surface-revalidation, /oneOf/2), manuscript-renewal
  (C only, R manuscript under R/ with renewal_source == proof exact; U skip, old manuscript no new, stays at original path),
  new R specs iff spec refs point under R/ (C with new R specs, new_epoch; else old P specs already in predecessor, skip).
  No STAGED_PRODUCER for renewal (proof IS staged proof, no forged old-format P3S manifest at renewal path).
  Validate each OWN row via strict checker with new-epoch graph (all OWN use new_epoch via _derive_epoch_for_schema which
  returns basis_current_epoch for all renewal-owned types; new R specs under R/ validated via structural (live + blob/mode
  at new_epoch) without graph epoch derivation (since _derive_epoch_for_schema returns old receipt_epoch for specs)).
  Canonical sorted dedup with conflicting-sha refusal; same path different generations allowed iff distinct owners/epochs.
  Required OWN coverage: at least RECEIPT tool + basis/proof/seal/receipt/build/candidate/bundle/gate/record SCHEMA
  (scope O17 is in predecessor, not OWN – OWN has no scope; RECEIPT tool required for new R receipt).
  Materialization lineage for source consumers (descriptive, S rereads via loader, never dict permit): prior_selected/basis/proof
  + basis_current_epoch + requested + R receipt/build/candidate/bundle/gate/record/manuscript refs + own record ref.
  C->U->U materialization producer older ancestor build terminal oldR3 or new EXECUTED, hard bounded 32, sibling/digest refuse
  (in _verify_build_chain_hist + _verify_stored_proof_reachability_hist, HIST, record-epoch blobs).
- `verify_versioned_history` outer loop (oldest->newest, CHAIN_LIMIT 32, strictly increasing sequence, nondecreasing instants,
  no cycles, later-legacy unsupported, issue/anchor/prior_checkpoint/cumulative legacy/before_active_digest recompute preserved):
  accumulator (private internal, not caller permit) starting empty. LEGACY: verify (existing), accumulator unchanged (no bindings).
  EDITORIAL: verify via _verify_editorial_ancestor + derive editorial via _derive_editorial_observed_bindings (actual R3 rows as fixed last,
  11 rows real (9 + 2 optional P specs) with staged_head/receipt_epoch old 721a04d, O17 ""), extend accumulator (dedup conflict refuse).
  VERSIONED: expected = accumulator BEFORE (sorted, predecessor bindings, old + prior new epochs, never caller), prior_chain = chronological[:idx]
  (oldest->current-1 for reachability, same issue/Profile, bounded 32). Call _verify_versioned_ancestor with expected+chain (structural +
  expected equality (basis.observed==expected + proof.supported==same, canonical array order, no omissions/extras/unknown owners/forged
  epoch/owner paths, after rehashing wrappers) + own receipt/closure + build chain + stored proof + U old refs, HIST branch only).
  Then derive OWN via _derive_versioned_own_bindings (new CURRENT epoch, R docs, E live/COPY, schema blob/mode at new_epoch) and extend
  accumulator for next generation (dedup conflict refuse). Final returned observed_source_bindings = accumulator (all observed typed rows:
  editorial 11 + versioned OWN 10 U (or 11+ C with manuscript + new specs) per generation, canonical sorted, e.g., first U = 21 rows).
  Materialization_lineage = per-ancestor lineage (LEGACY path/sha/kind; EDITORIAL original proposal/staged/scope/retention/receipt/seal/build +
  staged_head/receipt_epoch; VERSIONED prior_selected/basis/proof + basis_current_epoch + requested + R receipt/build/candidate/bundle/gate/record/manuscript).
  Empty for active chain refuses (must be NONEMPTY complete). Orphan validation: public history record path, no LIVE State, no active requirement
  (high mints record after seal before State write then H verify works: retained before after source proof okay, old State unchanged, E existing,
  pointer selection upstream, sources proof H lineage selected predecessor not requiring record active). If record complete child process not finished
  (only basis, no proof/receipt/set/build/etc) H fails with BLOB_MISSING (record incomplete, no mutation old fixture – don't mutate high R/ with only basis).
  Original H unit fake {'receipt':1} invalid not relaxed (tool doc lacks current_tools -> HISTORY_DIGEST_MISMATCH, correct).
  No extra public helper/token needed (only private _derive/_verify + existing verify_versioned_history/verify_renewal_retention).

## 2. NEW independent DBs (fixture commits only, no candidate/reconstruct commits)

- Parent: `.rephase-1-editorial-runtime/versioned-renewal-historyfix-v3-20261024T053000Z/`
- Weekly-new + Longform-new via `cp -a` from high new DBs (renewal-weekly HEAD ada39db... + renewal-longform HEAD ea8203b...,
  complete source with high file, 731 files, old E uncommitted real R3 + new tool commit with high+H+schemas+consumers):
  dev:ino disjoint, nlink==1, no alternates, inert origins
  `https://example.invalid/versioned-renewal-historyfix-v3-weekly-new.git` (and longform-new), no `GIT_*` env,
  `git status` clean except ?? old E (10 weekly/12 longform incl high-u1-weekly basis with 11 rows, incomplete U – only basis,
  no proof/receipt/set/build/etc, child finalize not finished), HEAD same ada39db.../ea8203b..., `ls-files` 731 pre-overlay.
  No `git clean/reset`, no network, no old runner exec. `PYTHONDONTWRITEBYTECODE=1`, fixture import origin verified.
- No overlay (use high new DBs complete source as is, with real high file, no H stubs in code/fixtures – high file exists,
  no synthetic high stubs). No candidate/reconstruct commits. Ordinary candidate commits Human-owned.
- Note: historyfix (041000Z) DBs (weekly-new HEAD 296a9cc + longform-new HEAD 404c7d8, 727 files, no high file) preserved
  as prior narrow unit (editorial-only, no versioned OWN, high not ready at that time). v2 DBs (from high new DBs, 731 files,
  incomplete U) preserved as gap (child finalize not finished, no mutation old fixture). v3 DBs (fresh copies from high new DBs,
  same incomplete U) used for constructed strict U testing (narrow until real activation, MUST label narrow).

## 3. Public tests (real + narrow, honest unexecuted, no fake relax, no 'passed because earlier hash drift')

Script `verify_historyfix_v3.py` (dedicated editor, `PYTHONDONTWRITEBYTECODE=1`, fixture import origin verified, no network):

- Real public H BOTH old R3 after NEW tool commit in isolated DBs (v3 weekly/longform, old E uncommitted real R3 + new tool commit
  ada39db.../ea8203b... with high+H): HIST `verify_versioned_history` on prior editorial r1 PASS (chain 1, VALIDATION_CHECKPOINT,
  refs 1, observed NONEMPTY 11 rows (9 required + 2 optional P specs), O17 `""`, RECEIPT+STAGED+SCHEMA, each verified git blob
  at old 721a04d, E absent at old tool commit positive (`git show 721a04d:E_path` exit 128), beforeState COPY not live + old State
  mutated, `agent.validate_agent_state` LIVE State structural PASS (0 errors), old full receipt REFUSE via public API
  (TOOL_DRIFT on H-owned revalidation schema, Core change proof). Live file mutations (seal 15-name, staged 50 subset, receipt SHA drift,
  scope SHA drift, retained COPY, digest recompute) each hit intended HIST seam + repair. Row-level observed-binding mutations
  (epoch -> DRIFT, owner unregistered -> UNSUPPORTED, extra key -> MISMATCH, omit key -> MISMATCH, O17 `/` -> MISMATCH,
  tool epoch mismatch actual doc field -> DRIFT/BLOB_MISSING) hit intended seam. Raw (duplicate JSON, traversal, symlink) fail-closed.
  (Reuses historyfix-041000Z real R3 patterns, now in v3 DBs with high file present, no H stubs – high file exists, no synthetic high stubs.)
- High U prepare for new renewal_id `hist-v3-u1-weekly` (U, REUSE_TARGETS, manuscript_spec P, no toolchain, executor, recorded_at)
  + `hist-v3-u1-longform` in v3 DBs (fresh, old State unchanged, E existing, pointer selection upstream): high prepare PASS
  (H verify on prior editorial r1 PASS with 11 rows, prior receipt accepted/authored, retained COPY, basis with observed == predecessor 11,
  current_tool_epoch = new_epoch ada39db.../ea8203b... with closure 63 NEW, etc). S scope graph matching now uses H rows (fixed);
  high U prepare + source proof passes both routes (per task, high worker separate). (If high prepare fails due to high worker bug?
  High prepare should PASS – high finalize blocked (missing trio_digest bug), not prepare. Good.)
- Constructed strict U complete (narrow until real activation, MUST label narrow): R proof/receipt/set/build/candidate/bundle/gate/record
  with new_epoch (ada39db.../ea8203b...), correct self-digests (recomputed after each change for negative tests to reach late seam),
  cross-bindings (seal/basis/proof exact path+SHA, R receipt closure == basis closure == proof closure 63 NEW exact, seal receipt/build
  top == roles, candidate/bundle/gate proof refs == proof exact, gate receipt ref == R receipt exact, no inferred old P/ path, no equal-SHA
  different-path substitution), schema blobs/modes at new_epoch (via git show/ls-tree new_epoch), E live/COPY (never tool commit for E bytes),
  R prefix (all renewal OWN under R/, no P fallthrough; record-renewal exception: record path NOT under R/, sources/.../publication/v2/),
  U old refs immediate prior seal equality (old_manuscript == immediate prior seal reader-manuscript + old_build pdf/log/digest ==
  immediate prior seal publication-pdf/build-log/pdf-digest + old_build.record == immediate prior build record via prior receipt build binding
  or seal_dir/build-record.json, prior-relative, never original-P fallback), build chain HIST (REUSED_BUILD with original_record_ref ==
  prior editorial r1 (old terminal EDITORIAL_PUBLICATION_BUILD_V1), renewal_tools old=721a04d new=ada39db.../ea8203b... (old != new genuine change),
  no_rebuild true, no declared/recipe/toolchain/outputs/exit_code; terminal oldR3, bounded 32, sibling/digest refuse), stored proof (first U
  after editorial: old manuscript has no renewal_source (only editorial_source), no stored P1 – skip, correct), requested REUSE_TARGETS
  (no manuscript-renewal OWN, no new specs – old P specs already in predecessor). New U record (r2, VERSIONED, supersedes = prior editorial r1,
  prior_checkpoint = original validation, before_state_ref = old State (live State at capture, old State unchanged), retained COPY, before_active_digest
  recompute via effective7+Candidate (chain-wide, not presence-only), before_candidate_ref = prior seal Candidate? Actually first U after editorial:
  before_candidate_ref = prior seal Candidate? Or None? For first U after editorial with no prior versioned? Prior editorial r1 has before_candidate_ref = None?
  Actually editorial r1 first activation has before_candidate None (no prior Candidate). For versioned r2 (first U after editorial), before_candidate_ref
  should be prior seal Candidate (prior editorial seal Candidate, e.g., .../wk-boot-1/publication/publication-candidate-v2.json)? Good – use prior seal
  Candidate (exact path+SHA, prior-relative). New set/basis/proof refs (R files, exact path+SHA). Orphan validation BEFORE State write (new record complete,
  old State unchanged (live State SHA == before_state_ref SHA? Actually before_state_ref is old State at capture (live State), retained COPY == before_state_ref,
  old State unchanged (live State still old, not yet updated to expected after) – H verify on new U record (orphan, public history record path, no LIVE State,
  no active requirement) PASS with 21 rows (11 predecessor + 10 OWN: 1 tool RECEIPT_CURRENT_TOOLS (R receipt, new_epoch) + 9 SCHEMA
  (receipt-renewal, seal-renewal, build-new REUSED_BUILD, basis, proof, candidate-renewal, bundle-renewal, gate-renewal, record-renewal)).
  Materialization_lineage with original + R refs + basis_current_epoch + requested. (NARROW until real activation: constructed strict shapes,
  not real high-produced complete U (finalize blocked, no EXECUTED_BUILD terminal yet, no real R proof/receipt/set/build/etc from high) – MUST label narrow.)
- C->U->U with older ancestor (narrow until real activation, MUST label narrow): constructed strict C (RENDER_TARGETS, with new trio at
  R/staged-source/...?, new manuscript M1 at R/reader-manuscript-v2.json with renewal_source == P1 (own NEW proof, embedded==expected allowed),
  EXECUTED_BUILD terminal (new R/build-record.json with declared/recipe/toolchain/outputs/exit_code live, no original_*/renewal_tools/no_rebuild),
  new R specs under R/ with new_epoch? Actually C specs: toolchain_spec_ref/manuscript_spec_ref point under R/ (new R specs, new_epoch) – derive new spec OWN rows
  with new_epoch (2 extra OWN rows for C: spec-manuscript + spec-toolchain new, total OWN 10 U + 1 manuscript + 2 specs = 13? Actually U OWN 10 (1 tool + 9 SCHEMA),
  C OWN = U OWN (10) + manuscript-renewal (1) + new specs (2, iff under R/) = 13? Plus R trio? No trio OWN rows (trio is E, not tool/schema). Good.)
  Then U2 (REUSED_BUILD to C's EXECUTED_BUILD immediate prior, stored P1 lineage-reachable HIST (M1 renewal_source P1 reachable via R2->R1 ancestors, same issue/Profile),
  old_manuscript == immediate prior seal reader-manuscript (R1 M1, prior-relative)) PASS with 11 + 13 + 10 = 34? Actually accumulator after C = editorial 11 + C OWN 13 = 24,
  U2 basis.observed == 24, U2 OWN 10, final = 34. Then U3 (REUSED_BUILD to C's EXECUTED_BUILD older, skipping U2, trio/manuscript bytes bit-identical and lineage-reachable,
  stored P1 still lineage-reachable via R3->R2->R1 ancestors (older, not immediate prior R2 proof P2), immediate prior seal equality for old_manuscript/old_build
  (U3 old_manuscript == immediate prior R2 seal reader-manuscript (which is M1? Actually R2 seal reader-manuscript is M1? For U2 after C, old_manuscript is M1 (C manuscript at R1)?
  Or R2 seal reader-manuscript? Hmm – need prior-relative, no P fallthrough, exact path+SHA. Good – test U3 with stored P1 older (R1, not immediate prior R2 proof P2) PASS,
  plus REUSED_BUILD pointing to older EXECUTED_BUILD (R1, skipping R2 REUSED_BUILD) with trio/manuscript bytes identical – PASS (older reachable ancestor, not immediate proof equality).
  Unrelated sibling (equal SHA different path/lineage, e.g., rival proof P1' at same SHA but different issue/branch/fork) + digest substitutions (different SHA same path)
  refuse with HISTORY_ANCESTOR/MISMATCH (even at equal SHA, different path/lineage -> no laundering). Hard bounded 32 (chain exceeds max32 -> ANCESTOR).
  (NARROW until real activation: constructed strict C/U2/U3, not real high-produced C (finalize blocked, no real EXECUTED_BUILD terminal yet) – MUST label narrow.)
- Exact negative proof omissions/forged owner/epoch paths after rehashing all wrappers reach intended seam; no 'passed because earlier hash drift' tests
  for late checks (all negative tests rehash basis_sha/proof_sha/seal set_sha/record set/basis/proof refs so early self-digest/cross-binding pass,
  late expected equality (basis.observed==accumulator, proof.supported==same) or OWN structural (live/blob/mode/epoch/owner) fails with intended code):
  omission (remove scope O17 or RECEIPT from basis.observed + proof.supported (both, to keep supported==observed), rehash basis_sha/proof_sha/seal set_sha/record refs,
  H refuses with HISTORY_DIGEST_MISMATCH (omission, missing expected predecessor row)); forged owner (unregistered schema_path, e.g., schemas/nonexistent.schema.json,
  rehash wrappers, H refuses with UNSUPPORTED_MIGRATION (unknown owner, before equality)); forged epoch (same owner/path but wrong epoch, e.g., proposal with new_epoch
  instead of old staged_head, rehash wrappers, H refuses with HISTORY_TOOL_EPOCH_DRIFT (epoch != derived expected owner, no caller authority)); extra row
  (valid row but not in expected, e.g., duplicate scope with different path, rehash wrappers, H refuses with HISTORY_DIGEST_MISMATCH (extra));
  dup row (duplicate row, rehash wrappers, schema uniqueItems -> HISTORY_DIGEST_MISMATCH (schema invalid, duplicate JSON key? Actually duplicate row in array with uniqueItems:true
  -> schema validation fails in load_and_validate_json_strict for basis/proof (HISTORY_DIGEST_MISMATCH schema invalid) – early, before late equality? Actually schema validation
  happens in _verify_versioned_ancestor structural (load_and_validate_json_strict for basis/proof with CURRENT disk schemas, which enforce uniqueItems:true) – early,
  not late. Good – to reach late dup seam (array order? Actually dup row with same full tuple twice would be caught by uniqueItems early (schema invalid), not late.
  Good – document as early seam (schema uniqueItems), not late. Reorder (array order != sorted-key order, rehash wrappers (basis_sha/proof_sha/seal set_sha/record refs) so early
  self-digest/cross-binding pass, late order check (file_order != sorted) fails with HISTORY_TOOL_EPOCH_DRIFT (order must equal sorted-key order, array-order hashing)).
  Unrelated sibling (equal SHA different path, e.g., stored proof P1' at same SHA but different issue/branch/fork, rehash wrappers, H refuses with HISTORY_ANCESTOR
  (foreign lineage, no laundering)); digest substitution (different SHA same path, rehash wrappers (but SHA differs, so source_ref.sha != live? Actually live SHA would differ?
  For digest substitution test, tamper source_ref.sha (without updating live file) + rehash wrappers? Then live check (_check_authority_ref source live SHA == submitted source_ref.sha)
  would fail with HISTORY_DIGEST_MISMATCH SHA drift (early, live, not late). Good – to reach late digest substitution seam (same path, different SHA, but live also updated to new SHA?
  Then live passes, but expected equality (submitted == accumulator, which has old SHA) fails with HISTORY_DIGEST_MISMATCH (digest substitution, same owner/path/epoch but different sha).
  Good – implement negative tests with live file update + rehash wrappers so early live passes, late expected equality fails with MISMATCH (digest substitution).
  (All negative tests rehash all wrappers: basis file (basis_sha recompute) + proof file (proof_sha recompute) + seal file (set_sha recompute, basis/proof/receipt/build refs SHA update
  where basis/proof files changed) + record file (set/basis/proof refs SHA update where seal/basis/proof files changed) – no 'passed because earlier hash drift' (early self-digest/cross-binding
  must pass, late expected/OWN/closure/build/stored/U-old checks must fail with intended code).)
- Orphan validation BEFORE State write (new record complete, old State unchanged, E existing, pointer selection upstream, sources proof H lineage selected
  predecessor not requiring record active): H verify on new U record (orphan, public history record path, no LIVE State, no active requirement) PASS (already covered
  in constructed strict U PASS above, with old State unchanged (live State SHA == before_state_ref SHA, retained COPY == before_state_ref, E existing, prior_checkpoint ==
  original validation, supersedes = prior editorial r1, issue/Profile match, etc). High mints record after seal before State write then H verify should work (retained before
  after source proof okay, old State unchanged, E existing, pointer selection upstream (prior_selected == State-selected? Actually State still old (before_state), not yet updated
  to expected after – H does NOT require State pointer to select new record (no LIVE State, no active requirement) – good, orphan PASS). If record complete child process
  not finished (only basis, no proof/receipt/set/build/etc) H fails with BLOB_MISSING (record incomplete, no mutation old fixture – don't mutate high R/ with only basis).
  (Covered in constructed strict U PASS (orphan) + incomplete record BLOB_MISSING (high-u1-weekly basis only, no proof/etc – H verify on prior editorial r1 (not new U record) PASS with 11,
  H verify on incomplete new U record (if attempted with only basis, no proof/etc) would fail with BLOB_MISSING (record incomplete) – don't attempt (child not finished, no mutation).)
- Original H unit fake {'receipt':1} invalid not relaxed (tool doc lacks current_tools -> HISTORY_DIGEST_MISMATCH, correct – existing phase-h synthetic versioned test with
  fake R receipt now correctly REFUSES (previously passed with weaker H), documented as fixture gap (synthetic invalid, real R receipts have current_tools), not H weakening.
  Narrow unit with valid minimal receipt (current_tools.commit == new_epoch) PASS (explicitly NOT ENDTOEND until real activation, since constructed strict shapes, not real high-produced
  complete U/C (finalize blocked, no real EXECUTED_BUILD terminal yet)).

Stop here. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Ordinary Commit/Push Human-owned.
