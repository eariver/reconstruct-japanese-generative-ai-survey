# DM021-P2V independent final resolution — B1 isolated State oracle (BOUNDED_PASS, scoped)

2026-10-16 JST. Same fresh author-independent reviewer as `independent-implementation-review.md` (preserved intact; this file only adds B1 resolution, does not edit that review). Read-only except this NEW file. No runtime/test/import/script/network/DB writes. Only executed commands: read-only `sha256sum` of candidate new3 + saved patch (allowed) — no candidate imports, no suite/proof reruns, no Git/source mutations.

## 1. Sources read

- Root `notes/rephase-1-dm021-p2v/astra-review-b1-selection.md` (15 lines, B1 scope + 2 precision corrections + targeted-only sufficiency condition + errata/relocation requirements).
- Co-Worker A `source-correction/b1-addendum.md` (95 lines, B1.1–B1.3 oracle + targeted run + v5 patch/proof + E1–E3 errata).
- `source-correction/old13-bodyhash.json` (13 old-test + 6 helper AST hashes, `changed_old_tests: []`, `changed_helpers: []`, `new_tests_extra.test_live_state_drift_refuses` only).
- `source-correction/test-d322-to-new.diff` (86 lines, 3 docstring + 78-line new method, purely additive).
- `source-correction/expected18-source-correction-v5.json` (test entry only vs v4).
- Targeted `evidence-20261016TB1-targeted/` (`stderr.txt` 1/1 OK 492.646s, `exit` 0, `stage-done.json` child_rc 0 wrapper_rc 0 post_errors [], `meta.json` selector = new method only, `pre.json`/`post.json` v5 pins + 102 rows + 84 caches + HEAD/tree/index).
- GEN `evidence-20261016TB1-gen/` (patch `dc5ae07b4acb19da2c1d56856f055dd4050530c23286cc0f45c1ae4dcc5ef514` 948373B, `stage-done.json` wrapper_rc 0, source-pre/post pinned).
- PROOF `evidence-20261016TB1-proof/` (`stdout.txt` `APPLY_PROOF_OK head=409b292… files=18 patch=dc5ae07b4acb`, `exit` 0, empty `stderr`, clean/applied freezes).
- `source-correction/relocation-record.md` + `relocation-record.json` (7 moves, before/after content identity, current TB1 apply path).
- `source-correction/preserved-test-d3224797.py` (old-13 body preservation reference, header read only).

## 2. Independent hash verification (read-only)

- Candidate P1 `scripts/survey_editorial_correction_proposal_v2.py` → `cdd69fe7c24de6dda9ee503cfcfbc791a9d7e421141dbb23586f1e4431c27eab` — UNCHANGED (matches v4/v5).
- Candidate observer `scripts/survey_editorial_current_authority_v2.py` → `79a3396cf07d85cfeb11df9f85910ba8aed2ed63f965713edab5b076d580d3f4` — UNCHANGED.
- Candidate test `tests/test_survey_editorial_current_authority_v2.py` → `c567715dfb4ffa04e7d70dfcf42072cf194d0d9239c2e5b664f7098eaa62009f` (74061B) — NEW, matches v5 (v4 `d3224797…` superseded, preserved via `preserved-test-d3224797.py` + diff chain).
- Saved patch `evidence-20261016TB1-gen/complete-p2v-18path.patch` → `dc5ae07b4acb19da2c1d56856f055dd4050530c23286cc0f45c1ae4dcc5ef514` 948373B — matches `.sha256` manifest and proof `stdout.txt:1` + gen `stage-done.json:49–50`.

## 3. B1 blocker resolved (test-only, no implementation defect)

New method `test_live_state_drift_refuses` (`test-d322-to-new.diff:12–86`, 14th method = 2 probes + 12 behavioral) satisfies all three selection requirements on a real captured Weekly fixture (`_build_weekly_pair`):

1. **State is COPY, never KEEP** (`diff:29–39`): `basis.state_ref.path` → single `retention_plan` row with policy `COPY_BEFORE_REPLACEMENT` + role `state:authority`; no other row carries that role; manifest holds exactly one `state:authority` row, also COPY. Matches selection (“State is already a COPY plan row”) and P1/P2R references cited in addendum §1.
2. **State-ONLY drift, setup proven healthy** (`diff:42–55`): `state_file.write_bytes(orig + b"\n")`; same parsed JSON asserted (`diff:43–45`); strict `agent.validate_agent_state(root, cfg, mutated_obj) == []` (`diff:47–48`) — a generic `STATE_INVALID` from broken setup is explicitly refused as acceptance. P2R still `RETAINED_SET_VERIFIED` (`diff:54–55`, retained COPY bytes intact, P2R re-reads retained rows not live State).
3. **P2V exact refusal + no-write + restore + clone pair** (`diff:58–86`): `assertRaisesRegex(BASIS_MISMATCH)` (`diff:58–59`, supplied-vs-rederived live basis; live-vs-rederived `STATE_REF` stays consistent since both derive from mutated bytes — correctly distinguished, not overclaimed as `STATE_REF_MISMATCH`); immediate full `_assert_no_write` vs mutated-pre snapshot BEFORE repair (`diff:61`); restore exact bytes → `NEEDS_SCOPE` + `state_ref.sha256 == sha256(orig)` + no-write (`diff:63–68`); same-byte unreferenced clone as `state_path` → `STATE_NOT_CANONICAL|STATE_CANONICAL` + no-write (`diff:75–77`); canonical `state_path` with clone present → `NEEDS_SCOPE` + no-write (`diff:80–84`, no invented historical inventory); clone removed (`diff:86`).

