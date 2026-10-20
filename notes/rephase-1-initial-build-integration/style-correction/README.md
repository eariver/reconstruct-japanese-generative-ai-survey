# One-line shared-style correction — technicalnote title contrast — 20261019T135318Z

Selected by `astra-postbuild-disposition.md` §5 item 1 (FIX; items 2–4 deferred/retained).
Root directly read real rasters/source; this implements ONLY the justified line.

Tool disclosure: `apply_patch` absent in this environment. The `.sty` line was
applied with the dedicated `Edit` editor (not shell); docs here with `Write`.
No historical runners, no test/rebuild/authority in this unit.

## Candidate (NEW independent copy, no commit)

- Location: `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`
- Byte copy (`cp -a`, no hardlinks) of current exact409+21 analysis source
  `/tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60`.
  Original/copy and both existing fixtures untouched (their heads/status verified unchanged).
- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` (detached), tree `8ce36998…` (uncommitted).
- Status22 `4M18A22`: 3 inherited modified + 18 inherited untracked (21/21 bytes
  re-verified vs static21 `1c0e339c…` BEFORE edit) + 1 new modified style line.
- Independence: `.git` 83 files, `dev:ino` overlap 0 vs source copy and 0 vs
  reconstruct DB; worktree style file not hardlinked; no `objects/info/alternates`;
  local config inert origin only; no inherited `GIT_*` overrides at execution.

## One-line diff (actual)

`templates/survey/jgaisurvey.sty` `technicalnote` env (line ~182), dark title on
same gray background/frame/layout; all other box styles/renderer semantics kept:

```diff
   colback=white,
   colframe=SurveyRule,
+  coltitle=SurveyInk,
   boxrule=0.6pt,
```

Full patch: `style-coltitle-fix.patch`. Full 22-path manifest: `final22-manifest.json`.

## Before/after hashes (style file)

- Before: sha256 `3b6d15627439b35a352d692c8c5f9c2ac25dd02968e75beb30a69b8c8f53e5cc`, 6547 B
- After: sha256 `035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec`, 6569 B
- `SurveyInk` (#17202A, line 29) already defined and used for cover headline; `SurveyRule`
  (#D5D8DC, line 32) unchanged. No other file touched.

## Status

No candidate commit (HEAD still 409), no tests/rebuild/new authority — awaiting root
code review of this diff. Next implementation recipe (short, concrete) follows in the
closeout reply: two fresh final22 fixtures → actual build/transfer → measured QA +
distinctly synthetic semantic/visual → real Gate/Candidate/Preview/Freeze/Release APIs + negatives.
