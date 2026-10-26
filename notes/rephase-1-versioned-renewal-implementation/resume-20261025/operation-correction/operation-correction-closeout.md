# Operation-correction closeout — HIGH/Freeze (owned only)

HumanHEAD f84fcf5321be3798c862c0156278afbba01f89f6 (clean except untracked
resume-20261025 packet, verified via git status).
Selected contract 478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf
including §11 unchanged. Root 7d7d5a4552eb7a1abcbafa79d8f358ff10ec96e885b55f09f271766b136cab57 §6 binding.

## Source pins (read-only, no commit)
- Reconstruct: HEAD f84fcf5, status untracked-only operation-correction packet.
- Writable candidate: .rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work
  HEAD 409b292756dd1277b9dfae87679934c0d2ce251c (actual409, tree 8ce36998).
- Fixed baseline snapshot: .rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work
  HEAD 409b292 (same), 731 files (R7b721+10renewal), READONLY.
- Isolated test baseline: .rephase-1-editorial-runtime/versioned-renewal-operation-correction-20261025T060000Z/baseline (copy of snapshot 731).
- Isolated patched snapshot: .../patched (baseline + only owned patch).
- Patched code SHA (patched snapshot, same as writable candidate):
  - survey_versioned_renewal_v2.py 9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152, 3565 lines
  - survey_publication_v2.py 02f8513445b1a264fbb5172af44bf3d85a553e4fc58ebf404e9b9a028e53c365, 1192 lines
  - tests/test_versioned_renewal_operation_correction_b1b2b3.py 37766d6bbdcf3665500cac1d195977976be877bafbe06ccd93613f27c0f83070
- Snapshot (pre-patch) code SHA: HIGH 1620b92c482a5c0c731b27ce7bf27a4eac59c45817da0910b6a7cf4c7a0ba8a2, PUB 6978ae8867b291f62cb9461283406353fb894d1be74bf105a8d2c2c820d4b01e.
- High24 real input (preserved read-only, never modified):
  weekly HEAD 50b03a64627a8bbcc7fcbebc3d305dce84c9b, longform HEAD dbdaf611206050dbc98e7973787ab77076cc4c73.
  U3d proof ecd4a5cd555c / basis 8f8428 / set e643c8fa / candidate 10d9bdac4173 (per reconciliation).

## Mutation (owned only, no S/Reader overlap)
- HIGH: FD-safe _fd_safe_read + _walk_existing_ancestors + _lexical_parts;
  _safe_path/_read_bytes_bounded via FD; canonical lexical expected_state_rel
  + no .resolve alias; cfg/Profile/State pins + _recheck_entry_pins before
  writes; _validate_pinned_instance for State/basis/proof/receipt/set/activation;
  _file_identity + _refuse_alias_unless_exact + _check_already_active_set/record;
  activate/resume unified ALREADY_ACTIVE (exact path+SHA+inode, alias REFUSE);
  CURRENT style vs retained trio + rerender with current style; prepare-targets
  doc as declared C half; _atomic_write_new/_replace_state_bytes/_next_record_rel/
  PdfReader via pinned BytesIO; _validate_build_record_container schema pin.
- PUB: renewal_authority return + union in _preflight (lexical+inode);
  _safe_file ancestor check + redirect refusal; _recheck_snapshot lstat/symlink/
  ancestor + SHA; ROOT correction comment (divergent REFUSES, not overwrite).
- New test: tests/test_versioned_renewal_operation_correction_b1b2b3.py (19 tests).
- NOT touched: survey_versioned_renewal_history_v2.py, survey_versioned_renewal_source_v2.py,
  survey_reader_publication_v2.py, schemas, stage, other tests (reader F4, source F1-F3).

## Test scope (isolated patched snapshot, NOT shared candidate)
- 19 tests OK in .../patched (0.016s): 8 static + 11 live (temp iso + synthetic prep).
  See test-live-stderr.txt (19 ok), test-static-stderr.txt, exits 0.
- B1 positive/negative/fault:
  - _existing_compatible_bytes divergent REFUSES, preserves bytes (proves ROOT correction).
  - Synthetic _preflight with renewal_authority ["proof.json"]: Freeze target==proof
    refuses "overlaps a Freeze authority input" (new overlap seam, not divergent).
  - Hardlink alias: same inode different spelling detected (inode equality, not ALREADY_ACTIVE).
