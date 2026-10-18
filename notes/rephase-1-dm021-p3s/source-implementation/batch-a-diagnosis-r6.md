# Batch-A R6 diagnosis — O4 LAYOUT_REFUSED vs PIN_FAILED (scoped, read-only)

2026-10-18. Fresh Co-Worker scoped diagnosis ONLY. No rerun/duplicate tests,
no imports/runtime/tests/network/DB/index. Source + durable raw read-only;
this doc is the only new file.

## 1. Identity scope (current)

- Candidate: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
  detached `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, `index_empty=yes`,
  `remote=inert`, `status_rows=105` per
  `notes/rephase-1-dm021-p3s/smoke-r6-batch-a-20261018T083224Z/batch-a.record.txt:16`.
- New3 R6: `scripts/survey_editorial_staged_source_v2.py` 126181B
  `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65`,
  `schemas/editorial-staged-source-manifest-v2.schema.json` 5627B
  `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46`,
  `tests/test_survey_editorial_staged_source_v2.py` 141792B
  `0e1cc20fa0d34f6d4096bd1f99865513d4c4f1e07e6fdf20a2c36dfff6c52d9d`
  per `notes/rephase-1-dm021-p3s/draft-history-r6/static21.json:52-95`
  and `.../correction-report-r6.md:17-19`. Module/schema unchanged R5→R6;
  O1/O2/helper bodies identical per `correction-report-r6.md:30-42`.
- Runtime: `/usr/bin/python3` `Python 3.14.4`, runner
  `verification-tools/run_p3s_b3.py` `dc695ace…`, launcher
  `verification-tools/launch_p3s_smoke_b4.py` `9a943c4a…`,
  manifest `draft-history-r6/static21.json` `f37cf825…` 3670B
  per `smoke-r6-batch-a-20261018T083224Z/batch-a.record.txt:13-15`.
- Batch-A selection: 8 ordered fail-fast (`-f`) selectors O3,O4,O5,O6a,O6b,O7,O8,O9
  per `notes/rephase-1-dm021-p3s/astra-batch-a-selection-r6.md:5-16`;
  spelling corrections O4→`test_o4_live_state_mutation_replay_ok_materializer_refuses`,
  O5→`test_o5_artifact_only_head_independence` per `batch-a.record.txt:2-11`.

## 2. Actual batch-A raw (saved, no rerun)

- `smoke-r6-batch-a-20261018T083224Z/launch.stdout:1-4`:
  `b2 child pid=3556296 ... child_rc=1 wrapper_rc=1 post_errors=[]`.
- `.../run-b3-batch-a-20261018T083224Z/run_p3s_b3.stderr.txt:1-22`:
  O3 `ok`, O4 `FAIL`, `Ran 2 tests in 951.172s`, `FAILED (failures=1)`,
  `File ".../tests/test_survey_editorial_staged_source_v2.py", line 1248,
  in test_o4_live_state_mutation_replay_ok_materializer_refuses`
  `self.assertEqual(outcome.get("code"), "PIN_FAILED")`
  `AssertionError: 'LAYOUT_REFUSED' != 'PIN_FAILED'`.
- `.../run_p3s_b3.stdout.txt:1-32` shows only 4 JSON lines (O3 materialize,
  O4 materialize, O4 replay, plus wrapper `child_rc=1`); six selectors
  O5,O6a,O6b,O7,O8,O9 unrun (fail-fast stop). `launch.record-done.json:82-86`
  `child_rc=1 wrapper_rc_final=1`.
- `.../run_p3s_b3.meta.json:39-40` cache/tmpdir absent-isolated;
  `run_p3s_b3.pre.json`/`post.json` both `head=409b292… tree=8ce36998…`.
- Original R5 smoke O1/O2 `2 tests/855.750s` PASS per
  `notes/rephase-1-dm021-p3s/astra-postsmoke-oracle-review.md:3`
  stays bound to R5; R6 preserves bodies per `correction-report-r6.md:30-42`.

### FULL O4 durable child raw (all 4 dirs, `cat` read-only; `Read` refuses `.bin`)

- `fixture-raw/p3s-p3s-sg4tfrxr/child.stdout.bin` (306B, O3 materialize):
  `{"ok": true, "result": "STAGED_SOURCE_MATERIALIZED",
  "staged": "sources/SP001/.../fixture-lf-p3s-3/staged-source/staged-source-manifest.json",
  "digest": "f0e9c2f0...", "head": "9e5f6327..."}`; stderr 0B.
- `fixture-raw/p3s-p3s-06h91h97/child.stdout.bin` (306B, O4 first materialize):
  `{"ok": true, "result": "STAGED_SOURCE_MATERIALIZED",
  "staged": ".../fixture-lf-p3s-4/staged-source/staged-source-manifest.json",
  "digest": "dc850d5a...", "head": "1c30a46c..."}`; stderr 0B.
- `fixture-raw/p3s-p3s-_djz2770/child.stdout.bin` (134B, O4 replay after drift):
  `{"ok": true, "result": "STAGED_SOURCE_REPLAY_VERIFIED",
  "reader": "e5105b31..."}`; stderr 0B.
  → replay-positive survives live-State drift (intended first half holds).
- `fixture-raw/p3s-p3s-844491nh/child.stdout.bin` (285B, O4 second writer — FAIL):
  `{"ok": false,
  "error": "StagedSourceError: LAYOUT_REFUSED: [PIN/REFUSED_PRE_WRITE] canonical proposal layout refused: STATE_INVALID: Production State fails strict validation",
  "code": "LAYOUT_REFUSED", "phase": "PIN", "disposition": "REFUSED_PRE_WRITE",
  "owned_files": 0, "owned": {}}`; stderr 0B.
  → full detail ends at `STATE_INVALID: Production State fails strict validation`
  (child script truncates `exc` to 2000 chars; P1 `STATE_INVALID` itself discards
  the `validate_agent_state` list — see §4). `owned_files=0` proves pre-write
  no-write for this refusal.

## 3. Actual test source (O4)

`/tmp/.../candidate-partial-b40de60/tests/test_survey_editorial_staged_source_v2.py:1224-1255`:

- `1224: def test_o4_live_state_mutation_replay_ok_materializer_refuses`
- `1235-1237: live_state = core.load_json(prep["state_path"]);
  live_state["p3s_artifact_probe"] = "mutable non-KEEP live change";
  core.write_json(prep["state_path"], live_state)`
- `1239: self._verify(...)` (replay must stay VERIFIED — actually VERIFIED per raw above)
- `1241-1244: outcome = _run_p3s_fixture(... _P3S_MATERIALIZE_SCRIPT ...)`
- `1245: self.assertFalse(outcome.get("ok"))`
- `1246-1247: # R5 prepin binds the original state_ref live before any observer...`
- `1248: self.assertEqual(outcome.get("code"), "PIN_FAILED")`
- `1249-1251: phase PIN, disposition REFUSED_PRE_WRITE, error contains REF_DRIFT`
- `1252-1254: live mutation still present + stale-basis no-write`.

