# Re:Phase — fixed-baseline candidate recovery bounded completion

Recorded **2026-10-03T18:47:53+09:00** (Astra clock). Human continuation began at clean reconstruct **`fe17541212a057522922b8aabf6d66b5a594a079`**, locally `main...origin/main` without fetch. **Recovery/source-runtime verification is bounded complete. Stop at this Human Commit Point before DM-001/019 implementation.** Whole candidate remains **NOT_READY**, step 4/B3 OPEN, canonical seven-point audit unstarted.

## 1. New, genuine-baseline child

| Field | Verified value |
|---|---|
| New candidate | **`b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`** |
| Tree | **`657032438c6ed8b1c055d5a120b67b4b261a5092`**, exactly historical 481's tree |
| Direct parent | **`774dd39a951c9ac3818e83dfffd4c7666efb0a20`**, unchanged Production baseline |
| Branch | `codex/rephase-candidate-recovery` |
| Independent fixture | `/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z` |
| Independently restored copy | `/tmp/opencode/jgas-recovery-restore-20261003T0445Z` |
| Inert origin | `https://example.invalid/rephase-candidate-recovery.git` |
| Runtime | `/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python`, CPython **3.12.14** |

This is **new commit identity, not recovered 481/e4 history**. Historical 481/e4/B/R1 DBs remain absent at their documented locations. Their historical bounded results stay intact; no PASS transfers to b40de60. Root independently read actual candidate/restored HEAD/tree/parent, the 32-path raw tree delta and archive hash. General executed recovery/tests; root did not execute tests.

## 2. Actual source application and isolation

[Packet entry](../notes/rephase-1-candidate-recovery/README.md), [task](../notes/rephase-1-candidate-recovery/task.md), [method decision](../notes/rephase-1-candidate-recovery/method-decision.md), [milestone-2 report](../notes/rephase-1-candidate-recovery/m2-20261003T0435Z/report.md).

- General acquired fixed baseline commit/tree metadata and then fetched **only the exact baseline** with `--depth=1 --filter=blob:none --no-tags` into an absent independent target. Sparse materialization includes the needed code/config/schema/tests/docs/templates. Production main, the already captured Summary, linked Issues and edition records were not refreshed.
- Acquisition remote was removed before checks; origin is inert. No alternates, inherited Git-root overrides, shared DB/hardlinks or fixture objects in reconstruct's DB. No explicit `git config` commands, no hook-bypass flags. Default hook samples were present, not executable project hooks; do not infer project-hook execution.
- Four actual `git apply --check`/application pairs (full baseline→A, A→B, B→e4 CLI, seven R1 paths) exited 0 with empty streams. R1's four preimages were compared to intermediate worktree bytes, not the still-baseline HEAD; three additions were absent.
- Final delta is **32 paths = 21 modifications + 11 additions**. The earlier Explore “31” count was an inventory error. All other tree references remain unchanged; full candidate tree has 32,152 entries and matches 481's tree. Nine Freeze-boundary paths remain baseline-identical; **no new Freeze repair** is included.
- This establishes clean application of the saved content chain in the acquired partial baseline repository. It is not proof of full hydrated assets/history, whole publication operation or application readiness.

### Final identity source — mandatory correction

Use [machine-generated final 32+9 binding](../notes/rephase-1-candidate-recovery/m3-20261003T0445Z/corrections2-identity-20261003T0944Z/final-identity-binding.json), SHA256 **`559512d3e48e0101af543fe1b36c0cfded0a1b6304837b1b5bac253c1eaed75e`**, together with the [final recovery manifest](../notes/rephase-1-candidate-recovery/m3-20261003T0445Z/corrections-20261003T0456Z/recovery-manifest.json).