- B2 positive/negative/fault:
  - _lexical_rel rejects traversal; FD refuses leaf symlink + symlinked ancestor.
  - _recheck_entry_pins detects cfg drift (zero-delta), refuses.
- B3 positive/negative/fault:
  - Exact path+SHA+inode True (ALREADY_ACTIVE path).
  - Hardlink alias same SHA/inode different spelling raises RECORD_COLLISION
    "NOT ALREADY_ACTIVE by same SHA" (refuse, not True).
  - Different set False (proceed, not ALREADY_ACTIVE).
- Style: static check for current_style_data vs retained_style_data + mismatch code.

## Actual fault seams (exact refusal, not false previous write)
- B1 exact-path: "Freeze record target overlaps a Freeze authority input: <norm>"
  (preflight spellings). Before guard, _existing_compatible_bytes would have
  refused divergent bytes ("refusing to overwrite divergent"), NOT overwritten
  proof. Missing overlap guard was contract gap; now closed. Do NOT claim confirmed overwrite.
- B1 hardlink: "Freeze record target is hardlinked to a Freeze authority input"
  (preflight identities). Same ROOT correction applies.
- B1 divergent (non-authority target exists with different bytes):
  "refusing to overwrite divergent" via _existing_compatible_bytes (preserves).
- B2 alias State: BASIS_STATE_PATH_IDENTITY "exact spelling required ... no .resolve alias".
- B2 parent symlink: HIGH_MODE "has symlinked ancestor component" / "ancestor is symlink".
- B2 cfg drift: BASIS_ENTRY_INELIGIBLE "implementation config bytes moved ... (selected zero-delta pins; cfg drift refuses)".
- B3 alias set/record: RECORD_COLLISION "alias input refused before writes ... NOT ALREADY_ACTIVE by same SHA".
- Style U mismatch: REUSE_TARGET_MISMATCH "current style template changed vs retained trio.style ... fresh C allowed".

## Source IDs
- Contract 478f0051, root 7d7d5a45 §6, independent-operation B1-B3, reconciliation run35-61/high24.
- Real U3d proof/basis/Candidate/approval paths (preserved, read-only for copy):
  sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u3d-weekly/{renewal-source-proof.json,renewal-basis.json,publication-candidate-v2.json}
  lifecycle-high-u3d-weekly-c/preview-approval.json (binds U3d Candidate).
  Copied bytes only into temp iso for tests; high24 originals never written.

## Unexecuted (explicit, not PASS)
- Full _prepare_freeze_inputs on real U3d Candidate + real approval in patched snapshot:
  triggers S-owned verify_renewal_source_proof -> history _git_run + jsonschema,
  hangs >25s (faulthandler Timeout in history:450 _git_run via source:1241 via reader:208/389).
  Same as reconciliation run54/59/61 timeouts. S-owned path, not our seam; reported, not retried.
  Synthetic _preflight with renewal_authority used instead for owned overlap seam.
- Full HIGH prepare/finalize/activate/resume E2E with genuine changed-tool epochs,
  both routes, repeat C→U→U, renewal→editorial, normal direct Candidate/Preview/Freeze/Release,
  failure/resume + affected regressions + independent final review: OPEN (assessment §5).
- S Layer-B CURRENT style git-blob binding (F3) and S F1/F2/F4: owned by other author;
  if S needs CURRENT style change, exact interface will be reported for root to coordinate (do NOT edit S).
- Stage expected_proof unification: optional, not owned file, not edited.
- No whole completion/CommitPoint/independent PASS. Production semantic NO-GO retained.
  Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.

## Original failure states preserved
1. Initial synthetic _preflight with real U3d _prepare_freeze_inputs hung (S-owned history timeout):
   faulthandler 25s Timeout in history _git_run:450 via source:1241 via reader:208/389 via publication:192.
   Repaired by switching B1 exact-path test to synthetic prep (no S/history), preserving S timeout as unexecuted.
2. Static string mismatches (2 failures): prepare-targets doc expected "no extra writes after external review"
   vs code "no extra writes occur after external"; freeze expected "No generic path dict walker"
   vs code "no generic walker"/"finite typed-ref". Repaired by aligning test to code wording.
3. First freeze copy baseline-count showed 4 files? No—baseline 731 verified; copy stderr 14k due to re-copy over existing baseline from hung run (exit 0, no data loss). Preserved in copy-baseline-stderr.txt.

No cleanup/reset/deletion/old-runner/network/candidate/reconstruct commit. Ordinary Commit/Push Human-owned.
