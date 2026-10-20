# Final22 two-route build → transfer → public admission + scoped negatives — 20261019T135318Z

Executes `astra-postbuild-disposition.md` on the root-approved one-line style fix
(`coltitle=SurveyInk`, style sha `035645ca…6569`). Root reviewed the actual patch
before this run. No new candidate source changes were made; two real blockers hit
were fixture-only harness bugs (fixed with unique namespaces + archived faulty bytes).

Tool disclosure: `apply_patch` absent. All code edits via dedicated `Edit`; docs via
`Write`. Two mechanical multi-occurrence patches used `python3` heredocs in bash
(review-evidence mapping fix, str(EVIDENCE) cwd fix) — deviation preserved here,
not repeated. No historical runners reused. `PYTHONDONTWRITEBYTECODE=1` everywhere;
no `__pycache__` in fixtures/notes (verified). `git clean -fdx` was used once for a
fixture reset (only generated `*.log`/untracked outputs removed; SOURCE commits intact).

Independent pre/postbuild inspections are PRESERVED and NOT converted to PASS:
fixture-fidelity OK for renderer observation; **production semantic NO-GO both routes**.
All synthetic PASS records are explicitly labelled TYPE-FIXTURE and point at the
NO-GO findings; no genuine reviewer PASS, no Human approval, no adoption.

## 0. Inputs (all read-only, verified unchanged at closeout)

- Final22 candidate `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`:
  HEAD `409b292…` (detached), status `4M18A22`, style sha `035645ca…` 6569 B — unchanged.
- Original21 fixtures/builds under `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z` and
  `jgas-initial-builds-20261019T134223Z` untouched (heads `88813a01…`/`d4078d1b…`, build dirs kept).
- Toolchain TL2026 reused as-is (LuaHBTeX 1.24.0, latexmk 4.88, biber 2.22); no reinstall.
- NEW fixtures (git init, no `.git` copy): `jgas-final22-fixtures-20261019T135318Z/weekly-final22`
  SOURCE `51b0e42b…`, `special-final22` SOURCE `9917a6ff…` — meaningful SOURCE commits
  before authority (synthetic snapshot ancestry, not candidate commits). 22/22 pins,
  `.git` dev:ino overlap 0 vs all other DBs, no alternates/hardlinks, safe local config.
- NEW builds under `jgas-final22-builds-20261019T135318Z/`, NEW evidence in this dir.

## 1. Positive flow — both routes RELEASED (74 exact operations: 36 weekly + 38 special)

Per route: accepted chain → DRAFT_COMPLETE → synthetic type-only pretex review →
actual pass2 CLI → disposable-build latexmk (SOURCE_DATE_EPOCH = fixture SOURCE ct;
Weekly +FORCE_SOURCE_DATE=1) → workflow log gates → 3-file transfer (absent-exclusive,
pre/post sha) → exact manuscript (actual coverage/requirements + actual source
locations) → Gate build+validate → receipt replays → deterministic QA → synthetic
postrender reviews → advance DRAFT_COMPLETE+7 → VALIDATED_DRAFT (+inherited gate site)
→ Candidate → RELEASE_CANDIDATE → synthetic Preview approval → profiled Freeze →
FROZEN (+readbacks) → merge verification + release record + checkpoint → RELEASED
(+readbacks). Ghost-state probe is a negative (N8), not run on positives.

| route | fixture HEAD | pass2 | build (exit/dur) | log gate / pages | transfer | QA genuine / synthetic | receipt+gate readbacks |
|---|---|---|---|---|---|---|---|
| Weekly 2026-W37 | `51b0e42b…` | exit 0 (8.7 s) | exit 0, 21.0 s, epoch 1792416843 | PASS, **5 pp**, 0 blocking | 3/3 OK | 3/3 genuine, 0 synthetic rows | PASS at post-manuscript, VALIDATED_DRAFT, FROZEN, RELEASED |
| Special SP001 | `9917a6ff…` | exit 0 (9.3 s) | exit 0, 23.9 s, epoch 1792416844 | PASS, **5 pp**, 0 blocking/layout | 3/3 OK | 4/4 genuine, 0 synthetic rows | PASS + surface-equality readbacks at FROZEN/RELEASED |

PDFs (real compiler only): weekly `899f0f2a…` 61151 B / log 92948 B;
special `71a2c98a…` 79156 B / log ~94 kB. Digests conventional `"<sha>  main.pdf"`.
(Special pdf sha differs from the attempt4 staging value by trailer /ID randomness
across rebuilds only; content identical. Weekly surfaces byte-identical to original21
(`136c0dd8…`); special surfaces byte-identical too (`f40db7f6…957cd5`) — the single
"drift" note in `special-surface-compare-attempt6.json` was an operator pin typo,
corrected by `special-surface-compare-correction.json`; both files re-hashed equal.)

Surface bytes identical on BOTH routes despite new fixture identities (all basis
material is content-addressed, not identity-addressed) — explanation recorded.

