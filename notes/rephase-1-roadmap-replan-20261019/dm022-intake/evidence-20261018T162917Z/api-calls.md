# DM-022 narrow intake — exact API call transcript

Packet: `notes/rephase-1-roadmap-replan-20261019/dm022-intake/evidence-20261018T162917Z/`

Authorization: Human message 2026-10-19 JST — narrow current DM-022 evidence inspection;
no general current-main/code refresh or rebaseline. Read-only `gh api` only.
No production writes, no candidate objects in reconstruct, no commit/push.

Summary path (discovered from prior packet
`notes/rephase-1-dm021-intake/evidence-20261009T171707Z/dm021-source.json`):
`docs/core-v2-deferred-maintenance-summary.md` — unchanged.

## Call 1 — resolve current main (read-only metadata)

```
gh api "repos/eariver/japanese-generative-ai-survey/commits/main" \
  >"$PACKET/main-commit-api.json" 2>"$PACKET/main-commit.stderr"
```

- UTC window: 2026-10-18T16:29:22Z → 2026-10-18T16:29:22Z
- Exit: 0 (`main-commit.exit` contains `0`); stderr: 0 bytes.
- Result SHA: `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`
  (`Merge pull request #567 from eariver/release-record/2026-W41-38651145434`).

## Call 2 — fetch Summary pinned to exact commit (single document only)

```
gh api "repos/eariver/japanese-generative-ai-survey/contents/docs/core-v2-deferred-maintenance-summary.md?ref=c8d0ecc1c9566a2303ad3b4c42635d4b672650e4" \
  >"$PACKET/raw-contents-api.json" 2>"$PACKET/contents.stderr"
```

- UTC window: 2026-10-18T16:29:27Z → 2026-10-18T16:29:27Z
- Exit: 0 (`contents.exit` contains `0`); stderr: 0 bytes.

## Local decode (no network) — byte-exact base64 decode of saved raw JSON

```
python3 - "$PACKET/raw-contents-api.json" "$PACKET/deferred-maintenance-summary.md"
  (assert encoding == base64; assert path == docs/core-v2-deferred-maintenance-summary.md)
```

- Exit: 0 (`decode.exit` contains `0`).
- Reported: `decoded_bytes=72465 api_sha=0a0fe3eb0a8f538a9c8c29455be5cef8f6999d57 api_size=72465`.
- `git hash-object` of decoded file == Contents API `sha`
  `0a0fe3eb0a8f538a9c8c29455be5cef8f6999d57` — content identity confirmed.
- SHA-256: `fa90ce8792440849df765c4fd54485acaa63cf442df979640174678275e668d7`;
  72,465 bytes, 918 lines.

## Call 3 (supplementary, explicitly authorized scope) — Issue #562 metadata+body

```
gh api "repos/eariver/japanese-generative-ai-survey/issues/562" \
  >"$PACKET/issue562-api.json" 2>"$PACKET/issue562.stderr"
```

- UTC window: 2026-10-18T16:29:43Z → 2026-10-18T16:29:44Z
- Exit: 0 (`issue562.exit` contains `0`); stderr: 0 bytes.
- Scope: issue metadata + body only. No comments, events, linked PRs, corpora,
  edition defect records, or workflow runs were fetched. Those remain
  reported secondary evidence cited by the Summary/issue, not independently read.

## Decode/supplied-error note

No decode errors occurred in this intake: both raw responses were valid JSON,
`encoding` was `base64`, `path` matched, and the decoded byte count equals the
API `size`. Unlike the DM-021 intake (v1 decoder no-op failure preserved there),
no correction script was needed. `decode.stdout`/`decode.stderr`/`decode.exit`
are preserved as the exact-run record.
