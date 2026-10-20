# Initial build integration — PREPARATION ONLY (R2 pre-step) — 2026-10-19

## CURRENT closeout — 2026-10-20 JST

**R2 BOUNDED COMPLETE** — [Astra assessment/next R3task](../../outputs/rephase-1-initial-build-integration-assessment.md). Read [root closeout resolution](astra-closeout-resolution.md), mandatory [independent final resolution §§2–6](independent-final-resolution.md), and [postfix visual resolution](independent-postfix-visual-resolution.md). They override early scope/next/PASS/exclusivity/repair/lossless claims below and in intermediate packets. Both real5pp PDFs and synthetic-authority RELEASED paths are evidenced; new O_EXCL transfer/targeted Gate supplement ends VALIDATED_DRAFT, not a full new RELEASED run. Production semantic NO-GO both remains.

Current source409＋22paths4M18A; only new source change technicalnote title `coltitle=SurveyInk`, style035645ca6569B. [Complete22 patch+direct clean409 proof](source-packaging/README.md) SHA7c82ec47/1233999B. Use corrected source-packaging manifest, not the typo in initial style manifest. Original21 unchanged. No candidate/reconstruct commit; packet/assessment/entry changes await Human Commit Point.

Evidence index: [baseline real-builds](builds-20261019T134223Z/README.md), [final22 positives/negatives](final22-integration-20261019T135318Z/README.md) (Weekly base/Special attempt6), [targeted stage/transfer supplement](final22-supplement-20261019T145007Z/targeted-gate-summary.md), its [evidence correction](final22-supplement-20261019T145007Z/evidence-correction.md) **as corrected by root/independent final resolution**. Raw losses/clean/editor deviations and old failure histories are preserved/qualified, not reconstructed. Independent visual resolution is complete; earlier pending wording is historical.

## Preserved preparation report (following scope/STOP statements are historical)

Scope: decision §5 next-task preparation only. No PDF builds, no tests, no fixture
generation, no candidate/reconstruct commit, no Production network/writes.
Root remains reviewer; this packet claims NO independent PASS.

Tool difference disclosure: task asked for `apply_patch or dedicated editor`.
`apply_patch` is absent in this environment. Packet dir was created with
`mkdir` (after parent `ls`), new files with `Write` (dedicated editor).
No historical runners/tests were executed. Source was treated read-only.

## 1. Inputs and starting point

- Workspace HEAD at start: `4b83a5294ed3ffab76e476d5cd4eb809456e4a1f` (`main...origin/main`),
  `git status --porcelain=v1 --branch` showed branch line only (clean) before
  this packet was created. This packet itself is now uncommitted work; no commit
  was created per instruction.
- AGENTS.md current entry + `outputs/rephase-1-integrated-admission-feasibility-decision.md` §5
  + `outputs/rephase-1-completion-roadmap-20261019.md` R2 read before work.
  R2 target fixed: generated Weekly (first) + THEMATIC/LONGFORM_SPECIAL (first),
  existing 2-pass publisher → persisted pre-TeX review → source/receipt/Gate,
  disposable build workspace with closed aux, explicit PDF/log/digest transfer,
  strict public receipt/Gate/QA/Candidate/State witness. Explore maps fixture
  producers separately; this packet does NOT duplicate fixture research.
