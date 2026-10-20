# Pass2 + real builds + transfer + strict receipt — 20261019T134223Z

Scope: `astra-pretex-build-selection.md` full mechanical witness on the two
fixture surfaces from `fixtures-20261019T133259Z/`. No manuscript/publication
reviews/bundle/Candidate/State (STOP before those for postbuild review + root plan).
No source/reconstruct commits, no Production actions, no generated-TeX edits.

Root remains reviewer; this packet claims NO production PASS and NO Human approval.

Independent pre-TeX inspection (`independent-pretex-inspection.md`) is PRESERVED:
fixture-fidelity OK for renderer observation on both routes; **production semantic
NO-GO for BOTH** (Weekly thin placeholder F-W5 + Unknown author F-W3; Special
single-DID four-family placeholder F-S2 + bib/date cautions F-S3/F-S4). Any
schema-valid synthetic PASS below is explicitly type-mechanics only and points at
that report's NO-GO; never a genuine reviewer PASS or Human attribution.

Tool disclosure: `apply_patch` absent. Harness scripts saved BEFORE execution with
`Write` (dedicated editor); dirs with `mkdir` after parent `ls`. Two mechanical
multi-occurrence patches (str(EVIDENCE) cwd fix; attempt4 copy SUF/dir-suffix fix)
were applied via `python3` heredoc in bash instead of repeated editor calls —
recorded here, bytes of all harness versions retained in this dir. No historical
runners reused. `PYTHONDONTWRITEBYTECODE=1` everywhere; no `__pycache__` in
fixtures/notes (verified absent).

## 1. Inputs verified (read-only)

- Selection + inspection + workflows read before execution (see commands logs).
- Original source `/tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60`:
  HEAD `409b292…` unchanged, status still 3M18A, before/after re-verified
  (`source-status-before.txt`, `source-status-after-attempt4` equivalent via fixture log tail).
- Weekly fixture HEAD `88813a01accb320b5948e368618e4061a4d72e0b` (= generation-time
  source-commit, NOT 409 ancestry); Special `d4078d1bc851b9977289acf4b9cd6560c080b69e`.
  Both: no tracked modifications (`diff HEAD` empty), control21 working-tree SHA
  21/21 vs static21, local config without `user.*`, inert origin, no alternates.
- Toolchain READY (no download): `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux`
  LuaHBTeX 1.24.0 (TeX Live 2026), latexmk 4.88, biber 2.22, jlreq.cls + luatexja.sty
  resolvable, HaranoAji OTF present (toolchain attempt4 evidence). Env per run:
  `PATH` prefixed with toolbin; `TEXMFHOME/VAR/CONFIG/CACHE` inside toolroot;
  `TEXDIR/TEXLIVE_ROOT`=toolroot/texlive; `SOURCE_DATE_EPOCH`=fixture commit ct
  (weekly `1792416843`, special `1792416844`); Weekly additionally `FORCE_SOURCE_DATE=1`.
- Missing-package additions into the SAME toolroot only (recorded, no global changes):
  `tlmgr install tikzfill` (tcolorbox skins requires `tikzfill.image.sty`;
  attempt2 builds failed exit 12 on it) and `tlmgr install pdfcol`
  (next missing `pdfcol.sty`; attempt3 failed exit 12 on it). Raws:
  `tlmgr-install-tikzfill-*`, `tlmgr-install-pdfcol-*`, exit 0 both.

## 2. Synthetic type-only pre-TeX reviews (mechanics only)

Created once (attempt1, reused after hash verification, never rewritten):
- Weekly: `sources/2026-W37/publication/v2/reader-surface-semantic-review-v2.json`
  sha256 `79b7cdff41b9509000d4da91d109d9c988ee7a8aeaa696fa8a180b8d5e2c954d9`
- Special: `sources/SP001/publication/v2/reader-surface-semantic-review-v2.json`
  (sha in `special-review-pin.json`)
Both: `review_kind SEMANTIC_EDITORIAL`, check `READER_PIPELINE_INDEPENDENCE PASS`,
`decision PASS / status PASSED`, but `reviewed_by` =
`synthetic type-mechanics fixture (NOT genuine reviewer, NOT Human)` and
detail/summary state type/identity fixture check only + production NO-GO pointer
to the independent report findings. Pins: `weekly-review-pin.json`, `special-review-pin.json`.

## 3. Actual pass2 (both PASS, exit 0)

Subprocess with `PYTHONPATH=<fixture>` (v1 harness omitted it → ModuleNotFoundError,
preserved as `pass2-weekly-stderr.txt` + `harness-exit.txt=14` + archived
`run_pass2_build_transfer-faulty-v1.py`; fixed in attempt2):
- Weekly: `survey_weekly_semantic_publication_v2.py --repo-root <fixture> --state <DRAFT_COMPLETE State> --input <authored>` exit 0 → installed
  `main.tex`/`references.bib`/`jgaisurvey.sty` + `validated-source-manifest.json` + archive + subject.
- Special: `survey_longform_semantic_publication_v2.py ...` exit 0 → same trio + receipt.
Raws: `pass2-*-stdout/stderr/exit-attempt2.txt`, commands in `pass2-*-command-attempt2.txt`.
Attempt3+ reused these outputs after hash verification (`pass2-reuse-verify-attempt*.json`);
pass2 was NOT rerun (publisher refuses existing artifacts).

