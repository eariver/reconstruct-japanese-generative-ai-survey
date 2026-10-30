# Author-A path-normalization return — DM022 pre-Architecture (A4 follow-up)

2026-10-28. Owner A (research operation). Binding: contract a345bb95 INCLUDING
§11, pre-code ROOT FULL `0425c530…`, R4 + literal schemas / R5 / R6, R2 + A4
independent reviews, integration-a4 diagnostics, and astra
`a4-regression-disposition.md` (§1 assigned to A). Human continuation authorized
ACTUAL CODE in independent candidate-work ONLY. No ordinary candidate/reconstruct
Commit/Push; no fixtures in reconstruct; no git config/global writes; no
network/Production/reset/clean/old-log overwrites. Python 3.14.4 + unittest +
jsonschema 4.23.0/pypdf 6.16.2. Unit continues — NO Commit Point claimed here.

## 1. Assigned defect (A-owned only)

Integration-a4 C2-01/REG-03: C2 release/refresh callers pass repository-relative
**strings** (`_ref["path"]` straight from JSON) into LOW's public typed loader,
which called `.is_absolute()` on the raw parameter → `AttributeError: 'str'
object has no attribute 'is_absolute'` instead of the mapped FileNotFound/
wrong-family refusal. Same crash shape in `survey_release_checkpoint_v2.py:77`.

Fix (A files only; no B/C/schema/contract changes):

- `scripts/survey_research_authority_v2.py` (155892B, SHA256
  `2aef837faaa549b9eab3f1a03696b5a44ef63ff63316cad817842c2110554fb3`):
  new private `_norm_path(value, label)` (`:92`, after `ResearchAuthorityError`)
  accepting exactly Path-or-non-empty-string, raising the typed error otherwise
  — never a bare `AttributeError`, never a silent misresolution (`""` →
  `Path(".")` is refused, not coerced). Applied consistently at every public
  path-taking entry: `load_typed_checkpoint_record` (`:310`, the reported crash
  site — coerce BEFORE `.is_absolute()`), `resolve_research_authority`,
  `load_revision_request`, `derive_before_context`, all builders/prove/checker
  path params, `require_completion_consistent`, `require_no_active_guard`,
  `guard_path_for`, `lstat_slot`, `_load_json_from_sized`,
  `_verify_sized_ref_bytes`, `_discover_repo_root_from_source`,
  `_verify_adopted_graph_full`, `_verify_completion_full`,
  `_verify_own_epoch_commit`, `_validate_against_report_def`, `_git_read`.
  Repo containment (`_repo_rel`) and no-follow reads (`O_NOFOLLOW`,
  FD-vs-lstat identity) are unchanged downstream of normalization.
- `scripts/survey_prearchitecture_acceptance_v2.py` (88603B, SHA256
  `f8af03cc5d58af1057ea26d9cef0eb87b1fd71118ddf63a2186e24da9bc1e751`):
  same file-local helper (`:50`, mirrors LOW wording) applied at every public
  entry (`prepare`, `adopt`, `resume`, `readback`, `claim_guard`,
  `verify_live_eligibility`, `_profile_and_source`, `_current_head_tree`,
  `_revision_root_for`, bound-context step oracles). No behavior change for
  valid inputs; invalid inputs now fail typed instead of `TypeError`/silent
  misresolution.
- `tests/test_dm022_prearchitecture_acceptance_v2.py` (80610B, SHA256
  `a08265175a1ea697cdf2fa8716cc2b53708ddf586de1a721505b76bc63b3f5e4`):
  two new unittest cases (no pytest): `test_loader_accepts_str_path_same_as_path`
  (`:630`, str vs Path on the same adopted PREARCH checkpoint → identical
  `{family, record}`, plus `resolve_research_authority` with a str state path
  and `check_supersession` with all-str paths) and
  `test_loader_wrong_family_str_path` (`:656`, legacy str path → LEGACY, never
  PREARCH; unknown-kind str → typed refusal, not AttributeError). The 4
  human-window tests (`:1104`–`:1168`, prior unit) are intact.

Public API is unchanged (same names, same shapes; `str` accepted at runtime
where a path was already documented); only the crash-on-str is fixed, plus typed
rejection of empty/non-path inputs. B's call sites need no adaptation.

