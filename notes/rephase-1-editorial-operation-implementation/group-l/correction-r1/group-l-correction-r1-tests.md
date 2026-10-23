# Group L correction R1 — test truths (isolated, no DST pollution)

All runs use `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/opencode/group-l-pycache-20261021`
from the DST root. No `__pycache__` for L-owned files was created in the DST
(the only `scripts/__pycache__` entries belong to parallel H/C workers).

## L behavioral suite: 18/18 OK

`python3 -m unittest tests.test_survey_publication_set_v2` — OK (3.7s).

- Seal schema exact-15/keys; revalidation two-branch + legacy shape;
  digest determinism + wrong-shape refusal (extras/missing/dup/origin/bad candidate);
  raw refusals (absolute/traversal/missing/symlink-alias/ancestor-alias/FIFO/duplicate-key);
  empty-chain anchor; unknown-branch refusal; sequence rules;
  legacy R1 cumulative anchor + live-effective selection (no live-original expectation);
  non-cumulative legacy refused; later-legacy-after-editorial refused (real files);
  full seal+retention activation validates and selects VERSIONED_ACTIVE with
  active7/Candidate binding; foreign before-Candidate refused; seal trio
  mismatch refused; repeated activation with predecessor seal Candidate validates
  and wrong-predecessor Candidate refuses; stage resolver (candidate token,
  template behavior, traversal/wrong-token refusal).

Fixture failures during development (preserved, all fixture-side, source not
weakened): staged `basis.contract_identity` 8-key requirement; toolchain
`/bin/true` symlink (L now accepts a resolved regular-file tool target);
proposal `retention_plan` COPY row keys; retained-State label keys;
same-P overwrite on repeat (fixed by new proposal ID per contract).

## Legacy regression: 31/31 OK + agent control 5/5 OK

- `tests.test_survey_publication_revalidation_v2` — 31/31 OK (156s).
- `tests.test_survey_agent_control_v2` — 5/5 OK.
- `tests.test_survey_publication_v2` + `test_survey_state_publication_authority_v2`
  — 8/10 pass; 2 errors are C-consumer issues on attestation-style fixtures
  (see coordination note), identical with R1 bytes (verified by archive hash
  `9ef94dfb…`: R1 performed the same strict checkpoint load).

During correction, `test_n6_immutable_multi_round_chain` and
`test_n7_historical_chain_tamper_fails` initially errored because the writer
pre-check ran full live enforcement at revalidate entry (legitimate pending
drift refused with a misleading message). Fixed by pointer-branch mode probe
(`resolve_publication_mode`; no live enforcement) driving
`assert_canonical_publication_mode`; `require_active_or_canonical` keeps full
live enforcement for read paths. Both tests pass since.

Combined final run: `test_survey_publication_set_v2` +
`test_survey_agent_control_v2` +
`test_survey_publication_revalidation_v2` = 54/54 OK.

## Not run (mandatory, lead/root)

No long authority/build fixtures, no combined-source integration (initial +
revised 2-route build, R1x2 anchor/refuse-after, repeat correction, consumer
matrix, fault/resume, §9 negatives on public callers). Requires H/C frozen
combined source + root review.
