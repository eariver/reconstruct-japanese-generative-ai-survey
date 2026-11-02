# Discovery/X dependency table + contract compare (compact, read-only prep — no admission)

Actual invocation clock (this artifact): 2026-11-01T03:18Z (tool `date -u`). Requested editorial times are fixture logical-historical references for factory windows, not real clock: W34 `now/recorded_at 2026-08-25T00:00:00Z` (post-cutoff 2026-08-21T18:00-04:00, preserves ROLLING_WINDOW); SP `recorded_at 2026-09-21T16:10:00Z` (= authorized `as_of`, preserves OPEN_HISTORY_AS_OF). No live clock claim.

## Public Discovery/X entries (final138 workdir `scripts/`)

- `survey_discovery_v2.build_acceptance(repo, discovery_path, x_manifest_path, issue_id, output_path)`: needs discovery JSONL present + X manifest `COMPLETE` (`x_intake.validate_manifest(..., require_complete=True)`) + every record Raw present (`_normalize_record` fail-close) + X↔Discovery binding (`_validate_x_integration`: every COMPLETE run has result; DISCOVERY_RECORDED ids exist and bind imported Grok Raw via `raw_refs`).
- `survey_discovery_v2.validate_acceptance(repo, acceptance_path)`: rechecks X manifest SHA + Discovery JSONL SHA + graph rebuild + X integration from bytes. No State, no approval.
- `survey_x_intake_v2.validate_manifest(repo, cfg, manifest_path, require_complete=True)`: schema + task-file authority SHAs + Drive task identity + every run result present + raw ref valid + disposition rules.
- Screening: `screening.prepare_package` (needs discovery JSONL + State DISCOVERY_COLLECTED) → interactive decisions (`run_screening_v2_interactive.validate_interactive_input`: exact accepted-ID coverage, `validate_decision` per row) → `screening.accept_results`.
- Evidence: `evidence.prepare_evidence_package` → interactive records (`run_evidence_v2_interactive.validate_interactive_input`: profile-bound per-record + exact non-DROP coverage + `task_source_ids` bindings) + completeness (`_validate_completeness_input`: exact universe U 3-field initial / 5-field named, DECLARATION_LOSS via parent_refs) → `accept_evidence_results` → views → ledger → completeness.

## Exact prerequisites / blocked paths (same fixed refs, intake owner has approval)

SP (all verified locally before staging; API size+blob == local size+git-blob, sha256 recorded):
- STAGED (owned input paths, proven): `sources/SP-efficient-llm-2026/raw/discovery-observations-*.md` 24/25 (P2, sizes verified) + `.../external/x/efficient-llm-reception-pass-01/raw/x-reception-result-r3.md` 30213B `b3a8a040…`/blob `11cecd33…` == API (P3 p3a59) + discovery JSONL 173299B. Graph check now OK 165 (log `check-graph-after-p3stage`).
- STILL BLOCKED: X manifest `sources/SP-efficient-llm-2026/external/x/x-source-intake-v2.json` (expected SHA `3465dc4f…` from `DATA.p2b21`, P4 pending). Acceptance build/validate + Screening/Evidence admission wait on it. NOT fetched by execution (intake owner P4).

W34 (P2 staged; P3a02–07 NOT consumed):
- STAGED: discovery JSONL 963155B (blob `928ff2ff…` == P2 API) + working-set `sources/2026-W34/intake/working-set/sol-discovery-event-inventory-v0.2.md` 31172B/blob `40ce19e1…` == API (P3 p3a54, verified before copy). Graph now advances past working-set, refuses next missing Raw (currently `external/x/dailyx/raw/2026-08-16_0700.md`).
- STILL BLOCKED: X manifest `sources/2026-W34/external/x/x-source-intake-v2.json` (`702881aa…`, P4) + ~54 collector/gapfill rerun Raws (incl. p3a02–07: API nonempty e.g. p3a02 1805968B/blob `90462213…` but local DATA 0B/empty-blob — do NOT consume; P4 repairs exact blobs). Full list enumerable from discovery `raw_paths` (55 distinct). No admission on unverified deps.

## Fresh vs old contracts (code evolved, research scope preserved)

- Fresh (final138, HEAD 48082356): pipeline `3adfbda2…`, quality/research/publication per current code. Old W34 DATA: pipeline `e6ae2637…`; old SP DATA: pipeline `ee897962…`. Versions `2.0-rc1` same; SHAs differ (expected — do NOT adopt old contracts as code).
- Preserved byte-identical: W34 question/window/dims/3 oblig ids; SP question/12 dims/`as_of`/12 oblig ids/paths. SP O13–15 (LIMITATION, dims attention/decoding/serving, from `DATA.p2b26`) staged as 5-field append in packet only (`input-archive/SP/...-adapted`), not executed.

## Separation (what each check proves)

- Graph (`_normalize_record`+`_validate_graph`+universe/loss): file existence + identity + parent/OID coverage. Now SP OK / W34 refused (above). Says nothing about publisher truth.
- Control (agent State, READY guard, lifecycle, checkpoint provenance): enforced at runner entry; our States ISSUE_INITIALIZED agent-valid, so Screening/Evidence runners correctly refuse lifecycle (no stub used).
- Raw semantic sufficiency (primary bodies, capture dates, vendor-vs-independent): NOT proven by counts/hashes; W34 boundary boxes + SP abstract-scope limits stay LIMITATION until primary Raw corroborated. No semantic PASS claimed.
- Typed review (independent SourceIntake/Screening/Research per governance + Human Gates): still required where governance requires; this packet generates no independent PASS and no approval.

## Corrections / bounds

- Packages: W34 actual 7, SP 9 (not 9 W34). Counts: W34 root 369/effective 439/evidence 409/selection SELECTED41; SP 165/165/160/112.
- Tree status: workdir HEAD 48082356 + dirty owned inputs (2 modified W34 fresh Profile/State + untracked SP dir + staged discovery/Raw). Partial/sparse DB — `git status` does NOT prove whole-tree clean; no such claim.
- No admission run, no commits (source base commit only, prior unit), no Production/network/readback. When P4 (repaired blobs + 2 X manifests + independent P1–P3 audit) lands, root dispatches normal accepted operations; no repeated failures before data fixed.
