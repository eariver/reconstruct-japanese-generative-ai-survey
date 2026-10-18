# P3S verification-tools B1 — DRAFT docs (NOT EXECUTED, root readback)

2026-10-17. CoWorkerB evidence-tooling only, in parallel with CoWorkerA code.
Read-only references: `task.md`, `astra-implementation-selection.md`, fixed
contract `outputs/rephase-1-dm021-staged-source-contract-decision.md`
SHA256 `42eb8dbbb1eeda362b264847c80bdbf478b433ab1fe9777e7fe49c8ed9df3472`,
mandatory S1–S5 (`notes/rephase-1-dm021-materialization/astra-review-resolution.md`),
§7 (`independent-design-review.md` §§0–7), P2V accepted
`verification-tools/run_p2v_b4.py` +
`source-correction/proof_apply18_b4v2.py` as READ-ONLY references with known
limitations (relative `GIT_INDEX_FILE` risk, disposable copy nested inside
outdir/notes, missing own-script sha, 102-row scope, no scratch-root
separation). No candidate/source/test/schema writes, no execution/DB/index/
network/tests in this unit. No PASS claims; root readback first.

## 1. New files (ONLY these, all DRAFT)

- `notes/rephase-1-dm021-p3s/verification-tools/run_p3s_b1.py`
- `notes/rephase-1-dm021-p3s/verification-tools/gen_complete21_b1.py`
- `notes/rephase-1-dm021-p3s/verification-tools/proof_apply21_b1.py`
- `notes/rephase-1-dm021-p3s/verification-tools/README.md` (this file)

No other writes. Future source21 = 3M18A (`MODIFIED3` + `NEW18`) + 84
preknown caches => 105 raw status rows. Explicit new P3S3 (subset of NEW18):

- `scripts/survey_editorial_staged_source_v2.py`
- `schemas/editorial-staged-source-manifest-v2.schema.json`
- `tests/test_survey_editorial_staged_source_v2.py`

Inherited18 (previous P2V18 all unchanged) = `NEW15_INHERITED` + `MODIFIED3`,
pins supplied at execution via `--p2v-expected18`
(default `notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json`).
Static cache (84) supplied via `--cache-inventory`
(default P2R `evidence-20261014T000000Z-correction2/cache-inventory-static.json`).
Static21 (`{path: {sha256, bytes, mode}}`, 21 entries) + candidate path are
REQUIRED CLI at execution after CoWorkerA return; no defaults that mask them.

## 2. Fixed identities enforced

- `FIXED_HEAD=409b292756dd1277b9dfae87679934c0d2ce251c`
- `FIXED_TREE=8ce3699861505f32d1d60bdc185d4d4f635aedb2`
- Detached HEAD, empty index (`git diff --cached --name-only` empty), all Git
  rc==0 checked pre AND finally-post.
- `MODIFIED3` (3, `" M "`), `NEW18` (18, `"?? "`), caches (84, `"?? "`).
  Full EXACT status: rowset equality + len (105) + duplicate check; no
  filter/count-only. Runner/proof/generator all compare `set(rows)` to the
  exact expected set and `len(rows)` to 105/21.
- No new candidate commit; generator/proof never run `commit`/`add` in active
  DB; proof/generator byte-copies use `cp -a --reflink=never` only.

## 3. Guard map

### run_p3s_b1.py (runner)

- Pre: `rev-parse HEAD`, `rev-parse HEAD^{tree}`, `status --porcelain=v1
  --untracked-files=all`, `diff --cached --name-only`, `diff --name-only`
  (rc==0); canonical21 keyset; each static21 `{sha256,bytes,mode}` vs live
  `lstat`-regular/type/nlink + `read_bytes` hash/size/mode; inherited18 vs
  P2V v5 exact equality (live + manifest); NEW_P3S3 presence; cache len 84 +
  each `{sha256,bytes,mode}` vs live; full 105 rowset+len.
- Child: `python -u -m unittest` (default
  `tests.test_survey_editorial_staged_source_v2`; smoke via explicit
  selectors), `cwd=candidate`, direct held exclusive `xb` stdout/stderr,
  `start_new_session=True`, sanitized `_child_env` (strip all `GIT_*` +
  `PYTHONPATH`/`PYTHONHOME`; force `GIT_NO_LAZY_FETCH=1`,
  `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`,
  `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPYCACHEPREFIX=<absent>`,
  `TMPDIR=<own-under-/tmp/opencode>`), `-u`, timeout default/max 18000s,
  TERM→KILL on original pgid + reap; orphan limit recorded
  (double-forked escape not claimed reaped).
- Finally-post: same `_observe`+`_check_pins` + pre/post rowset equality +
  cache-prefix-still-absent; `PYTHONPYCACHEPREFIX` never mkdir'd.
