# Closeout availability qualification — root environment

2026-10-11 JST. During final closeout, root attempted a read-only `git -C /tmp/opencode/jgas-lf2-design-20261009T113013Z diff --name-status HEAD` followed by source hashing. Git refused because that directory **does not exist in the root tool environment now**. The subsequent hash command in that chained invocation did not run. A directory read of `/tmp/opencode` showed none of the documented `jgas-*` copies there. The reason/timing of the availability change is unknown; do not attribute it to a particular actor or infer another environment's availability.

Earlier root source reads/hash observations and the independent source supplement remain their recorded observations. They are not proof that a live copy still exists at closeout. No source/code/test edits or recovery were performed by root in this design unit. Contract07e89990 remains a design against the exact preserved composite, not a runtime result.

## Durable inputs re-checked now

All following workspace files are present and were hashed successfully after the missing-directory observation:

| Recovery/content input | SHA256 |
|---|---|
| `notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz` | `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c` |
| `notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-pack.pack` | `2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99` |
| `notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/w1-222-to-e1705b7.pack` | `97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9` |
| `notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/dm004final-e1705b7-to-409b292.pack` | `e3d941653eadf2459a13f1b85b9fbbffd819f0a0ad6bb77eb121b2cba02279bf` |
| `notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/complete-overlay.patch` | `5c7e7503851f5cdbc30b6827560219f48ce75d4a6cf64ba13516ed97e0cea4f9` |

This verifies input bytes/presence, **not a restoration performed in this unit**, complete history, or runtime availability. The partial/shallow26309-missing-blob and unbundled-runtime qualifications remain. Current contract hash07e89990 was also rechecked successfully.

## First next-session action (before P1 interface/code work)

General must check actual availability in its current environment, not assume historical `/tmp` paths exist. If an exact available copy is found, verify real HEAD/tree/parent/all9 source hashes/allowed delta and independent DB/inert-origin/no-alternates/no-sharing before use.

If unavailable, restore **actual409** offline from the four verified recovery inputs into a NEW absent task-specific `/tmp/opencode/` destination, using a new fail-closed extraction/import procedure: verify hashes and archive member paths/types/containment, preserve all old evidence, import the exact packs, switch to the actual409 identity and verify its available ancestry/tree/clean materialized bytes. Then apply the COMPLETE9file patch as saved and verify all9 hashes/modes plus2M7A delta. Do not apply LF1patch first, substitute a fresh-root commit, create empty commits, fetch current main or run historical restoration/proof wrappers.

Save actual commands/raw exits and current isolation/identity/runtime observations. Stop on a concrete extraction/object/identity/runtime gap rather than fabricating availability or transferring old test PASS. This source-availability preparation precedes the already-selected P1 exact graph/schema/API/fixture return; it does not authorize Production changes, candidate commits or an automatic old-suite rerun. Stop at the current design Human Commit Point now.
