# SP r7 input-only preflight — commands note (review only, NO EXECUTION)

Fixes D165 binding only. DATA `sp-corrected-input-r5-D165fix-20261105.json`
355643B `697a4ed0…` (r4 `0ee3187e…` +257B; 1 record `EFF-D165`, 2 fields).
New manifest `sp-prepare-expected-manifest-r7-D165fix-20261105.json` 608012B
`6c61b254…` (r6 base + NOW 1056/37 + canonical `253cb2ea…`/`18a05292…` +
old+new accepted sets + r5 corrected input). Tool
`sp-operator-preflight-r7-D165fix-20261105.py` 13785B `c432d66d…`
+ this launcher. Delta `8de011e5…`, rationale `42763646…`.

## Exact writes readiness (after later authorization only)

- Active: exactly 1 NEW `evidence/proposed-input/interactive-evidence-<NEW_ID>.json`
  (verbatim r5 bytes, O_EXCL 0o664). No Raw/supplement/active-tree else.
- Packet-local: NEW retention (`READY.json` + `journal.json` + `pkg-<ID>/`
  160 tasks) + run bundle. `staged_raw` (17) + `new_supplement` (`ffcd0a7e…`)
  listed as retained inputs, NOT new writes.
- All 1056 retained except later exact2 regen (`253cb2ea…`/`18a05292…`,
  still CAND unaccepted); original `ee13b8ee…`/`c60a9624…` backups preserved.

## r2 dispose-run reuse (no code change needed)

Tool `2044257f…` derives sets dynamically (`exp = manifest files +
READY staged_raw/new_input/new_supplement`; 570/569 via del; labels 571
irrelevant). Guards hold with new baseline/READY if: `len(new_rels)==19`
(17 retained Raw + 1 retained supplement + 1 NEW input), 160/15 counts,
165 discovery from live file, audit NEW-archive binding, umask modes.
`corrected` r4 supplement basis unchanged; supplement30/771 unchanged.
No new fetch/schema/source/Git. Prior semantic PASS HELD for this fix.

## Invocation (DO NOT RUN until root+independent review)

```sh
notes/rephase-1-operational-rehearsal-resume-20261104/sp-preflight-launcher-r7-D165fix-20261105.sh \
  --retention-dir notes/.../retention-SP-preflight-YYYYMMDDTHHMMSSZ \
  --new-input-id r7-D165fix-YYYYMMDDTHHMMSSZ \
  --expected-tool-sha <tool hash at authorize> \
  --expected-manifest-sha 6c61b254a11a5a318fbe9be4ac97c18a0a9686cb0eb1343309304ba6de9dd80f
# then (separate auth): r2 dispose+retry with new baseline+READY (exact2 regen).
```
