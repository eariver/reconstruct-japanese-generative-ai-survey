# DM021-P2V Phase A — read-only source binding (direct observations)

2026-10-15 JST. General Phase A, read-only. No code/tests/fixtures/copies/restores/execution/imports/commits/network. Only NEW files in this packet are `interface-proposal.md` + this file. All Git via sanitized env (`GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`, all inherited `GIT_*` removed). Python byte/hash/mode reads via stdlib only, no candidate-module imports, no cache execution.

## 1. Reconstruct identity (sanitized, all rc=0)

In `/home/eariver/git/reconstruct-japanese-generative-ai-survey`:

- `git rev-parse HEAD` → `b385deb69f5472377737ea2a4138b2d20b119dec`, rc=0. Matches task starting point.
- `git rev-parse HEAD^{tree}` → `f24415842252d458394047512413720b773c7840`, rc=0.
- `git status --porcelain=v1 -uall` → 1 row, rc=0:
  - `?? notes/rephase-1-dm021-p2v/task.md` (task input, preexisting).
- `python3 --version` → `Python 3.14.4`, `/usr/bin/python3`, `sys.version 3.14.4 (main, Aug 20 2026, 10:41:58) [GCC 15.2.0]`. Observed without candidate imports. This is the absolute available runtime for any future implementation unit.

Fixed contract `outputs/rephase-1-dm021-current-authority-contract-decision.md` SHA256 (direct `hashlib.sha256`):

- `2ea1d98f1b3658430342e4ec2a2cd9639327557ca6ae2d6d4ea0665708f5f8fd`, matches task.

Mandatory companions read (no edits): `notes/rephase-1-dm021-current-authority/astra-review-resolution.md` V1–V5 (41 lines), `independent-design-review.md` §§0–16 (436 lines, §16 appended V1–V5 resolution).

## 2. Candidate identity (sanitized, all rc=0)

In `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`:

