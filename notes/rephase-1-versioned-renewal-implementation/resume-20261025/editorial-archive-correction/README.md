# Editorial archive correction — owned evidence (parallel, no shared writes)

Human continuation, AUTHOR editorial-high integration fix ONLY. Selected contract
478f0051 incl §11, ROOT 7d7d5a45 §6 binding (strict LIVE State, `""` pointer,
no Path fix, no verify_state_basis substitution). Writable candidate
`.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
current H6fe86 P1825dba PUB3f4039 S20f HIGH9a Reader098 (FIXED739) + OWN patch:
`survey_editorial_publication_v2.py` 85814124 (264756B, kind-aware renewal
authoring_refs vs editorial authored_refs, fully validated public renewal
receipt/source-proof/HIST context, no fallback, no raw kind/digest rewrite) +
NEW `tests/test_editorial_renewal_archive_correction_20261025.py` 5e5a0bdc
(5/5 OK). FIXED739 repair snapshot READONLY
`.rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work`
(739 files, dst-hash 20f1967f, H6fe86/P1825dba/PUB3f4039/S20f/HIGH9a/Reader098).

Failure under repair: LONGFORM new public P1→P2R→P2V→P3S63 ALL green on U4 r7/G6
(`longform-integration-repair/run-ed-.../ed-prepare-pub` exit1
`ACCEPTED_DRAFT: before receipt drafting archive invalid` at
`survey_editorial_publication_v2.py:1851-1863`, prior receipt
`VERSIONED_RENEWAL_SOURCE_V1` with renewal `authoring_refs` vs old
`authored_refs` assumption). Weekly extended same paths needed.

Scope: OWN `survey_editorial_publication_v2.py` + NEW dedicated test ONLY.
No H/S/HIGH/Reader/PUB/schema edits. P1/P2R/P2V/P3S only minimal exact necessary
compatibility callers if discovered report ROOT before edit (none needed:
existing public `validate_renewal_receipt` reused, no P1 etc edits). Canonical
old-kind drafting-reference branch unchanged. New editorial receipt STILL old
EDITORIAL kind under NEW63 epoch; P3S staged stays actual newP path + new
retention; closure 63 unchanged (S/H fingerprints existing files only).

Validation (this dir): NEW independent clone valid U4 prePreview +
fixed739+patch SOURCE-only commit → fresh U refresh under new epoch → new
editorial proposal ID P1/P2R/scope/P2V/P3S → real TL2026 build/postrender
QA+review fixtures → finalize→activate→history/current Candidate. Preserve all
failed P roots/old C/old timestamps. New candidate current StyleVariant from
fixture preserved before SOURCE commit (longform b1cbbdd, weekly a4bd), no
old-E style revert. Source 739 base + explicit style variant + patch manifest.
Both routes if possible per invocation; if one full route complete return precise
other pending not 'complete' at prepare only. No source fixture commits
candidate/reconstruct; all GitDB independent/no alternate/hardlink/Gitroot env,
raw guards/exits/PID/per-phase 1200s, fresh Python per Code epoch; no
network/old runners/cache purge/temp cleanup failed. P1 helpers stage valid
3-paragraph/synthesis witness (no genuine approval). No CommitPoint/whole PASS.
Root final State lifecycle separate workers, not duplicated here.

Pins:
- Candidate edpub 85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a (264756B)
- New test 5e5a0bdc9d950c7ef0d409be8fd6245ad8830cf8bcaf001bca429c309f5d57d7 (4521B)
- H 6fe86e78..., P1 825dba1d..., PUB 3f4039fd..., S 20f63eaf..., HIGH 9a0469ef..., Reader 098a2c82... (unchanged)
- FIXED739 dst-hash 20f1967f9f3085bcd3c710ef9ade2c49c594584805b2a004403eb7f59e704283 (739 lines)

Results (this invocation, no CommitPoint/whole PASS):
- LONGFORM FULL (see `codepin.md`, `raw-progress.md`, `run-u5-longform-*/`, `run-ed-lf4-*/`):
  U5 r8 + lf-ed-4 P1/P2R/P2V/P3S63/prepare (OWN fix PASS, EDITORIAL receipt) + QA/reviews +
  finalize seal + activate r9 + State r9 + history/current. Finalize/activate/resume wrappers
  TIMEOUT 1200s (performance, seal/record/State valid, preserved).
- WEEKLY PENDING (precise, not complete at prepare only; see `raw-progress.md`,
  `run-u5-weekly-*/`, `run-ed-wk5-*/`): U5 r7 COMPLETE, wk-ed-renew-5 P1/stage COMPLETE (0),
  P2R→prepare→finalize→activate OPEN (P2R running at invocation timeout). Same OWN fix paths
  (`WEEKLY_GENERATED_V2` branch) pending prepare proof.
- Unit: new test 5/5 OK + P1 dispatch 4/4 OK in candidate-work (no fixture authority).
- Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN, Production semantic NO-GO
  (synthetic, no genuine approval). Ordinary candidate/reconstruct Commit/Push Human-owned.
