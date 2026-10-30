# Shared-Core defect — Evidence authority source-class map gap (SP-efficient-llm-2026)

Status: `RECORDED / BLOCKING / SHARED_CORE_UNCHANGED`
Date: `2026-09-22`
Edition: `SP-efficient-llm-2026` (work branch `special/efficient-llm-2026-work`)
Reporter role: Muse (Luna/Work execution role)

## 1. Symptom (exact reproduction)

Command (repo root, `PYTHONPATH` set to repo root):

```text
python3 scripts/run_evidence_v2_interactive.py \
  --state sources/SP-efficient-llm-2026/production-state.json \
  --input /tmp/opencode/ev-gen/interactive-evidence.json
```

Result: exit 2 with

```text
unsupported source_type for Evidence authority: 'PRIMARY_DOC'
```

The failure is raised by `_source_class()` in `scripts/survey_evidence_v2.py`
(lines 177–183) via `task_authority_sources()` (line 423), called from
`run_evidence_v2_interactive.run()` while resolving per-task authority
sources. The Evidence Task package itself builds successfully (160 tasks);
resolution of the first `PRIMARY_DOC`-bound task (EFF-D004) fail-closes the
whole run. No Evidence, Edition View, Materiality, or Completeness artifact
was written by the failed run (verified: no `evidence/` tree exists under
the edition source root).

## 2. Scope of the block

Against canonical Discovery (`discovery-v2.jsonl`, 165 records) joined with
canonical Screening acceptance (165 decisions), **67 of 160 non-DROP tasks**
bind one of **10 source types absent from the Core v2 Evidence
`SOURCE_CLASS_MAP`** (`scripts/survey_evidence_v2.py`, lines 44–109):

| Discovery source_type | Tasks (non-DROP) | Recommended class (provenance-mirroring) |
|---|---:|---|
| PRIMARY_DOC | 13 | PRIMARY_OFFICIAL (first-party docs/recipes) |
| PRIMARY_REPO | 21 | PRIMARY_REPOSITORY |
| PRIMARY_ANNOUNCEMENT | 8 | PRIMARY_OFFICIAL |
| PRIMARY_MODEL_CARD | 6 | PRIMARY_OFFICIAL |
| PRIMARY_SPEC | 4 | PRIMARY_OFFICIAL |
| SECONDARY_REFERENCE | 8 | SECONDARY |
| SECONDARY_TECHNICAL | 4 | SECONDARY |
| RUNTIME_RECIPE | 1 | PRIMARY_OFFICIAL (maintainer recipe docs) |
| PACKAGING_DOCS | 1 | PRIMARY_OFFICIAL |
| RUNTIME_PR | 1 | PRIMARY_REPOSITORY |
| **Total blocked** | **67** | |

Mapped and runnable: `PRIMARY_PAPER` (92) + `x-community-signal` (1) = 93.
The blocked set includes load-bearing capstone/runtime records (D004, D028,
D029, D030, D031, D032, D039, D040, D049, D052, D063, D078, D127, D129, D130,
D132, D141, D142, D153, D163, D164, D165, and others), so partial
Evidence execution over the runnable 93 alone would silently collapse the
Special's deployment/runtime/capstone lanes and is rejected as an option.

## 3. Why this is a shared-Core defect (not edition-local)

- Core's own Discovery and Screening stages accept `source_type` as an open
  vocabulary (presence-checked only): canonical Discovery (165) and the
  DIRECT-basis Screening acceptance (165, `CORE_STAGE_CONTRACT PASS`,
  checkpoint `DISCOVERY_COLLECTED.json`) both validated with these 10 types
  present.
- Core's Evidence stage fail-closes on the same vocabulary via the fixed
  `SOURCE_CLASS_MAP`. The Thematic collector vocabulary therefore passes two
  Core gates and dies at the third: an internal Core inconsistency.
- The map's own comments document the established repair pattern for exactly
  this failure ("edition-found fail-closed gap blocked fresh Evidence",
  W34 2026-09-09 additions, lines 79–89): extend the map with
  edition-found values classified by provenance.
- No edition-local workaround exists within current Core: Discovery
  `source_records` always pass through `_source_class`
  (`task_authority_sources`, line 423; also line 923), and the Evidence
  Authority Supplement path only *adds* supplement sources with their own
  pre-mapped classes — it cannot substitute the Discovery-bound source
  authority. Rewriting Discovery source types edition-locally would falsify
  accepted canonical bytes and is rejected.

## 4. Production/Core-boundary handling (AGENTS.md + issue §19)

- Shared Core left **unchanged** (verified by `git status`: no modification
  under `scripts/`, `schemas/`, `config/`, `.github/workflows/`, `docs/`).
- No silent patch, no local monkey-patching of Core imports, no forked
  runner: the failed run used exact repository Core bytes.
- Edition work is preserved for clean resume after reviewed Core repair:
  `execution/evidence-interactive-input/` (160-record interactive input,
  generator parts, task-target dump, retrieval provenance) and the
  stage-blocked authority-consumption package
  (`execution/reviews/evidence-authority-consumption-package-r1.md`).
- The formal Evidence/Materiality/Completeness production run is **failed
  evidence**: after reviewed Core repair (map extension +全套 regression per
  Core change-management), the preserved input must be re-executed cleanly;
  no PASS verdict from any partial run may be carried forward.

## 5. Requested Core repair (for Core maintenance, not this edition)

Extend `SOURCE_CLASS_MAP` in `scripts/survey_evidence_v2.py` with the 10
values in §2 using the recommended classes (each mirrors an already-mapped
sibling by provenance), following the W34 comment-precedent, then run the
Core change-management audit. The identical narrow map in
`scripts/run_evidence_v2_interactive.py` (lines 38–45) should be triaged by
Core maintenance for the same gap (it is currently unreachable for these
types for the same reason).

## 6. Secondary observation (non-blocking, for triage)

`survey_orchestrator_v2.py plan` reports a Production State semantic
inconsistency ("checkpoint discovery/screening authority path is not
canonical; history implementation SHA divergence") while
`survey_agent_control_v2.validate_agent_state` (the gate actually enforced
by the Evidence runner) returns clean. Recorded here for Core-maintenance
triage; it did not block this run beyond the §1 defect.

## 7. Resume criteria

1. Reviewed Core repair lands on `main` extending the Evidence source map.
2. Work branch rebases/includes the repaired Core (no edition-byte change
   needed: Discovery/Screening acceptances are unaffected).
3. Re-run `run_evidence_v2_interactive.py` with the preserved
   `execution/evidence-interactive-input/interactive-evidence.json`
   (re-validate byte-identity first); expect 160 Evidence Cards + Edition
   Views + Materiality Ledger + Profile Completeness, then advance State
   through Core to `EVIDENCE_REVIEWED`.
4. Sol performs authority-consumption / materiality review on the produced
   artifacts (this run's audit package stands as the Luna-side input).
