# H bounded history traversal optimization — AUTHOR traversal-opt (parallel, root FULL operation remains)

2026-10-25. AUTHOR narrow bounded traversal optimization. Human `f84fcf5`. Correct candidate
`.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`,
H before `70bcdbb8602dd012cd300eba3e9972735ea5dd29e52cfb76e59cee6605230467` (3989 lines, batched),
H after `6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad` (4172 lines, traversal-opt).
Other authors untouched: PUB `02f851...`, S `20f63e...`, HIGH `1620b92...`/`9a0469...`, Reader `098a2c...`, schemas unchanged (4 versioned + amended, no uniqueItems/allOf removal, no validator turn-off).

## Scope (root-selected FULL operation remains, this is narrow H-only)

- Read AGENTS (no authority cache), root `7d7d5a45...` §6 (pointer `""`, strict LIVE State, no Path fix),
  contract `478f0051...` §11 (typed history/source/high, exact U/C, proof threading).
- Read ROOT `astra-integration-corrections.md` §Bounded history traversal optimization (this unit's permission).
- H source batched base (70bc...) + traversal-opt: per-PUBLIC-invocation validated SCHEMA node set,
  identity-edge without repeated FULL instance ONLY when independently validated earlier + fresh hash equal.
- Real high24 weekly r1 (chain1, 11 bindings) and r8 (chain8, 82 bindings) + real old R3 graph (r1)
  + source-proof relevant entry (H chain; S file untouched).
- Fresh controlled cProfile + Git counting + full public results equality + event trace, retaining all
  source pins/guard/exits. No old saved-runner execution, no network, no fixture cleanup, no ordinary
  candidate commit.

## Before (batched H 70bc..., 20261025 fresh run on high24 weekly)

- r1: 0.503s, git 3 (show 0, ls-tree 1, cat-file -e 1, other 1), chain1, 11 bindings, PASS
- r8: 28.739s, git 20 (show 0, ls-tree 7, cat-file -e 7, other 6), chain8, 82 bindings, PASS
- Profile: jsonschema 25.8s of 28.7s. Dominant repeated instance validation confirmed:
  `_validate_instance_against_schema_blob` 1360 calls 25.8s, `_check_observed_binding_row_structural` 1460 calls 25.2s,
  `_norm_structural` 21 calls 15.1s. Each unique node validated ~16x repeated across predecessor edges + order re-validation.
- Raw: `before-measure-20261025.json` + `before-profile-r1/r8-20261025.txt` (this dir, H 70bc...).

## Fix (traversal-opt, SAME predicates, graph-node once per PUBLIC invocation, not persistent cache)

- `verify_versioned_history`: fresh `_inv_cache["__validated_schema_nodes"]=set()` every PUBLIC call (resets everything).
  No global/persistent cache, no caller dict/token/skip flag, no cross-invocation permission. Immutable RAW Git
  batch cache unchanged (batched ls-tree/cat-file by OID, per-invocation only); HEAD/dirty never cached.
- New `_mark_validated_schema_node` / `_is_validated_schema_node` / `_check_observed_binding_row_identity`:
  - OWN generation FULL schema always (editorial derive + versioned OWN derive populate validated set after FULL strict validation).
  - Subsequent predecessor-array edges (`_norm_structural` for basis.observed/proof.supported) use identity:
    strict row shape, safe fresh source-byte/ref checks (`_check_authority_ref` live), registered epoch/schema/pointer
    identity, FILE blob SHA/mode via batch, O17 `""` (never `"/"`), finite fingerprints, tool actual field equality.
    Skip repeated FULL `jsonschema` ONLY on validated-set hit + fresh hash equal (live SHA just rechecked + blob SHA/mode just rechecked).
    Cache miss → FULL structural (SAME predicates, no bypass). Can't trust claimed observed: exact equality to independently
    derived accumulator still enforced separately (omission/extra/forged epoch/owner/order), plus direct equality supported==observed.
  - PRIVATE internal expected graph only from actual bounded oldest→newest walk (accumulator); no public verified dict.
  - Malicious swap between first node validation and later repeated edges refuses via fresh live SHA on every edge + final live recheck.
- Order reuse (no repeated FULL): narrow fallback reuses `norm_observed`/`norm_supported` (already FULL validated) for order;
  expected branch reuses `norm_obs_struct`/`norm_sup_struct` (already identity-validated with fresh checks) for order;
  `norm_sup_check` reuses `norm_sup_struct` (same rows, same fresh checks). Same predicates, no bypass.
- Final fresh Evidence recheck before history return: re-reads live bytes for all `ordered_bindings` + prior checkpoint
  (`_check_authority_ref` fresh, no writes). Catches swap after last edge but before return. Own-generation full schema
  and exact H before-digest/Contract8/epoch checks preserved (derive paths always FULL, no recursive new public State/Source/Gate).
- Schemas unchanged (no uniqueItems/allOf removal, no validator turn-off). No new public State/Source/Gate calls.

## After (traversal-opt H 6fe86..., same fixture/pins)

- r1: 0.500s (first after) / 0.272s (test, warm) vs 0.503s before → ~1.0–1.8x (r1 small, dominated by fixed overhead, not regression)
- r8: 3.803s (first after) / 3.690s (test) / 1.440s (perf-test warm) vs 28.739s before → 7.5x–20x faster, git 20 vs 20 (same batch, 462x fewer than pre-batch 9247)
- Gain: r8 28.7s→3.8s (7.5x first, 20x warm), `_validate` 1360→75 (18x fewer), `_check_observed_binding_row` 82 (OWN+editorial derive, graph-node once).
  Remaining ~1.5s is jsonschema for 75 unique SCHEMA nodes (SAME predicates, cannot cache results; validator construction ~1.3s).
  Semantic identity: chain1/11 and chain8/82 unchanged, observed_refs/observed_source_bindings/materialization_lineage byte-identical
  (verified in traversal test + before/after JSON equality).
- Raw: `after-measure-20261025.json` (=before with new H hash/times), `after-profile-r1/r8-20261025.txt` (this dir).

## Tests (NEW independent DBs only, no candidate commit)

- New: `tests/test_versioned_renewal_history_traversal_opt_20261025.py` (4 tests, 20.7s, PASS):
  - `test_01_identity_gain_and_event_trace`: isolated high24 copy, r1/r8 PASS with same chain/bindings/refs/lineage byte-identical to before-measure;
    git <=30, r8 faster than batched before; `_validate` 11 (r1) / 75 (r8) vs before 1360 (graph-node once);
    event trace (monkey-patch `_validate`) proves each unique SCHEMA validated >=once per entry, total == unique SCHEMA (73) + scope/build (2) =75;
    repeat still validates ~75 (no persistent cache returning 0) and still passes; zero-write inventory.
  - `test_02_repeat_after_mutation_refuses`: first PASS chain8, mutate new basis SHA → second refuses (no cached PASS);
    restore basis, mutate old repeated E (scope, part of every expected) → second refuses fresh SHA drift (late swap across repeated edge);
    final live recheck catches swap after last edge; repaired control passes. No writes beyond intentional mutations.
  - `test_03_malformed_schema_first_occurrence_rejects`: tamper scope E to schema-invalid JSON (valid JSON, missing required) → editorial derive first occurrence refuses
    (SHA drift fail-closed for live tamper); direct structural with correct SHA but schema-invalid JSON refuses via `instance fails own recorded schema`
    (proves FULL validation still runs on cache miss, not skipped); repaired control passes.
  - `test_04_claimed_omission_dup_order_foreign_pointer_epoch`: deep tamper basis/proof with rehash (self-digests + record refs so digests pass, H must still refuse via deep equality):
    omission/extra/order (swap first two)/foreign pointer (`/properties/...` inventory)/slash `/`/foreign epoch (`0*40`) each refuse `HISTORY_*`/`UNSUPPORTED_*`
    (late, not digest drift; seal/basis mismatch or basis schema invalid or extra/omission/order/pointer/epoch – all fail-closed); repaired control passes.
- Existing author-H: `test_versioned_renewal_history_author_h_20261025` 5/5 OK with traversal-opt code (7.06s vs 17.9s before, PASS).
  Proves SAME predicates for deep negatives (T1 genuine style-change, T2 NEW63/UNKNOWN, T3a/b/c/d/e scope/selfdigest/extra-keys/pointer/foreign epoch, all late after rehash).
- Existing perf-batched: `test_versioned_renewal_history_perf_batched_20261025` 3/3 OK with traversal-opt code (9.7s, PASS):
  r1 0.155s git3 chain1/11, r8 1.44s git20 chain8/82 (warm, vs 8.9s before), zero-write, repeat passes, negatives refuse.
  Proves SAME batch predicates + additional traversal gain preserved.
- Exits: `test-exits-20261025.txt` (all 0). No full integration, no independent PASS, no CommitPoint.

## Source pins / guards

- Candidate HEAD `409b292...`, fixture weekly HEAD `50b03a6...`, status `??` only (resume packet + new test + H untracked, no tracked mods).
- H before `70bcdbb8602dd012cd300eba3e9972735ea5dd29e52cfb76e59cee6605230467` (3989), H after `6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad` (4172).
- New test `6347d5db4ff7eb6782873803e1ac4a44c2f7bb610e69e3d1b1a194fcf78d2a0e` (398 lines).
- S `20f63e...`, HIGH `1620b92...`, PUB `02f851...`, Reader `098a2c...` untouched; schemas 4 versioned unchanged (basis `76f77...`, set `a759...`, manifest `9d588...`, proof `4c641...`).
- Frozen baseline: `.rephase-1-editorial-runtime/versioned-renewal-combined-freeze-20261025T041436Z/snapshot-work` (735 files, 409b292).
- Own patch: H traversal-opt diff only (see `git diff` in candidate-work, H file only + new test file untracked). New test file independent DB commits only (fixture DBs, never reconstruct DB).
- No network, no old runners, no cleanup of failed fixtures/raw (all scratch preserved under `versioned-renewal-test-scratch-authorH/trav-opt-*` + `perf-batched-*`).

## For root

- Combined final source = frozen baseline (735) + own H traversal-opt patch (6fe86...). New test file for parallel route exec reference.
- Report: exact gain r8 28.7s→3.8s (7.5x first, 20x warm, 895→3 / 9247→20 git vs pre-batch, 1360→75 _validate vs batched);
  scoped tests 4/4 new PASS + 3/3 perf + 5/5 existing OK; failures none (malformed/omission/dup/order/foreign pointer/epoch/late swap all refuse, repaired passes);
  not full integration (no U/C, no renewal→editorial, no normal lifecycle, no regressions beyond H); final H `6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad`.
  No independent PASS, no CommitPoint. Ordinary Commit/Push Human-owned.