`core.write_json` is `scripts/survey_production_v2.py:90-92`
(`json_bytes` `indent=2+"\n"`, no `sort_keys`); `load_json` `78-83`.
Mutation appends a new top-level key, not whitespace.

## 4. P1 current layout guard / ref checks (original cp vs active-before)

- `scripts/survey_editorial_correction_proposal_v2.py:87-234` `_Collector`
  (`safe` raw-first alias/regular pin, `pinned` exact `{path,sha256}` + `REF_DRIFT`,
  `reverify` HEAD/bytes).
- `355-377` `_original_checkpoint` (exact validation-checkpoint ref + `ORIGINAL_*`);
  `380-411` `_active_effective` (exact `active-before` equality:
  `col.pinned(... ORIGINAL)` when no active record, else `ACTIVE_PATH_REBIND` /
  `ACTIVE_SUPERSEDED_DRIFT` / `ACTIVE_PRESERVED_DRIFT`).
- `1576-1609` `_validated_state_profile_for_tree`: `col.safe(State)` →
  `json.loads` → `agent.validate_agent_state(root,cfg,state)` →
  if non-empty list `raise STATE_INVALID` (`1597-1598`, message fixed
  `"Production State fails strict validation"`, underlying list discarded) →
  `_eligibility` → `_load_profile` → canonical-State-path check.
- `1641-1707` `_pin_proposal_layout`: strict State/Profile authority BEFORE
  broad `_tree_map` walk (`1664`), then canonical `expected_dir` derivation
  (`1667-1678`), proposal-dir entries, staged authoring/reader pins.
- State schema `schemas/survey-production-state.schema.json:6`
  `"additionalProperties": false` with required 18 keys; extra top-level
  `p3s_artifact_probe` is schema-invalid. `survey_agent_control_v2.py:353-368`
  `_validate_agent_state` returns `[str(exc)]` on `validate_instance` failure.
- Hence any semantic extra-key State mutation fails at layout with
  `STATE_INVALID`, before any `state_ref` byte-drift comparison.

## 5. Current module PIN order (why early refusal)

`scripts/survey_editorial_staged_source_v2.py`:

