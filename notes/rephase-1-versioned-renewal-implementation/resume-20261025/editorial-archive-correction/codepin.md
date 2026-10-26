# Code pin — editorial archive correction (OWN fix)

- Writable candidate `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
  (HEAD `409b292`, no commits, 39M+50U+1newU intended):
  - H `scripts/survey_versioned_renewal_history_v2.py` `6fe86e78...` 288349B (unchanged)
  - S `scripts/survey_versioned_renewal_source_v2.py` `20f63eaf...` 127981B (unchanged)
  - HIGH `scripts/survey_versioned_renewal_v2.py` `9a0469ef...` 202862B (unchanged)
  - P1 `scripts/survey_editorial_correction_proposal_v2.py` `825dba1d...` 158652B (unchanged, strict new-kind dispatch already fixed)
  - PUB `scripts/survey_publication_v2.py` `3f4039fd...` 125977B (unchanged)
  - Reader `scripts/survey_reader_publication_v2.py` `098a2c82...` 46395B (unchanged)
  - OWN `scripts/survey_editorial_publication_v2.py` `85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a` 264756B
    (was FIXED739 `3fd26901...` 256672B; +8084B explicit kind-aware renewal
    `authoring_refs` vs editorial `authored_refs`, fully validated public
    `validate_renewal_receipt` + `authoring_refs`/`accepted_refs` selection,
    no `.get(a) or .get(b)` fallback, no raw kind/digest rewrite, canonical old
    branch unchanged, new EDITORIAL kind under NEW63, P3S staged newP path +
    new retention, closure 63 unchanged)
  - NEW `tests/test_editorial_renewal_archive_correction_20261025.py`
    `5e5a0bdc9d950c7ef0d409be8fd6245ad8830cf8bcaf001bca429c309f5d57d7` 4521B, 5/5 OK
    (fail-closed kind/authoring/arch, no fixture authority)

- FIXED739 READONLY `.rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work`
  (739 files, dst-hash `20f1967f...`, H6fe86/P1825dba/PUB3f4039/S20f/HIGH9a/Reader098,
  edpub old `3fd26901...` preserved, not modified)

- No H/S/HIGH/Reader/PUB/schema edits. P1/P2R/P2V/P3S no edits (existing public
  `validate_renewal_receipt` reused; if compatibility callers needed, report ROOT
  before edit — none needed). Closure S/H fingerprints existing files only, no new
  module budget change (HIGH/history/source already in 63).

- Source intent: 739 BASE + explicit fixture style variant (longform `b1cbbdd...`,
  weekly `a4bd...`, not baseline `035645...`) + patch manifest (edpub 85814 + new test 5e5a).
  New candidate current StyleVariant from fixture preserved before SOURCE commit for U input;
  no reverting old E style.