Targeted evidence is isolated and properly guarded: B4 AS-SAVED, v5 manifest, NEW exclusive outdir, `/usr/bin/python3` 3.14.4, exact single selector (`meta.json:16/33–35`), `stderr.txt` 1/1 OK 492.646s, `exit` 0, `stage-done.json` child_rc 0 wrapper_rc 0 post_errors [], PRE/POST 102 rows (18 source + 84 caches) + HEAD `409b292…`/tree `8ce36998…`/empty index pinned with v5 `files` (P1 `cdd69`, observer `79a339`, test `c567715d`) and 84-entry `cache_detail`.

## 4. Scoped 13+1 basis (NO full14 run claimed)

- Old13 bodies/setup demonstrably unchanged: `old13-bodyhash.json` 13 old-test AST hashes + 6 helper hashes (`_run_git`/`_make_p2v_source_root`/`_run_fixture_code`/`_observe_with_timeout`/`setUp`/`_build_weekly_pair`), `changed_old_tests: []`, `changed_helpers: []`, sole extra `test_live_state_drift_refuses`; `test-d322-to-new.diff` is 86 additive lines (3 docstring + new method, 0 modified old lines). Prior full13 green is `evidence-20261016T000000Z-full3` on test `d3224797` (13/13, child/wrapper 0); B1 green is targeted 1/1 on test `c567715d`. Per selection §11, targeted + prior full13 is sufficient scoped affected evidence **because** runtime P1/observer and old-test bodies are byte/AST-proven unchanged — no automatic PASS transfer to new code is claimed, and no full14-method run occurred or is implied.

## 5. Corrections to my initial review (scoped, original preserved)

- **C1 — “State not in retention” was wrong.** Initial review §6 stated 0 State-file hits and “State missing from retention plan.” Selection §3 and the new oracle prove State IS a `COPY_BEFORE_REPLACEMENT state:authority` plan/manifest row. Corrected by scope: the missing oracle was an *isolated live-State byte negative*, not absence from retention. No other initial-review finding relied on that error.
- **C2 — “Deleting STATE_REF/BASIS checks would fail nothing” was speculative.** Selection notes the shared complete-basis comparator also checks State, so removing one explicit duplicate line is not a proven mutation-test result. Corrected by scope: the requirement met by B1 is the end-to-end invariant (whitespace-only State drift → P2R VERIFIED yet P2V exact `BASIS_MISMATCH` + no-write + restore/clone pair), not proof about any particular duplicated line.

## 6. Prior-report errata (as required by selection §13)

- **E1 — full2 exit:** `final-report.md` §3 “exit 0 with failures” is wrong. Durable raw `evidence-20261015T223000Z-full2/run_p2v_b4.exit` contains `1`; full2 `stage-done` records child_rc 1 wrapper_rc 1. Corrected value is **exit 1** (the §7 list entry “(11/13, exit 1)” was already correct). My initial review already reported exit 1 and needs no correction here.
- **E2 — lost wrong-source proof refusal raw:** `final-report.md` §6 “preserved in the removed proof2 dir, then reused path” is self-contradictory. Truth per addendum §4: that 4-file refusal outdir (`PROOF_REFUSAL: … freeze lstat failed … ENOENT`) was deleted via `rm -rf` and the path reused for the green proof — **no raw survives** (only a session-transcript line). Loss disclosed, NOT reconstructed. Substantive lesson (proof `--source` must contain all18; P2V candidate used for proof2-green and TB1-proof) is re-proven and stands.
- **E3 — full1 orphan:** no POST guards exist (wrapper killed by tool timeout; no `post.json`/`stage-done`/`exit`). History only, distinct from E2. Already disclosed in final-report §§2–3/Q5 and my initial review Q5; restated for completeness.

## 7. Packaging relocation (nested DBs moved, content identity checked)