QA (all genuinely evaluated, none synthetic): pypdf page parse (5, not hardcoded 1)
+ sha/bytes + workflow log regex; identifier presence in main.tex bytes AND pdftotext
output (`2026-W37`/`SP001`, `Target Model`); subject binding via publisher result
cross-checked vs surface bibliography (weekly) / draft evidence cards (special,
bounded single-DID comparison, no fabricated metric); wrapper parse (1 weekly /
5 special nonempty environments). `quality.build_bundle` with actual checks.

Manuscript/Gate/Candidate/Preview/Freeze/Release all via actual public builders with
strict replays at each boundary. Preview approval identity is explicitly synthetic
type-fixture. Evidence packet: `weekly-main.pdf/log/pdf.sha256`, `special-main-attempt6.*`,
extracted texts, `weekly-page-1..5.png`, `special-page-attempt6-1..5.png` (150 dpi,
real-compiler PDFs only; build dirs preserved).

## 2. Negatives — 25 on NEW byte-independent copies (exact oracles, repairs verified)

Copies via `cp -a` per negative with zero `.git` inode overlap vs positives; snapshots
before vs fault-present after; no validator/Git mocks; transfer/build failure injection
via disclosed witness harness only. Honest preemptions recorded (layered validators
fire in order; the first exact refusal wins, deeper oracles reached by precise faults).

- N1 undeclared input: `contains undeclared entry: extra.sty` (build-dir + receipt paths); repair → PASS.
- N2a source tamper at RELEASED: state-derivation guard preempts —
  `Production State invalid for Weekly derivation: … validated-source …` /
  `Production State invalid for Longform readback: … validated-source …` (route-specific entry points).
- N2b receipt tamper (envelope digest recomputed): `Weekly/Longform deterministic primary replay mismatch`. (Naive tamper refused earlier at `… source receipt digest mismatch` — preserved.)
- N3a pdf swap: bundle refuses first — `quality review pdf bytes drifted after validation` (+ State observation recorded).
- N3c candidate binding rewritten to other-route bytes: `Publication Candidate PDF authority diverges from coupled quality bundle`. (Rebound-bundle variant preempted at `Publication Candidate quality bundle bytes drifted` — preserved.)
- N3b zeroed digest: harness postread `REFUSE (mismatch)`; State/bundle/candidate shas unchanged.
- N4a decoy manuscript at gate: `MANUSCRIPT_MANIFEST does not bind the exact expected Reader Manuscript`.
- N4b coverage-dropped decoy at candidate build: `Reader Architecture coverage mismatch`.
- N5a stale surface vs pretex review: `Reviewed surface bytes drifted for …` (recorded, not the expected-sha variant).
- N5b stale source vs postrender review+gate: `Reader primary source authority drift` (manuscript semantics preempts review-source check — documented) + `Reader-Surface Gate scanned surface bytes drifted`.
- N6 failing build (undefined command before `\end{document}`): engine exit≠0, no transfer (destinations absent), State unchanged; repair → rebuild content-identical (extracted text + 5 pages equal; trailer /ID differs — random per run, documented) + transfer/postread OK. (First fault placed after `\end{document}` passed silently — preserved lesson.)
- N7 partial transfer (staged log chmod 000, expectations pre-computed): `REFUSE PermissionError` after exactly one write (`partial_set=[main.pdf]`); State/QA/admission shas unchanged; no new files; repair → transfer OK, postread equal. (Naive shared-function call refuses pre-write via pre-read — documented.)
- N8 ghost COMPLETE state (special): `Production State invalid for Longform readback`; ghost removed, never referenced.

Per-negative raw stdout/stderr/exit + before/after snaps + repair controls saved
(`<route>-n<tag>-*.txt`, `negatives-part{1,2,3}[-<route>-done].json`). Initial
attempt deviations (wrong PYTHONPATH, review-evidence markers, readback archive path,
log-gate evidence mapping, N7 ordering) preserved as `worker_final22_route-faulty-v*.py`
and `*-preempted/bundle-preempted/manifest-preempted/envelope-preempted` raws.

## 3. Counts (operations, not test-method counts)

- Positive: 74 exact operations (36 weekly + 38 special), 2 pass2 CLI, 2 latexmk builds,
  2 log gates, 6 file transfers, 2 candidates, 2 profiled freezes, 2 releases, 10+ receipt/gate readbacks.
- Negatives: 25 refused-as-expected (12 part1 + 8 part2 + 5 part3) + 7 documented preemptions, all repaired with positive controls.
- Blockers: none remaining in this witness. No source bug found; no candidate modifications beyond the approved line.

## 4. STOP

Real post-fix visual check (not yet done — rasters above are the input), plus final
author-independent code/evidence resolution, remain required. No new content/research/
approval claims; no whole-project readiness inference. Ordinary commits/push and any
Production adoption stay Human-owned.
