# Narrow mechanical-refresh witness — evidence supplement (corrected first/repeat, true criteria negative, no-write deltas)

- Role: General author-side Co-Worker execution. Not independent audit/review. No delegation; no independent review commissioned. Supplement tests belong to this harness; root does not execute them.
- Authority: root review of the full original harness/report/raw logs (defects A–F); `outputs/rephase-1-weekly-regeneration-decision.md` unchanged and unedited here, as is the handoff.
- Run clock (live, never assumed): run id **`20260927T160625Z`** from `date -u` at execution. Revalidation `recorded_at`: r1 `2026-09-27T16:12:03Z`, r2 `2026-09-27T16:12:57Z` (per-call live clocks).
- Runtime: pre-existing `/tmp/jgas-rephase-application-venv` CPython 3.12.14 (pypdf 6.16.2, jsonschema 4.23.0). No installs, no network, no pip. New isolated fixture `/tmp/jgas-rephase-witness-supp-20260927T160625Z` (H0 `48720ada77088ba16a4a8b1cc55fe76ff62e21b4`, root commit). e4c8269/B/production verified intact before every phase (read-only rev-parse/status) and untouched.
- Packet: NEW `notes/rephase-1-weekly-regeneration/witness_harness_supplement.py`; raw outputs/exits/machine sidecars in `notes/rephase-1-weekly-regeneration/logs/20260927T160625Z/`; `identities-supplement.json` (top-level IDs). Original `witness_harness.py`, `witness-report.md`, `logs/20260927T153429Z/identities.json` are byte-identical and unmodified (pre/post sha256 in §F). Baseline `w0a`/`w0b` on the new fixture ran through the UNMODIFIED original harness; all corrected phases are new supplement code.

## Corrected answer (supplement scope only)

With commit-only and verify/refresh split into distinct OS processes and real current-helper imports logged per run: after committed comment-only control change S1 (`6de6bbb7…`, parent H0) with scope bytes + criteria identical, strict State + `load_derivation` pass, old receipt/Gate reject at the old-tool boundary, the rebuilt receipt replays with accepted/authored refs identical, the CLI-renewed Gate binds the new receipt, strict drift + gate-only pending basis hold, and existing revalidation establishes r1 (`3f195000…`, supersedes null). After S2 (`b41c58f2…`) with intact r1 predecessor, the same sequence establishes r2 (`b8f82855…`, supersedes r1, r1/checkpoint unchanged). Four instrumented negatives — including a TRUE criteria-contract mutation — refuse fail-closed with mutation-baseline snapshots proving no writes before restore, byte-exact restores, and State/record-listing invariance. Candidate-stage still not exercised; no compile/real publication.

## A — actual-current-import execution (first + repeat)

Original defect: `phase_w1`/`phase_w5` imported runtime modules before committing in the same process; `fresh_import_check` only printed a path in a child. Comment-only semantics kept those results informative, but fresh-current execution was unproven — labeled here, not hidden.

Correction: `s-commit` is stdlib-only (argparse/json/os/subprocess/sys/pathlib/git-metadata; asserts `sys.modules` contains no `scripts`/`tests` at commit time, logged per run). `s-refresh-first`/`s-refresh-repeat` start in NEW processes after the commit, import edition code, and log `core.__file__`, helper path, helper file sha256, and HEAD before executing any validator:

- S1 verify (`s-refresh-first.log`): `helper=…/supp-…/scripts/survey_weekly_derivation_v2.py`, `helper_sha=47e961c2…`, `HEAD=6de6bbb7…`; strict State `[]`; recomputed surface identical; old receipt/Gate negatives with raw errors saved; rebuilt receipt replays; accepted/authored refs identical to superseded receipt.
- S2 verify (`s-refresh-repeat.log`): `helper_sha=18a88161…`, `HEAD=b41c58f2…`; strict State passes with intact r1; identical surface; H1-era receipt rejects; new receipt replays; r2 supersedes intact r1.

## B — true criteria negative (N3-FAIL kept as supplemental)

