# Master binding pointer (new supplement — no old file overwritten)

The durable identity record for the fixed-baseline recovery is now two files
read together:

1. `../corrections-20261003T0456Z/recovery-manifest.json` — master recovery manifest (corrections packet;
   unchanged): candidate/parent/tree, paths, methods, probes, archive,
   restoration, scripts, failures, limitations, correction links. It contains
   no 32-blob table, so the typo below does not touch it.
2. `final-identity-binding.json` (this directory) — **authoritative
   32+9 mode/blob binding**, machine-built from live Git, superseding:
   - `m2/.../manifest.json` → `final_32_identities[] path
     tests/test_survey_findings_v2.py` blob `6e178887...` (wrong; correct
     `6e179887...`), and
   - `m3/.../manifest.pretty.json` (same copied entry).

Every other identity entry in those files is confirmed identical across
raw20, both manifests, and both live trees (`comparison-report.txt`,
TOTAL_MISMATCHES=1). Cite `final-identity-binding.json` for blob/mode
bindings going forward; cite the originals only with this pointer attached.

Astra link-only correction, 2026-10-03: fixed item 1's relative path following
`independent-identity-resolution.md` §4. Identity/raw/manifest/archive bytes
were not edited.
