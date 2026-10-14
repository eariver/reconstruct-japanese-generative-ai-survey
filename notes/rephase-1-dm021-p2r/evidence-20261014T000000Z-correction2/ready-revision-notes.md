# READY revision notes (root draft-review fixes) — NO EXECUTION

2026-10-14. Root reviewed both DRAFTs; fixes applied in NEW READY files.
DRAFTs preserved (see incident note below). Shipping source stays pinned
`ee7ebc48`/`8c4c2ea1`/`347e5499` pending targeted final review. No long
run, no proof execution, no `-O`, no new runtime features, no source
edits in this unit (evidence/packet files only).

## Incident disclosure (DRAFT preservation)

While authoring the READY proof I mistakenly deleted
`proof_apply16_v3.py.DRAFT` (`rm` instead of keeping it alongside the new
file). I restored it immediately in the same session from the full read
transcript. It parses (`AST_OK`) and is preserved in intent, but I cannot
certify byte-identity against the deleted original — no other copy exists.
Root should treat the READY files as operative and the restored DRAFT as
historical reference only. The runner DRAFT was never deleted and is
byte-untouched.

## Runner: DRAFT → `run_p2r_correction_v7.py.READY`

1. `_check_pins` now enforces EXACT source-row status pre AND post: len 16,
   duplicate check, set equality vs `EXPECTED_STATUS_ROWS`; non-cache
   extras/missing refuse. Cache rows (`__pycache__/`/`*.pyc`, never
   cleaned — live status shows ~84 such rows) are partitioned and
   RECORDED. Post source rows must also equal pre source rows.
2. Startup validates the expected manifest is exactly the canonical 16
   paths (no unlisted sources). New `inherited13-static-freeze.json`
   (13 pins copied verbatim from authoritative P1
   `evidence-20261012T072355Z-correction4/freeze-post.json`; current
   candidate re-verified byte-identical before writing) is checked
   sha+mode+bytes for all 13 in pre AND post.
3. Pre-guard failure writes through the HELD `xb` handles only (the
   `wb`-reopen path is gone); handles live for the whole run under
   manual management (ExitStack dropped: the trailer must precede close).
4. Flush/close failures recorded in terminal metadata and force rc 5 when
   otherwise clean; `KeyboardInterrupt`/`RuntimeError`/generic `Exception`
   paths record type/message with rc 130/2/1; timeout/interrupt (and any
   launch failure after a successful Popen) kills+reaps ONLY the own
   process group (`start_new_session=True`, `killpg`, `wait`); child
   exact cmd/cwd, `sys.executable`, and the FORCED env recorded in
   stage-running; child runs `python -u` with `PYTHONDONTWRITEBYTECODE=1`.
   Single end return with precedence
   interrupt > timeout > launch-error > pre-errors(2) > child-rc >
   flush-errors(5) > post-errors(3) > 0; nothing returned from finally;
   pre-observe failure records exit 2 and returns 2 (agreeing).
5. Git trust override is the exact repo per call
   (`safe.directory=<resolved cwd>`); no wildcard anywhere.

## Proof: DRAFT → `proof_apply16_v3.py.READY`

4. Regular `.git` entries with `nlink != 1` are problems (refusal);
   active AND applied 16 files compared to saved STATIC
   `expected16-correction2.json` (exact path set + sha/mode/bytes);
   `FIXED_TREE` enforced with HEAD/index in clean AND applied freezes;
   clean requires exactly empty status+index; whole effective
   remote/config persisted for active (once) and copy (pre- and
   post-apply); all-entry errors fail (problems list / RuntimeError /
   OSError-to-fail path).
5. Outputs use HELD `xb` handles; every return appends only through owned
   handles (`_emit`); JSON freezes each `x`-written exactly once; no
   `wb`/`w` reopens, no overwrites. `SAFE_DIRECTORY` constant removed
   (exact repo per call). Docstring scopes the config/remote policy as
   observation (exact remote pair + exact inert URLs + whole-output
   persistence), not a strict full-config matcher. Patch sha COMPARED to
   saved `complete-p2r-16path-v3.sha256` (64-hex validated; absent →
   refusal). Declared copy-cache-removal qualification kept; no active
   cleanup.

## Packet state (all in `evidence-20261014T000000Z-correction2/`)

- `expected16-correction2.json` (static 16, correction2 pins) — unchanged.
- `inherited13-static-freeze.json` (NEW; P1-authoritative 13 + provenance).
- `run_p2r_correction_v7.py.DRAFT` (byte-untouched) + `.READY` (NEW).
- `proof_apply16_v3.py.DRAFT` (restored, see incident) + `.READY` (NEW).
- `correction2-notes.md` (prior unit) — unchanged.
- `ready-revision-notes.md` (this file).

## Checks executed (cheap only, exact commands)

- `python3 -c "import ast; ast.parse(...)"` over both READY files and the
  restored DRAFT + `run_p2r_correction_v7.py.DRAFT` — all `AST_OK`.
- `python3 -c "import json; json.load(...)"` over both static manifests —
  16 / 13 entries.
- Read-only `git status`/`rev-parse` observations only. No runner/proof
  execution, no fixture builds, no cache writes or cleanup.

## Proposed next (for root ack; NOT started)

Same as `correction2-notes.md` §"Proposed final checks", with v7-READY /
v3-READY substituted for the drafts and the v3 patch + hash manifest
generated after final-pin confirmation, compared (not merely printed) by
the READY proof at execution time.