Original N3 changed the review DECISION (PASS→FAIL), not criteria — kept as a non-PASS supplemental negative, not re-run, not relabeled.

New `SN-n3-criteria`: with review/source bytes unchanged, `WITNESS_SUPPLEMENT_REQUIRED_CHECK` appended to `publication_profiles.WEEKLY_MAGAZINE.semantic` in `config/publication-review-v2.json` (structure-preserving, novel ID avoids the duplicate-guard). Clear baselines: S0 pre-mutation snapshot → M1 post-mutation → harness-policy refusal (`criteria drift`, `sneg-n3-criteria-policy.err.txt`) → M2==M1 → real-validator refusal (`validate_review_record` on unchanged bytes: `Publication Review check family differs from bound Profile`, `sneg-n3-criteria-runtime.err.txt`) → M2b==M1 → restore → M3==S0; State sha + revalidation-record listing unchanged throughout; strict State passes after restore.

Labeled dirty-config observation (read-only, separate): strict `validate_agent_state` under the mutated contract returned `[]` — checkpoint validation compares checkpoint-internal recorded contracts, so it does NOT detect criteria drift. This is NOT claimed as a refresh-scope guard; the criteria refusal comes from the review validator + harness policy only.

## C — no-write assertions (retractions + new proof)

Retracted as false: “every sidecar embeds before/after” (sidecars held phase-end snapshots only) and “W0 CLI only-Gate-added oracle” (W0 asserted no such snapshot comparison). Neither is retrospectively invented; original files stand unmodified.

New proof in this packet: per-critical-operation BEFORE/AFTER tree deltas excluding ONLY `.git`, `.witness-evidence/` instrumentation, and `__pycache__` (all disclosed here): verify-only ops assert zero delta; receipt write asserts delta == receipt file only; Gate CLI asserts delta == gate file only; revalidation asserts delta == new record + State pointer. Negatives assert M1==M2 (post-refusal, pre-restore) and M3==S0 with State/record-listing invariance (`s-negatives.log`, `s-negatives.sidecar.json`; N4 records `sneg-n4-*.err.txt`). Prior H0/W1/W4 State/record hashes and the full sidecar inventories support inspected byte preservation but are not cited as intermediate no-write guarantees.

## D — independence, prior deviations, boundary hash

- New fixture independence (read-only, `s-db-checks.sidecar.json`): gitdir==commondir, no `objects/info/alternates`, inert origin `https://example.invalid/witness-edition.git`, no alternate config keys, 12-file inode sample with distinct inodes and nlink==1, clean inherited-GIT-env. Same checks pass read-only on the preserved original fixture (`s-db-checks-orig-readonly.*`).
- Content boundary, corrected: the original `content_boundary_hash` is a sha256 over 657 sorted PATHNAMES, not file content — described correctly here, not reused as a content claim. Byte comparison of committed subset blobs vs exact e4c blobs: 657/657 names match; 656 entries mode+blob identical; exactly ONE exception — `scripts/survey_core_execution_bridge_v2.py`, identical blob `54f6bb15…`, mode `100644` (edition, `shutil.copyfile` drops the exec bit) vs `100755` (e4c). Same single exception verified on the original fixture. Semantically inert for this witness (all invocations via interpreter; no oracle hashes modes). Recorded as the exception, not waived.
- Prior deviations, exact scope as known: report § failures lists `git clean -fdx -- sources surveys`, a full untracked clean with marker round-trip, and `reset --hard 41027f1…`. Raw shell transcripts for those calls were not saved (missing-raw-output limit, stated). Read-only `git reflog --date=iso` on the preserved original fixture corroborates the sequence: H0 `c1f738b` → H1 `41027f1` → H2 `c13bd5a` (failed attempt, object preserved) → reset to `41027f1` → H2 `4ddc88c9`. No further reset/checkout/clean/destructive operations were used in this supplement; on any residue the instruction is to stop, not clean.

## E — corrected evidence fields (originals preserved, never replaced)