- `git rev-parse HEAD` → `409b292756dd1277b9dfae87679934c0d2ce251c`, rc=0.
- `git rev-parse HEAD^{tree}` → `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, rc=0.
- `git status --porcelain=v1 -uall` → 100 rows total, rc=0 (captured to transient `/tmp/opencode/p2v-phaseA-status.txt`, not persisted as evidence):
  - 16 source rows: 3 ` M` + 13 `??` (exactly `3M+13A`).
  - 84 `__pycache__` rows (`??`).
- `git diff --cached --name-only` → empty, rc=0 (no staged/intent delta).
- `git diff --name-only` → exactly 3 modified paths, rc=0:
  - `schemas/reader-surface-gate-v2.schema.json`
  - `schemas/reader-surface-semantic-review-v2.schema.json`
  - `scripts/survey_reader_surface_gate_v2.py`

Source rows (sorted, direct observation):

```text
M schemas/reader-surface-gate-v2.schema.json
M schemas/reader-surface-semantic-review-v2.schema.json
M scripts/survey_reader_surface_gate_v2.py
?? schemas/editorial-correction-proposal-v2.schema.json
?? schemas/editorial-retention-manifest-v2.schema.json
?? schemas/longform-publication-source-manifest-v2.schema.json
?? schemas/longform-reader-input-v2.schema.json
?? scripts/survey_editorial_correction_proposal_v2.py
?? scripts/survey_editorial_retention_v2.py
?? scripts/survey_longform_derivation_v2.py
?? scripts/survey_longform_generated_v2.py
?? scripts/survey_longform_semantic_publication_v2.py
?? tests/test_survey_editorial_correction_proposal_v2.py
?? tests/test_survey_editorial_retention_v2.py
?? tests/test_survey_longform_derivation_v2.py
?? tests/test_survey_longform_publication_integration_v2.py
```

## 3. Exact 16-file pins (direct re-observation, ALL_MATCH)

Compared working-tree bytes/mode/size against static `notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/expected16-correction2c.json` (82 lines, read) via stdlib `hashlib.sha256` + `os.stat` (read-only). All 16 match hash+bytes+mode `0o664`:

| Path | SHA256 (full) | bytes | mode |
|---|---|---|---|
| `schemas/editorial-correction-proposal-v2.schema.json` | `5623c0d92e3dfc5415e1ab73c73b3d5f1b147f265f2255469cede2ec333a4607` | 3945 | 0o664 |
| `schemas/editorial-retention-manifest-v2.schema.json` | `347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c` | 5618 | 0o664 |
| `schemas/longform-publication-source-manifest-v2.schema.json` | `4dadf873096f31cf564a7db4fee42a1fc8cdd8fc039dd14a7ee01cf26043e8ca` | 2720 | 0o664 |
| `schemas/longform-reader-input-v2.schema.json` | `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643` | 10624 | 0o664 |
| `schemas/reader-surface-gate-v2.schema.json` | `fe4a96f4aa87f2a527096c4d3040f92e0217ef972ddae1d7140498184a13322c` | 6894 | 0o664 |
| `schemas/reader-surface-semantic-review-v2.schema.json` | `e8598239d3ca00441f61110fd77a7b7edf063ac15a7a6a1c2efdb38e73d6699b` | 4219 | 0o664 |
| `scripts/survey_editorial_correction_proposal_v2.py` | `5d2fde456d42d494acc93d3ce6cab51bcd3ee56178b62cdf9eb31554db03c346` | 110155 | 0o664 |
| `scripts/survey_editorial_retention_v2.py` | `3833b14a281ab82999410d91361d5aace3c77015484e621c62077e480b73f5b2` | 122231 | 0o664 |
| `scripts/survey_longform_derivation_v2.py` | `c09c5558f9668906b7d2ed34c55281d5f6d9ed279d3237a8ffc18ac84ea41149` | 62260 | 0o664 |
| `scripts/survey_longform_generated_v2.py` | `d480e11d1c398f79f3e894e2e1e1f56ceec507dfde376a163a58b0ebed97d3c2` | 39992 | 0o664 |
| `scripts/survey_longform_semantic_publication_v2.py` | `4d235a388955dcedd34d6a7dc5ac7761f9fc91de8bc723eb11f68cec6a229195` | 36224 | 0o664 |
| `scripts/survey_reader_surface_gate_v2.py` | `e73058841cfa1a841030b96d5cd2fb756c6ba99d1b99522ddbf0131d1f06bbe4` | 94511 | 0o664 |
| `tests/test_survey_editorial_correction_proposal_v2.py` | `f581fad0a483303f2bed1de080dd1a9e6f07928d228ef8f24d7c4a7c1242dbac` | 112708 | 0o664 |
| `tests/test_survey_editorial_retention_v2.py` | `4155baab733e8bddc0b7cbc34b83fe801def2927a716d43132321f8f083d614e` | 93733 | 0o664 |
| `tests/test_survey_longform_derivation_v2.py` | `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913` | 91161 | 0o664 |
| `tests/test_survey_longform_publication_integration_v2.py` | `4a03b564f8fa4dd39f2b48766ddb7612cf2d8d4dacdcc42ac39f637d2bca11a4` | 107757 | 0o664 |

Direct `wc -l` (read-only, no execution): P1 1830, P2R 2080, P1-test 1847, P2R-test 1818. P1 `5d2fde45` / P2R `3833b14a` prefixes match final P2R closeout.

Inherited13 check (direct): `inherited13-static-freeze.json` is wrapper `{provenance, files: {13 entries}}`, provenance `notes/rephase-1-dm021-p1/evidence-20261012T072355Z-correction4/freeze-post.json`. All 13 `files` entries equal `expected16-correction2c.json` subset (`mismatch NONE`). Delta `expected16 - inherited13` is exactly 3 P2R paths (`editorial-retention-manifest-v2.schema.json`, `survey_editorial_retention_v2.py`, `test_survey_editorial_retention_v2.py`).

Complete16 patch `5b79218e…` (830622B) cited from durable P2R packet, not rehashed here. No new HEAD/commit. HEAD409 alone does not contain overlay.

## 4. Exact 84-cache accounting (path-set only, not byte proof)

Static `cache-inventory-static.json`: `{provenance, files: {84 entries}}`, provenance `candidate live status at correction2b authoring; regular non-alias only`.

Direct observation (stdlib set comparison, read-only):

- Status cache rows: 84. Status source rows: 16. Total 100.
- Static 84 keys vs status 84 cache paths (`[3:]` stripped): sets equal (`static==status`, both diffs empty).
- Caches preserved in active tree (not cleaned). No cache bytes read, hashed, or executed; modes/sizes not re-observed here. Byte authority remains v9 `pre/post.json` (`pre==post`) in P2R packet.
- No `PYTHONPYCACHEPREFIX` manipulation, no bytecode writes, no imports.

This is direct path-set observation, honestly labeled as such (not a persisted raw-proof file, not a byte rehash). Same scope as prior design `source-binding.md` §§1–3.

## 5. Method / limits

Direct commands only (§§1–4); file/line citations in `interface-proposal.md` via `Read`/`Grep` (no imports, no execution). Counts below are summaries of direct reads, not raw packets:

- P1/P2R/route/test line maps verified by read (see interface-proposal V1).
- P1 final 36 (9P1+27Gate), P2R final 25/7936.817s + affected2 + optimized1, proof v7 `APPLY_PROOF_OK` cited from durable packets, not re-executed.
- All P1/P2R qualifications (filtered status, HEAD-inode proof, transient `add -N` erratum, late-plant post-removal narrowing, proof-logger fault-propagation limit, 1818-line erratum, unexecuted draft) remain in force.
- No copies/restores/fixtures/tests/code/commits/network in this Phase A unit. Next is Astra selection; implementation candidate creation only after selection.