- Outputs (exclusive `x`/`xb`, no overwrite): `run_p3s_b1.stdout.txt`,
  `.stderr.txt`, `.exit` (child+wrapper rc), `.pre.json`, `.post.json`,
  `.meta.json` (argv/cwd/python/executable/pip-freeze-truncated/forced-env +
  redaction count + input_ids + runner sha; no full env dump), 
  `.stage-reserved/running/done.json`. Outdir/TMPDIR/cache-prefix existence
  refusal writes console only (rc 40). Flush/close/trailer/stage/exit write
  failures force nonzero (5/6); no `return` inside `finally` (wrapper_rc
  variable, single return after `finally`).
- Smoke vs full: different exclusive outdirs required; script sha persisted
  (`runner_sha256`); requested selectors persisted.

### gen_complete21_b1.py (generator)

- Requires `--scratch-root` under `/tmp/opencode` (pre-existing dir);
  disposable copy/index = `<scratch>/<outdir-name>-disposable-copy|-index`
  (resolved absolute, escape refused); durable patch/meta/logs only under
  `--outdir`. No relative `GIT_INDEX_FILE` bug (absolute resolved path).
- Pre: same 21+84 source guards; inert remote exact pair + config exact inert
  URL + no `alternates` on source AND copy (bounded scope); all-entry `.git`
  lstat (dirs/regulars/types/nlink/errors) + inode-set disjointness.
- Sequence in disposable copy with disposable index only:
  `read-tree HEAD` → `add -- MODIFIED3 NEW18` → `diff --cached --binary`;
  raw cmds/rc/stderr persisted in `meta.json`. No active index/objects.
- Saves: `complete-p3s-21path.patch` (`xb`), `.sha256` (`"<sha>  <name>\n"`),
  `source-pre/post.json`, `meta.json`, `stdout/stderr.txt`, `exit`,
  `stage-done.json`. Source-post unchanged check (pre/post rowset + per-file
  sha). No commits/network/cleanup.

### proof_apply21_b1.py (proof)

- Consumes SAVED patch+hash+static21 only; never generates patch.
- Requires `--scratch-root` under `/tmp/opencode`; `copyrepo =
  <scratch>/<outdir-name>-clean409-copy` (resolved, escape refused). No notes
  nested DBs, no archive/fakeRoot/borrowedGit.
- Active checks: static21 keyset==canonical21 + NEW_P3S3 present; saved hash
  64-hex + patch sha match; active full freeze (HEAD/tree/index) +
  per-file static21 match + inherited18 vs P2V v5 + full 105 rowset+len=105 +
  84 cache hash/mode/size/regular/type; inert remote/config.
- Copy: byte-copy + per-file byte equality + all-entry isolation +
  inode-set disjoint + remote inert; declared copy cache omission/removal
  (`scripts|tests|schemas/__pycache__` + `*.pyc`) recorded as full inventory
  in `proof-freeze-clean-b1.json`; `checkout HEAD -- MODIFIED3`; `unlink`
  NEW18 (18 absent, never read); clean freeze: HEAD/tree/index/status-empty +
  3M bytes==HEAD bytes + 18 new absent.
- `--check` then `apply` saved patch; applied freeze: HEAD/tree/index
  unchanged + per-file static21 + mode + byte equality source-vs-copy +
  status==EXACT21 rowset + len 21; source pre/post equality. Failure paths
  log actual file/rc and return nonzero via `_fail`/`_emit`; flush/close
  errors force nonzero with `PROOF_LIMIT` note when exit already recorded.
  One-off tool, not generic certification.

## 4. AST checks (allowed, no side effect)

Planned root/CoWorker check (NOT executed here; run only with
`PYTHONDONTWRITEBYTECODE=1`, no imports, no bytecode claim):

```python
import ast
for p in ["run_p3s_b1.py","gen_complete21_b1.py","proof_apply21_b1.py"]:
    ast.parse(open(p, encoding="utf-8").read(), filename=p)
```

- Never `py_compile` (writes bytecode; forbidden claim).
- Checks syntax only; no guard/functional PASS implied.
- This unit performed no execution; `ast.parse` deferred to root readback
  if desired. No `__pycache__` effects asserted.

## 5. Static assumptions (no PASS claims)

- Candidate + static21 supplied after CoWorkerA return; inherited18 pins =
  P2V `expected18-source-correction-v5.json`; caches = P2R static inventory.
- 21 = `MODIFIED3` (reader-surface-gate 2 schemas + 1 script) + `NEW18`
  (`NEW15_INHERITED` + `NEW_P3S3`); modes `0o664` assumed, verified at run.
- Timeout 18000s covers P2V13~5500 + P3 extra; smoke/full via different
  outdirs; no old13+1/25/36 transfer.
- Scratch roots REQUIRED under `/tmp/opencode`, separate from durable
  outdirs; no notes DBs; inert origin
  `https://example.invalid/rephase-candidate-recovery.git`.
- Tools are one-off exact-run evidence, not universal rerunners; every
  failure path returns nonzero and preserves raw logs. No full source
  copies/long tests/proof executions yet; stop for root readback.
