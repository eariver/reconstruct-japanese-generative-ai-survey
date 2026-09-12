# Survey Production Core v2 — Article Drafting

Prompt ID: `article-drafting-v2`

Produce exactly one JSON Draft Result conforming to `schemas/draft-v2-result.schema.json` from the supplied Draft Package.

Rules:

1. Use only the factual Evidence contained in `evidence_inputs`. Do not use Raw source payloads or unstated external facts.
2. Preserve the distinction between `PRIMARY_SUBJECT`, `COMPARATOR`, and `RELATED`. A comparator-owned value must never be written as a primary-subject property.
3. Every factual, attributed, social, inference, metric, event, or limitation assertion that depends on Evidence must carry the corresponding structured Evidence reference.
4. Evidence references must use the stable `EVENT`, `CLAIM`, `METRIC`, or `LIMITATION` IDs from the supplied Evidence Cards and must preserve their subject ID and subject role.
5. Unknowns remain unknown. Do not resolve an unresolved question or contradiction by prose invention.
6. Cover every `must_cover_requirement` and report its block IDs in `must_cover_coverage`.
7. Dispose every Architecture boundary explicitly. Use `EXPLICITLY_STATED` when the limitation/boundary is reader-facing; use `RESPECTED_BY_OMISSION` when the correct behavior is to avoid an unsupported claim. Explain the handling rationale.
8. Keep Profile-specific behavior inside `profile_extensions` and Publication-specific behavior inside `publication_extensions`. Do not invent Weekly fields for Thematic/Period work or vice versa.
9. Do not emit generic `late_breaking`, `this_week`, `watchlist`, or similar Weekly-only fields unless the supplied Profile extension explicitly owns such semantics.
10. Return JSON only. Do not return Markdown fences, commentary, LaTeX, or prose outside the JSON object.
