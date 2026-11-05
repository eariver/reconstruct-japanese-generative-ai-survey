# current-observation correction addendum r3 — 4 SHAs + tree (no Git, no reconstruct readback)

2026-11-04. SP preparation/operation owner. **Old `current-observation.json` preserved untouched; do NOT use its 4 corrupt pins as authority. NEW `current-observation-r3-20261104.json` 22708B `3f350e3a86122a3a94d5745a46c5ebdb2e454939b76697ff7b459e1b180a179b` is machine authority for r3.**

Independent review (`reviews/sp-disposition-plan-r2-independent-review-20261104.md` §2 + findings `B1`) found 4 wrong-length/wrong-byte SHAs + 1 short tree in old JSON (machine `sha256sum` authority only). Re-observed NOW via stdlib `hashlib.sha256` + `os.lstat` (no project import, no Git, no reconstruct `git -C .`, no network/Production checkout, no active writes). Hex length validation: file SHAs must be exactly 64 hex `[0-9a-f]{64}`, commit SHAs 40 hex, Git tree 40 hex. Programmatic check confirms old file had 57/61/65/62-char file SHAs + 36-char tree (all invalid); NEW file has zero non-64/40 hex strings.

## Corrected pins (active e84 files, `isfile true`, `islink false`, mode `0o664`)

- SP State `sources/SP-efficient-llm-2026/production-state.json` 3454B: OLD `4865998b99ab2902954619b2a7761c4ae0de77695b6d25d49dff4eb89` 57 chars (corrupt, dropped `06ddd5b5e25`) → NEW `4865998b99ab2902954619b2a7761c4ae0de77695b06ddd5b5e25d49dff4eb89` 64 chars, valid hex64, `nlink 1`.
- W34 supplement `sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json` 389414B: OLD `ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b6b6b8f0fbc704e` 61 chars (corrupt) → NEW `ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b14b6b6b8f0fbc704e` 64 chars, valid.
- W34 audit `sources/2026-W34/evidence/v2/accepted/bf208f96d6b66e257c80af3b1bf3d85cdc8c6b63178ace7dbe292624aa8559d2/interactive-audit.json` 1041B: OLD `0a41ec9dce66337d6cf3cfb5431a7defa0408f7ccab0b5253e3c78a77b8de7fe5` 65 chars (extra byte) → NEW `0a41ec9dce66337d6cf3cfb5431a7defa0408f7ccab0b525e3c78a77b8de7fe5` 64 chars, valid.
- SP audit `sources/SP-efficient-llm-2026/evidence/v2/accepted/09f487ab1ecb6dc7dd3851ba8791c02fba85d6ecb0d0aac834432a3b701b8e2f/interactive-audit.json` 1145B: OLD `890a43239dacd50f867f43a672798c40e735a42dc1830a5427036f5f3dcaad` 62 chars (missing `e`) → NEW `890a43239dacd50f867f43a672798c40ea730435fdc1830a5427036f5f3dcaad` 64 chars, valid.

All other file/contract pins in old JSON were already 64/40 hex and match active files (770/771 source comparison, State/Profile/DCP/SCP/Ledger/Completeness/Evidence/Views hashes in `current-observation.md` §§1-4 re-verified; no change in r3 except the 4 above). Real State/contract/pins in r3 bind real active files, not old corrupt data. All r3 guards/manifests MUST bind NEW 64-char hashes, never printed prefixes (`ee13b8ee...` etc. are shorthand, not authority).

## Tree identity (no Git run, no reconstruct readback, no invention)

- OLD `active_instance.recorded_tree` `fb8e536ed2860acef8feb2eac7992a69e3ae` 36 chars (invalid; Git tree must be 40 hex).
- Saved raw packet `notes/rephase-1-evidence-scaling-repair/real-w34-retry-20261103T172327Z/artifact-manifest.json` `tree` = `fb8e536ed2860acef8feb2eac7992a69e4b03ae9` 40 chars, valid hex40 (packet DATA, recorded at e84 creation, NOT Git run now, NOT reconstruct readback, NOT active Git).
- NEW r3 `recorded_tree` = saved-raw 40-char value above, provenance explicitly `saved-raw packet, hex-validated, no live-Git binding`. No Git invoked now (active e84 isolated Git ONLY if later actual operation needs it; now file-read/data generation only). If Root requires live-Git tree binding, authorize explicit isolated `cwd=.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work git rev-parse HEAD^{tree}` later; do NOT run `git -C .`.

## Preservation

Old `current-observation.json` + `current-observation.md` preserved untouched (evidence of deviation, per review). NEW file + this addendum are r3 authority. No active State/products/source writes, no Raw staging, no imports/runtime execution in this correction (stdlib hash/lstat only). W34 State `7e6a50c2...` was already 64 and unchanged.
