# LONGFORM repeat-epoch diagnosis — U3 r5 HISTORY_TOOL_EPOCH_DRIFT (READ-ONLY, no PASS)

Status: parallel status only, not stop cause. No source/tests/Git mutation, no network, no ordinary commit.
Scope: `notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/` G3→G4 U3-activate r5 vs G5 U3b r6. Original chrono run55 NOT conflated. All orphan records preserved; no time/supersedes repair.

## 1. Verdict (one line)

No actual product bug. `high-u3-longform` refusal is correct: second U was prepared at the same tool epoch it derives `old` from, so `old==new`. Harness batched G3+G4 before U2, leaving U3 with no genuine delta. G5 `18587b6` is the required forward-only genuine epoch for the second U. Fix owner is LONGFORM integration harness, not HIGH/H.

## 2. Exact G3/G4 diff (fixture DB only, no reconstruct mutation)

Fixture: `.rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform`, HEAD `18587b67d2f96e7e5b761712eb5aa5f5ebbb3c9a`.

- G1 `381c05f486d4956efa275843f7158d9392942d0d`, G2 `5740d67fcb76c137c2c6aef5a0058f81873cd146`, G3 `e25a467025013bdfd193b7401edd6623c5b64830`, G4 `efea07d74a49bbd9167d51bc3b951c7575ca08dc`, G5 `18587b67d2f96e7e5b761712eb5aa5f5ebbb3c9a`.
- `git diff 5740d67..e25a467 --name-only`: `scripts/survey_versioned_renewal_history_v2.py` only (1 insertion, comment `# G3 LONGFORM eligible Core comment`).
  Blobs: `d0b8ae9cdce6149b550c144accf921198e599590` → `dda4217cfbee1c4df6a70140fe359130a1ffc8ee`.
- `git diff e25a467..efea07d --name-only`: `scripts/survey_versioned_renewal_source_v2.py` only (1 insertion, comment `# G4 LONGFORM eligible Core comment`).
  Blobs: `75f251debd566b0184cc965ddff5e5f5e7aee75d` → `73d887f04acaa4d667ae027f6f771c3495256377`.
- `git diff efea07d..18587b6 --name-only`: `scripts/survey_versioned_renewal_v2.py` only (1 insertion, `# G5 LONGFORM` second HIGH tidy).
  Blobs: `9a66ba13adf4bea913c0dff0aa55edd6098dc160` → `95d924e3a13fed968e01b4dbc2c36a80ae68a91a`.
- Style `templates/survey/jgaisurvey.sty` SHA `b1cbbdd93711aef17b37d3bbbedda25aa0bcb51f462bdc7ad172ce2aa103c8f4` before G3 (`run-g34/style-before.txt`), after G3/G4/G5 identical. No style delta to misclassify.

Key sequencing fact (`run-g34-uu-20261025T060000Z.py:166-208`): G3 commit → G4 commit → `do_u(high-u2)` → `do_u(high-u3)`. Both tool deltas are consumed by U2. There is no commit between U2 and U3.

## 3. U3 ToolEpoch fields (committed bytes, read-only `python3 -c` JSON loads)

- U3 basis `.../renewals/high-u3-longform/renewal-basis.json`: `current_tool_epoch.repository_commit_sha=efea07d74a49bbd9167d51bc3b951c7575ca08dc`, `prior_record_ref=r4 3f76b3d736a4b64d86288ccec331d545c45b508e78c5c9b76a68007f9b64eb29`, `prior_selected_ref=high-u2 set 2cee9de6413f6476d5338aad01e6c5e99bd643b9d204027f53fdaa0dd3bafb88`, `recorded_at=2026-10-25T05:33:56.641796Z`.
- U3 receipt `.../high-u3-longform/validated-source-manifest.json`: `current_tools.repository_commit_sha=efea07d74a49bbd9167d51bc3b951c7575ca08dc`.
- U3 build `.../high-u3-longform/build-record.json`: `variant=REUSED_BUILD`, `renewal_tools={old: efea07d74a49bbd9167d51bc3b951c7575ca08dc, new: efea07d74a49bbd9167d51bc3b951c7575ca08dc}`, `original_record_ref=r3 c41159ded5b26f3443f147ee52cc72041f7b8330a03696dd66b386a2a84a26d5`, `recorded_at=2026-10-25T05:33:56.641796Z`.
- U3 proof `renewal-source-proof.json` `recorded_at` same `05:33:56.641796Z`.
- U3 orphan record `sources/SP001/publication/v2/publication-surface-revalidation-r5.json`: `kind=VERSIONED_RENEWAL_ACTIVATION_V1`, `recorded_at=2026-10-25T05:33:56.641796Z`, `set_ref=high-u3 set 9281280e...`, basis `95dd1fe4...`, proof `4b03da0f...`. State never switched to it; pointer stayed r4 then moved to r6. Preserved, not deleted/rewound.
- U3 exits: prepare 0, qa 0, finalize 0 (`REUSED_TARGETS`), activate 2 `SEAL_BIND/HISTORY_TOOL_EPOCH_DRIFT: REUSED_BUILD renewal_tools.old must differ from new (genuine Core change)` (`run-g34/u3-activate-stderr.txt:1`, `u3-activate-exit.txt:2`).

