# Evidence preservation — limitations and deviation record

## What was overwritten or lost
- During earlier correction work this session, `correction/round3/` evidence
  files were re-anchored in place from `20177a1` to `57853cb` (manifest,
  results, commit-evidence, four suite logs) without separate filenames. The
  original `20177a1`-anchored raw log bytes are therefore NOT recoverable as
  raw logs and are NOT reconstructed here; no summary is presented as raw
  output. What remains fully recoverable from immutable Git objects
  (`20177a1`, `57853cb`): all source diffs and file contents for both states.
- No prior packet was touched: `correction/` top-level 269c-era files
  (`manifest.json`, `correction.patch`, `correction-final.patch`,
  `changed-files/`, `final-batch1.*`, witness files), `correction/round2/`
  (8a544f9 matrix, patches, copies, manifest), and all fixture branch commits
  remain byte-identical (verified by listing; round2 `changed-files/` copies
  hash to the 8a544f9 blobs).

## What was archived
- `correction/returned-57853cb/` is a bit-identical copy of `correction/round3/`
  as found (21 files), plus `SHA256SUMS.txt` covering those 21 files (the
  SHA256SUMS file itself excluded). It protects the 578-anchored evidence
  against any later move; `correction/round3/` itself was left untouched
  afterwards.

## Current-round rule (followed)
- No existing evidence file was overwritten this round. All new evidence lives
  under new unique dirs: `correction/final-b74db67…/` (this successor) and
  `correction/returned-57853cb/` (archive). Pre-existing dirs were refused
  before creation (verified absent first).
- No saved scripts write into existing evidence dirs: the reused read-only
  runner takes an explicit new log path per invocation.
- All report numbers below are observed, not recollected: HEAD/tree/parent from
  `git rev-parse`/`show`; blob IDs from `git ls-tree`; sizes from `wc -c`;
  worktree hashes from `sha256sum`; patch hashes from `sha256sum` of written
  files; test counts/exits from the durable logs' own `Ran/OK/EXIT` lines;
  commit dates from `git log`. Ranges: prior delta `57853cb..b74db67`;
  final full `a1a4242..b74db67` (known fresh root `a1a4242`, not e4 ancestry;
  41 historical data blobs remain unverified per intake).

## Limits
- Durability covers committed Git objects + the new unique-dir files. Re-running
  historic states would produce new evidence, not recover old raw logs.
- No independent PASS is assumed at any stage; the independent reviewer judges
  from `8a → b74db67` full resolution plus these packets.