Per `relocation-record.md/json`: 7 entries (5 worktrees + 2 temp indexes) `mv`d exact from `source-correction/evidence-*/{disposable-copy,disposable-index,clean409-copy}` to `/tmp/opencode/jgas-dm021p2v-preserved-proof-20261015T171102Z/` (verified absent before creation). Nothing deleted; all proof/gen raw/hash/patch/status/meta files keep original packet paths. Before→after identity by content (cross-filesystem `mv` reallocates inodes): all worktrees HEAD `409b292…`/tree `8ce36998…`; disposable copies 102 status rows, clean409 copies 18 rows; `.git` 134 files/96 dirs (proof/clean) and 152/106 (disposable, +GEN blob hashing confined to copy); temp-index hashes match. Current TB1 apply path is `/tmp/opencode/jgas-dm021p2v-preserved-proof-20261015T171102Z/TB1proof-clean409-copy` (directory read: worktree present with `.git/`); relocation record §50 verifies it independently: HEAD/tree match, **all18 vs v5 ALL_MATCH (incl. test `c567715d`)**, status exactly canonical 18 rows (3M + 15 new, no caches per declared removal). Raw historical paths inside proof JSONs (e.g. `proof-freeze-*.json` `safe.directory=…/source-correction/evidence-20261016TB1-proof/clean409-copy`) are unchanged historical strings; the mapping table explains current availability. Active candidate/P2R copies, reconstruct `.git`, manifests (P1 `cdd69`, observer `79a339`, test `c567715d`, v5 hash `7462c04e…` in TB1 `meta.json:38–40`) verified unchanged after ops.

## 8. New patch + fresh proof (final v5 pins)

- GEN `evidence-20261016TB1-gen/` (absolute `--outdir`, B4 AS-SAVED): `stdout.txt` source-pre 18+84 pinned → copy-completeness → separation/inert observed → `bytes=948373 sha=dc5ae07b4acb` → source-post unchanged; `stage-done.json` copy_rc 0 diff_rc 0 patch bytes/sha match, wrapper_rc 0; source-pre/post carry v5 `files` + 84 caches + HEAD/tree/index/status.
- PROOF `evidence-20261016TB1-proof/` (corrected `proof_apply18_b4v2.py`, `--source` P2V candidate → fresh unique `clean409-copy`): `stdout.txt:1–9` saved-sha match + active-18+84 pinned + copy-completeness + `.git` 134/96 both sides + `APPLY_PROOF_OK`; `exit` 0, empty `stderr`; `proof-freeze-clean-b4.json` empty status/index, 15 `new_absent`, 3M `modified_match_head`, 84 `caches_removed`; `proof-freeze-applied-b4.json` HEAD/tree `409b292…/8ce36998…`, exact18 status, all18 sha/mode/bytes match v5 (test `c567715d` 74061B). No old proof dir deleted/reused for this proof.

## 9. Remaining qualifications (exact, bounded)

- **Scoped 13+1, not full14:** green = full3 old13 (d322) + TB1-targeted new1 (c567). Old13 bodies/helpers AST-proven unchanged and P1/observer byte-identical, so selection’s targeted-sufficiency condition holds; any future runtime/old-test change invalidates this composition and requires justified affected/full rerun.
- **Source/caches/imports as actually shown:** TB1 PRE/POST pin static18 v5 + inherited15 (P1 deliberately differs from P2R; other 15 match P2R `expected16-correction2c.json` values) + 84 caches + exact102 + HEAD/tree/index + forced env/isolation; fixture source binding is the same committed-meaningful-source recipe (`_make_p2v_source_root` + `_build_weekly_pair` + real Weekly/Longform/R1-owner chains) — B1 adds the State-COPY isolation case (State drift does NOT trigger KEEP preemption, unlike R1-stale `REF_DRIFT`), which is why this oracle is non-redundant.
- **Helper-failure windows:** B1 proves the State/strict-validation/P2R-verified/P2V-BASIS/no-write/repair/clone windows actually exercised (`diff:42–86`); unexercised windows from the initial review (Q1 preempted `SCOPE_DRIFT`/`SCOPE_DIGEST` reachability, Q2 disjunctive codes, Q3 close-count fragility, Q6 schema-dep isolation) remain as stated in the preserved initial review and are not re-litigated here.
- **Summary vs raw:** this resolution’s method/coverage statements are summary of the read files above; durable raw proof is the cited JSONs/logs/patch/proof files themselves. Prior failure/orphan/tooling limits (smoke1 1/2, full1 POST-less 9/13, full2 exit-1 11/13, gen1 refusal, original B4 SyntaxError, E2 loss) stay in force.

## 10. Verdict

**BOUNDED_PASS (scoped 13+1 + v5 patch/proof TB1)** — B1 blocker from `independent-implementation-review.md` §6 is resolved by the exact `BASIS_MISMATCH` State-ONLY oracle with healthy-setup proof (`validate_agent_state == []`), P2R-persistence separation, immediate no-write, restore positive, and canonical/non-canonical clone pair; P1/observer unchanged; old13/helper bodies unchanged; targeted 1/1 (492.646s, child/wrapper 0) + prior full13 + v5 `dc5ae07b…` 948373B + fresh `APPLY_PROOF_OK` satisfy the selected final evidence. No new implementation defect found. No canonical audit, adoption, semantic approval, or global-CAS/continuous-drift claim follows. Whole NOT_READY, step4/B3 OPEN, audit unstarted, DM021 OPEN. Ordinary Commit/Push Human-owned.