- `597-619` Session pins State/Profile/proposal/manifest/scope (still JSON-valid).
- `625-672` schema/style/S2/code-deps pins + `_check_runtime_binding`.
- `680-691` fresh live `p1mod._Collector(root_path)` + sanitized `HEAD` pin.
- `692-696` `layout = p1mod._pin_proposal_layout(live,...)` except →
  `raise LAYOUT_REFUSED ... canonical proposal layout refused: {exc}`.
- `697-714` live-vs-retained cross-checks (`PIN_DRIFT`), then `718-725`
  `_prepin_known_live_refs` (basis `state_ref`/proposed/retention-plan
  `live.pinned` → `REF_DRIFT` preserved as `PIN_FAILED` per `342-415`).
- `790-833` fresh in-call P2V `OBSERVE` + `OBSERVER_MISMATCH`/`HEAD_MOVED` checks.

O4's mutated State reaches `693` with schema-invalid bytes → `STATE_INVALID`
inside `_validated_state_profile_for_tree` → wrapped `LAYOUT_REFUSED/PIN/
REFUSED_PRE_WRITE` (`844491nh` raw). It never reaches `719` prepin, so
`PIN_FAILED`/`REF_DRIFT` is unreachable for this mutation type.

## 6. Determination

- **Semantic invalid, not whitespace-only.** `live_state["p3s_artifact_probe"]=...`
  adds a new top-level property; `additionalProperties:false` makes the live
  State fail strict validation. `core.write_json` reformats with same `indent=2`
  style, but the delta is a semantic key addition, not trailing-whitespace.
- **Early layout refusal is honest module behavior, not a module defect.**
  Layout is the selected strict-current guard before broad walks and before
  prepin; `LAYOUT_REFUSED` with `STATE_INVALID` cause, `PIN/REFUSED_PRE_WRITE`,
  `owned_files=0` is a correct pre-write refusal. Replay staying `VERIFIED`
  (raw `_djz2770`) confirms the verifier correctly ignores current State
  (`verify_staged_source` docstring `1699-1705`: no P2V/no current-State/no HEAD).
- **Test oracle is wrong for this mutation.** R6 comment at `1246-1247`
  assumes prepin `PIN_FAILED/REF_DRIFT`; that path requires a schema-valid
  State whose bytes differ from `basis.state_ref`. A schema-invalid State
  legitimately preempts earlier. Do NOT change expected to `LAYOUT_REFUSED`
  without proof as a generic acceptance — that would weaken the intended
  `replay-positive/current-before-negative-via-prepin` distinction and mask
  the `REF_DRIFT` seam. Do NOT change the module to skip State validation
  or to propagate P1 `REF_DRIFT` through layout — that would violate the
  selected strict-current-guard order.

### Specific suggested test-only repair (preserves intent)

Replace the semantic insertion with a **whitespace-only byte drift**
(P2V B1 precedent: whitespace-only liveState drift):

```python
orig = prep["state_path"].read_bytes()
prep["state_path"].write_bytes(orig + b"\n")  # or orig.rstrip(b"\n")+b"\n\n"
# assert: json.loads unchanged, sha changed, raw ends with extra newline
```

Keep all other O4 asserts exactly (`PIN_FAILED/PIN/REFUSED_PRE_WRITE`,
`REF_DRIFT` substring, mutation-present, replay `VERIFIED`, fault-present
no-write). Whitespace-only keeps `validate_agent_state` passing, layout
passing, then `_prepin_known_live_refs` `live.pinned(state_ref)` fails with
`REF_DRIFT` → `PIN_FAILED` as the test intends. Verify the fixture State file
ends with `\n` (it does via `core.json_bytes`) so `+b"\n"` is JSON-semantics
preserving; assert `core.load_json` equality + `sha256_bytes` inequality in-test
to prove whitespace-only. No module/schema change.

Alternative (weaker, not recommended): keep semantic key but expect
`LAYOUT_REFUSED/PIN/REFUSED_PRE_WRITE` + `STATE_INVALID`. This proves only
early strict refusal, not the prepin `state_ref` seam, and should not replace
the prepin test without a new scope decision.

## 7. Next-six audit (definite issues only; no invented findings)

Read exact R6 bodies `1257-1673` against current module call graph above.

- **O5** `test_o5_artifact_only_head_independence` (`1257-1276`): artifact-only
  `sources/artifact-only-note.txt` commit changes HEAD, then `_verify`.
  Verifier `1699-1705` explicitly has no HEAD/current-State comparison; only
  staged-vs-proposal/retained/replay checks. No definite preemption. Likely PASS
  (unrun). No repair suggested.
