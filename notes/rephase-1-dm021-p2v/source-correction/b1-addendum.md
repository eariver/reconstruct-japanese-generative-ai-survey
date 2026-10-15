# DM021-P2V B1 addendum — isolated live-State oracle + documentation errata

2026-10-16 JST. Co-Worker A targeted remediation of independent-review blocker
B1 (`independent-implementation-review.md` §6) per root `astra-review-b1-selection.md`.
Test-only addition; P1 `cdd69fe7`/observer `79a3396c` byte-identical (no
implementation defect found). No source/P2R/schema/config/branch/commit/
network/intake/subagents. No independent PASS claimed; root + same independent
reviewer resolve.

## 1. New oracle: `test_live_state_drift_refuses` (B1.1–B1.3)

Appended as method 14 (2 probes + 12 behavioral) in candidate
`tests/test_survey_editorial_current_authority_v2.py`. Full new-test hash
**`c567715dfb4ffa04e7d70dfcf42072cf194d0d9239c2e5b664f7098eaa62009f`**
(74061B). Prior-13 bodies/setup demonstrably unchanged: `old13-bodyhash.json`
(AST `ast.dump` SHA per method — 13 old tests 0 changed, 6 helpers incl.
`setUp`/`_build_weekly_pair` 0 changed, only addition is the new method);
`test-d322-to-new.diff` is 86 additive lines (new method + 3 docstring lines).

Actual healthy Weekly captured fixture (`_build_weekly_pair`), then:

1. **State is COPY, never KEEP:** `basis.state_ref.path` resolves to a
   `retention_plan` row with policy `COPY_BEFORE_REPLACEMENT` and role
   `state:authority`; no other row carries that role; manifest holds exactly
   one `state:authority` row, also COPY. (Matches P1 `_build_graph`
   `mutable.add(state_rel)` — "State adoption changes State: COPY" — and P2R
   I1 chain `state:authority must be COPY`.)
2. **State-ONLY drift:** `state_file.write_bytes(orig + b"\n")`. Same parsed
   JSON asserted; strict `agent.validate_agent_state(root, cfg, mutated)` is
   `[]` (setup not broken — a generic `STATE_INVALID` would mean broken setup,
   and is explicitly not accepted).
3. **P2R still `RETAINED_SET_VERIFIED`** (retained COPY bytes intact; P2R
   re-reads retained rows, not live-State bytes).
4. **P2V refuses exact `BASIS_MISMATCH`** (supplied basis vs rederived live
   basis; live-vs-rederived `STATE_REF` stays consistent since both derive
   from the same mutated bytes) + immediate full files/special/head/status
   equality against the mutated-pre-call snapshot BEFORE repair.
5. **Restore exact bytes → `CURRENT_BASIS_OBSERVED_NEEDS_SCOPE`** again with
   `state_ref.sha256` equal to the original, + no-write.
6. **Cheap clone:** same bytes at unreferenced
   `<source_root>/unreferenced-state-clone.json` passed as `state_path` →
   `STATE_NOT_CANONICAL` + no-write; canonical `state_path` with the clone
   still present → `NEEDS_SCOPE` + no-write (no invented historical
   inventory); clone removed afterwards.

## 2. Targeted verification (isolated, no full rerun)

B4 `run_p2v_b4.py` (e05c02f, AS-SAVED) with `expected18-source-correction-v5.json`
(test entry only), NEW exclusive outdir
`evidence-20261016TB1-targeted/`, `/usr/bin/python3`:
exact selector `...EditorialCurrentAuthorityV2Tests.test_live_state_drift_refuses`
→ **1/1 OK in 492.646s**, child_rc 0 wrapper_rc 0 post_errors [], exit 0,
PRE/POST 102 rows + 84 caches + HEAD/tree/index pinned. Prior full13 (full3)
bodies are byte-proven unchanged above, so scoped affected evidence is this
target + full3; **no full14 run is claimed**.

## 3. New patch + fresh proof (final v5 pins)

- GEN `evidence-20261016TB1-gen/` (absolute `--outdir`, B4 AS-SAVED): exit 0 —
  `complete-p2v-18path.patch` **948373B**,
  saved hash **`dc5ae07b4acb19da2c1d56856f055dd4050530c23286cc0f45c1ae4dcc5ef514`**.
- PROOF `evidence-20261016TB1-proof/` (local corrected `proof_apply18_b4v2.py`
  6fd12225, `--source` P2V candidate byte-copied to fresh unique
  `clean409-copy`): exit 0 —
  `APPLY_PROOF_OK head=409b292756dd1277b9dfae87679934c0d2ce251c files=18
  patch=dc5ae07b4acb`; applied freeze HEAD/tree `409b292…/8ce36998…`, all18
  match v5; candidate verified unchanged. No old proof dir deleted/reused.

## 4. Documentation errata (prior-report contradictions corrected)

- **E1 — full2 exit:** `final-report.md` §3 line ~73 says full2 "wrapper
  survived, exit 0 with failures" — **wrong**. Durable raw
  `evidence-20261015T223000Z-full2/run_p2v_b4.exit` contains `1`, and
  `stage-done.json` records child_rc 1 wrapper_rc 1 post_errors [].
  The §7 evidence list entry "(11/13, exit 1, preserved)" was already correct
  and stands; §3 line ~73 is corrected to **exit 1** here.
- **E2 — proof2 wrong-source refusal loss:** `final-report.md` §6 says the
  P2R-active `--source` refusal raw is "preserved in the removed proof2 dir,
  then reused path" — self-contradictory. Truth: that refusal outdir
  (4 files: exit/meta/stderr/stdout with `PROOF_REFUSAL: ProofFailed: freeze
  lstat failed … survey_editorial_current_authority_v2.py … ENOENT`) was
  deleted with `rm -rf` and the path reused for the green proof, so **no raw
  of that refusal survives** (only the transcript line in session output).
  Loss disclosed; no reconstruction attempted. The substantive lesson stands
  and is re-proven: proof `--source` must contain all18 (P2V candidate used
  for proof2-green and TB1-proof).
- **E3 — full1 orphan:** no POST guards exist (wrapper killed by tool timeout);
  already disclosed in `final-report.md` §§2–3/Q5 and independent review Q5.
  Restated here for completeness; that run is history only.

All intermediate orphan/tooling-failure cases are preserved untouched:
smoke1 (1/2), full1 (POST-less 9/13), full2 (exit-1 11/13), gen1 refusal,
original B4 proof (SyntaxError, byte-identical), plus intermediate manifests
v1–v4 and diff chain. Whole NOT_READY, step4/B3 OPEN, audit unstarted, DM021
OPEN. Ordinary Commit/Push Human-owned.