- Actual source (available, NO restore/reapply):
  `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60`
  expected detached `409b292756dd1277b9dfae87679934c0d2ce251c` /
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` +21 (3M18A),
  static21 `1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5`,
  cache0.

## 2. Method (new script before execution, sanitized env, durable raws)

- New current-run script saved BEFORE any execution:
  `prepare_verify_20261019T132209Z.py`
  (`247a93065fc930370d88338e53e59d27678627b6152a359eb2659740949bd280`, 23299B).
  Prior packet checker `check_current_source.py` was read for reference only,
  never executed (no historical runner reuse).
- Git sanitization on every invocation: inherited `GIT_*` inspected;
  `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE/GIT_CEILING_DIRECTORIES` removed,
  `GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
  GIT_OPTIONAL_LOCKS=0` enforced + `git --no-optional-locks`.
  Pre-enforcement check showed `NO_INHERITED_GIT_ENV`; script `PREP 0`
  `INHERITED` lines are the enforced values themselves (set for the script
  process), not pre-existing overrides. No fetch, no system/global config,
  no alternates, inert origin only.
- Filesystem targets: parent `ls` before each creation; proposed packet
  `notes/rephase-1-initial-build-integration` ABSENT_OK, proposed
  `/tmp/opencode/jgas-initial-build-20261019T132209Z` ABSENT_OK + NO_SYMLINK_OK.
  Evidence files checked ABSENT_OK before each capture; unique before/after/copy
  names, no overwritten logs.
- Direct capture: each run `> stdout.txt 2> stderr.txt; echo -n $? > exit.txt`.
  See `evidence-20261019T132209Z/` (6 durable files + copy logs + this README).
- Source before/after guards: same script run pre-copy (no `--dest`) and
  post-copy (`--dest <new copy>`). No imports of source modules, no writes into
  source/dest `.git`, no `__pycache__` creation in source/dest (verified 0).
- Full `.git` separation (not pack-only sample): `PREP 8` walks ALL files under
  `source/.git`, `dest/.git`, `reconstruct/.git`, compares full `dev:ino` sets
  + worktree 21 hardlink check. Prior R1 packet compared only 5 pack files vs
  durable inputs vs reconstruct HEAD file; this packet supersedes that domain
  for execution isolation only, without re-certifying old restoration raw.

## 3. Source identity / separation result (current observation, not generic cert)

Pre-copy (`prepare_before_stdout.txt` `2e1ec5c7…`, 157 lines, exit 0, stderr 0B)
and post-copy re-guard agree:

- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` match, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2` match, detached True, shallow true,
  git-dir/common-dir `.git`.
- `status -z` 1084B, 21 NUL entries, M=3 untracked=18 (3M18A OK);
  `diff HEAD` 3 lines (the 3M), `diff --cached` 0 lines,
  `ls-files --stage` 32155 (normal index holds HEAD bytes; NOT claimed empty).
- static21 file sha `1c0e339c…` match before trusting; all21 21/21 OK
  (sha+bytes+mode per-file; full per-file lines in raw).
- `.git` census files=83 dirs=48 symlinks=0; alternates absent; config
  `--show-origin` only `.git/config` + `.git/config.worktree` (include/insteadOf
  none; `include.path` rc=1 none); remote `https://example.invalid/...` inert;
  hooks 14 entries all `.sample`, active 0.
- `__pycache__` 0; `rev-list --count` 13; `rev-list --objects --missing=print`
  total 28685 / present 2376 / missing 26309 (matches retained census; summary
  only, no 28k dump in this packet).
- New analysis/execution copy by independent byte copying (no hardlinks):
  `mkdir /tmp/opencode/jgas-initial-build-20261019T132209Z` (exit 0),
  `cp -a <source> <dest>/candidate-partial-b40de60` (exit 0, stdout/stderr 0B).
  Dest: `/tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60`,
  no symlink. Post-copy `prepare_after_stdout.txt` (`f0ab8bc9…`, 183 lines,
  exit 0, stderr 0B): dest HEAD/tree/detached/status 3M18A/VERIFY21 21/21/
  `.git` 83/48/0/no-alternates/inert/cache0 all OK.
  Full inode separation: src 83 vs dst 83 vs reconstruct 2567 `.git` files,
  collisions total 0 cross-domain 0; worktree 21 hardlink-shared 0.
  Source before vs after identical; source unmodified by copy (read-only held).

This supports actual exact-source availability for future execution setup.
It is NOT runtime/fixture/test/PDF/approval/adoption evidence and NOT a generic
tool certification. Future fixture DB still needs its own isolated creation +
  separation checks at execution time.

## 4. Environment checklist (this container, 2026-10-19 UTC)

From `PREP 6` + targeted read-only probes (no network/install; `PYTHONDONTWRITEBYTECODE=1`):