- Preserved original H0 receipt raw-byte sha256: `ca04815b72db6b770723573bdcf99a728f9033bb110c84243ced20d0f487f624` (computed read-only over `logs/20260927T153429Z/preserved-evidence/receipt-superseded-H0.json`). The original `w2-sidecar.json` field `receipt_old_sha256` is sha256-of-parsed-JSON, NOT this file hash — original field and file stand untouched; the corrected hash lives only here and in `identities-supplement.json`. Preserved H0 gate raw sha256: `93b24026aea1cbf19bac75f07108ee6b4d92b762af0922d6356094f3d61fd588`.
- Accepted/authored refs: new receipt `accepted_refs`/`authored_refs` asserted list-equal to the superseded receipt's in both refreshes (`s-refresh-first.log`, `s-refresh-repeat.log`). No broader “all accepted refs unchanged” claim is made beyond these runtime-compared lists plus the scope/criteria hash inventories.
- Per-run metadata (cmd, cwd, python 3.12.14, pypdf/jsonschema versions, supplement + original harness file shas, runtime source path/sha, HEAD) is logged in every supplement phase log; supplement revisions used: `cc9a9d26` (s-commit-S1/S2 path — unaffected code) then `3e188674` (all later phases; delta = diagnostic detail + `--tag` + evidence-dir `mkdir`, documented in § failures).

## F — preservation, rerun warning, failure separation

- Originals untouched: pre-session sha256 `witness_harness.py=4b6d529d…ca6ffc8`, `witness-report.md=f529865b…1085f50f`, `logs/20260927T153429Z/identities.json=763dd015…36da60b02`; post-session re-hash below in Verification. Original fixture/logs/failed H2 (`c13bd5a`, reflog-preserved) unmodified; original logs never overwritten (new run-id directory used throughout).
- Rerun warning: supplement phases refuse to overwrite their own outputs (fail-closed; a rerun against the same logs dir aborts — demonstrated by the `s-db-checks` guard firing before `--tag` was added). Saved scripts are NOT safe reruns unless the target logs dir is fresh; the original harness has no such guard and must not be rerun against existing dirs.
- Runtime vs harness failures, separated: all supplement phase exits 0 except `s-refresh-first` attempt 1 (exit 3, HARNESS bug: missing `.witness-evidence` mkdir, `FileNotFoundError` before any canonical write; traceback tool-captured, no file-saved raw stdout for that attempt — stated limit; rerun green after fix, with its own preconditions re-proving no mutation). No runtime validator failure occurred in the supplement; had one occurred, the exact failing call/bytes would be returned per the decision, with no runtime repair.
- No-op negative CLI logs (`s1-noop-repeat.out/err/exit`) are saved unconditionally in the supplement (original saved them only on the unexpected branch).

## Scope, limits, non-claims; partial status

- The original packet remains PARTIAL evidence as reviewed: informative positive CLI revalidation signal, but its W1/W5 freshness, N3, no-write, boundary-hash, and `receipt_old_sha256` claims carry the defects corrected above. This supplement completes exactly the listed oracles — first/repeat fresh-current execution, true criteria negative, per-op no-write deltas, independence + byte-compare, corrected receipt hash — and nothing else.
- Not claimed: candidate-stage, real publication/compile, all-profile support, lifecycle savings, operational interface acceptance, whole-#495 readiness. Changed files: `witness_harness_supplement.py`, `logs/20260927T160625Z/` (incl. `identities-supplement.json`), this report. No candidate/runtime/test edits; no reconstruct commits/push (Human-owned); e4c8269/B/production untouched.

## Verification (post-session, read-only)

- Originals re-hash: harness `4b6d529d…`, report `f529865b…`, identities `763dd015…` — match §F baseline (see commands in session transcript).
- e4c8269 `e4c82692…` / tree `bc377b6b…` (pycache untracked only); B `c04f32ad…` (pycache only); reconstruct `git status` shows only pre-existing untracked `notes/`, `outputs/…decision.md` plus this supplement's new files; HEAD `d665af89…` unchanged.