## 4. Selected predecessor r4 vs new G4 HEAD (no delta)

- r4 `publication-surface-revalidation-r4.json` `recorded_at=2026-10-25T05:31:17.224144Z`, `renewal_basis_ref=high-u2 basis 5a94aa19...`.
- r4 lineage last (U2): `basis_current_epoch=efea07d74a49bbd9167d51bc3b951c7575ca08dc` (`run-g34/u2-history-stdout.txt:627`).
- U2 basis `current_tool_epoch=efea07d...`; U2 receipt `current_tools=efea07d...`; U2 build `renewal_tools={old: 5740d67fcb76c137c2c6aef5a0058f81873cd146, new: efea07d74a49bbd9167d51bc3b951c7575ca08dc}`, `original_record_ref=r3 c41159de...`. U2 exits 0/0/0, history chain 4.
- New G4 HEAD at U3 prepare time = `efea07d...` (same commit U2 used). So predecessor epoch == current epoch == `efea07d`. `_derive_old_tool_epoch` correctly returns predecessor `efea07d`; `new` is also `efea07d`; `old==new` is factual, not `old=max-ancestor` misread (predecessor and max coincide here, but derivation is prior-record lineage, `survey_versioned_renewal_v2.py:2000-2032` reading `verify_versioned_history(prior_record_ref)` last `staged_producer_head/receipt_epoch/basis_current_epoch`).
- Chrono is clean and distinct from run55: U3 `pred 2026-10-25T05:31:17.224144Z now 2026-10-25T05:33:56.641796+00:00 CHRONO_OK` (`run-g34/u3-chrono-stdout.txt:1-2`). Run55 was `HISTORY_ANCESTOR`; this is `HISTORY_TOOL_EPOCH_DRIFT`. Do not conflate.

## 5. Code predicates (frozen736 vs fixture, same logic)

- Frozen input `.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work`: H `70bcdbb8602dd012cd300eba3e9972735ea5dd29e52cfb76e59cee6605230467`, HIGH `9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152`. Fixture HIGH at G5 differs only by G2+G5 comments; H/S differ only by G3/G4 comments. No semantic drift in the checked predicates.
- HIGH `.rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform/scripts/survey_versioned_renewal_v2.py:1952-1998` (`_write_reused_build_record`): `terminal_ref=_resolve_reused_terminal_record` (`:1749-1815`, EDITORIAL terminal or EXECUTED-terminal VERSIONED, REUSED→REUSED walks to terminal, bound 32), `old_epoch=_derive_old_tool_epoch` (`:2000-2032`), `renewal_tools={old, new=basis.current_tool_epoch}` (`:1988`). Writer does not pre-check `old!=new`; H is authority at activate. Finalize therefore writes the orphan R files (expected), activate fails closed `PRESERVED_INCOMPLETE`, State stays r4.
- H `scripts/survey_versioned_renewal_history_v2.py:2326-2471` (`_verify_build_chain_hist`, frozen736 identical at `:2470`): REUSED requires reachable `original_record_ref` in chain + terminal EDITORIAL (`EDITORIAL_PUBLICATION_BUILD_V1`) or VERSIONED `EXECUTED_BUILD` (`:2390-2455`), then `renewal_tools.new==new_epoch` (`:2468-2469`) and `old!=new` (`:2470-2471` `REUSED_BUILD renewal_tools.old must differ from new (genuine Core change)`). U3 terminal `r3 c41159de...` (C1 `EXECUTED_BUILD`) satisfies reachability/terminal; only `old==new` fires. Correct refusal.
- Prepare/finalize do not enforce `old!=new` (prepare checks history non-empty, entry pins, closure; `prepare_renewal:1000-...`). Late `SEAL_BIND/PRESERVED_INCOMPLETE` with orphan R dir + r5 file is the designed fail-closed path, same class as preserved `u1-history-pre`/`u1-current-state` harness probes. An early-prepare refusal for a true artifact-only/unchanged control would be a new HIGH predicate (contract change), not a missing repair for this U3.

