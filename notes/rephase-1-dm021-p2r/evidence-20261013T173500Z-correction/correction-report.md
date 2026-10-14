# P2R correction report (resumed worker, v6 final)

2026-10-14. Resumed after the interrupted correction subagent per
`notes/rephase-1-dm021-p2r/resume-after-interruption.md`. No running P2R
process was found before launch (narrow `pgrep -f "[r]un_p2r_correction_v5"` /
`"[t]est_survey_editorial_retention_v2"` both rc=1; the only `pgrep -a` hit
was the querying shell itself). No process was killed. This worker acted as
correction implementer/test runner; root reviews.

## 1. Starting state verified (before any edit)

- Current exact16 matched `expected16-pinned-v5.json` for all 16 paths
  (sha256 + bytes + mode): ALL_OK by direct rehash.
- Inherited13 all matched the P1 freeze (`inherited13-comparison.json`,
  13/13 `match: true`); P1 files unchanged.
- Candidate module was already the corrected 1838-line form and the test the
  1230-line form (not initial fd22732a/4143190e).
- Pre-edit snapshot preserved at
  `/tmp/opencode/jgas-dm021p2r-resume-20261014T000000Z/`
  (`module-19fc5923.py`, `test-2dca78f3.py`, `schema-347e5499.json`;
  rehashes equal the v5 pins).

## 2. Changes made (only these; no P1/source13 edits, no commits)

Candidate `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`:

1. `scripts/survey_editorial_retention_v2.py` (+4 lines, 1838 -> 1842):
   owned COPY file entry-vs-creation identity check after each write
   (`FILE_REPLACED` when post-write `os.stat` dev/ino differs from the
   dev/ino recorded at exclusive-create time; guarded when creation
   identity is unavailable). This closes the R4 file-identity gap: the
   comment already promised "dev/ino must be the created one" but no
   comparison existed. Healthy path unaffected (entry necessarily equals
   the just-created file absent a race/attack).
2. `tests/test_survey_editorial_retention_v2.py` (1230 -> 1305 lines,
   18 -> 19 methods):
   - New `test_replacement_owned_file_midcapture_refuses`: swaps one fully
     written owned COPY file (same bytes, new inode) exactly when manifest
     publish opens (manifest create is post-COPY by construction); expects
     `FILE_REPLACED` with disposition `OWNED_PARTIAL` from the pre-close
     reverify, plus partial preservation, retry refusal
     (`RETAINED_ROOT_EXISTS`), live-original stability and owned-prefix-only
     delta. Genuine capture-time file-replacement oracle (R4/B1).
   - `test_replacement_ancestor_and_file` file-part comment corrected to
     the exact reachable mechanism (see §4); assertions unchanged.
   - `test_replacement_root_ancestor_file_refuses` header corrected to
     root-only scope (ancestor/file live in sibling methods).
3. No schema change (`347e5499259a…` throughout). No `assert`-statement
   guards added (explicit raises only; `-O` safe by construction).

Final pins (mode `0o664` throughout):

- module `77ee2a3e690c23f64b7dfa4c6c5ef0ec55920644c34a247f8e4e3fc469a0e964`,
  106221 bytes, 1842 lines.
- test `22f5604165f837ae631feabb26859cdc2e2e443e3e6dc4875ec85071bd94e741`,
  67735 bytes, 1305 lines, 19 methods.
- schema `347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c`,
  5618 bytes (unchanged from initial).

## 3. Evidence: final full focused suite (v6)

Runner
`evidence-20261013T173500Z-correction/run_p2r_correction_v6.py`
(NEW versioned file; v1–v5 never re-executed/overwritten):

- Preselected `expected16-pinned-v6.json`; pre-guard HEAD +
  all16 sha/mode/bytes verified before launch.
- Pre: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status/index rc 0.
- Child `python -m unittest tests.test_survey_editorial_retention_v2 -v`
  streamed (pump threads) to EXCLUSIVE durable files DURING the run.
