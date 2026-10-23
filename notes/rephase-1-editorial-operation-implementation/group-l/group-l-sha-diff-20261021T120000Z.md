# Group L — source changed hash/diff report (owned paths only)

DST: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
HEAD (detached, unchanged): `409b292756dd1277b9dfae87679934c0d2ce251c`
Other DST modifications/untracked files from parallel H/C workers exist and are
NOT included here; this report covers ONLY Group L owned paths.

Owned paths:
- `scripts/survey_publication_set_v2.py` (NEW)
- `schemas/publication-surface-revalidation.schema.json` (branch edit)
- `schemas/editorial-publication-set-v2.schema.json` (NEW)
- `scripts/survey_agent_control_v2.py` (branch/resolver wiring only)
- `tests/test_survey_publication_set_v2.py` (NEW pure tests)

## SHA256 (owned)

- schemas/editorial-publication-set-v2.schema.json: `7beebcef48d7777144f7df7ce3fddc27c0d39df685fdc49cbfdd7d798c7e61e9`
- schemas/publication-surface-revalidation.schema.json: `2d0a9499af0456c071f88b5deb2971b7abbee838ed73cf5a5595ae418f41e9ed`
- scripts/survey_publication_set_v2.py: `6e753dc33d67356077502b22720d743e6b6de5a4e33bd62d33d0e638bc96db46`
- scripts/survey_agent_control_v2.py: `9ef94dfb50724361692e524920c31a4ee3187db2bbcd2282d41e31576e9e8e94`
- tests/test_survey_publication_set_v2.py: `f7cf26662cb84ba6ca5cf0d74ab74636ebb447abf7813b4ed358b0bbe5f55c20`

## Line counts (owned)

- schemas/editorial-publication-set-v2.schema.json: 92
- schemas/publication-surface-revalidation.schema.json: 246
- scripts/survey_publication_set_v2.py: 1066
- scripts/survey_agent_control_v2.py: 2663 (was 2389; +274 net)
- tests/test_survey_publication_set_v2.py: 216

## Tracked diff stat (owned modified only)

- schemas/publication-surface-revalidation.schema.json: 223 changed lines (refactor to oneOf)
- scripts/survey_agent_control_v2.py: 298 changed lines (branch/resolver wiring)

Untracked owned NEW files (no diff, hashes above):
- schemas/editorial-publication-set-v2.schema.json
- scripts/survey_publication_set_v2.py
- tests/test_survey_publication_set_v2.py

## Full owned diff (truncated reference)

See DST `git diff -- schemas/publication-surface-revalidation.schema.json scripts/survey_agent_control_v2.py`
for the complete tracked diff. New files are full content at the DST paths above
(hashes pinned here). No candidate/reconstruct commit, no Production action,
no reset/clean/raw deletion, no network.