## 6. Hypotheses disposition

- Legitimate same-contract Core change misclassified because `old=max-ancestor/current`? Rejected. There was no unconsumed Core change between U2 and U3: G3 (H) + G4 (S) both precede U2; U2 `new=efea07d` already folds both; U3 `new=efea07d` is byte-identical epoch. `old` is predecessor-derived (`efea07d`), `new` is current (`efea07d`); equality is true. U2 (old `5740d67` vs new `efea07d`) passing proves the predicate distinguishes genuine deltas.
- Harness G4 artifact-only/unchanged control that must reject at prepare before writes not late? Not applicable as a product bug here. U3 was intended as genuine second U (`reason=Core change: LONGFORM G4 S comment...`), not an intentional unchanged control, and correctly passed prepare→finalize (basis/receipt/proof/build writes) then failed at H authority. If a future explicit unchanged-control is wanted, it belongs as a new HIGH prepare-time `old!=new` refusal — owner HIGH — but it is not required to explain or fix this status.
- Stale fixture (old bytes, wrong HEAD, style drift, cache)? Rejected. Fixture ancestry `721a04d→381c05f→5740d67→e25a467→efea07d→18587b6`, style pinned, `dst-hash-intended d7d7f6df...` (736), H/S/HIGH pins per README §1, all exits present, live `sys.path.insert(0, root)` fixture-first imports, `TMPDIR` workspace-local, inert origin, no shared writes.

## 7. Concrete fix needed (file + predicate + owner)

- Fix: future LONGFORM C→U→U harness must interleave one genuine tool epoch per U: `G3→U2→G4→U3` (or `G3+G4→U2→G5→U3b` as done). Never `G3+G4→U2→U3` at same epoch. Predicate: `U_n.basis.current_tool_epoch != predecessor.basis_current_epoch` (equivalently `R/build-record.renewal_tools.old != new`) must hold before activate; harness must assert it after prepare (compare `renewal-basis.json:current_tool_epoch` vs predecessor lineage last epoch) and mint a new SOURCE-only fixture commit if equal, instead of proceeding to a known-doomed activate.
- Owner: LONGFORM integration harness/worker domain (`notes/.../longform-integration/run-g34-uu-20261025T060000Z.py:158-208`), not HIGH (`scripts/survey_versioned_renewal_v2.py`) nor H (`scripts/survey_versioned_renewal_history_v2.py`) nor S. No product file change, no schema change, no orphan edit, no `recorded_at`/`supersedes` repair, no rewind of U2/U3.
- If root later wants early refusal: add explicit `old!=new` check in HIGH prepare/finalize pre-write (owner HIGH). Treat as contract amendment with Astra confirmation, not as part of this diagnosis.

## 8. Why G5 was needed (from committed bytes)

Each U requires `old!=new`. After `C1(G2 5740d67)→U2(old 5740d67/new efea07d)`, the chain tip epoch is `efea07d`; U3 at `efea07d` has no delta. Re-sequencing without a new commit would require redoing U2 (forbidden: preserve orphans, no time/supersedes repair). G5 (`scripts/survey_versioned_renewal_v2.py` comment, `efea07d→18587b6`) supplies the missing genuine epoch forward-only: U3b `prior=r4 3f76b3d7...`, `current_tool_epoch=18587b67d2f96e7e5b761712eb5aa5f5ebbb3c9a`, receipt `current_tools=18587b6...`, build `renewal_tools={old: efea07d..., new: 18587b6...}` differ → activate 0 `r6 f76d5552...`, history chain 5 (`EDITORIAL 2bd14fc + U1 f653c92 + C1 c41159de + U2 3f76b3d7 + U3b f76d5552`, `n_bindings 52`), `CURRENT_PROOF_READBACK_OK`, `NO_OLD_STATE_EQUALITY_OK`. C→U→U completes as `r1→r2 U1→r3 C1→r4 U2→r6 U3b` with r5 orphan skipped and preserved. U3b reuses the same prior r4/U2 set as failed U3 (`prior_selected 2cee9de6...`), proving the only missing input was the new epoch.

H/raw code/current fixture known-source epochs bind descriptive proposal only; no PASS claimed. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN remain.
