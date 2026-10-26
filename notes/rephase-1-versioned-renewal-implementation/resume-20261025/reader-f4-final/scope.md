# Reader F4 final — scope (TEST-only, no runtime edits)

- Candidate: `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
  HEAD 409b292756dd1277b9dfae87679934c0d2ce251c (actual409), dirty M/U (test-only).
  Reader fixed 098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c.
  Source H74275d22a342 / S2290ddd0dc83 / HIGH1dad1ad12ba50 / PUB3f4039fd76 / edpub85814124 / P3S9e2a0ad6b42.
  Tested file `tests/test_versioned_renewal_reader_f4_20261025.py` v6 SHA 63323adc839b31826daf0d45c04b33d3799052f8bd58bad6cda9373cdbf3f36a.
- Fixture src (genuine, no foreign high24):
  weekly `.rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly`
  HEAD 6141dad65f985f246cd6cbd766d1afbf250ab296, Reader 098a2c82 at all epochs.
  Epochs from recorded basis current_tool_epoch (no checkout original):
  U1 G1 85eac6f4e2c042c45603552a729770683982c7be,
  C1 G2 cec67e52ca689933977e717dd89066dc96161086,
  U3 G4 296c46072e1009511058ee444bb97639f57647c1.
  Real C build fixed TL2026 recipe, synthetic reviews labelled not genuine, no stub HIGH/S/mocked validators/fake epochs.
- Isolation per case: git clone --no-hardlinks + untracked/ignored E copy (excluding pycache/pyc, SHA verified),
  inert origin example.invalid, no alternates, checkout epoch in clone only, original HEAD verified pre/post.
  Child fresh python cwd/PYTHONPATH=clone, public validate_manuscript_manifest, module __file__ under clone guard.
  Mutations only NEW owned clones/unique owned files (f4-neither-tmp, f4-sibling-tmp + sibling proof), exact repair.
- 7 cases:
  1. canonical no-field healthy (U1 epoch G1, no proof) → PASS.
  2. canonical+renewal context refusal (U1 epoch G1, canonical + U1 proof) → REFUSE REVIEW_TARGET_MISMATCH.
  3. correct C embedded own proof healthy (C1 epoch G2, C1 + C1 proof) → PASS.
  4. C delete embedded+rehash without stored proof (C1 epoch G2, tmp neither + C1 proof) → REFUSE REVIEW_TARGET_MISMATCH.
  5. wrong foreign/sibling proof even equal bytes (U3 epoch G4, tmp sibling-embedded C + U3 proof) → REFUSE lineage-reachable (not drift).
  6. U editorial stored old + current external healthy (U1 epoch G1, editorial + U1 proof) → PASS.
  7. U-after-C stored ancestor + current U healthy (U3 epoch G4, C1 + U3 proof) → PASS.
- Run: 1200s bound, PID/heartbeat/terminal exit guard, no network/old-runner/cleanup/ordinary commit.
  7 actual methods, no skips. No whole PASS/CommitPoint claimed here (test-only).
