# Partial-tree experiment — `git write-tree --missing-ok` cache-tree enabling normal commit (BOUNDED FIXTURE ONLY)

Root §15 (`astra-operation-resolution.md` §15 FULL read) authorizes narrowly isolated Git-only fixture experiment, not active-repo retry. Active failure raw read only: `artifact-epoch-20261114T123542Z-execution-report.md` + machine JSON + `.commit-stderr.txt` (exit 1, double `invalid object 100644 b797783c401a3d7b5dbdfcb2ef63d7b1d6295740 for sources/2026-W34/architecture-review-attention-v2.json` + `Error building trees`, HEAD still `cc1c7fd1…`, staged exact 2 profiles kept, no new epoch).

## Fixture (OWN, independent, no active mutation)

- Scratch: `/tmp/opencode/partial-tree-fixture-20261114T124450Z` created AFTER `ls -ld /tmp/opencode` verification (20261114T124444Z, git 2.53.0). `git init` empty, no `objects/info/alternates`, `git remote -v` empty (inert origin), `find .git/objects -type f` link count all `1` (no hardlinks), process-scoped `-c user.name/user.email` only, no `git config --global`, no HOME writes, no `--allow-empty`/`--no-verify`/`commit-tree`/network/reconstruct Git. Packet: `notes/rephase-1-repaired-correction-rehearsal-20261112/partial-tree-experiment-20261114T124450Z/`.
- Initial meaningful commit `6bcf79b88a4a8a6cbf3e2179628d8f81826b9a5f` tree `89be4105a433415737c8f2758a8c178e3b5c1d27`, 4 files:
  - `sources/2026-W34/production-profile.json` v1 blob `80c01d8a…`
  - `sources/SP-efficient-llm-2026/production-profile.json` v1 blob `6512e4ea…` (existing other profile)
  - `sources/2026-W34/architecture-review-attention-v2.json` unrelated blob `83335e83803877d05ec9807302847c4042270a13` 131B SHA256 `63d9298d…` (to-be-missing, simulates active `b797783…`)
  - `sources/2026-W34/nested/unrelated-data.json` second nested unrelated blob `233513ee…`
- Sentinel normal `pre-commit` hook in OWN fixture only (no bypass): appends `pre-commit-ran pid=… date=…` to `.git/pre-commit-sentinel.log`, exit 0. SHA256 `197b2b5e…` in `04-hook.sha256`.

## Missing simulation (OWN fixture only)

- Recorded expected OID `83335e83803877d05ec9807302847c4042270a13` via `ls-files --stage` + `hash-object` + `rev-parse` (STEP 05). Preserved original bytes outside DB: `preserved-architecture-review-attention-v2.json` (131B) + `preserved-blob-83335e.loose-object` (118B compressed) + `cat-file -p` text. Then `rm .git/objects/83/335e…` only. Other 8 objects remain. `cat-file -e` exit 1, `cat-file -p/-t` exit 128 `Not a valid object name` (STEP 06b), worktree file SHA still `63d9298d…`. No active/history DB touched.

## Control → plumbing → normal commit

- Updated exact 2 profiles to `fixture-v2-artifact-only` (`f20d28f1…`/`93dad36d…`), unrelated bytes unchanged, `git add -- <exact 2 profiles>` exit 0, `diff --cached --name-only` exact 2, `ls-files --stage` shows 2 new + 2 unrelated (one missing).
- Control normal commit `git -c user.name=… commit -m …` (no bypass) exit 1, stdout empty, stderr exact double `invalid object 100644 83335e… for sources/2026-W34/architecture-review-attention-v2.json` + `Error building trees` — reproduces active failure. HEAD still `6bcf79b`, staged 2 kept. Sentinel DID run once (`563030…124634Z`) — hooks run before tree failure. Expected, not unapproved retry; stopped, no repair.
- Standard plumbing `git write-tree --missing-ok` exit 0, stdout tree `6a903407788eb5fddd5c6bea913303ca6f20c567`, stderr empty. Populates index cache-tree.
- Subsequent NORMAL commit same argv exit 0, stdout `[master 453a1fa] … 2 files changed`, stderr empty. Sentinel second line (`563768…124646Z`, 2 lines total) proves normal hooks executed, no `--no-verify`. HEAD `453a1facc89190e607753482d90763d84328445c`, status clean. No `commit-tree`, no empty, no bypass.

