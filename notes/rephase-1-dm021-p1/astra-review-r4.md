# DM021-P1 final closure/evidence check — Discovery refs and runner

2026-10-12 JST. Preserve correction3/code69790944/test84a6e4a11 and its independent report. Root confirms checkpoint-bound selection/views/completeness corrections. Two concrete omissions remain; no new runtime paths or policy scope.

## D1 — Discovery acceptance local refs are still dropped

The collector adds the Discovery acceptance node and raw discovery JSONL via Evidence-package basis, but never traverses Discovery acceptance's REQUIRED `x_source_intake{path,sha256}` or `records[].raw_refs{path,sha256,byte_count}` (`discovery-acceptance-v2.schema.json:7,11,85–97`). These are explicit local authority refs, not URLs/free text. Raw artifacts can be outside source_root (the fixtures use `raw/source.json`), so edition-tree walking does not substitute for graph/frozen/retention membership or drift detection.

Add finite type-specific collection and verification of these exact refs and the X-intake manifest's actually required local refs through its schema/validator conventions. Distinguish research/raw evidence KEEP+frozen from any referenced tool/prompt/control file KEEP+operational; no generic path-string recursion or new source intake. Bind exact size as well as hash where supplied. Missing/unclassified required local dependency stops; do not claim full closure if deliberately excluded.

Extend independent expected-set assertions using the fixture's actual Discovery acceptance and X manifest (not implementation nodes), including a raw file outside edition roots. Add a late mutation seam for that raw dependency demonstrating refusal after scope, with explicit injected-only delta and no cleanup masking. Preserve all existing route/predecessor/frozen exclusion cases. If current validators do not require a particular metadata literal as a live dependency, record that distinction precisely rather than following arbitrary strings.

## E1 — final runner claims exceed code

`run_correction.py` still checks existence then writes logs with `w`/write_text (not atomic exclusive creation); parent freeze Git calls inherit routing and ignore returncodes; Python routing isn't fully rejected; finally deletes active-source `__pycache__` dirs BEFORE post-freeze, masking changes. These are actual script facts. Preserve/qualify prior exact-run evidence; don't call it a certified fail-closed/exclusive/no-cleanup runner.

Use a NEW small runner at new final pins: explicit errors, exclusive `open(x)`/O_EXCL logs, sanitized no-network Git for parent AND child, reject inherited Git/Python routing/optimized mode before candidate Git calls, check every Git returncode, record exact argv/cwd/interpreter/env, compare all13 expected hashes/modes/named-status/base pre AND finally-post, preserve timeout output. Never delete/repair source/cache paths before comparison; record any cache side effects separately. Don't touch active index to build patches.

Run the final focused P1+affected cases once after final source fixation, with realistic timeout based on the measured prior3255s. Complete13path patch generated in copy/no-index and applied AS SAVED to a new independent actual409 base; all13 hashes/modes/status plus object separation. Old36 stays its own scope, no count transfer. No code in controller/publishers/reason/State, no network/commits/empty fixtures. Return for root and independent resolution of D1/E1 with actual source/log citations.
