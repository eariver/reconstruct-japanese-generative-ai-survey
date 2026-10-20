# Current source observation — R3 Worker A (read-only, new packet)

> Role: Worker A source-availability observation. Read-only inspection only; no restore,
> no copy, no checkout, no hook/script rerun, no Git mutation, no network.
> Sanitized env for Git reads: `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
> GIT_OPTIONAL_LOCKS=0` + `git --no-optional-locks`. No `apply_patch`; this packet's
> three files are the sole writes (dedicated `Write`).
> Date (UTC): 2026-10-20. Workspace HEAD is the Human-committed prior unit head.

## 1. Workspace (reconstruct checkout, read-only)

- Command: `git rev-parse HEAD && git log --oneline -3 && git status --porcelain=v1 --untracked-files=all | head -50` (workdir: workspace root). Exit marker: `---EXIT:0`.
- Observed: HEAD `144246892f7e40cc1e73a3868a405e1b883eb3a5`; log `-3` =
  `1442468` / `4b83a52` / `eb6b79b` (all "Astra work RE: Phase 1 continuation (human commit)");
  `status --porcelain` EMPTY (clean) → matches task premise (Human HEAD1442468, root clean).
- Raw status bytes: none (empty output before marker). No commit/push performed.

## 2. Candidate source (actual, read-only)

Location: `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`
(the R2 final source per assessment §3; reused here read-only, no copy/restore).

| Check | Command (sanitized env as above) | Observed | Exit |
|---|---|---|---|
| HEAD | `git --no-optional-locks -C <cand> rev-parse HEAD` | `409b292756dd1277b9dfae87679934c0d2ce251c` | 0 |
| tree | `git --no-optional-locks -C <cand> rev-parse HEAD^{tree}` | `8ce3699861505f32d1d60bdc185d4d4f635aedb2` | 0 |
| detached | `git --no-optional-locks -C <cand> symbolic-ref -q HEAD` | no output (detached) | 1 (expected: not on a branch) |
| status22 | `git --no-optional-locks -C <cand> status --porcelain=v1 --untracked-files=all \| sort` | 4×` M` + 18×`??` = 22 paths (exact list §3) | 0 |
| cached | `git --no-optional-locks -C <cand> diff --cached --name-only` | empty (no staged entries) | 0 |
| tracked diff | `git --no-optional-locks -C <cand> diff HEAD --name-only \| sort` | 4 tracked modified (list §3) | 0 |
| root cache | `ls <cand>/__pycache__` | `No such file or directory` | 2 (absent at root) |
| deeper cache probe | `find <cand> -maxdepth 2 -name __pycache__ -o -maxdepth 2 -name '*.pyc' \| head` | no output | 0 |
| patch SHA | `sha256sum notes/.../source-packaging/complete22-409-clean.patch` | `7c82ec47eb82dc56210b82063fe04c583d29cd36df5ce19f48297ebd4f000334` | 0 |
| patch bytes | `stat -c '%s %n' <patch>` | `1233999` | — |
| 22 pins | `python3 -c` (hashlib compare vs `complete22-manifest.json`: SHA256+bytes+mode per path) | `OK: 22 / 22`, zero mismatches | 0 |

Mode note: manifest records mode `0o664` for all 22; the python check compared
`oct(st_mode & 0o777)` per file — all matched (included in the 22/22).

## 3. Status path list (sorted, exact)

Modified (4):
`schemas/reader-surface-gate-v2.schema.json`,
`schemas/reader-surface-semantic-review-v2.schema.json`,
`scripts/survey_reader_surface_gate_v2.py`,
`templates/survey/jgaisurvey.sty`.

Untracked (18):
`schemas/editorial-correction-proposal-v2.schema.json`,
`schemas/editorial-retention-manifest-v2.schema.json`,
`schemas/editorial-staged-source-manifest-v2.schema.json`,
`schemas/longform-publication-source-manifest-v2.schema.json`,
`schemas/longform-reader-input-v2.schema.json`,
`scripts/survey_editorial_correction_proposal_v2.py`,
`scripts/survey_editorial_current_authority_v2.py`,
`scripts/survey_editorial_retention_v2.py`,
`scripts/survey_editorial_staged_source_v2.py`,
`scripts/survey_longform_derivation_v2.py`,
`scripts/survey_longform_generated_v2.py`,
`scripts/survey_longform_semantic_publication_v2.py`,
`tests/test_survey_editorial_correction_proposal_v2.py`,
`tests/test_survey_editorial_current_authority_v2.py`,
`tests/test_survey_editorial_retention_v2.py`,
`tests/test_survey_editorial_staged_source_v2.py`,
`tests/test_survey_longform_derivation_v2.py`,
`tests/test_survey_longform_publication_integration_v2.py`.

Style delta (from manifest, re-verified in pin check): `templates/survey/jgaisurvey.sty`
after SHA256 `035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec`, 6569 B
(single `coltitle=SurveyInk` line vs before `3b6d1562…`/6547 B per manifest `before_*`).

## 4. Scope qualifications (mandatory)

- These observations verify CURRENT availability + pin equality ONLY. They are not
  all-entry isolation proof, guard/tool certification, execution-fixture isolation, or
  continuous no-drift evidence. Inode separation, alternates config, census
  (present2376/missing26309), and GEN/PROOF isolation are packaging-packet records
  (cited, not re-observed here); no claim beyond the table above is made from hashes.
- Old checker scripts were NOT rerun; the python comparison above is a new read-only
  observation for this packet, not a guard certification.
- Machine JSON companion: `current-source-observation.json` (same pins + commands/exits).
- No source mutation, no new candidate/reconstruct commit. Stop at Human Commit Point.

*End of observation.*