## Verification (no pretend hydrated)

- `HEAD^{tree}` = `6a903407…` exactly matches `write-tree --missing-ok` OID — cache-tree reused.
- `diff --name-only HEAD~1 HEAD` exact 2 profiles, `diff --stat` 2 files, full diff only `epoch: fixture-v1 → fixture-v2-artifact-only` in 2 profiles.
- `ls-tree -r HEAD` retains unrelated missing `83335e…` + nested `233513…` unchanged, plus new `d5c0f53…`/`5521993…`; old `ls-tree` had `80c01d8a…`/`6512e4ea…`. Missing OID retained not replaced/deleted.
- Needed profile blobs `cat-file -t blob`, sizes 142/153, `cat-file -p` bytes match worktree SHA `f20d28f1…`/`93dad36d…`.
- Missing `cat-file -e` exit 1, `-p` exit 128 `fatal: Not a valid object name` after success — integrity still enforced on explicit read, not fully hydrated.
- No alternates, no remote, link counts `1`, index still lists missing OID.

## Result

Supported method: YES — bounded. `git write-tree --missing-ok` (plumbing) + immediate normal `git commit` (hooks) preserves all unrelated tree entries and commits staged-only 2 profiles in partial DB with one missing unrelated blob. Normal hooks proof: YES (2 sentinel lines, control + final, hook script preserved).

Risks / noGo limits:
- New commit tree still references missing OID; any explicit read/checkout of that path still refuses. Do NOT claim hydrated/full-tree clean.
- Proven only for single missing unrelated blob with otherwise intact DB and staged 2-profile delta; not proven for missing needed blobs, multiple missings, tree-object missings, or cache-tree invalidation paths. No broad variants attempted per root.
- Hook ran even on failing control; hook success does not imply tree success. Final hook line plus exit 0 + HEAD/tree/diff binding required.

## Exact proposed new ACTIVE operation (requires root decision, NOT executed)

In selected new rehearsal repo only (HEAD still `cc1c7fd1…`, staged exact 2 live profiles, missing `b797783c401a3d7b5dbdfcb2ef63d7b1d6295740`), with same process-scoped identity/no-config/no-bypass constraints, unique packet raw, STOP on any unexpected:
1. Verify `git status --short`, `diff --cached --name-only` exact 2 profile paths, `ls-files --stage`, `rev-parse HEAD/HEAD^{tree}`, `cat-file -e b797783…` fails, no reset/cleanup.
2. `git write-tree --missing-ok` — capture OID/exit; expect exit 0.
3. Immediate normal `git -c user.name=artifact-only-epoch -c user.email=artifact-epoch@example.invalid commit -m "Artifact-only profile-data epoch"` — no `--allow-empty`/`--no-verify`/`commit-tree`; capture exit/stdout/stderr/sentinel if hook present (active has only `.sample`; do NOT install new hook in active without explicit root auth — fixture hook proof does not transfer).
4. Verify `HEAD^{tree}` equals write-tree OID, `diff --name-only HEAD~1 HEAD` exact 2, `ls-tree -r HEAD` retains `b797783…` unchanged, profile blobs `c2990d4f…`/`9251f487…` exact bytes, `cat-file -p b797783…` still refuses, source773/States/CPs unchanged except new child HEAD/tree. Then normal W34 readback only.

No active Git/index/objects/State/source mutation was performed by this fixture unit. All argv/env/PID/cwd/time/exits/stdout/stderr in this packet (00/02/03/05/06/06b/08/09/10/11/12/13 + sha/sentinel/final files). No subagents used.
