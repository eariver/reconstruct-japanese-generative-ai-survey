# DM-001/019 design — concise source binding (b40)

Parent candidate for the joint unit (verified read-only this session,
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`):

- HEAD: `b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`
- Tree: `657032438c6ed8b1c055d5a120b67b4b261a5092` (exactly historical 481's tree)
- Direct parent: `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (fixed production baseline)
- Live DB: `/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z`
  (`rev-parse HEAD`, `rev-parse HEAD^{tree}`, `log --format='%H %P' -1`,
  `status --porcelain=v1 --untracked-files=no` empty, exit 0)
- Independent restored copy: `/tmp/opencode/jgas-recovery-restore-20261003T0445Z`
  (same HEAD/tree/parent, tracked-clean, exit 0)
- Reconstruct worktree: `066436d6d43a4fcf0b96ed1e8678e7f1edb082c2`
  (matches `066436d`, tracked-clean)
- Runtime (not executed): `/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python3.12` → `3.12.14`

Authoritative recovery binding (NOT the typo'd m2/m3-pretty entries):

- `notes/rephase-1-candidate-recovery/m3-20261003T0445Z/corrections2-identity-20261003T0944Z/final-identity-binding.json`,
  SHA256 `559512d3e48e0101af543fe1b36c0cfded0a1b6304837b1b5bac253c1eaed75e`,
  plus `.../m3-20261003T0445Z/corrections-20261003T0456Z/recovery-manifest.json`.
- Full 32-path + 9-path tables are in that JSON. Corrected blob:
  `tests/test_survey_findings_v2.py` = `6e179887284026d1fb6fc33522b5fb28afc4788e`
  (m2 + m3-pretty `6e178887...` is the preserved typo; originals retained).
- Untouched Freeze-9兄弟 blobs pinning this design's inputs:
  `scripts/survey_publication_v2.py` `af760e198a5d64e2e3998d600b91404e21e27078`,
  `scripts/survey_profiled_freeze_v2.py` `27e5bcb1ee4f892d9a57a3dfdd99e6166f0e98d9`,
  `tests/test_survey_profiled_freeze_v2.py` `83be691fca2fd9aa1103458c67845ab6404cb07e`,
  `tests/test_survey_publication_v2.py` `033234633d0680e05a5fabb97a1487731d66ad2c`,
  `.github/workflows/survey-production-v2-release.yml` `de6531d70453dacf9745dae75564020da104420c`.

Key source anchors at b40 (see `design.md` for full line ranges):

- Canonical Freeze: `scripts/survey_publication_v2.py` 330–383
  (visual 341–346, PDF-only gap 347–348, freeze 349–367, manifest+identity 368–382);
  `release_identity(str,str)` 71–76; `_write_immutable` 62–68.
- Wrapper Freeze: `scripts/survey_profiled_freeze_v2.py` 70–136
  (legacy visual 79/87, State gate 45–59, PDF-only 95–96, identity 123,
  late consumer 135); slug helpers 25–42; `_write_immutable` 62–67.
- Import constraint: `survey_agent_control_v2.py:34` imports `publication`,
  so shared code lives in `publication` (leaf), State preflight stays in
  `profiled`.
- Genuine consumers (no edits proposed): stage RELEASE_CANDIDATE
  `scripts/survey_stage_validation_v2.py` 575–596; release predicate
  `.github/workflows/survey-production-v2-release.yml` 59–103
  (slug/tag recompute 84, `tag != expected_tag` 96–97).
- Fixture sources: `tests/test_survey_publication_revalidation_v2.py`
  (`Fixture`, `survey_dirname` default `"survey"` — wrapper tests must use
  issue-matching dirname); `tests/test_survey_publication_v2.py::_candidate`
  (SP001 Thematic convergent chain); `tests/test_survey_freeze_stage_boundary_v2.py`
  (real stage→checkpoint→FROZEN pattern); `tests/test_survey_profiled_freeze_v2.py`
  (slug/workflow/quality pins, never calls `build_profiled_freeze`).

No code, tests, refs, or reruns executed. Design selection with Astra next;
implementation + runtime tests after review, then an independent reviewer
distinct from General.