Root found one transcription error after the first independent resolution: m2's manifest and its m3 pretty copy give `tests/test_survey_findings_v2.py` blob `6e178887...`; actual Git and the original raw20 have **`6e179887284026d1fb6fc33522b5fb28afc4788e`**. General generated the corrected binding from parsed Git output, and the reviewer independently machine-compared all **41 paths** against raw/candidate/restored bytes: no other mismatch. The originals stay preserved. The reviewer's original “full 32 match” statement was an overclaim based on path/sample checks; its [identity resolution](../notes/rephase-1-candidate-recovery/independent-identity-resolution.md) explicitly corrects that claim. This typo never changed the candidate or archive.

## 3. Fresh runtime evidence

General provisioned isolated uv **0.12.15**, CPython **3.12.14**, fixed direct requirements **jsonschema 4.23.0 / pypdf 6.16.2**, and observed the same five recorded transitive versions. Import metadata is saved. An initial wrong-`sys.path` import probe failed and was corrected; the original traceback remains setup evidence, not a source defect or clean-first-attempt claim.

The [selected verification task](../notes/rephase-1-candidate-recovery/verification-decision.md) ran **five existing methods once**, all successful, no failures/errors/skips (37.834 seconds total reported method time):

| Check | Actual evidence scope |
|---|---|
| Profiled Weekly/Special identity | Pure public-slug helper regression; does not invoke `build_profiled_freeze` |
| Weekly approved Preview → FROZEN | Real validators/stage/checkpoint/State advance using synthetic edition data and the recovered Git root |
| Missing/extra/wrong VISUAL | One method, three subcases; real stage rejection with the recovered Git root |
| Persisted-review Gate CLI | One method, three path/cwd subcases; real recovered CLI with synthetic direct-primary inputs, not its unselected Weekly Git fixture |
| Canonical exact-PDF chain | Real lower-level validators/builders over synthetic temporary data, through a synthetic Release record, no live Release |

The code/raw review corrects General's initial no-Git claim for the stage methods and its recovered-index claim for selected direct-primary CLI. No unexecuted helper supplies runtime evidence. Synthetic reviews/PDFs/checkpoints are flow/type/identity evidence, not real editorial/visual quality or Human approval.

**Test identity binding limitation:** `run_five.py` guards bracket the **whole five-method suite**, not each subprocess. Per-method logs lack embedded HEAD/hash headers; binding relies on saved literal argv/cwd, suite HEAD/tree/parent/clean-tracked guards, actual sources and unchanged final bytes. Root and independent reviewer accept this only for this bounded recovery. Saved runners reuse paths and are not safe rerun instructions.

**Recovered-DB diagnostic:** the actual `current_closure` + `_verify_head_bytes` passed for eight source rows at b40de60. A single in-memory SHA corruption was rejected with exact `ValueError: Weekly receipt current-tool closure drift: scripts/survey_weekly_derivation_v2.py`. No code/file/history mutation or publication replay. The restored copy separately passed only the positive diagnostic; the five tests were not repeated there.

## 4. Portable partial DB and offline restoration

[Archive](../notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz): **5,152,199 bytes**, SHA256 **`faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c`**. Included in the packet under `-text` protection, so Human Commit/Push can preserve more than the former `/tmp`-only DB. It contains **760 regular-file members**: 74 available `.git` files plus **686 materialized tracked files**, with shallow/sparse/ref/config/object data. Excludes FETCH_HEAD, pycache, venv/tooling and credentials.

The second DB restored from this archive has the exact same HEAD/tree/direct parent and materialized file/object inventories, no shared inodes/alternates, inert origin and a passing actual current-source diagnostic under `GIT_NO_LAZY_FETCH=1`, `GIT_ALLOW_PROTOCOL=file`. `.git/index` stat-refresh bytes differ but staged entries/clean tracked content agree. The external pinned venv was reused, **not restored from the archive**.

This is a verified snapshot of the **available partial DB**, not a complete Git history/assets backup. Census reports 2,317 reachable present objects (2 commits/1,608 trees/707 blobs), 26,309 missing reachable blobs, shallow at baseline; 686 of 32,152 tracked files materialized. Earlier R1's 41 unverified historical data blobs and missing non-baseline ancestry are not repaired by this unit.

