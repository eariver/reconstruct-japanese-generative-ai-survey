# Attempt 07 analysis (exit=1: 3 failures + 2 errors of 32; source freeze identical pre/post)

Four defects across candidate module and test:

1. Module `Collector.safe` resolved symlinks before the alias check, so a
   symlinked authoring input resolved into the repo and passed. Fix: check
   `is_symlink()` on the lexical (unresolved) path first, then resolve and
   re-check (TOCTOU edge) plus containment/traversal/regular-file gates.
2. Frozen-digest kinds for manuscript refs used bare tails (`profile`,
   `architecture`, `approval`), diverging from accepted-ref names. Fix: map to
   `production-profile` / `issue-architecture` / `architecture-approval`.
3. Test ordinary-review construction recomputed `review_sha256` over a dict
   still carrying the old digest key. Fix: delete the key before recompute.
4. Test snapshot windows covered the test's own proposal staging. Fix: refresh
   snapshots after staging, asserting no-write only across P1 calls.
5. Predecessor regeneration via publisher CLI is impossible by design (it
   requires DRAFT_COMPLETE and refuses existing artifacts). Fix: fixture
   replays the exact pass2 producer tail with real producers at VALIDATED_DRAFT
   (strict derivation, same-byte proof, bound review, deterministic render,
   `build_receipt` + schema + full `validate_receipt`, subject QA rewrite).

Rerun as attempt-08 with exclusive outputs; attempts 01–07 preserved unmodified.