- Result: `Ran 19 tests in 6391.813s OK`, child_rc=0, timed_out=False.
- Finally-post: HEAD/tree unchanged, index empty, all16 sha unchanged;
  wrapper exit 0. No cleanup; status/caches recorded, not asserted away.
- Runtime: Python `3.14.4 (main, Aug 20 2026, 10:41:58) [GCC 15.2.0]`,
  cwd `/home/eariver/git/reconstruct-japanese-generative-ai-survey`,
  argv `run_p2r_correction_v6.py`, inherited `GIT_*` env `{}`
  (all stripped; forced `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
  GIT_ALLOW_PROTOCOL=file`), pip freeze rc 0 (see `run_p2r_correction_v6.meta.json`).
- Runner PID 2666673 / child PID 2666721, started
  `2026-10-14T00:08:12Z` (see `run_p2r_correction_v6.state.json`).
  No duplicate launch; no `-O` inside the long timeout; no full-suite `-O`.

Cheap optimized check (R6): `run_opt_correction_v2.py` (NEW, mirrors v1),
single weekly positive under `python -O`: `Ran 1 test in 251.675s OK`,
exit 0. Full-suite `-O` remains unproved (same bounded limit as before;
new code uses explicit raises only).

## 4. Coverage matrix (finding -> proving method, all PASS in v6)

| Finding | Method(s) |
|---|---|
| Positives Longform/Weekly/R1x2 + snapshot deltas | `test_longform_capture_verify_positive`, `test_weekly_capture_verify_positive`, `test_r1_double_refresh_capture_verify` (incl. cross-proposal drift refusal) |
| Existing-root refusal (empty/same-byte/alias) + no-write | `test_refuse_existing_retained_root` |
| R1 raw paths/aliases/nonregular, lexical dot/`//`/trailing/absolute, leaf alias, FIFO guarded oracle | `test_refuse_unsafe_paths_aliases_nonregular` |
| B2 typed hops: missing/duplicate `state:authority`, disagreeing `state_ref`, ambiguous KEEP, omitted/extra rows | `test_verifier_typed_hop_negatives` (coordinated untrusted-artifact fixtures, exact codes) |
| R2 bindings: wrong COPY capture hash, missing P2R dep, moved dest (absent -> `PATH_MISSING`), moved dest WITH same bytes present -> `RETENTION_DEST_MISMATCH` at the dest-recomputation check BEFORE any read of the moved path, byte_count, extra empty dir | `test_verifier_capture_inputs_deps_dest_dirs_sizes` |
| R2 order/canonical/schema-shape | `test_verifier_staged_canonical_order` |
| X vs required KEEP drift, positive distinct-identity asserts | `test_keep_profile_distinction_and_all_drift` |
| Live-State replacement persistence vs retained drift/staged drift/cross-proposal refusal | `test_persistence_live_state_replacement` |
| Post-capture P1 refusal + no-P1/Git in verifier (mock raises) | `test_p1_refuses_after_capture_no_p1_git_in_verify` |
| Short-write loop success, zero-progress, fsync, owned-partial + retry | `test_fault_write_zero_progress_fsync` |
| B3 manifest write/zero/fsync/close -> distinct `MANIFEST_*` codes, all `INDETERMINATE_INVOCATION`, retry refuses | `test_fault_manifest_write_fsync_close_indeterminate` |
| Combined write+close, primary preserved | `test_fault_combined_write_close_primary_preserved` |
| B1 root swap mid-write -> `ROOT_IDENTITY_CHANGED`, retry refuses | `test_replacement_root_ancestor_file_refuses` |
| B1 ancestor swap mid-write; post-capture file-swap + in-tree `.bak` refused by closed retained inventory (`INVALID_RETENTION` extra) | `test_replacement_ancestor_and_file` (comment now states this exact mechanism; a baseline-free same-byte inode swap alone is beyond a fresh verifier — capture-time continuity is proved by the next row) |
| R4 owned-file swap mid-capture -> `FILE_REPLACED`/`OWNED_PARTIAL` | `test_replacement_owned_file_midcapture_refuses` (NEW) |
| Pre-final KEEP drift, control-file injection, empty edition dir, HEAD move | `test_drift_prefinal_and_finalization`, `test_control_edition_head_drift_refuses` |