Known-installed:
- `python3` `/usr/bin/python3` 3.14.4 (workflow asks 3.12; local 3.14 has
  `jsonschema 4.23.0` + `pypdf 6.16.2` matching
  `config/survey-production-v2-requirements.txt`, verified via import probes).
- `python3 -m pip` 26.2.1 (module present; `pip3`/`pip` binaries NOT_FOUND).
- `git` 2.53.0.
- `fontconfig` `fc-list`/`fc-match` 2.17.1; 563 fonts; Noto Sans/Serif CJK JP
  present (Regular/Medium/Black etc.).
- Poppler `pdfinfo`/`pdftotext`/`pdfimages`/`pdftoppm` 26.01.0.
- `gs` (Ghostscript) 10.06.0.

Required-but-missing (blocks local direct build):
- `lualatex`, `latexmk`, `biber`, `bibtex`, `kpsewhich` — all NOT_FOUND.
  (TeXLive 2026 required by workflows; none installed.)
- `pip3` binary missing (workaround: `python3 -m pip` exists).
- `docker` NOT_FOUND (no container fallback available locally).
- `convert`/`magick` (ImageMagick) NOT_FOUND; `qpdf` NOT_FOUND.
  (Rasterization fallback currently only `pdftoppm` + `gs`; ImageMagick/QPDF
  unavailable.)

Unknown (cannot decide without TeXLive or execution):
- HaranoAji/Japanese TeX font bundling (`fc-list | grep -i harano` empty;
  `luatexja-preset[haranoaji,...]` in `jgaisurvey.sty` resolves via TeXLive
  packages, not system fonts — UNKNOWN until TeXLive present).
- `jlreq` class, `luatexja-preset`, `biblatex`, `tcolorbox`, `fancyhdr`, etc.
  availability — UNKNOWN (no `kpsewhich` to query).
- `texlive_version: 2026` exact reproducibility, `SOURCE_DATE_EPOCH` handling,
  `latexmk_use_lualatex` behaviour — UNKNOWN locally.
- Network egress / Docker Hub reachability — NOT TESTED per scope
  (no network test attempted).

## 5. Relevant actual build commands / workflow dependencies (read-only)

Read-only sources: `.latexmkrc`, `.github/workflows/build-weekly-survey.yml`,
`.github/workflows/build-special-pdf.yml`, `templates/survey/jgaisurvey.sty`
(header), `templates/survey/weekly-final-main.tex.in`,
`config/survey-production-v2-requirements.txt`.

- Recipe (both routes): `latexmk` with `$pdf_mode=4` (`lualatex
  -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error`),
  `$biber`, `$max_repeat=5` (`.latexmkrc`). Weekly pins
  `xu-cheng/latex-action@v4` with `texlive_version: 2026`, `os: debian`,
  `latexmk_use_lualatex: true`, `root_file: main.tex`,
  `working_directory: surveys/weekly/${ISSUE_ID}`; Special same action with
  `working_directory: ${survey_root}` from LONGFORM_SPECIAL Profile resolution.
- Weekly inputs: `surveys/weekly/<YYYY-Www>/main.tex` (+ `sections/`,
  `references.bib`, `templates/survey/jgaisurvey.sty`, documentclass `jlreq`).
  Template `weekly-final-main.tex.in` requires `../../../templates/survey/jgaisurvey`
  + `references.bib` + `sections/00-frontmatter` + generated section inputs.
- Weekly gates: `test -s main.pdf && test -s main.log`; grep FAIL on
  `LaTeX Warning: (There were undefined references|Citation .* undefined)` |
  `Package biblatex Warning: Please (re)?run` | `Overfull \hbox|Underfull \hbox` |
  `Missing character:`; then `sha256sum main.pdf | tee main.pdf.sha256`;
  upload `main.pdf` + `main.pdf.sha256`.
