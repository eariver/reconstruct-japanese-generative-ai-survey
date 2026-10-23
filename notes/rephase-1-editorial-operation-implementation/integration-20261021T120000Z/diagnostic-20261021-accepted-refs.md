# Accepted_refs coupling — exact lines/control flow (leave code now)

## Current code (DST, no edits in this unit)

File: `scripts/survey_editorial_publication_v2.py`

- Before-kind detection (lines 692-698, 1-indexed in DST current `5aee10f9...`):
  - `692: gen_authored = {r.get("name"): r ...}` (authored roles)
  - `693-698`: `if set(gen_authored)=={"publication-semantic-input","drafting-authored-archive"}: before_is_editorial=False`
    `elif set(gen_authored)=={"proposed-publication-authoring","accepted-draft-archive"}: before_is_editorial=True`
- Receipt accepted_refs creation (prepare, line ~1686):
  - `"accepted_refs": [{"name": "validation-checkpoint", "path": ..., "sha256": ...}]` (single entry only)
- Validate branches (Weekly lines 812-827, Longform 878-893):
  - `812: ctx_accepted = ctx.get("accepted_refs", [])` (full list from NEW authoring `load_derivation`, ~10 entries: production-profile, issue-architecture, synthesis-input/result, draft-package/result ×N, evidence/matrix/ledger/discovery, cards)
  - `813: if not before_is_editorial:` → only then `814: gen_accepted = gen_receipt.get("accepted_refs", [])` + `_norm` compare `826: if _norm(gen_accepted) != _norm(ctx_accepted): raise ACCEPTED_MISMATCH`
  - Else (editorial-before): skip full equality, comment `810-811`: “before-editorial carries only validation-checkpoint (already bound to State), so skip full equality and rely on retained archive + surface checks below.”
  - Longform identical guard at `879: if not before_is_editorial:` with `_norm2`.

Control flow: `before_is_editorial==True` → no `gen_accepted` vs `ctx_accepted` check; only `receipt validation-checkpoint == State validation` (line 714) + `receipt archive == ctx.archive` + `ctx.surface == proposed reader` are enforced.

## Required unconditional (root flag, for future correction, NOT applied now)

- `ctx.accepted_refs == receipt.accepted_refs` unconditionally, using NEW proposed authoring (`proposal.proposed.authoring_input_ref` via `weekly.load_derivation` / `longform.load_derivation_for_readback`) and accepted Draft (`ctx.archive_path` vs `receipt accepted-draft-archive` path+sha + `drafting-authored-archive` bytes), regardless `before_is_editorial` (initial vs prior EDITORIAL), zero caller-list trust (no `gen_receipt` accepted list trust; rederive independently).
- Concretely: receipt `accepted_refs` must become full `ctx.accepted_refs` (not single `validation-checkpoint`), or receipt must carry full list in addition to checkpoint, so equality is well-typed (both `list[{name,path,sha256}]` sorted, no dups). Current receipt has 1 entry vs ctx ~10 → equality impossible as typed; `if not before_is_editorial` papers over by skipping.
- Do NOT paper over with P3S historical sufficient: `verify_staged_source STAGED_SOURCE_REPLAY_VERIFIED` proves retained COPY/scope/trio replay, but does NOT prove current accepted research (`ctx.accepted_refs`) equals receipt claim; only independent `load_derivation` on NEW authoring does.

## Remaining coupling/limitations (extracted, no fix now)

- Receipt shape coupling: `editorial-publication-source-manifest-v2.schema.json` allows `accepted_refs minItems:1` (currently 1), while `ctx.accepted_refs` is 10+; unconditional equality requires schema + prepare + seal + L `validate_seal`/`_validate_receipt_bindings` to handle full list (L currently expects exact keys but does not check accepted_refs length; seal `roles` do not include accepted research, only `source-receipt` file; `source-receipt` file would grow).
- Before-receipt coupling: `proposal.basis.generated_receipt_ref` may be initial (full accepted list) or prior EDITORIAL (single checkpoint); unconditional `ctx==receipt` removes `gen_receipt` accepted-list trust, but `gen_receipt` still needed for `accepted-draft-archive` path+sha pin (before archive) + `active_reader_input_ref`/`preserved_upstream_digest` for scope `before_reader` check – those remain, only accepted-list comparison becomes unconditional.
- `validation-checkpoint` still required to equal strict State (`line 714`); full `ctx.accepted_refs` includes `production-profile`/`issue-architecture`/etc., but NOT `validation-checkpoint` (which is State checkpoint, not derivation accepted list) – so unconditional equality is `ctx.accepted_refs (full derivation)` vs `receipt.accepted_refs (must become full derivation)`, while `validation-checkpoint` stays as separate State binding (already enforced). Do not conflate.
- Performance coupling (see hang diagnostic): unconditional full-list compare adds negligible cost vs 40s jsonschema; slow is validator creation + `$ref`/`urljoin`, not compare.