Every verifier refusal case compares mutated-pre-call vs immediate-post-call
state before repair; fault cases assert live-original stability and
owned-prefix-only deltas. No fake PASS, no current-Git/P1 standalone
verifier, no delete-to-rerun (independent pristine fixtures per case).

## 5. Preserved history and disclosures

- v4 (`run_p2r_correction_v4.*`, exit 1): 18 methods, 17 pass, 1 failure
  (`test_verifier_capture_inputs_deps_dest_dirs_sizes`: moved-dest refusal
  was `PATH_MISSING`, outside the then-expected regex). Preserved as the
  failed suite; not edited, not re-executed.
- v5 (`run_p2r_correction_v5.meta.json`/`.pre.json` only): interrupted; no
  stdout/stderr/post/exit ever produced. Treated as incomplete, not as a
  result. v6's streaming design exists specifically so an interruption
  preserves partial output; residual limitation: the child was not started
  with `python -u`, so OS/child block buffering delayed visible chunks
  (progress was tracked via fixture-dir cycling instead); flushed bytes
  persist regardless.
- Initial3 (`initial3-hashes.json`, `initial-module-fd22732a.py`,
  `initial-schema-347e5499.json`, `initial-test-4143190e.py`) and v1–v5
  runners/outputs/pins are intact. `py_compile` of the v6 runner left one
  `__pycache__/run_p2r_correction_v6.cpython-314.pyc` in the packet
  (tooling residue, disclosed, not cleaned per no-cleanup rule).
- Proof-copy cache inventory recorded pre-removal in
  `proof-freeze-clean-v2.json` (includes `.opt-1.pyc` from the `-O`
  smoke, which ran before the proof copy; active pycache never part of
  the 16 pins and never concealed: v6 pre/post caches are saved
  separately).
- Earlier proof/failure logs (`evidence-20261013T123807Z-impl/`,
  correction v1–v5) are preserved alongside, not superseded.

## 6. Final patch + independent apply proof (v2)

- `complete-p2r-16path-v2.patch` (787863 bytes,
  sha256 `f42af778da95e025fb09d21fc0aca1ed19e6ff62b2256d613c70cc5df69555d7`),
  generated by `gen_16patch_v2.py` (NEW): disposable byte-copy at
  `/tmp/opencode/jgas-dm021p2r-gen-20261014T000000Z`, disposable-index
  `add -N` + `diff` only; active index verified empty afterwards; gen rc 0.
- `proof_apply16_v2.py` (NEW, R6-hardened) in NEW disposable copy
  `/tmp/opencode/jgas-dm021p2r-verify-20261014T000000Z`: whole-`.git`
  separation (134 regular entries each side, zero shared (dev,ino), zero
  symlinks/non-regulars), no alternates either side, exact inert
  remotes (`https://example.invalid/rephase-candidate-recovery.git`) with
  checked Git rc, clean409 verified (HEAD detached 409, empty status),
  `apply --check` + `apply` rc 0, all16 bytes/modes/sha equal active,
  applied status `3M13A` with empty index. `APPLY_PROOF_OK`, exit 0.
- Old v1 patch/proof (`evidence-20261013T123807Z-impl/`) untouched.

## 7. Boundaries kept

No commits/branches/network/intake/Production/State adoption; no source13
edits (all13 re-verified equal to P1 freeze in v6 pre); no subagents; no
old-script reruns (all runners/outputs versioned-new); reconstruct HEAD
untouched (`a45e1bf…`, only untracked `notes/rephase-1-dm021-p2r/`
additions). The module/test file headers retain the interrupted worker's
3-line "Note on edits" pointer (no `apply_patch` binary; detail disclosed
here, not in the docstring): editing it now would invalidate the v6 pins
for a cosmetic change, so it stays as a pointer and the full detail lives
in this report (§2). Whole NOT_READY, DM021 OPEN;
stopping here for root review and the Human Commit Point.
