# SP preflight r8 — commands note (review only, NO EXECUTION)

r8 successor of r7 `c432d66d…` (preserved): fixes root-read defects —
`supplement30` `sha256`/`bytes` row keys (was `raw_sha256`/`byte_count`
KeyError after input staged), READY `stage prepare-only` (r3 consumer
contract; input-only preparation, same contract), `package_json_sha`
(real retained `package.json` hash), end-phase `_finish_authority_phase`
with owner callback (invocation-scoped; later disposer cannot close it),
terminal 771/gates/refscan, packet-only (RESUME direct-child) retention,
pass placeholder removed (17 retained Raw live-pinned via `R6._pin_live`).

## Files

- `sp-operator-preflight-r8-D165fix-20261105.py` (r8 tool)
- `sp-preflight-launcher-r8-D165fix-20261105.sh` (`preflight-r8-*` bundles)
- This note. Manifest reused r7 `6c61b254…` 608012B (1056/37, canonical
  `253cb2ea…`/`18a05292…`, r5 `697a4ed0…`); no new manifest needed.

## Invocation (DO NOT RUN — root+independent review before execution)

```sh
notes/rephase-1-operational-rehearsal-resume-20261104/sp-preflight-launcher-r8-D165fix-20261105.sh \
  --retention-dir notes/.../retention-SP-preflight-YYYYMMDDTHHMMSSZ \
  --new-input-id r8-D165fix-YYYYMMDDTHHMMSSZ \
  --expected-tool-sha <r8 hash at authorize> \
  --expected-manifest-sha 6c61b254a11a5a318fbe9be4ac97c18a0a9686cb0eb1343309304ba6de9dd80f
# READY: stage prepare-only, 17 retained Raw live pins + retained ffcd supp
# + 1 NEW input + package_json_sha; then separate auth: r3 dispose+retry.
```

r3 disposer unaltered (true mismatch none beyond fixed producer). Prior PASS HELD for D165 fix.
