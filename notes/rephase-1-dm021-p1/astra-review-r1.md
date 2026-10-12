# DM021-P1 initial implementation — CHANGES_REQUIRED

2026-10-12 JST. Root read actual module801 lines/schema/test867 lines/report and independent review. Independent frozen-membership defect is accepted, but the following additional source/oracle gaps are blocking. Preserve all Phase-B attempts, final32 raw, current four P1 source bytes/full13-path patch before correction. No change to the selected 3A1M runtime budget.

## R1 — frozen membership AND full graph/retention completeness

`_frozen_member_kind:324–327` partitions once, so `head` can never equal `receipt:accepted`/`receipt:authored`. Fixing that alone is insufficient: the prefix table also wrongly classifies mutable publication-authored input as frozen. Explicitly enumerate accepted research/Architecture/Draft/Synthesis/Evidence/etc kinds, include the Draft authored archive, exclude publication authoring archive and all State/QA/tool/current-publication metadata. Preserve all applicable frozen logical roles, not an arbitrary first role.

Graph currently omits live State node, all predecessor links beyond the active record, checkpoint/upstream local dependencies not in receipt.accepted_refs (including accepted Evidence package/tasks, screening/views/completeness/selection and required upstream authority records). Later review refs are appended as edges without complete equality to the selected effective manuscript/source/PDF; bundle source/Profile/PDF edges are missing. Candidate path483 is wrongly derived from `profile.path.parent.parent` (for normal Profile it drops the issue); only3 candidate SHAs are compared, not paths/bundle/later reviews. Fix from validated Profile source_root and existing canonical/actual validators. Unknown/mismatched Candidate stops; no ownership inferred.

Retention wrongly excludes later semantic/visual reviews from `mutable`, and defaults old publication authoring archive/pre-TeX review/Candidate to KEEP. State adoption also changes State. Classify the selected OLD MUTABLE publication/State artifacts as COPY; immutable research/checkpoints/prior revalidation records/tools are KEEP. Keep original historical checkpoint row hashes as metadata, not live nodes requiring superseded bytes. Walk the complete actual State-bound predecessor chain with bounded cycle handling, not directory recency.

Add exact expected-role/path-set and digest-membership oracles, not only node_count>20 or containsProfile/Architecture. Assert frozen digest excludes each operational class and includes all actual required upstream kinds. Test union roles and HASH/POLICY conflict refusals. If a required transitive local edge cannot be safely classified, return that exact blocker rather than drop it or invent a generic resolver.

## R2 — proposal binding is incomplete / returned object silently repaired

Schema lacks the selected persisted `proposed_reader_ref`; `active_revalidation_ref` must be required nullable. Remove undocumented singular `role` from retention rows, keep sorted plural roles; enforce policy-specific retained_ref XOR retained_dest. `_pipeline` must produce the planned canonical proposed-reader path/hash from independently derived bytes.

`validate_proposal:779–791` compares only basis/retention, ignores supplied top-level issue/research/publication fields, authoring ref PATH and proposed canonical digest, then inserts new reader-ref/hash fields not allowed by its own schema. It can return REVIEW_BOUND_PROPOSAL for a mismatched proposal header/ref. Compare ALL derived identity/ref/digest fields; do not repair supplied claims. Require exact canonical proposal directory under validated source_root (checking only final2directory names is insufficient), safe files, exact supplied refs and FILE bytes. Return an unchanged schema-valid proposal + separate measured binding data if needed.

Keep author-supplied nonempty change_description as descriptive input, not machine approval; it need not equal a generated placeholder. For simplicity require the supplied authoring file already at the named proposal `authoring-input.json` when preparing; fixtures/operator prepare that input outside P1, P1 writes nothing. This avoids the tests' current external-path ref copied to a new path and silently accepted by digest alone. Plan reader ref may remain prospective until validate requires the file.

Add forged-header, same-byte wrong-authoring-PATH, wrong proposed-digest/ref, missing-nullable, wrong directory, extra/omitted/conflicting retention cases; ensure no returned proposal differs from the supplied document to manufacture success.

## R3 — path safety / canonical State / token rules