## 4. Disposable builds (real compiler, NEW dirs, exact trio + declared recipe)

Build roots (preserved, outside source/fixture Git): `/tmp/opencode/jgas-initial-builds-20261019T134223Z/`
- Attempt2 dirs `weekly-build`, `special-build`: input census exactly
  `{.latexmkrc, jgaisurvey.sty, main.tex, references.bib}` (hash-verified copies,
  no legacy `sections/`), but latexmk exit 12 (missing tikzfill) — preserved.
- Attempt3 dirs `*-build-attempt3`: same census, exit 12 (missing pdfcol) — preserved.
- Attempt4 dirs `*-build-attempt4`: exit 0 both (weekly 31.4 s, special 24.5 s).
  Full stdout/stderr/exit + input/output census + env in `build-*-attempt4.*`.
  No TeX edits were made at any point; on the two failures only the toolchain
  gained the missing packages (above), never the generated sources.

## 5. Workflow log gates (engine success separated from log gate)

- Weekly (blocking incl. over/underfull + Missing character):
  0 blocking lines → PASS (`logcheck-weekly-attempt4.txt` empty), page count 5.
- Special (blocking minus over/underfull; layout separate):
  0 blocking, 0 layout lines → PASS (`logcheck-special-blocking/layout-attempt4.txt` empty), page count 5.
Result: `logcheck-results-attempt4.json` both `log_gate PASS`, `blocking_n 0`.

## 6. Stage + transfer (ONLY 3 allowed files, absent-only, hash-verified)

Staged in build dirs: `main.pdf.sha256` with conventional `"<sha>  main.pdf\n"`.
Transferred to canonical survey_roots exclusively (preflight: all 3 destinations
absent; postread sha equality; no audit JSON/aux copied):
- Weekly `surveys/weekly/2026-W37/`: pdf `7230540e…937774c4` (61151 B),
  log 92948 B, digest `1cba981d…` (line `7230540e…  main.pdf`).
- Special `surveys/special/SP001/`: pdf `e181c19a…1e388d` (79128 B),
  log 94005 B, digest `8e3a10a1…`.
Expected/actual pins: `transfer-*-expected/actual-attempt4.json` (equal);
attempt5 re-verified equality (`transfer-*-reverify-attempt5.json`).

## 7. Post-transfer strict receipt (actual validators, both PASS)

Attempt4 harness called nonexistent `gate.validate_survey_build_directory`
(preserved: `receipt-weekly-stderr-attempt4.txt`, harness exit 27, faulty bytes
archived as `run_build_transfer_attempt4-faulty-v2.py`). Attempt5 used the correct
route modules and passed:
- Weekly: `survey_weekly_derivation_v2.validate_receipt` + `validate_survey_build_directory`
  → `RECEIPT_OK sources/2026-W37/publication/v2/validated-source-manifest.json` (8.6 s).
- Special: `survey_longform_generated_v2.validate_receipt` + `validate_survey_build_directory`
  → `RECEIPT_OK sources/SP001/publication/v2/validated-source-manifest.json` (8.9 s).
Raws: `receipt-*-stdout/stderr/exit/command-attempt5.txt`. No QA bundle, no Gate,
no Candidate/State — intentionally not built.

## 8. Evidence packet for independent visual reviewer (real-compiler PDFs only)

Hash-equal copies in this dir: `weekly-main-attempt5.pdf/log/pdf.sha256`,
`special-main-attempt5.pdf/log/pdf.sha256` (assert sha-equal to survey_root files).
Never the old pypdf blank-generator PDFs. Derived inspection inputs:
`weekly/special-extracted-attempt5.txt` (pdftotext -layout), `*-pdfinfo-*-attempt5.txt`,
per-page 150 dpi PNGs `weekly-page-1..5.png`, `special-page-1..5.png` (pdftoppm).
Build dirs preserved for re-inspection. No embedded `.git` in notes.

## 9. Per-route report (counts/status, not test-method counts)

Full machine report: `final-report-attempt5.json`.

| route | fixture HEAD | pass2 | build (exit/duration) | log gate / pages | transfer | receipt |
|---|---|---|---|---|---|---|
| Weekly 2026-W37 | `88813a01…` | PASS (exit 0) | BUILT (0 / 31.4 s) LuaHBTeX 1.24.0 + latexmk 4.88 + biber 2.22, epoch 1792416843 | PASS, 5 pp, 0 blocking | 3/3 OK | PASS (8.6 s) |
| Special SP001 | `d4078d1b…` | PASS (exit 0) | BUILT (0 / 24.5 s) same engine, epoch 1792416844 | PASS, 5 pp, 0 blocking/layout | 3/3 OK | PASS (8.9 s) |

PDFs: weekly `7230540e…` 61151 B / log 92948 B; special `e181c19a…` 79128 B / log 94005 B.
Current blockers: none in this mechanical witness. No renderer/style bug encountered,
so no minimal-fix proposal was needed; had one occurred the raw error + source line
would be returned WITHOUT editing generated TeX (none was edited).

## 10. STOP

STOP before building manuscript/publication reviews/bundle/Candidate/State, to allow
real postbuild review and root plan. Tool scripts in this dir are exact-run evidence
only unless root reviews them; not certified rerun tools (they assume the fixture
states recorded here). Ordinary commits/push and any Production adoption remain
Human-owned.