### Restore/evidence qualifications

- The initial restore wrapper had layout and count errors; final restoration was completed with manual empty-directory cleanup and separately checked. **Do not run saved `restore.sh`**: it lacks fail-closed command/pipeline handling and a hash gate. Successful wrapper exit is not the acceptance oracle; the final extracted DB, inventory checks and restored diagnostic are.
- First tar stderr, initial member-list versions and v1 restore-script source were overwritten. Some empty-directory/intermediate-tar removals have only observed terminal output. These are deviations from the no-overwrite evidence task, explicitly preserved as limitations, not retroactively called clean. Final archive/hash/content proof survives independently; no test rerun was needed to disguise those losses.
- The final identity comparison had two setup `KeyError` attempts before success; their outputs survive, script revisions are not a versioned three-script history. Abbreviated m2 command meta is not a full literal argv transcript. One environment value was redacted at initial capture; the stored environment record is not pristine raw.
- Read [first correction supplement](../notes/rephase-1-candidate-recovery/m3-20261003T0445Z/corrections-20261003T0456Z/corrections.md) and [identity correction](../notes/rephase-1-candidate-recovery/m3-20261003T0445Z/corrections2-identity-20261003T0944Z/correction.md) with the original reports. The “3rd hex position” prose in the latter is inaccurate; the exact full wrong/correct IDs above control (the differing digit is fifth). None of these qualifications authorize deletion of pre-existing authority.

## 5. Review conclusion and next unit

The [initial independent review](../notes/rephase-1-candidate-recovery/independent-recovery-review.md) required documentary corrections. Its [scoped resolution](../notes/rephase-1-candidate-recovery/independent-recovery-resolution.md) and subsequent [all-41 identity resolution](../notes/rephase-1-candidate-recovery/independent-identity-resolution.md) support **BOUNDED_PASS for recovery only**, with the original contrary statements preserved. Root reviewed source/oracles/raw outputs, actual objects, archive hash, corrections and both resolutions; the final relative manifest link was fixed by root. This is author-side Astra acceptance plus author-independent recovery review, not canonical audit or production adoption.

**After Human continuation, next bounded unit is DM-001/019 joint Freeze implementation at b40de60**, under the [selected contract](rephase-1-dm001-019-contract-decision.md). First internal action: General returns concrete shared-helper placement, Candidate/Profile binding, predictable-failure preflight and installation-failure handling, plus valid Weekly/Special test-fixture/oracle plan. Astra resolves that interface/writer design before code; this is an internal milestone, not another general inventory or Summary intake.

Then General implements in a **new independent byte-copy of available b40de60 DB**, preserving original/restored/archive. Initial budget is two runtime modules (`survey_publication_v2.py`, `survey_profiled_freeze_v2.py`) plus focused tests and necessary affected existing fixtures. Both builders must use Candidate-bound VISUAL, reject mismatched approved Candidate even for identical PDF, derive public identity from validated Profile slug, and reject predictable failures/conflicting outputs before writes. Preserve State/Human guards; no arbitrary tag override, generic resolver, authority-success mocks or broad backlog repair. Demonstrate parent defects and corrected exact-head behavior, retain failures, then Astra and fresh implementation reviewer inspect the result before that unit's Commit Point.

If the live DBs disappear, hash-check/read the saved archive with a **new fail-closed, no-overwrite extraction procedure** and verify the recorded identity/available closure before use; never execute the saved restore wrapper. No need to reacquire production or rebuild content while the verified packet is usable. Runtime reinstall is separate and must use recorded pins. New output/harness paths are mandatory; do not regenerate or overwrite current evidence.

DM-003/004, build-transfer, Special supporting semantics/DM-016/017, rendered/semantic acceptance, optional findings transport and whole-candidate diagnostics/audit remain separate. **No next-unit code has started. Ordinary reconstruct Commit/Pull/Push remains Human-owned. Stop now.**
