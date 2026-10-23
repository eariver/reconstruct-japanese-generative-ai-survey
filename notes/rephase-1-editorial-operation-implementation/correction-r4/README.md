# correction-r4 pre-edit archive + return (central CODE corrector R4, 2026-10-22)

DST: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` (detached actual), tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`
- Status at archive: 25 tracked M + 10 new schemas + 9 new scripts + 10 new tests + `__pycache__` + `tmpvr07sdme/` (preserved, not cleaned)
- Frozen R3c (readonly): `/tmp/opencode/jgas-editorial-r3c-20261021T144500Z/candidate-partial-b40de60`
  HEAD `0d9857e6132fb314a2e2ba141da79c54f4ec5e06`, tree `44bfc1864d269e338bdb64bcc030e5fd558bf060` (40, actual Git)

Pre-edit SHA256 (DST bytes at archive time):
- `export-workflow.pre-r4.yml` `872f31e8879c8b3718e1dfcf092312a7256e1d6a60c532fb61108aaefda6fc`
- `survey_editorial_publication_v2.py.pre-r4` `d57542e0e3e54a2bdbcbd957df99d7380d1659e9e78f71b6c5e729fb2d5eea61097816076f3eaa8f84dd64`
- `survey_agent_control_v2.py.pre-r4` `05f1ee03a91b647d88bd66877e702c7044a34c6d5b44bdbeb46710375a104103`
- `survey_agent_tool_v2.py.pre-r4` `0ff3bd9a0b13509554f82bf2a4c5e729fb2d5eea61097816076f3eaa8f84dd64`
- `survey_longform_derivation_v2.py.pre-r4` `c09c5558f9668906b7d2ed34c55281d5f6d9ed279d3237a8ffc18ac84ea41149`
- `survey_evidence_v2.py.pre-r4` `f7478d8646c2258adc563c2684f2c20a42970c0647831c01499e6ae08ef10341`
- `survey_publication_set_v2.py.pre-r4` `d2909bbaead935d6fba548b9f0b6ee8f02f2c1`

Files in this dir: `*.pre-r4*` are byte copies of DST files before R4 edits.
Edits after this point use dedicated Edit only; no shell source write, no clean/reset,
no network, no candidate commit. Focused DST tests only in temporary dirs, never in
DST original or SOURCE snapshot; `PYTHONDONTWRITEBYTECODE=1` + external `PYTHONPYCACHEPREFIX`
enforced before python startup; no source `__pycache__` growth.

## Corrective identity note (do NOT edit old manifest raw)

- `verify-lifecycle-r3c-20261021T160000Z/source-manifest-r3c-frozen.json` tree field
  `44cbfc1864d269e338bdbd6060305e5fd558060` is 39 chars (Worker C vs actual Git 40).
  Actual frozen Git: HEAD `0d9857e6132fb314a2e2ba141da79c54f4ec5e06` (40),
  tree `44bfc1864d269e338bdb64bcc030e5fd558bf060` (40, via `git rev-parse HEAD^{tree}`).
  Old manifest JSON preserved unchanged as evidence; this note is the correction.
  Body hashes: manifest file itself SHA `8f9b9aaf…` (R3b report), frozen HEAD/tree above,
  DST HEAD/tree above. No rebaseline, no manifest rewrite.
- Canonical7+active7 repeat fixes retained: effective7/canonical7 remain exact 4-key
  `{path,sha256,byte_count,origin}` rows (R3 low+agent), no relaxation to 3-key or default omit.
- SourceDraft stats (new version, not stale 52 summary): DST tracked `ls-files --cached`
  32155 (full 409 index, sparse-worktree preserved), schemas 84 files, scripts 224 files.
  Frozen R3c tracked 718 (partial materialized). Counts are observed, not authority.
  No old positives/faulted copies changed; future testing uses new source epoch (R4 pins below).

## R4 pins (DST after edits, observed, not committed)

- export workflow `c38423be044a557b6f696b8c7365eda13bf95c07ab4e470c6f111f319a1d2710`
- high `survey_editorial_publication_v2.py` `3f9d8e9e7db248f90c2546136a8742e9996d3e25b5a9281d7483f4521ccd7859`
- agent `survey_agent_control_v2.py` `fb41bde6732bc98b52cc1ade64812e2640432a5549892edba463ed9bf2215462`
- runtime_tool `survey_agent_tool_v2.py` `fb25cf558f3e02d5c4d7c55ad8cb4862c7c0cfbb94cb2030d9b4375ff74f68f3`
- longform derive unchanged `c09c5558...`, evidence unchanged `f7478d86...` (runtime_tool fix covers)

## Scope (central CODE corrector, not independent reviewer)

Whole implementation ongoing. Code DST above; frozen R3c readonly; tests workers paused.
StorageWorker archives ONLY yearly inactive other copies to free EDQUOT; this worker
does not touch those or compile/build large fixtures until root reports quota.
Edits only in selected DST files (high, agent, export, Longformderive/evidence/runtime-tool
justified scope). No clean/reset/raw delete/network/ordinary commits.
