# Re:Phase 1 Increment A evidence packet

This packet records the isolated Sol Co-Worker implementation of exact stage-selected Reader Manuscript admission. It is evidence for Astra review, not adoption authority, independent acceptance, whole-B3 closure, application readiness, or a canonical Human Gate.

The fixed local candidate is `1a9649129d1745fed0b98db46ef15f014407e6fc` (tree `5e933aa54034ed227216252a2c8707a59f293acf`), with f1 parent `bf32edf98ba8f605169d7188bbc764de74ee4f6e`. The fixture is `/tmp/jgas-rephase-increment-a-sol-copy` on local branch `codex/rephase-1-increment-a`, with inert origin `https://example.invalid/rephase-increment-a.git`, no alternates, no inherited Git-root environment, and no multiply linked Git object files found.

The change makes the Reader-Surface Gate validator require one manifest surface and one primary surface, binds them to the caller-selected manifest and its primary reference, forwards the exact manifest from both active stage sites, and validates the exact Gate/manuscript pair before publication revalidation writes authority. Standalone Gate inspection retains its own unique recorded-manifest fallback.

Exact-head verification:

- Dedicated Increment A module: 11 test methods, 11 passed, 0 failures/errors/skips reported. The unique-surface method contains 6 passing subtests: missing, duplicate, and conflicting manifest/primary cases.
- Affected existing modules: 61 tests, 61 passed, 0 failures/errors/skips reported.
- Separate f1 parent witnesses: 4 tests, 4 expected failures, exit 1. Each failure says the expected stage or revalidation exception was not raised, demonstrating wrong-manuscript acceptance at both stages and both revalidation boundaries. No witness failed from an unknown keyword or setup error.

The fixtures use synthetic research/editorial/visual/Human records. They prove exact admission using schema-valid Reader Manuscripts and real validators, not real publication approval. The inherited revalidation fixture's reader input uses `final_summary` rather than the publisher's `final_summary_paragraphs`; it is not a complete publisher-valid reader input and does not prove Increment B, derivation, supporting semantics, all profiles, publication, or B3 closure. The candidate remains partial B3 only.

`increment-a.patch` is the f1-to-candidate delta. `application.patch` is the fixed-production-baseline-to-candidate patch. `candidate-files/` contains exact full snapshots of all four files changed by Increment A. Raw combined stdout/stderr, commands, runtime, isolation checks, and failure history are preserved alongside them.
