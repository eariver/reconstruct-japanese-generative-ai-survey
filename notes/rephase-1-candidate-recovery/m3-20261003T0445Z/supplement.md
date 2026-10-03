# Milestone-2 evidence supplement (wording corrections — originals preserved)

Date: 2026-10-03. This file corrects wording in `m2-20261003T0435Z` materials
without editing them. The original compact `manifest.json`, `report.md` and all
`raw/` files remain byte-intact; a pretty-printed view is added alongside as
`manifest.pretty.json` (same parsed content, no new claims).

## C1. `.gitattributes` authorship

`m2` report/manifest describe the `/notes/rephase-1-candidate-recovery/** -text`
rule as a "Human" edit. Corrected: the rule was added by **Astra (root)** as
stated in the verification decision. No General edits to `.gitattributes`
were made in either milestone.

## C2. "Normal hooks" scope

`m2` records hooks as "normal (no --no-verify/-n, no core.hooksPath override,
empty stderr)". Corrected meaning: **no bypass arguments were passed** and the
commit ran through the default hook path. Hook presence was inspected
(`.git/hooks/` holds default samples only); with no custom hooks installed,
"normal hooks" does **not** constitute proved execution of project hooks.

## C3. Initial imports failure retained

`m2` raw `35-imports.*` preserves a `ModuleNotFoundError: No module named
'scripts'` failure (probe used the scripts directory on `sys.path`, while the
modules require repo-root packaging via `from scripts import ...`), followed by
the corrected repo-root probe `35b-imports.*` (IMPORTS_OK, exit 0). The failure
is a **setup/probe-path failure followed by corrected success**, not a code
defect. `m2` "all exits 0" language covers the acquisition/patch sequence only.

## C4. Abbreviated milestone-2 meta records

Some `m2` meta files abbreviate the target as `TGT` and the commit message as
`<message>` instead of literal argv. Those originals are preserved as-is; no
transcript is reconstructed or invented. Binding summary for the record:
actual target `/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z`;
actual committed message subject `Candidate recovery: fixed-baseline 32-path
content (A/B/CLI/R1) for DM-001/019 Freeze boundary` with the honest-identity
body recorded in `17-commit.stdout.txt`. Milestone-3 runners (`run_five.py`,
`run_closure.py`) capture literal argv/cwd/allow-listed env for all new runs.

## C5. Environment/credential inspection of milestone-2 raw

`m2/raw/00-env-sort.txt` was captured with value-redaction applied at write
time: it stores `OPENCODE_SERVER_PASSWORD=<redacted>` (key name + placeholder;
the actual value was never written). It is therefore **not a pristine
full-environment transcript** and must not be cited as one. Verified present:
no secret VALUES exist in any preserved raw artifact (`00-env-sort.txt`,
`05-gitconfig.stdout.txt`, `10-gitconfig.stdout.txt`, both `.git/config`
copies hold only core/sparse/inert-origin settings). `OPENCODE_SERVER_USERNAME`
and `SSH_AUTH_SOCK` path are operational identifiers, not credential material.
All milestone-3 runs record an **allow-listed env subset only**
(`runner-env-allowlisted.txt`, `closure-argv.txt`); no further full-environment
dumps are taken.
