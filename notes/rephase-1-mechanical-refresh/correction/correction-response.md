# R1 correction round 2 — response to root's 7 defects (269c review)

Branch `codex/rephase-1-mechanical-r1-correction`; 269c packet (`manifest.json`,
`correction.patch`, `correction-final.patch`, `changed-files/`,
`final-batch1.log`, witness files) left immutable; new evidence under
`correction/round2/`. No hook bypass/reset/clean/config; normal commits only.
Scope kept to the existing seven-path inventory; `survey_reader_surface_gate_v2.py`
needs no change (private inspection + public full replay already correct).

1. COMPLETE SNAPSHOT — Rewrote `_capture_bound_snapshot` around authoritative
   recorded refs with `_add_expected` (conflicting expectations fail instead of
   overwriting) and `_expect_file` (missing required dependency fails at capture,
   live drift at capture refused without blessing). Now covers: old Gate scanned
   surfaces; bundle deterministic-result refs + pdf; manuscript/profile/approval
   refs; EVERY State-bound checkpoint file with artifacts + deterministic review
   results (validation rows use current-effective shas for ALL roles, so a
   healthy prior metadata revalidation with changed manuscript/reviews does not
   false-fail); full predecessor chain via `supersedes` (depth-capped at 33);
   control/contract tracked files enumerated via `git ls-files` with membership
   sentinel `__CONTROL_MEMBERS__` (no `__MISSING__` acceptance, no dir skips).
   `_recheck_bound_snapshot` now takes `controls` and, at EVERY boundary, checks
   HEAD, all hashes, membership, untracked absence, and clean `git diff HEAD`
   (catches staged-index changes hashing alone cannot see). Removed the
   manuscript re-hash overwrite and the synthetic-not-files branch. Snapshot is
   rechecked BEFORE guard creation; new `test_post_preflight_drift_refused_without_writes`
   injects checkpoint/control-dirty/untracked drift after capture and asserts no
   guard/retention/live/record writes.
2. RAW PATH — New `_check_raw_rel_ancestors` / `_check_raw_abs_ancestors` run
   lstat walks BEFORE any `.resolve()`/`core.repo_local_path`; `_safe_existing_file`
   calls them first. Raw user `--state` is checked before `_rel()`; Profile
   source/survey roots before `repo_local_path`; publication dir derived
   lexically from the raw Profile string. CLI refresh branch got a scoped
   config-ancestor check (no global core change). Writer cross-checks the
   resolved Gate role against the lexical Profile path so inside-root aliases
   fail explicitly as alias. New `test_alias_state_and_inside_root_symlinks_refused`
   drives the REAL library/CLI entry with a symlinked State path and a symlinked
   publication dir (not helper-only). Retention-base raw handling kept.
3. GUARD OWNERSHIP — Guard bytes now carry a per-operation `nonce`+`pid`, and the
   fd-captured `(st_dev, st_ino)` identity is checked with the bytes by
   `_verify_guard_owned` BEFORE guard/retention creation is followed by: after
   acquisition, before retention mkdir AND after it, before receipt/Gate
   installation and Gate computation, before revalidation, first in the failure
   path (loss stops everything immediately, no restore through a foreign guard),
   and on every release (signature now bytes+identity; identical-contents
   replacement still refused). `test_two_cooperating_calls_controlled_overlap`
   is now a TRUE overlap: a second real writer runs synchronously inside the
   first writer's retention phase and must refuse on the occupied guard while
   the first completes. `test_foreign_guard_replacement…` now asserts precommit
   refusal with old authority, no record, foreign guard + retention base left.
4. REVALIDATION POST-RENAME — `_atomic_replace_state_bytes` captures temp fd
   identity and `_drop_own_temp` only unlinks its own temp (unknown bytes
   retained); the bare `os.replace` is wrapped. The caller classifies ACTUAL
   State disposition (original vs exact known new vs unknown/unreadable)
   regardless of the return flag: a post-rename readback failure rolls State
   back first and deletes the record only once orphaned and byte-identical, so
   the pointer never dangles and a referenced record is never deleted. Ancestor
   checks rerun at rollback time. Cause preserved throughout. New
   `test_r1_post_rename_readback_failure_no_dangling_pointer` fails once-only
   after the real rename and asserts original State + removed orphan + no
   dangling pointer.
5. RECORD INVENTORY — New `_record_inventory` maps names to hashes/identity
   including symlinks/partials (no `is_file` filtering); unreadable inventory
   is UNKNOWN and fails closed (never treated as clean). The wrapper compares
   full pre/post dicts. The predecessor chain files are pinned in the snapshot
   (point 1), not just the State pointer hash.
6. GATE EQUALITY — Removed the summary/recorded_at/reviewed_at relaxation. The
   writer forwards the old VALIDATED `semantic_authority` dict through the
   existing `evaluate_reader_surface_gate(semantic_authority=…)` API, whose
   strict loader still reopens/revalidates the persisted review
   (review_sha256 + PASS/blocking consistency), and `_compare_gate_reports`
   requires full `semantic_authority` equality; only top-level `recorded_at`,
   `gate_sha256`, and the derivation receipt replacement may change. Heavy
   success (wrapper-built old Gate) plus the extended equality unit test
   (wrapper-style summary preserved; timestamp/summary/surface mutations
   refused) cover both wrapper and direct initial-Gate shapes through the same
   exactness mechanism.
7. EVIDENCE — `witness-afd.py`/`witness-afd-against-afd925d.log` are RELABELED
   as heuristic source-string inventory, not runtime failure witnesses or
   executions, and are not counted as confirmations. The 269c manifest's
   broader run claims without durable logs are superseded by this round: every
   final test below runs ONCE at the committed successor with a durable unique
   log under `correction/round2/` containing exact HEAD/tree, relevant source
   hashes, argv, cwd, python/deps, and explicit exit/counts/skips. No
   tool-only results are claimed. The earlier head/state split stays labeled as
   antecedent scope, not the final matrix.

Limits: no multi-file atomicity, no crash/power-loss automation, no global CAS
against noncooperators; cooperating writers only. Synthetic reviews/PDFs stay
synthetic. For ROOT review again before any independent review; no PASS claimed.