- Special gates: `setup-python 3.12` + `pip install -r
  config/survey-production-v2-requirements.txt` (`jsonschema==4.23.0`,
  `pypdf==6.16.2`); Profile must be repo-local non-symlink file with
  `publication_profile == LONGFORM_SPECIAL`; `survey_root/main.tex` must exist
  non-symlink; `SOURCE_DATE_EPOCH=$(git show -s --format=%ct HEAD)`; compile as
  above; analyze: `test -s pdf/log`, blocking grep (same minus over/underfull,
  which go to layout field), page count via `Output written on ... (N pages`
  regex, `sha256sum` + `stat -c %s`, JSON audit `special-pdf-build-audit.json`
  (issue/profile/source/pdf/build/commit/texlive/engine/blocking/layout/status),
  exit 1 if blocking non-empty.
- Style deps (`jgaisurvey.sty`): `luatexja-preset[haranoaji,deluxe,match,nfssonly]`,
  `geometry`, `xcolor`, `graphicx`, `booktabs`, `tabularx`, `array`, `multicol`,
  `needspace`, `rotating`, `enumitem`, `tcolorbox[most]`, `fancyhdr`, `xurl`,
  `hyperref`, `bookmark`, `etoolbox`, `biblatex[backend=biber,style=numeric,…]`.
- Closed-aux expectation: disposable build workspace holds aux/log/bbl/bcf/blg/
  run.xml/synctex; only explicit `main.pdf`/`main.log`/`main.pdf.sha256` (Weekly)
  or `main.pdf`/`main.log`/`special-pdf-build-audit.json` (Special) transfer to
  publication side with ownership; existing closed-inventory validator must not
  be weakened (decision §5).

Missing locally to run the above verbatim: entire TeXLive/lualatex/latexmk/biber
chain + `jlreq`/HaranoAji/biblatex packages; `pip3` binary (non-blocking);
Docker (for `xu-cheng/latex-action` parity); ImageMagick/QPDF if rasterization
comparison needs them.

## 6. Safe minimal setup proposal (no global sudo/install without root selection)

No network/install was attempted. For ROOT execution selection, in order:

A. Preferred — local disposable TeXLive via container or user-space install
   (no global sudo, no workspace mutation):
   1. If Docker becomes available (explicit root approval + network egress
      allowance): use `xu-cheng/latex-action@v4` image or `texlive/texlive:2026`
      equivalent in a disposable container, mounting ONLY the new
      `/tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60`
      copy read-write + a separate empty disposable build workspace + a separate
      isolated fixture DB (to be created at execution time, NOT now).
      Keep `GIT_NO_LAZY_FETCH=1`, inert origin, no alternates; record image
      digest, `tlmgr` package list, `lualatex --version`/`latexmk --version`/
      `biber --version` raw.
   2. Else user-space TeXLive: install TinyTeX/TeXLive scheme-small + required
      collections (`luatex`, `latexextra`, `bibtexextra`, `langjapanese`,
      `jlreq`, `luatexja`) under `/tmp/opencode/texlive-<ts>/` (NOT system
      `/usr`, NOT workspace), with `TEXMFHOME`/`TEXMFVAR` inside disposable dir,
      `SOURCE_DATE_EPOCH` handling as workflows. Record installer hash, package
      versions, disk cost, wall-clock. Do NOT `apt-get`/sudo without explicit
      root instruction.
   3. Fallback if TeX unavailable: run ONLY the non-TeX half (fixture-producer
      mapping by Explore + Python `jsonschema`/`pypdf` checks already present)
      and return `NOT_READY (toolchain-blocked)` with measured missing-tool
      evidence — do NOT fake a PDF or weaken log gates.

B. Explicitly NOT proposed now: global `apt install texlive-full`, sudo,
   workspace `.git` mutation, Production network fetch, reusing old
   `/tmp/jgas-*` runners, creating fixture SOURCE commits (permitted later ONLY
   in an independently isolated fixture DB after root selects execution).

Suggested next execution command set (for root to approve, NOT run now):
- Re-verify dest identity via existing script `--dest` (already green for
  isolation; re-run at execution time for freshness).
- Fixture generation (Explore-owned producer map) → disposable build dirs
  `build-weekly-<issue>/`, `build-special-<issue>/` OUTSIDE the source copy,
  aux closed there; `latexmk -lualatex` per `.latexmkrc`; capture `main.pdf`,
  `main.log`, `sha256`, page count, audit JSON verbatim per workflows;
  transfer ONLY the explicit sets with ownership; run strict receipt/Gate/QA/
  Candidate/State readback on the SAME source identity; record
  semantic/visual vs type-fixture separation.

