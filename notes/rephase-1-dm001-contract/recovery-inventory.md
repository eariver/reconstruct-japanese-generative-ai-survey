# Candidate recovery inventory — Astra synthesis of Explore observation

Recorded 2026-10-03T13:05:57+09:00 or later in this session. This is a **summary of Explore's read-only inventory**, not a recreated raw transcript or a recovery run. General's earlier missing-fixture observation remains in [report.md](report.md).

## Observed availability

- The documented `/tmp` assembly/e4/R1/B/A/f1/a1/witness DB paths and `/tmp/jgas-rephase-application-venv` are absent **in this environment**. Their availability in a previous WSL installation or external Human-held backup is unknown; this observation does not establish global destruction.
- No candidate backup/bundle was found in the scoped workspace/known local roots. Two local ignored nested DBs (`.phase-5-inputs/runtime-repair-candidate/.git`, `.rephase-1-inputs/integration-r2/.git`) contain disposable historical identities, not the fixed candidates. Reconstruct's DB does not contain their commits, as required by isolation.
- Reconstruct started at clean Human commit `a6d834be7da6828740bcddd9b63477064015de80`. Root's `a22d693..HEAD` diff-stat shows the preceding assembly closeout (48 paths, 2011 insertions/8 deletions), not a new shipping implementation. The committed packets remain available.

## Durable content chain

| Transition | Durable patch/input |
|---|---|
| fixed baseline → A (includes a1/f1) | `notes/rephase-1-increment-a/application.patch`, SHA256 `0f4bee2c53e96a2f7dd58a76bee2bdc4040e77114f4102ec3523940886d2bb41` |
| A → B | `notes/rephase-1-increment-b/increment-b.patch`, SHA256 `bdff2c296867b31dbc2946526ec97490c054bc48c4ab9a8473eb5ded1248ab81` |
| B → e4 | `notes/rephase-1-gate-cli/increment-gate-cli.patch`, SHA256 `29b7f187417df5f7524087c25a4f0931d4906ba3ffd502104baa59e8cd3cb726` |
| e4 → assembled R1 content | `notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch`, SHA256 `7817fa4fc027ae0bac9bbd7e7bbd18c588ba3373b52e17730eafebe2b92aab01`; assembly packet proves the earlier e4 preimages/application |

These are a content chain, **not a complete Git database or every intermediate commit object**. The R1 patch name's `a1` is its fresh-root basis shorthand, not production a1 ancestry. Earlier f1/a1 full patches and manifests also survive; do not apply overlapping full patches cumulatively. All changed-file copies and recorded final hashes remain evidence inputs. Explore counted a 31-path union; that count is not an application check.

The ignored fixed-baseline cache contains `tree.json` (non-truncated captured API listing, 34,155 entries including trees) and a sparse subset of files. It is not a hydrated Git tree. Exact commit metadata for several A/B/e4 ancestors is missing. Re-creating a matching tree or even one commit object would not restore its complete ancestry, historical receipts or missing promisor blobs. No exact-481 restoration was attempted or proved.

## Static source fallback used now

The two Freeze scripts and relevant tests/workflow/schemas are unchanged across the saved chain. General hash-compared cache/snapshot bytes to selected baseline-listing entries and saved nine byte-exact files in [fixed-content](fixed-content/SOURCE-BINDING.md). Changed stage/reader/controller bytes are referenced from their committed B/R1 packets. This permits **packet-bound static analysis**, not live-481 verification. The selected-entry extract preserves observed path/blob bindings but is not a full Merkle proof of the production tree; source-copy hashes alone do not prove parentage.

## Next executable unit

Use the [Astra decision](../../outputs/rephase-1-dm001-019-contract-decision.md). Existing `restart-context.md:53–61` permits General isolated fixed-baseline recovery under an Astra task; the initial Worker's Human-only recovery wording is superseded by its correction. No extra Human approval ceremony is introduced.

First prefer an actually available fixed DB/backup, verified without mutation. If none exists, inventory and reconstruct explicitly from **774dd39a only + the durable chain**, in a new independent DB, inert origin after acquisition, no hardlinks/alternates/inherited Git-root overrides. Record any new identity as new; do not forge/backdate commit metadata to claim 481. Preserve full tree references where feasible; materialize only justified required assets and disclose closure gaps. No current-main refresh or production checkout repair. A synthetic fresh-root fixture cannot stand in for the assembled candidate without a separate explicit design decision.

General must return recovery/source-equivalence/runtime prerequisites and fresh affected verification proposals to Astra **before DM-001/019 code**. Recovery and its affected verification deserve their own bounded Commit Point. Subsequent implementation uses the newly established identity and fresh evidence. Saved runners are evidence only; do not execute their fixed paths or overwrite their output files. Plan durable independently restorable candidate storage/backup and verify its scope rather than again relying solely on `/tmp`.
