# Capture log — single-document intake 2026-10-03 (session label, not timing authority)

Real clock: `2026-10-03T03:51:24Z` UTC / `2026-10-03T12:51:24+09:00` at start.
Fetch window: `2026-10-03T03:51:44Z` (UTC_START=UTC_END, script-recorded).
Fixed production baseline (unchanged): `774dd39a951c9ac3818e83dfffd4c7666efb0a20`.

## Authorized scope

Human authorized ONE latest observation of production
`eariver/japanese-generative-ai-survey`
`docs/core-v2-deferred-maintenance-summary.md`, newer than saved
`f85539c31a079ab7a7fa86185f3cbb0fcad0485a`.
Exactly two read-only GitHub API calls were made, both via `gh`:

1. `gh api repos/eariver/japanese-generative-ai-survey/commits/main --jq '{sha, commit: {message: .commit.message}, parents: [.parents[].sha]}'` — main resolution, metadata only. Exit 0.
   Observed: `d6381568cc897a47d6de992189e20339350342b7`, message `Merge pull request #558 from eariver/docs/core-v2-deferred-maintenance-w39-closure-20260930 / Docs: update Core v2 deferred maintenance through W39`, parents `239ef2703a93fa802f232978c7166d04d6cc3d49` + `2ca12b787d3e943e4f93fa23e197fffe93ac31d4`.
2. `gh api "repos/eariver/japanese-generative-ai-survey/contents/docs/core-v2-deferred-maintenance-summary.md?ref=d6381568cc897a47d6de992189e20339350342b7"` — the single named-document fetch at that exact SHA, inside `acquire-single-document.sh`. Exit 0, stderr 0 bytes (`fetch.stderr`, `fetch.exit` preserved).

No general main tree/code listing, no linked Issues/PRs/primary defect records, no checkout/fetch/clone, no production writes, no rebaseline. No re-fetch after successful capture.

## Why shell subprocess was necessary

The Contents API returns JSON with a base64 `content` field. Only a byte-preserving base64 decode yields the exact source bytes. `acquire-single-document.sh` (preserved as evidence) performs the single `gh api` call, saves `raw-contents-api.json` (77,132 bytes, SHA-256 `8fe4b02fd4c044b29d3b5b30d1701aacf710e9d01f5a414b0d86cffe7144f78f`), then decodes exactly once from the saved JSON via python3 `base64.b64decode` into `deferred-maintenance-summary.md`. That decoded file was never created or altered through text editing; text tools only read it afterward for delta analysis.

## Pinned identities (new snapshot)

- observed `main`: `d6381568cc897a47d6de992189e20339350342b7`
- document Git blob SHA (`git hash-object` == API `sha`): `ad86f1f2754366a0b30200c6b229121ba9290095`
- SHA-256: `a30ee17c309d96e0b59a4991a9a9d4a6cfc4d1407ad625589e932633c02bcb95`
- size: 55,021 bytes (API `size` agrees), 799 lines
- decoded URL: `https://github.com/eariver/japanese-generative-ai-survey/blob/d6381568cc897a47d6de992189e20339350342b7/docs/core-v2-deferred-maintenance-summary.md`
- `.gitattributes` read (no edit): existing `-text` rules cover `phase-5b`, `rephase-1-increment-a/b`, `rephase-1-gate-cli`, `rephase-1-weekly-regeneration`, `rephase-1-mechanical-refresh`, `rephase-1-r1-assembly`. The NEW `notes/rephase-1-deferred-intake-20261003/` directory has no `-text` rule; per instruction no entry/handoff/gitattributes edit was made — Root/Human to decide byte-protection.
- Tool note: instruction said "use apply_patch for file edits". No `apply_patch` tool exists in this environment; only NEW files were created via `Write`, zero existing files edited, so no reconstructed-byte risk to existing evidence.

## Files in this packet

- `deferred-maintenance-summary.md` — exact decoded bytes (script-written only)
- `raw-contents-api.json` — full API response (single fetch)
- `acquire-single-document.sh` — acquisition script (evidence)
- `fetch.exit` (`0`), `fetch.stderr` (0 bytes)
- `deferred-maintenance-source.json` — source pins
- `capture-log.md` — this file
- `delta-analysis.md` — old-vs-new comparison + Re:Phase mapping + recommendation

## Verification performed locally (no network)

- `git hash-object deferred-maintenance-summary.md` == API `sha` `ad86f1f2...`
- `sha256sum` / `wc -c` recorded above; old snapshot re-hashed to confirm `ace0d9a9...` / 24,234 bytes / 496 lines.
- Local `diff -u` old-vs-new: 327 added / 24 deleted lines across 505 diff lines (see delta analysis). Linked production records were NOT opened to verify Summary claims.
