# Fresh-process timings (DIAG copy of FIX23, no DST edits, PYTHONPATH=DIAG only)

Commands (all `timeout 120 python3 -c ...`, exits 0):
- `validate_prepared_set` → `FRESH validate_set OK 43.2507128760044` (exit 0)
- `validate_editorial_receipt` → `FRESH receipt OK 40.138838740997016` (exit 0)
- `validate_reader_surface_gate` → `FRESH gate OK 1.639296909008408` (exit 0)
- `validate_candidate` → `FRESH candidate OK 2.543154734012205` (exit 0)
- `activate_publication ALREADY_ACTIVE` → `{'status':'ALREADY_ACTIVE','record_path':'sources/.../publication-set.json','state_path':'sources/.../production-state.json','observed':'new'} 87.93600938402233` (exit 0)

Note: fresh activate returns wrong `record_path` (seal `publication-set.json`, not record `r1.json`) because DIAG is FIX23 (old code, before DST ALREADY_ACTIVE fix at 16:45 > FIX23 commit 16:23). Confirms fix timing. No authority rebind (no writes, hashes unchanged – see hash guards in v2 stdout).

Same-process v2 (120s timeout, INCOMPLETE as expected due to cumulative slowness, not deadlock):
- `validate_set round1 dt=42.8s` (8 P3S verifies, each 0.3-0.4s – fast)
- `receipt round1 dt=39.5s` (1 P3S verify 0.3s, rest 39s in jsonschema)
- `gate round1 dt=0.5s`, `candidate round1 dt=1.3s`
- `activate` started at 84.8s, timed out at 120s during inner `validate_set #2 → receipt #3` (CALL verify #14 at 86.8s, RETURN 87.2s, then sampler stacks in jsonschema `urljoin`/`dynamicRef`/`allOf`/`ref`/`lookup`)
- Call counts: `verify_staged_source` 14 in 86s (each 0.3-0.4s, fast); slow is jsonschema, not P3S file reads.
- Sampler stacks (actual paths, not guesses):
  - `survey_publication_set_v2.py:1539 resolve_publication_selection | ... | read_repo_bytes | resolve_raw_path | _walk_existing_ancestors`
  - `survey_agent_control_v2.py:677 _resolve_checkpoint_artifact | ... | _validate_agent_state | ... | sha256_file`
  - `survey_weekly_derivation_v2.py:557 load_derivation | ... | accepted | resolve_checkpoint_artifact | ...`
  - `jsonschema` `validators.py:432 descend | _keywords.py:279 dynamicRef | ... | _keywords.py:334 allOf | ... | _keywords.py:275 ref | _validate_reference | _core.py:680 lookup | parse.py:643 urljoin` (repeated, 30s faulthandler dump shows `urllib/parse.py urljoin` invalid frame – jsonschema `$id https://example.invalid` ref resolution)
  - `validators.py:432 descend | _keywords.py:44 additionalProperties | ...` (schema `additionalProperties:false` checks)
- Before/after hash guards in v2 (INCOMPLETE run, no writes yet for ALREADY_ACTIVE – hashes same for checked files before timeout; full AFTER not reached due to timeout, recorded as INCOMPLETE per bounded-trace rule).
