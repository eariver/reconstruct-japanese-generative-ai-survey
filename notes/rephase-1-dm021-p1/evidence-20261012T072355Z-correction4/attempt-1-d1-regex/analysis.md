# R4 Attempt-1 (failed, preserved, NEW runner PASS on E1)

36 tests, 3300.380s, 1 failure (D1 outside-raw regex too strict, code correctly
refuses). NEW E1 runner itself PASSES (exclusive O_EXCL, sanitized parent+child
Git3 with rc checks, routing/optimize rejected before Git, named-status pre/post
identical, caches recorded {} with PYTHONDONTWRITEBYTECODE=1 (no caches), no
cleanup before post, timeout preserved). E1 code facts fixed vs old runner.

## D1 regex

Outside `raw/source.json` (repo-root, outside edition trees) mutated before
validate-with-scope → `_derive/load_derivation` fails first with
`DERIVATION_REFUSED: accepted Discovery graph differs from current Discovery/Raw
bytes` (discovery validator, before D1 graph pin which would give
DISCOVERY_RAW/REF_DRIFT). Both fail-closed, correct (outside-tree refused, no
false accept). Test expected `DISCOVERY|RAW|...` (all-caps, case-sensitive) and
missed `DERIVATION_REFUSED` (with capital-D Discovery message). Fixed to accept
`DERIVATION` as well (early derivation refusal, still proves outside-tree drift
refused, explicit injected delta, no P1 writes beyond injected raw).
