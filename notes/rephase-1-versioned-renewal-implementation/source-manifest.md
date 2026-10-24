# Versioned renewal M1 — source/manifest/isolation record

- Date: 2026-10-24. Reconstruct HEAD c5b0d7cff9f978a2823f9a9e00ae1e0f9d5b3e1f (Human commit, clean).
- Proof input: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
  HEAD 409b292756dd1277b9dfae87679934c0d2ce251c, tree 8ce3699861505f32d1d60bdc185d4d6f635aeda2b (actual409 +57).
  `git status --porcelain=v1` pre/post identical M list (57 intended, no new writes to proof-copy).
  Full patch 659063dc27f0926aaf6d.../2018112B DIRECT409 per editorial packet (not re-applied; available proof-copy preferred).
- Isolated workspace: `.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work/`
  rsync without .git/__pycache__/*.pyc; independent `git init -b main`, inert origin example.invalid, no `objects/info/alternates`, no hardlinks (verified distinct inodes 21530788 vs 21529959), no GIT_* env, no inherited GIT_DIR.
  Isolated HEAD a8890d4ff612563e71b7dcf5db76287acfe4ea35 (3 fixture commits, no --allow-empty, code committed before authorities).
  `git status` clean (pycache residue removed, not source). No Git DB in notes/.
- Changed files (M1):
  New schemas 4: versioned-renewal-basis/source-proof/source-manifest/publication-set.
  Amended schemas 5: reader-manuscript, publication-candidate, quality-bundle, reader-gate, revalidation.
  New modules 3: history/source/high.
  Consumers: publication_set, reader_publication, publication, quality, gate, staged, weekly_derivation, longform_generated, editorial_publication, config pipeline, test_group_c, new test_m1.
- Pre/post hashes: isolated base = proof-copy applied state (409+57) plus M1 deltas above; exact per-file SHAs in isolated DB (`git ls-files -s` + `git rev-parse HEAD`). No full57/721 inode recertification claimed; partialDB/missing26309/runtime/TeX limits retained.
- Raw outputs/child exits recorded: `python3 -m unittest tests.test_versioned_renewal_m1 -v` exit 0 (7/7 OK); closure python snippet exit 0 (63/63/66, 29/34, 71); `git diff --check` clean in isolated workspace (verified before commits).
- Full-chain restore NOT executed (input available; new safe procedure required only if absent, root return first).
- Ordinary candidate/reconstruct commit/push forbidden; isolated fixture commits permitted/required before authorities (done). Human Commit Point preserved.
