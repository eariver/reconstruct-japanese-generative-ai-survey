# SP dispose-run r3 — commands note (review only, NO EXECUTION)

r3 successor of reviewed r2 `2044257f…` (preserved untouched): removes
hardcoded `R4_INPUT`/`R4_SUPP` globals (r2:81-82) and P1 hardcoded reads
(r2:459-460) per r7 independent review §3 REUSE_BLOCKED. All proven r2
guards/normal-run paths preserved (571→570→569 derived sets, 771, State/DM022,
O_EXCL backups, one `rn.run`, 160/165/15 validators, NEW-archive audit binding,
umask modes, return-gate no-reseal).

## What changed (only the packet-input derivation)

- No `R4_INPUT`/`R4_SUPP` globals. Corrected packet paths derive from
  `manifest["corrected"]["input"|"supplement"]["path"]` with same-hash checks
  (r7 manifest: r5 `697a4ed0…` 355643B + r4supp `1221d293…` 31278B; never old r4 names).
- Staged current input/supplement derive from `READY.new_input` /
  `READY.new_supplement` live pins (`R6._pin_live` 0o664) + staged SHA must equal
  manifest corrected input SHA (verbatim packet DATA bytes).
- Supplement sources/rows/`stable_task_id`/`_source_class`/counts (160/15) and
  `exp_oblig_n`/`exp_closure` come from staged live files (what `rn.run` uses),
  not unstaged packet. `supplement_id` must equal READY (staged binding);
  packet draft ID must differ (not staged).
- Default `--manifest` is now r7 `6c61b254…` (1056/37); works with r6 manifest
  too (packet r4 SHA + staged r4 SHA coincide there).

## Files (this packet only)

- `sp-operator-dispose-run-r3-20261105.py` (r3 tool)
- `sp-dispose-run-launcher-r3-20261105.sh` (points at r3 tool + r7 manifest, `dispose-run-r3-*` bundles)
- This note + `sp-dispose-run-delta-r2-to-r3-20261105.json` (machine delta).

## Invocation (DO NOT RUN — r7 preflight root read pending, no execution authorized)

```sh
notes/rephase-1-operational-rehearsal-resume-20261104/sp-dispose-run-launcher-r3-20261105.sh \
  --retention-dir notes/.../retention-SP-dispose-YYYYMMDDTHHMMSSZ \
  --ready-path notes/.../retention-SP-preflight-YYYYMMDDTHHMMSSZ/READY.json \
  --expected-tool-sha <r3 hash at authorize> \
  --expected-ready-sha <new READY hash> \
  --expected-manifest-sha 6c61b254a11a5a318fbe9be4ac97c18a0a9686cb0eb1343309304ba6de9dd80f
```

No State/CP/Human/source change here. Prior semantic PASS HELD for D165 fix.
