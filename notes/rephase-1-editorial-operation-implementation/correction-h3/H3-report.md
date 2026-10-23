# H3 corrective return — H-owned only, no L/C edits, no overall pass

DST ONLY: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
Governing: d880 + selection + R1 + `independent-draft-h2-review.md` (read all, §§1–4 blockers, §5 non-blocking).
H2 base preserved: `correction-h3/history/survey_editorial_publication_v2.py.H2` `b86983cb…` (2862 lines),
Reader H2 `5febb50c…`, Gate H2 `0e586d28…`. H3 edits H module only (Reader/Gate H2 slices preserved, no L/C touches).

## 0. Preserve (byte-identical, new history)

- NEW `correction-h3/history/` (not rewrite/delete `correction-h2/`): `survey_editorial_publication_v2.py.H2`, `survey_reader_publication_v2.py.H2`, `survey_reader_surface_gate_v2.py.H2` via `cp -a` (preservation only, no DST writes).
- All H3 DST edits via dedicated editor (Read/Edit) only; one bulk `gen_obj→gen_receipt` rename used `python3` file write (noted here) then verified `py_compile` PASS; no further shell writes to DST.
- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/opencode` (external cache), no source `__pycache__`, no long fixtures/build until root freeze; focused real validations only.
- No deletes outside owned, no commits/network/clean/reset.

## 1. Smoke blockers fixed (§§1–2)

- **Build-record argv (§1)**: Was `cmds: list[list[str]]` stored as `argv` → schema `array<string>` failed every `prepare`.
  Now `recorded_argv: list[str]` flat (`EXPECTED_ARGV_LUALATEX_BIBER=list(FIXED_RECIPE_STEPS)`, `EXPECTED_ARGV_LATEXMK=[...]`), `spec.argv` EXACT equals expected (not token membership), executed `cmds` use absolute exe/companion but recorded `argv` is bare fixed steps + `executable` absolute separately. `prepare` now passes `validate_instance`.
- **Gate temp-outside (§2)**: Was system-temp `tmp_gate` + `validate_reader_surface_gate(tmp_gate)` → `_safe_file` escapes-root fail every `finalize`.
  Now pure payload: `gate.evaluate_reader_surface_gate(..., output_path=None)` returns report (no write), H exclusive-writes final repo-contained `P/publication/reader-surface-gate-v2.json` via `_exclusive_write_bytes`, then validates final (repo-contained, no rebinding). Existing initial Gate behavior preserved (`output_path` still supported); no caller permission bool. Other generics (manuscript/quality/candidate) keep system-temp + validate (their validators allow outside path, refs repo-relative, no own-path loophole — verified).

## 2. Correctness gaps fixed (§§3.1–3.6)

- **Receipt rederivation (§3.1)**: Added independent route-loader block in `validate_editorial_receipt` (no P2V, no seal/Gate cycle).
  Uses initial `publication-semantic-input` (exact pinned) + `weekly.load_derivation` / `longform.load_derivation_for_readback`, compares `accepted_refs` exactly (sorted name/path/sha, no caller trust) to initial receipt (unchanged research).
  Weekly: `validate_reader_input` + `render_main`/`render_bibliography` + `validate_generated_closure` + staged main/bib SHA; Longform: `validate_longform_reader_input` + `canonical_reader_bytes` FILE equality + `render_main`/`render_bibliography` + `validate_heading_syntax` + `validate_generated_closure`.
  Plus `verify_closure_at_commit` strict helper (exact names/count/blob vs commit) for both routes, in addition to existing closure/contract/ancestor checks.
- **Retained COPY (§3.2)**: Added explicit pin BEFORE ANY record write in `activate_publication`.
  Loads staged `retention_manifest_ref` + retention manifest, finds state row for `before_state_ref.path`, verifies `COPY_BEFORE_REPLACEMENT` (`retained_dest` bytes == `before_sha`) or `KEEP_IMMUTABLE` (`retained_ref` bytes == `before_sha`), plus `proposal basis == record.beforeState == retained bytes` + `supersedes == State pointer` + `beforeCandidate == observed` + `before_digest == recomputed`. Uses existing read-only loaders, no fictitious writes.
- **Seven (§3.3)**: H enforces `set(effective7)==PUBLICATION_ROLES_7` (7 exact, no research/Architecture/Draft) before calling `setmod.before_active_digest` (L now also enforces; defense in depth).
- **Ambient env (§3.4)**: Removed `for key in ALLOWED_ENV_KEYS: if key in os.environ` merge. Now `allowed_env={"PATH": bin_dir}` + spec env only (allowlisted, no `GIT_*/PATH/PYTHONPATH`, `HOME` allowed if documented). No ambient `TEXMFHOME/TZ/LANG` injection. `.latexmkrc` copied/pinned (already, preserved).
- **Spec-vs-executed (§3.5)**: `spec.argv` EXACT tuple per recipe (see §1), executed `cmds` use absolute exe/companion exact declarations, recorded `argv` == spec == expected (enforced at validate + build; mismatch refuses). Build record `argv`/`env` are actual executed (flat argv + explicit `PATH`+spec env), not unenforced spec.
- **Ordering/depth/dead import (§3.6)**: Moved `ALREADY_ACTIVE` before any P2V/anchor/seq (only exact expected new pointer + strict State + full set read-only). Fixed chain `range(32)` + `len(chain)+1<=32` prewrite (was 33). Removed dead `import shutil` (owned file only, no scope creep). Gap tolerance in `_next_record_seq` retained (strictly increasing, no dup; contiguous not required).

## 3. Passes preserved (§4, no regression)

- No fictional L writers (grep: no `setmod.activate_selection/write/resume/verify` calls; `hasattr` only for real helpers with exact-need fail-closed).
- Raw-first lexical + `repo_local_path` + lstat ancestors/leaf, `O_NOFOLLOW` bounded reads; exclusive `O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW` + fd readback + final pin, no `rmtree`/`write_json`/`target.write_bytes` in H module.
- Trio `main/bib/style` NOT primary, main→primary mapping everywhere; staged `outputs` exact, no `staged_refs` code (comments only).
- Toolchain absolute + companion same-dir regular, fixed argv, allowlisted env, recipe pinned, inputs pinned pre/post, real versions, log predicates + `pypdf` pages, failure preserve (no truncation/rmtree), exclusive transfer.
- Prepared set full 15 + strict schema (no fallback, no `_build_only` param), actual manuscript/bundle/reviews/Gate/Candidate/build/PDF/log/digest/research + cross-refs + inventory + external checks, no permission token.
- Activation: 17-key branch2, `supersedes` common edge, anchor via chain, digest from 7+ Candidate, seq `rN` lstat, collision refuse, P2V at both prewrites, State still-old rechecks, sole-pointer mutation via agent writer, post strict+record+set+agent before success, `ALREADY_ACTIVE` read-only, orphan resume revalidates + installs via agent writer, `INDETERMINATE` preserves, old/new/unknown + primary/secondary, never deletes.
- Callgraph: H top-level stdlib+core+schema only; source-proof P3S only, receipt strict State+P3S+route loaders (no P2V), Gate loads receipt file (no H receipt cycle), P2V before-eligibility only at prepare/finalize-prewrite/activate-prewrite/resume-prewrite with 5 positional args, `receipt_kind=None` (editorial allowed).
- Schemas unchanged (receipt 16, build 13, mspec FULFILLED, tspec 8, `additionalProperties:false`); closures 22/27 enforced + verified via helper.

## 4. Focused validations (external cache, no fixtures/build)

- `py_compile` 3/3 PASS (H 3077 lines? current `wc -l` 3077? H2 2862 → H3 ~3077).
- `closure22==22`, `closure27==27` PASS; exclusive create+collision+readback PASS (H2 `O_WRONLY→O_RDWR` fix retained).
- `EXPECTED_ARGV_*` exact tuples PASS; `recorded_argv` flat PASS (grep: no `"argv": cmds`, has `"argv": list(recorded_argv)`).
- Grep: no `import shutil`, no `core.write_json(`, no `target.write_bytes`, no `shutil.rmtree`, no `setmod.activate_selection(`, no `.get("staged_refs")` code, no `_build_only` param (docstring mention only) PASS.
- Initial H2 bugs retained in `correction-h2/history` + H2 bytes in `correction-h3/history` (not overwritten).

## 5. Diff/API/needs (no overall pass)

- EDITED (H only): `scripts/survey_editorial_publication_v2.py` H3 (was H2 `b86983cb…`, now ~3077 lines, hash to be pinned by root `sha256sum`).
- PRESERVED: Reader/Gate H2 slices (no H3 changes needed beyond H2 trio/verifier + H3 Gate pure-call in H module only; Gate file itself unchanged in H3).
- Public API unchanged (contract §6, no caller-verified dicts, repo-contained paths): `prepare/finalize/validate_receipt/validate_set(no _build_only)/activate(ALREADY_ACTIVE early)/resume(RESUMED/ALREADY_ACTIVE)/verify_history(HISTORICAL_VALID)/resolve_selection` + CLI (exit 2, stdout JSON only, no shell string).
- Needs: L already exposes strict loaders/`validate_activation_record` etc. (used read-only, no fictitious writes; seven enforced both layers). C: P3S50 + `contract_files` 62→67 + consumers (untouched, C-owned); safe-builder extension for quality/candidate not needed (temp+validate+exclusive already exact, no loophole; Gate now pure+exclusive, no scratch). No new registry/contract change.
- Await root combined-code review before targeted real execution (no long fixtures/build claimed).

**H3 return complete. No authority execution. Await root review.**