Collector.safe resolves BEFORE traversal/ancestor checks; its `..` check on resolved parts is ineffective, and directory aliases aren't rejected. Config is read/hashed before safe handling. Normalize root once, raw-check lexical traversal/leaf+ancestor aliases before any read, require regular files (no FIFO/device), pin exact bytes; reverify path safety/type too, not only bytes through a possibly replaced link. Enforce State path equals the Profile/config-derived canonical authoritative State path — an unreferenced regular-file clone of valid State is not live State authority.

`PROPOSAL_ID_RE.match` accepts a trailing newline via `$`; use true full-match/strict terminal grammar. Retention destinations need raw ancestor checks even when absent; namespace must not overlap current inputs or existing target aliases. Add inside-root traversal, ancestor alias, outside unreadable/FIFO sentinel, shadow State and trailing-newline token controls through PUBLIC APIs.

## R4 — snapshot is CWD-dependent and incomplete

`_tree_map:145` resolves Profile-relative roots against PROCESS CWD, not repo_root. Current fixture calls can compare empty unrelated trees. Correct this or replace the product-wide directory walk with an explicit COMPLETE typed consumed-dependency snapshot; tests still inventory owned trees. Never open undeclared FIFO/device nodes or silently skip symlink directories in a supposed complete inventory.

Pin required dependencies before their actual consumption, not merely after validators have already used changed data. Recheck after scope validation too (current tree check ends inside `_pipeline`, before `_validate_scope`). Verify all-control-root/current receipt predicates again before return: HEAD/config alone does not catch a dirty unlisted helper/schema after initial receipt validation. Compare proposed accepted_refs/Draft archive/Architecture authority to the before context, not only receipt vs before context. Use real rederivation/validators without pending/fake State. Add mutation seams for actual upstream/container/record/control/scope bytes at late phases, with explicit injected delta separated from forbidden writes.

## R5 — test strengths and predecessor attribution

Current predecessor changes an EMITTED TeX comment and manually regenerates source/QA then calls the real generic Core-change adoption API. That can be a useful honest generic Core-change fixture, but it is **not R1 same-byte mechanical refresh** and does not exercise R1 owner. Relabel it; add the selected real R1 owner with a non-emitted derivation-file-only source commit and unchanged reader/output bytes. Prefer two successive supported refreshes on one fixture to exercise actual supersedes chain and original-vs-active differences. No fake pointer/reason/State, no empty commit. If R1 cannot be constructed, stop with the exact gap rather than claiming equivalence.

Most current negatives restore/delete mutations BEFORE the sole aggregate no-write comparison (`test_weekly...`, matrix). Put file/directory/symlink/Git snapshots immediately around EACH call after setup/fault mutation, before cleanup, recording deliberate injected changes precisely. Add REQUIRES_OWNER_DECISION, wrong AFTER binding, artifact-only commit allowed vs control drift refused, optional Candidate healthy/stale, predecessor chain retention and exact frozen-set completeness. Retain ordinary-review compatibility and genuine synthetic scope binding; no semantic/publication acceptance claims.

## R6 — evidence and packaging

Final source/pins at the new hash require fresh focused tests and only justified affected controls; old32 is superseded. Strict runner pre+finally-post must compare all13 declared hashes/modes/status/base and reject routing/optimized safety bypass, exclusive logs with actual exits/timeouts. Preserve every failed/setup attempt; do not overwrite executed scripts/logs.

Complete13path patch must actually apply AS SAVED (`git apply --check` + apply) to a NEW independent actual409 baseline copy, then full hash/mode/status comparison. Reconstructing new-file text from patch is not complete Git patch-application proof. To avoid unnecessary archive restoration, a new independent byte-copy of the existing restored DB may be made and ONLY known declared overlays removed/reverted in THAT disposable copy to its existing409 HEAD after verifying contents/isolation; preserve the active source and all prior inputs. No candidate commits/branches, network or protected-DB changes.

Return corrected implementation/report/raw evidence for root and the same author-independent reviewer. No extra Source/State/reason/approval runtime scope; DM021 stillOPEN, wholeNOT_READY.
