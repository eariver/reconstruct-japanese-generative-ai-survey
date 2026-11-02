# Intake — fixed-ref W34 @774 + SP-efficient-llm @c8 (20261101T023147Z)

Owner: General (fixed-material intake only). No subagents.
Authorization: Human 2026-11-01 — Target 2026-W34 + SP-efficient-llm-2026, fixed-ref limited intake of ONLY those editions' Raw, accepted inputs, reader manuscript/PDF and necessary worklogs at `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (W34) and `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4` (efficient-LLM). No current-main follow, Production writes, code adoption, rebaseline, normal Git Commit, readback. Local `/home/eariver/git/japanese-generative-ai-survey` checkout is NOT authorized acquisition method — Explore deviation quarantined below, NOT reused as corpus proof. `gh` API read-only GETs at exact refs only. Frozen final source 138 remains code authority; never adopt remote code from intake.

## What this intake did

- Reused authorized archived bytes (no restore, no child Gitlink fishing, no rerun scripts):
  - `.rephase-1-inputs/774.../sources/2026-W34/` (15 files: profile/state, gates, FROZEN checkpoint, execution index, 2 luna worklogs, 1 review) + `tree.json` (full 774 tree, 3351 W34 paths with blob SHAs/sizes, used for dependency walk without new whole-tree fetch).
  - `.phase-5-inputs/774.../sources/2026-W34/publication/v2/reader-manuscript-v2.json` (19652B, sha256 `c453bea7...`).
  - `.phase-5-inputs/3e3eebe0.../surveys/weekly/2026-W34/main.pdf` (338722B, sha256 `e93db71a...`, blob `a9d0b661...`) + publication-candidate/release-record/merge-verification (historical ref, verified reusable by exact SHA at 774 — no new PDF byte fetch).
  - `notes/rephase-1-profile-support-contract/intake-20261030T124140Z/` 4 docs at c8 (DATA + manifest, `.py` DATA never executed).
  - Notes DM021/DM captures secondary (not corpus proof).
- New minimal network (6 fixed GETs, all within allowed roots `sources/2026-W34`, `sources/SP-efficient-llm-2026`, `surveys/special/efficient-llm-2026`):
  - `acquire-fixed-refs.sh` (fail-closed, read-only `gh api -i`, no git config/auth changes, no push/Issue/Actions, no token in logs; local python only for base64/hash verify, never acquired Python).
  - get01 W34 publication-candidate at 774, get02 W34 release-record at 774, get03 SP sources listing at c8 (20 entries), get04 SP production-profile at c8 (13748B), get05 SP production-state at c8 (7394B), get06 SP surveys listing at c8 (3 entries).
  - Each GET saved `command/url/ref/time/stdout.raw/headers.txt/body.json/exit/stderr`, decoded `DATA.*` where applicable, full SHA256/bytes/Git blob SHA verified against API (see `manifest.json`). All 6 HTTP 200 exit 0, stderr empty. No fallback to different ref. Times in `get0N.time.txt` (2026-11-01T11:33Z run).
  - No PDF/tex/bib byte fetch, no recursive tree, no main/history dump, no extra review/version fetch. Stopped after two dependency sets sufficiently known / specific gaps identified (see `material-sufficiency.md`).

## Verification (hashes after saving, no fake download proof)

- get01: 1504B, blob `6ff5bd37...` (matches `tree.json` at 774), sha256 `df376f47...` (matches historical Candidate raw SHA). Content `candidate_sha256 52c8d0bc...`, pdf sha256 `e93db71a...`, reader-manuscript sha256 `c453bea7...`.
- get02: 736B, blob `a2f40925...`, sha256 `6808dbb0...`. Content `pdf_sha256 e93db71a...`, manifest/merge paths+SHAs match 3e3e historical values.
- get04: 13748B, blob `37be89b9...`, sha256 `22f2e822...` (matches SP state `profile.sha256`).
- get05: 7394B, blob `0c36ec15...`, sha256 `bf209d41...`.
- W34 PDF reuse: local `.phase-5/.../3e3e.../main.pdf` 338722B sha256 `e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de` == expected at 774 (get01/get02); blob `a9d0b661...` == `tree.json` 774 `surveys/weekly/2026-W34/main.pdf` blob. No new PDF ref read.
- W34 reader-manuscript reuse: local `.phase-5/.../774.../reader-manuscript-v2.json` 19652B sha256 `c453bea7...` == expected in get01. No new fetch.
- Transport hash ≠ editorial completeness. No corpus completeness claim from these hashes.

## Read-access deviation — preserved, not intake authority

Explore task `ses_e6b1dbe5fffeyNaEvdeGPvcPkv` inspected edition trees under `/home/eariver/git/japanese-generative-ai-survey` (W33/W34/SP001/named Thematic/Retrospective, selected bytes/hashes/state/approval fields, comparison with fixed snapshots). This exceeded its boundary; read-only does not supply permission. Root has not re-read that checkout and will not repeat access. No content from that checkout was adopted as rehearsal corpus, baseline change, approval or completeness proof. Detailed checkout data is not used to choose target or claim sufficiency. This intake uses ONLY authorized archived captures above + 6 fixed-refs GETs. Do NOT use that inventory as corpus proof.

## Bounds

- This invocation handled MATERIAL INTAKE + sufficiency only. No project code/runtime/test/build/fixture creation, no production execution, no synthetic Gate creation, no imported Python execution, no `git` status/log/HEAD (Human commit readback not performed), no ordinary Commit/Push/Human readback.
- See `material-sufficiency.md` (concrete input sets, reference counts vs Raw proof, missing/permission, reusable products without rebinding approvals, worklogs vs UNKNOWN). Root selects stage rehearsal after this return; do not auto-start runtime or fetch extra asset/ref.
