# H2 correction history — original H draft bytes (pre-H2)

DST: /tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60
Archived: 2026-10-21 H2 start, before any H2 edits.
Rule: preserve initial draft bytes/reports and all pure-check failures before edits.
No rewrite/delete of original packet files. This directory holds byte-identical
copies of H-owned files as they existed at H2 start (hashes below).

Original SHA256 (tool-observed, before H2 edits):
- scripts/survey_editorial_publication_v2.py: 40887b70b9a86d2360cd83ea9b70d239f7da520874b4045107128dca1a277617
- schemas/editorial-publication-source-manifest-v2.schema.json: 494a1d152c76bca810d30e743d567210f130cb4197561d82b276f24ef69441bc
- schemas/editorial-publication-build-record-v2.schema.json: b7c82476047373995cd5c4733ce2ba0b1c53fef72a84bceb26feec9078fea4ba
- schemas/editorial-manuscript-spec-v2.schema.json: 043ce8a565385549265d6666642c2e3ec8ce0d8e8e5544a7eddfb32691478250
- schemas/editorial-toolchain-spec-v2.schema.json: 50b5dc3ee05c496b2c2da13377c5ee0a883dfb52d9b9785189cb00a75d6e4db4
- schemas/reader-manuscript-v2.schema.json: (tracked edit, see DST git diff)
- schemas/reader-surface-gate-v2.schema.json: (tracked edit, see DST git diff)
- scripts/survey_reader_publication_v2.py: (tracked edit, see DST git diff)
- scripts/survey_reader_surface_gate_v2.py: (tracked edit, see DST git diff)
- scripts/survey_weekly_derivation_v2.py: (tracked edit, 22-closure, see DST git diff)
- .latexmkrc: 5 lines, $pdf_mode=4 etc. (control root, not H-owned, unchanged)

Copies in this directory are byte-identical (Write via dedicated editor, no shell
write/clean/reset/commit/network, no import to original src, no bytecode/cache
pollution). Tracked-edit originals are recoverable via HEAD + DST git diff;
untracked NEW originals are copied verbatim below.
