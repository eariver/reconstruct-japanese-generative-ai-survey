# Independent implementation review — DM-001/019 only (candidate 490414c)

2026-10-03. Fresh author-independent reviewer for DM-001/019 only.
Did not author design/code/tests. No agents spawned. No code/test
execution, fixture writes, network, checkout, ref or config mutation.
All Git inspection read-only with
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`,
no root overrides, no alternates/object sharing. Read `AGENTS.md`,
`notes/rephase-1-dm001-019-implementation/implementation-task.md`,
`design/astra-selection.md` + `design/corrected-plan.md` (initial
`design/design.md` rejected alternatives stay historical, not authority),
exact candidate diff, test oracle/fixture validity, parent witnesses,
exact-head raws at
`notes/rephase-1-dm001-019-implementation/evidence-impl-20261003T100801Z/`,
`implementation-report.md`. No actual probes executed; failing tests
below are source-grounded proposals only. Source/evidence never edited.
Review fixes initially only candidate
`490414cef5be71d3b373171d8abeb0674b1f1c71`. Worker corrections (if any)
belong in a separate new candidate. No whole-candidate adoption.

## 1. Candidate and scope binding

- Candidate **`490414cef5be71d3b373171d8abeb0674b1f1c71`**,
  tree **`f5009749e1b2bcd49b35c5c4320ec76f4c3568a6`**,
  direct parent **`b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`**
  (verified `log --format='%H %P'`, `rev-parse HEAD^{tree}`,
  `status --porcelain=v1 --untracked-files=no` empty in
  `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z`,
  branch `codex/dm001019-freeze-implementation`).
- Changed paths (only 3, `diff --stat b40..490`):
  `scripts/survey_publication_v2.py` (blob `12f22e87…`, 515-line delta),
  `scripts/survey_profiled_freeze_v2.py` (blob `8d218aa9…`),
  new `tests/test_survey_dm001_019_freeze_equivalence_v2.py`
  (blob `03cc6f9e…`, 1316 lines).
  No schema/stage/workflow/config/other-producer edits — within
  `implementation-task.md` allowance.
- Public `build_freeze(repo,cand,appr,frozen_at,freeze,manifest)`
  signature byte-identical parent→candidate (parent
  `survey_publication_v2.py:330`, candidate `:766`; verified via
  `git show` both). No caller tag/slug/Profile override added. Good.
- Old two-string `publication.release_identity(str,str)` retained at
  candidate `survey_publication_v2.py:507-512`; `grep release_identity`
  confirms no builder calls it — both builders use
  `profile_release_identity(prep["profile"])` (publication `:777`,
  profiled `:74`). Good.
- Legacy `validate_visual_review` retained at publication `:755-763`
  but no Freeze path calls it; `prepare_freeze_inputs` (`:174-228`)
  uses `reader.validate_review_record(..., expected_kind="VISUAL")`
  on the Candidate-bound path. Wrapper drops legacy `visual_path`
  (profiled diff `-visual_path = .../visual-review-v2.json`,
  `-validate_visual_review`). Good.

## 2. What is genuinely correct (bounded)

- **Both builders visual/exact-Candidate/Profile-slug truth:**
  `prepare_freeze_inputs` validates Candidate, typed approval,
  exact approval→Candidate path+hash (`:186-190`), Candidate-bound
  pre-preview VISUAL (`:191-196`), PDF chain (`:197-198`),
  bundle→Profile resolution with issue/publication-identity checks
  (`:199-209`). Both `build_freeze` (`:766-810`) and
  `build_profiled_freeze` (profiled `:64-109`) funnel through it;
  both derive `release_tag` from the same `prep["profile"]` via the
  single authority `public_issue_slug_from_profile` /
  `profile_release_identity` (publication `:83-106`), profiled
  `:23-30` pure delegating shims. No convergence gate, no scanning.
  Matches Astra items 1-3.
- **Real State/wrapper interlock:** profiled `:56-72` keeps real
  `_safe_state_profile` (`validate_agent_state`, `RELEASE_CANDIDATE`,
  approved Preview, current-Profile SHA), approval-drift gate
  (`:60-62`), State-issue checks (`:66-69`), bundle≡State-current
  check via `prep["profile_ref"] != expected_profile` (`:70-72`).
  No `_safe_state_profile`/`validate_agent_state` mocks in the new
  suite (only `mock.patch.object(os,"write"/"open")` at the real
  write boundary, lines 1019/1035/1219 — explicitly allowed).
  Negatives W4/W5 prove the gate (stale approval, profile drift,
  lifecycle, pending Preview). Good.
- **Serialization retry:** `_existing_compatible_bytes`
  (publication `:147-171`) preserves existing equal-payload bytes
  (lstat symlink/nonregular refusal, JSON-dict equality, return
  existing bytes); `preflight_freeze_pair` (`:355-360`) hashes the
  preserved bytes (`sha256_bytes`) so Manifest embeds the true
  on-disk Freeze SHA. L7 idempotent retry passes. Good.
- **Bounded writer core:** `O_CREAT|O_EXCL|O_NOFOLLOW` + write loop
  + fstat-owned identity + known-prefix-partial cleanup
  (`:420-473`), completed-Freeze-retained on Manifest failure
  (`:476-504`), foreign residuals never deleted, post-install byte
  rechecks. L8b (mid-`os.write` partial removed), L8c/W6
  (Manifest failure retains Freeze + identical retry) genuinely
  exercise the boundary. Good.
- **Real extracted workflow predicate + Weekly/Special
  convergent+divergent:** `_extract_workflow_predicate`
  (test `:685-699`) fail-closed extracts the pinned
  `release.yml` Python block (step-anchor/heredoc/head/identity
  asserts), `_run_workflow_predicate` (`:702-724`) executes it
  locally with `cwd=repo`, scrubbed env, synthetic files only.
  S2 runs Weekly (`weekly/2026-W35`) + Special convergent
  (`special/SP001`) + divergent (`special/SP002-DIVERGED`) to exit 0
  with exact `tag=...` stdout; parent W3 proves the predicate
  rejects old issue-based bytes (`SP002 != SP002-DIVERGED`, exit 1).
  L2 (wrapper-first→reset→canonical) + W3b (canonical-first→
  reset→wrapper) give both-order byte equality with same
  `frozen_at`. Special fixtures use real validators
  (no stubs). Good.
- **Parent witnesses honest:** W1a legacy load/type refusal (no
  files), W1b late `validate_release_manifest:408-409` refusal WITH
  Freeze+Manifest residuals recorded, W2 lower-level mixed-Candidate
  same-PDF ACCEPTED (both outputs), W4 divergent-Manifest conflict
  with Freeze residual + Manifest unchanged, W3 convergent exit 0 /
  divergent exit 1. `witness_parent.py` asserts
  `HEAD==b40` and prints `HEAD_AFTER=b40`; harness outside control
  roots as allowed. Wrapper-mixed-State early refusal honestly
  recorded as shared-prepare coverage instead of a false
  wrapper-PDF-gap claim. Good.

Verdict on these rows: BOUNDED_PASS within DM-001/019 scope. They do
not transfer to whole-candidate adoption, all-profile/application,
DM-003/004/016/017/018/020, build-transfer or findings transport.

## 3. Findings — actionable, severity-graded, cited-line

### F1 [HIGH] Nested output destinations bypass predictable preflight
- **Where:** `preflight_freeze_pair` equality-only check
  publication `:313-316` (`if norm_freeze == norm_manifest`);
  `_check_output_ancestors` early-return `:136-138`
  (`except FileNotFoundError: return`);
  `install_freeze_pair` `:487-498` (`_ensure_parent_dir` for Manifest
  outside the retained-for-retry wrapper).
- **Defect:** No output-output ancestry check. If one target nests
  under the other (e.g. `freeze=…/freeze.json`,
  `manifest=…/freeze.json/nested.json`, or reverse), preflight
  passes when both are absent (missing ancestor returns early),
  installs Freeze, then fails unpredictably at Manifest parent
  setup with a bare `ancestor is not a directory` / `EISDIR` /
  `ENOTDIR` OSError — not the documented full pre-write
  `ValueError` with neither target touched. Freeze residual is left
  in an unresumable nested layout (retry now fails preflight because
  the Freeze file blocks the Manifest parent). Violates
  task "full exact-byte Freeze/Manifest preflight before write,
  including … target parent/type/conflict hazards" and selection
  item 6 ("check both output parent chains, including non-directory
  components, before installation").
- **Proposed source-grounded failing test (no probe run):**
  `test_nested_outputs_rejected_pre_write`: build valid Weekly
  prep/payload as in L6, call
  `publication.build_freeze(t.root,c1,approval1,t.now, pub/"freeze.json",
  pub/"freeze.json"/"manifest.json")` (and the reverse nesting);
  assert `ValueError` matching `must differ|ancestor|nested` AND
  `assertFalse(freeze.exists()) and assertFalse(manifest.exists())`
  / no parent directory created. Current code installs Freeze then
  raises outside preflight — test fails.
- **Fix:** In preflight after lexical normalization, reject if
  `norm_freeze in norm_manifest.parents or norm_manifest in
  norm_freeze.parents` (plus equivalent `parents` including the
  file itself already covered by equality). Must precede any write
  / `mkdir`.

### F2 [MEDIUM] `FileExistsError` race path skips type/symlink revalidation
- **Where:** `_install_owned_json` publication `:429-436`.
- **Defect:** On `FileExistsError` the handler does
  `path.read_bytes()` directly — no `lstat`/`S_ISREG`/`S_ISLNK`
  revalidation mirroring preflight (`:160-163`). A symlink/FIFO
  swapped in between `os.open` failure and `read_bytes` would be
  followed (symlink with identical bytes falsely resumes as success;
  FIFO blocks). Violates selection item 7 ("race to an existing
  target must revalidate safe type/path and exact compatible content
  or refuse"). Pre-existing symlink at `os.open` time happens to
  fail closed via `ELOOP→OSError` (not `FileExistsError`), so the
  window is narrow TOCTOU — still a contract gap. Root's
  "race/FileExists + symlink handling" concern confirmed.
- **Proposed test:** Direct `_install_owned_json` unit: plant
  symlink `link→real` where `real` holds `data`; call
  `_install_owned_json(link, data, …)` after forcing the
  `FileExistsError` branch (e.g. mock `os.open` to raise
  `FileExistsError` with `link` now a symlink); assert symlink
  refusal. Current code `read_bytes`-follows and returns success.
  Alternatively assert `lstat`-first in code review.
- **Fix:** In the `FileExistsError` branch, `os.lstat`, reject
  symlink/nonregular before `read_bytes` (same messages as
  preflight), then compare bytes.

### F3 [MEDIUM] `os.close` failure with landed bytes silently returns success
- **Where:** publication `:461-473` (`except OSError … landed ==
  data: return`).
- **Defect:** A close-time I/O error is swallowed when post-close
  bytes happen to match. POSIX close errors can signal writeback
  failure; hiding them misreports durability. Selection item 8
  requires distinct tested `close` outcome — L8 covers pre-open
  (chmod), mid-write (`os.write` fault), Manifest-install
  (`os.open` fault) but no close fault. Untested + incorrect
  success path.
- **Proposed test:** `mock.patch.object(os,"close",side_effect=OSError("injected close"))`
  around `build_freeze` with otherwise valid inputs; assert
  `ValueError` (fail-closed, Freeze retained-or-explicit), not
  silent success. Current code returns normally when
  `landed==data`.
- **Fix:** Propagate close failure as `ValueError` (retained-Freeze
  semantics for Manifest-close; owned-partial policy for
  Freeze-close) — never bare `return` on `close` exception.

### F4 [LOW-MEDIUM] PDF authority omitted from input-alias set
- **Where:** `preflight_freeze_pair` `:322-332` (`authority_raw`
  lists `reader_manuscript/source/quality_bundle/semantic_review/
  visual_review` + candidate/approval/visual/bundle/profile — no
  `candidate["pdf"]["path"]`).
- **Defect:** Freeze/Manifest target overlapping the bound PDF file
  (same spelling or hardlink) is not flagged as
  `overlaps a Freeze authority input` / `hardlinked to a Freeze
  authority input`; it only fails later as generic
  `refusing to overwrite divergent …` (fail-closed by luck, since
  PDF bytes never equal Freeze JSON). Error provenance wrong;
  hardlink-identity set incomplete. Selection item 6 claims
  "target≡input incl. hardlink".
- **Proposed test:** `attempt(pdf_path_as_freeze, manifest)` with
  valid prep; assert `overlaps a Freeze authority input`. Current
  code yields `refusing to overwrite divergent Freeze record`.
- **Fix:** Add `repo_root / candidate["pdf"]["path"]` (and its
  `os.stat` identity) to `authority_raw`. Consider State file for
  the wrapper path (shared helper lacks `state_path`; at minimum
  document the wrapper-fixed-path limitation).

### F5 [LOW] Duplicate `_write_immutable` definition
- **Where:** publication `:65-71` and `:74-80`, byte-identical.
- **Defect:** Second definition shadows the first. No functional
  divergence today (Freeze path no longer uses it; Candidate/
  approval/visual/merge/release producers use the survivor), but
  dead duplication signals missed lint/review and risks future
  divergence if one copy is edited. Root-spotted; independently
  confirmed.
- **Fix:** Delete one copy (keep single `_write_immutable`);
  `git diff --check`-clean + existing 8+4 publication/profiled
  tests re-run at the new HEAD.

### F6 [LOW] (Advisory, not must-fix for this unit) Parent-dir `mkdir` TOCTOU
- **Where:** `_ensure_parent_dir` `:382-384`
  (`_check_output_ancestors` then `mkdir(parents=True,exist_ok=True)`
  with symlink-following semantics, no post-`mkdir` revalidation).
- **Note:** Concurrent symlink planted between check and `mkdir`
  could escape `repo_root`. Task explicitly requires "no mandatory
  cross-process framework" — treat as disclosed limitation, not a
  CHANGES_REQUIRED driver, unless F1's fix already re-touches this
  area. Do not claim crash-atomicity (already disclaimed).

## 4. Packaging — 7 new objects vs actual portable availability

- `50-packaging/successor-manifest.json:26-54` lists 7 new objects
  (`rev-list --objects parent..head`, independently re-verified):
  commit `490414c`, tree `f5009749…`, `scripts` tree, 2 runtime
  blobs, `tests` tree, 1 test blob.
- Actually portable in `50-packaging/`: `successor.patch`
  (101,721 B), `changed-files/` (3 file copies + SHA256 list),
  manifest JSON, `gen-manifest.py`, `apply-check.log`.
  **No bundle/pack/commit-object backup.** `apply --check` exit 0
  against pristine b40 (log shows 3 `Checking patch …` lines)
  proves patch applicability only — not exact-commit restoration.
- Consequence: offline recovery is
  parent-portable-snapshot (prerequisite, untouched) + patch apply +
  **re-commit with new author/committer time** → different commit
  SHA, not `490414c`. Trees/blobs rebuild identically only if
  content+mode identical, but commit identity cannot be preserved.
  The 7-object metadata is descriptive, not a backup. Report
  discloses "no full clone/bundle created" (`implementation-report.md:118-124`)
  — packaging must be labelled "patch-based successor delta,
  not exact-commit offline backup". Do not run old restore scripts
  or promisor-hydrating bundles to fill the gap.

## 5. Test/evidence scope, raw failures, limits

- New suite: **19/19 OK** at claimed `490414c` (182 s,
  `final-test_survey_dm001_019_freeze_equivalence_v2-stderr.log:1-24`).
  Affected same-HEAD: publication **8/8**, profiled **4/4**,
  freeze-stage-boundary **8/8** — total **39 methods, 0 skips**.
- Initial `new-module-run1-stderr.log:1-55` honestly preserves
  **2 failures + 1 error** (harness-oracle side: missing legacy
  schema copy in self-contained root; directory-target specificity
  prompting preflight reorder; stale-approval oracle naming the
  real drift gate). Correction deltas preserved, not reworded.
  No per-method HEAD pinning claimed (report `:106-107`).
- **Evidence gap (limits verifiability, not code):**
  `30-tests/*-stdout.log` are all 0 B; stderr logs carry only
  unittest lines with no per-module `HEAD/tree/parent/clean-tracked`
  headers. `40-commit/commit-state.log` pins `490414c/f5009749…/b40`
  + clean status, and parent witness asserts/prints
  `HEAD==b40`/`HEAD_AFTER`, but new/affected runs lack in-log
  binding. Accept the reviewer's independent `rev-parse`/`status`
  re-verification above as the binding for this review; future
  units should emit `rev-parse HEAD^{tree} + status --porcelain`
  headers into each test log dir per `implementation-task.md:18`.
- **Portability limit:** L8a read-only-dir refusal assumes
  non-root (uid 1000 disclosed at report `:107`). Running as root
  would bypass `chmod 555`. Disclosed; consider fault-injection
  pre-open instead of permission bits for root-proofing.
- **Coverage note:** Legacy-presence-irrelevance post-repair
  (extra valid legacy file alongside canonical VISUAL) is proven
  at parent (W1b) but not re-asserted as a repaired-code positive
  (new tests prove legacy-cannot-enter-Candidate at L3, not
  legacy-ignored-on-Freeze). Low gap; code path clearly ignores
  the hardcoded legacy path.
- Whole-candidate audit, seven-point audit, step 4/B3, DM-003/004/
  016/017/018/020, build-transfer, findings transport, Windows/
  Actions, all-profile/application remain out of scope and untested
  here by design.

## 6. Verdict

**CHANGES_REQUIRED** — DM-001/019 scope only, candidate `490414c`
only. Must-fix before any adoption claim for this unit:

1. F1 nested-output preflight (HIGH) + regression test.
2. F2 `FileExistsError` lstat revalidation (MEDIUM).
3. F3 close-error propagation + close-fault test (MEDIUM).
4. F4 PDF-path alias inclusion (LOW-MEDIUM, cheap).
5. F5 duplicate `_write_immutable` removal (LOW, trivial).

Advisory: F6 disclosure, per-module HEAD headers, L8a root-proofing,
legacy-irrelevance positive, packaging "delta not backup" label.

On correction, Worker returns a **separate new candidate** (new HEAD/
tree, fresh diff/oracle review); this review stays fixed to `490414c`
and must not be relabelled as approval of any successor. No
whole-candidate PASS, no Freeze/Release/State/production authority
inferred. Stop at this review; Astra synthesis + Human Commit Point
own the next decision.