## 7. Paths to source copy / evidence (this preparation unit)

- Source (read-only, unmodified): 
  `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60`
- New analysis/execution copy (independent bytes, inert, full separation OK):
  `/tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60`
  container: `/tmp/opencode/jgas-initial-build-20261019T132209Z/`
- Packet: `notes/rephase-1-initial-build-integration/`
  - `prepare_verify_20261019T132209Z.py` (new script, before-execution save)
  - `evidence-20261019T132209Z/prepare_before_stdout.txt` (`2e1ec5c7…`, 157L),
    `prepare_before_stderr.txt` (empty), `prepare_before_exit.txt` (`0`)
  - `evidence-20261019T132209Z/copy_stdout.txt` (0B), `copy_stderr.txt` (0B),
    `copy_exit.txt` (`0`)
  - `evidence-20261019T132209Z/prepare_after_stdout.txt` (`f0ab8bc9…`, 183L),
    `prepare_after_stderr.txt` (empty), `prepare_after_exit.txt` (`0`)
  - `evidence-20261019T132209Z/commands.log` (raw command/cwd/exit record)
  - `README.md` (this file)
- Reference pins: `notes/rephase-1-dm021-p3s/draft-history-r11/static21.json`
  (`1c0e339c…`, 3670B); workflows/style/requirements listed in §5.

## 8. STOP — awaiting ROOT execution selection

Preparation complete. No PDF was built, no test was run, no fixture was
generated, no commit was created. Next step needs explicit root choice of setup
path A1/A2/A3 (container vs user-space TeXLive vs toolchain-blocked NOT_READY)
before any build/fixture work starts. This packet is author-side preparation,
not an independent review PASS.

## 9. Correction appendix — root selection 2026-10-19 (original §§1–8 preserved above)

Per `astra-execution-selection.md` §§6–7, 16–21 (this appendix supersedes only
the wording noted; original preparation text is NOT edited away):

- Generated-route build inputs are the **generated trio**
  `main.tex / references.bib / jgaisurvey.sty` plus the declared build recipe /
  toolchain in an isolated disposable directory. Legacy
  `weekly-final-main.tex.in` and its `sections/` tree (cited in preparation §5
  as template context) are NOT the generated-route inputs.
- Canonical survey-root transfer set is exactly
  `main.pdf, main.log, main.pdf.sha256` (3 source + 3 allowed outputs).
  A Special build audit JSON (`special-pdf-build-audit.json`) is
  **evidence-packet-only, never copied into the closed survey_root**.
  Preparation §5–6 wording that listed audit JSON alongside the transfer set /
  implied legacy `sections/` inputs is corrected to the above.
- Preparation-phase `NO_NETWORK` / preparation-only statements described that
  phase only. This toolchain unit's official TeX/CTAN downloads were separately
  authorized (selection §2); origin/version/digest/closure/failures recorded in
  `evidence-toolchain-20261019T133205Z/` (attempts 1–4 preserved, no overwrites).
- Existing Python 3.14.4 + `jsonschema 4.23.0` / `pypdf 6.16.2` are local runtime,
  not workflow Python 3.12 parity. `pdftoppm`/`pdftotext` + `python3 -m pip`
  cover inspection/setup; ImageMagick/qpdf/pip3-binary/Docker absence are not
  blockers per selection §16.
- Toolchain result (A2 user-space, attempt 4 exit 0): TeX Live 2026
  (LuaHBTeX 1.24.0, latexmk 4.88, biber 2.22, kpathsea 6.4.2) under
  `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive` (+ texmf-home/var/config
  scoped under same toolroot); all required `.cls/.sty` + HaranoAji OTF resolve
  via `kpsewhich` (22/22, `references.bib` excluded as route-generated).
  Exact caller env/argv in attempt-4 `STEP 33`. No production build run;
  no source-copy writes; no commit.