- **O6a** `test_o6a_tool_drift_reaches_check` (`1278-1322`): tampers
  `scripts/survey_review_attention_v2.py` which is in `_SHARED_PY`
  (`survey_editorial_staged_source_v2.py:109`) and thus in `_route_code_deps`
  S2 set. Verifier PIN order `1786-1802`: `CODE_DEPS_MISMATCH` shape check then
  per-dep `TOOL_DRIFT` before `RETAINED` phase; no KEEP/schema preemption on
  this verifier path. Expects `TOOL_DRIFT/PIN/INVALID` — reachable. No repair.
- **O6b** `test_o6b_keep_drift_preempts_honestly` (`1324-1376`): target is
  lexicographically first KEEP `retained_ref` excluding individually-pinned
  State/Profile/proposal/manifest/scope/config/authoring/reader
  (`1339-1354`); appends `b"\n"` (whitespace for JSON/text, new bytes for hash).
  Writer layout still schema-valid (State untouched) → reaches prepin `719`
  → `live.pinned(retention_plan row)` mismatch → `PIN_FAILED/PIN/
  REFUSED_PRE_WRITE`, `TOOL_DRIFT` absent (`1367-1371`). Matches
  `correction-report-r6.md:97-108`. No definite blocker; re-verify selected
  path only if fixture recipe changes (report already notes this).
- **O7** `test_o7_scope_refusals` (`1378-1458`): missing scope →
  `WRITER_FAILED/PIN/REFUSED_PRE_WRITE` is the actual wrapped code for
  `session.safe_read` `RetentionError` via generic `except Exception`
  (`1424-1430`); ordinary/malformed/stale reach `OBSERVE` →
  `OBSERVER_REFUSED/OBSERVE/REFUSED_PRE_WRITE` + `SCOPE_NOT_WITHIN_AUTHORITY` /
  `SCOPE_UNREADABLE` / `SCOPE_STALE_UPSTREAM`. Matches R6 correction
  (`correction-report-r6.md:44-59`) and root item 1 disposition. No definite
  blocker; do not invent late `SCOPE_` for missing.
- **O8** `test_o8_path_ref_schema_inventory_tamper` (`1460-1572`): pristine
  restore + `_retamper_manifest` (digest+canonical recompute) per case;
  duplicate-key at canonical filename → `PIN_UNREADABLE/PIN` via
  `retention._parse_json_strict`; verifier order proposal-ref→label→basis→
  proposed→contract→schema→route→code-deps→TOOL_DRIFT→retained→replay supports
  each listed `code/phase` (`STAGED_SET_MISMATCH/VERIFY`, `OUTPUT_PATH_MISMATCH/
  REPLAY`, `SCHEMA_INVALID/PIN`, `CODE_DEPS_MISMATCH/PIN`, `BASIS_MISMATCH/PIN`,
  `PROPOSED_MISMATCH/PIN`, `STYLE_REF_MISMATCH/REPLAY`, `PROPOSAL_REF_MISMATCH/
  PIN`, `LABEL_MISMATCH/PIN`, `CONTRACT_IDENTITY_MISMATCH/PIN`,
  `REPLAY_MISMATCH/REPLAY`). No definite preemption found in source.
- **O9** `test_o9_alias_fifo_no_read` (`1574-1673`): alias reader →
  `LAYOUT_REFUSED/PIN/REFUSED_PRE_WRITE` + `PATH_ALIAS` via `col.safe` leaf
  check (`survey_editorial_correction_proposal_v2.py:143-144` wrapped at
  staged `695`); FIFO at actual reader path → `PATH_NOT_REGULAR` (test allows
  `PATH_NOT_REGULAR|PATH_UNREADABLE|PATH_ALIAS` alternation, exact
  code/phase still asserted); scope-ancestor symlink → `WRITER_FAILED/PIN`
  + `PATH_ALIAS` via Session pin (`1424-1430`). Rename-restore preserves
  `base` equality. No definite blocker.

No costly guaranteed failures identified in O5–O9 source; do not relaunch
automatically. Only O4 is a definite test-oracle blocker.

## 8. Blocker classification

- **Module defect blocker: none.** `LAYOUT_REFUSED/STATE_INVALID` is the
  selected honest behavior for schema-invalid live State.
- **Test defect blocker (definite): O4 oracle.** Expected `PIN_FAILED/
  REF_DRIFT` cannot be reached by a semantic extra-key State mutation;
  actual is `LAYOUT_REFUSED` caused by `STATE_INVALID` at layout, with
  replay `VERIFIED` and `owned_files=0` intact.
- **Suggested action:** test-only whitespace-only State drift repair above;
  keep module `7059166e`/schema `4fa61723` unchanged; keep `static21.json`
  `f37cf825…`; single fail-fast relaunch of O3+O4 only after root selects it.
  No full-suite/proof/commit/push.