## 2. Real scope actually executed (not claim-only)

Fresh private copy `/tmp/dm022-a5p-priv` = current idle candidate worktree
(765 intended files excl. `.git`/caches; rebuilt AFTER all A edits via rm -rf
+ full copy, pycache purged) + independent `.git` byte-copy from frozen A4
`git-independent` (83 files, 0 symlinks, 0 inode overlap, inert origin, HEAD
`409b292…`). All 5 A-owned files priv == candidate-work (LOW/HIGH/test above;
evidence helper `8b55dc6c3289…` + fixtures `7fdc692ccba6…` byte-identical to
snapshot). B/C/C1/C2 files carried byte-identical from the idle candidate,
untouched by A (B SizedRef Path-wrap + C2 schema-fixture fixes present as
idle-candidate state). No saved runners; no shared-candidate tests; fixture Git
DBs were independent temp dirs per test.

- Targeted (recorded raw `dm022-a5-path-targeted-raw.txt`, 77 lines, 3381B,
  SHA256 `7213b03deb2cacf460b90c1a5a4f5f255eb6216578b31c33dd57811823a74de6`,
  exit 0): **4/4 PASS** — 2 new loader tests (A-scoped proof: LOW called
  directly with `str`, no B wrap involved); release
  `test_cli_main_success_and_error` PASS (REG-03 AttributeError gone: the exact
  `survey_release_checkpoint_v2.py:77` str call now normalizes and the CLI
  completes `main == 0` plus the expected already-RELEASED refusal); C2 refresh
  `test_weekly_refresh_validation_healthy_legacy_accepts_whole_path` PASS
  end-to-end. That C2 green is a three-part combination, attributed precisely:
  B wraps the call site in `Path()` + C2's fixture now copies `schemas/` into
  the temp repo root + A normalization accepts str at the public contract. No
  single component is over-claimed: without A, a direct-str caller still crashed
  (proven by the loader tests); without C2's fixture fix, the run reached a
  typed schema-missing refusal instead (observed on the stale A4 fixture).
- Full A suite (recorded raw `dm022-a5-full-20261028.txt`, 49 lines, 5357B,
  SHA256 `d77d5776a5e942ab8b74509c4e7611461cfeadbe9b8cbbeb696ae1fa43578e0d`,
  exit 0): **25/25 PASS in ~26s** — all 23 carried positives plus the 2 new
  loader tests, proving the shared-entry normalization broke no existing
  prepare/adopt/resume/readback/checker path.
- Supersedes: an earlier draft of this return described the stale
  `/tmp/dm022-a4p-path` run (exit 1, 3 PASS + 1 C2-fixture-owned ERROR, 21 tests,
  old SHAs). That run is superseded by the two final raws above; its draft
  numbers are withdrawn, not preserved as alternate evidence.

## 3. Explicit non-scope (no weakening, no bypass)

- Missing-State READY is NOT weakened to green legacy tests.
  `require_no_active_guard` still refuses unreadable guard paths;
  missing/unparseable State still refuses (covered:
  `test_unreadable_paths_fail_closed_not_coerced`, `test_interrupted_*`,
  `test_unknown_live_resume_indeterminate`).
- C2-02 (finalize guard ordering / MISSING_ANCESTOR) is C2-owned; untouched.
- No unmapped dependency was added (only stdlib `jsonschema` function-local use
  already present in A4 for the report $defs check, plus `subprocess` for
  read-only git object reads).

## 4. Files for root freeze / next steps

A-owned writes this unit: the 2 normalized modules + the A test file (plus
evidence packet `evidence/A4-path-normalization-20261028T164439Z/` with both
final raws, `private-source-manifest.json` (765 files, SHA256
`f5fa1269e932598aa2899bdfaff35146ada5066ca98b49f172f00e3ec82a99cb`),
`a-binding.json`, `a4-path-raw-binding.md`, and this return). Root may now bind
the next frozen snapshot and run the remaining affected suites (P1/P2R/P2V/P3S/
renewal, later lifecycle witness, independent review). Whole NOT_READY/step4B3
OPEN/audit unstarted/DM021+022 OPEN preserved. No implementation acceptance
claimed. Ordinary Commit/Push Human-owned.
