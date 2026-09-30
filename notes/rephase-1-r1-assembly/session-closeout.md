# Assembly session — context-to-file closeout supplement

Recorded `2026-09-30T20:06:10+09:00` (root clock), in response to Human asking whether important context remained unpersisted. **Document closeout only.** No candidate changes, tests, new Worker/reviewer or next implementation unit started.

## What was already persisted

The [assembly assessment](../../outputs/rephase-1-r1-assembly-assessment.md), [packet entry](README.md), [handoff](../../handoff/rephase-1-continuation.md) and AGENTS already contain: exact 481dec0/e4/b74 identities and paths; seven-file equivalence; four-method versus actual-history diagnostic scopes; root and independent conclusions; raw-evidence limitations; fixed-baseline/production/Human authority; General/Explore role/model-visibility limits; pause-at-Commit-Point preference; and the next fixed-481 DM-001 contract task. No hidden design choice or approval is needed from this chat to resume that task. All delegated work in this completed assembly unit returned; no background Worker or test process is intentionally left running.

## Newly recorded tooling observation

During root's assembly README closeout, one `apply_patch` invocation contained **two `Update File` sections for the same path**. The tool reported success, but readback showed only the later edit had survived: the README still had its milestone-1 header/stop text while the later hook-language edit was present. Root then reapplied the header/body changes in a **single file section with multiple hunks**, and readback confirmed the completed-unit entry.

This is an observed local editing issue, not a claim about every implementation of the tool and not an explanation retroactively assigned to earlier Worker failures. Future work should use one file-operation section per path in each patch, or separate calls with readback/diff checks. Tool success alone is insufficient proof that all intended hunks persisted. This occurrence affected the documentary README only; candidate/test evidence was not changed.

## File persistence, Git persistence and fixture recovery are separate

- At this check, reconstruct HEAD is `a22d69308e9bbfb84cee9d8530c258a2a911d059`; local tracking shows `main...origin/main`. The completed assembly packet/assessment are **untracked** and the entry documents/`.gitattributes` are modified. They are saved on disk, but **not committed/pushed at this observation**. Recheck status after any Human action; ordinary Commit/Push remains Human-owned.
- The actual assembled Git database is in WSL `/tmp/jgas-rephase-r1-assembly-20260929T143833Z`; original e4, B and R1 databases are also separately located under WSL `/tmp`. Those paths are execution storage and may disappear independently of reconstruct's Markdown/patch/log files.
- The assembly packet preserves identities, commands, comparison observations, selected logs and scripts; the R1 packet preserves the seven final files and increment patch. **The assembly packet has not been created or verified as a standalone backup of the complete Git database, exact commit graph or all historical objects.** Pushing reconstruct does not itself push the fixture branch/database. Inherited promisor/shallow gaps remain.
- If a later session loses a fixture, first inventory the remaining exact databases and durable inputs. Prefer surviving fixed objects; do not silently substitute a fresh-root reconstruction, label recovered content as the original commit, hydrate unrelated history or follow production main. Content recovery and recovery of exact HEAD/tree/ancestry are different claims. Rebind review/verification if identity changes. Do not auto-run the saved fixed-path assembly scripts to recover it.

## Missing raw evidence is not newly recoverable context

Some original comparison stdout and the four-test runner wrapper stdout were not saved as raw files; earlier R1 round3 outputs were overwritten/lost. Their gaps and the scope of replacement observations are already recorded in the assessments/independent reports. Do not manufacture raw transcripts from summaries or describe a new run as restoration of the original output. The four-test output, diagnostic output, manifests and final independent assembly report remain the stated evidence.

## Resume state

Remain stopped at the assembly Commit Point. Next on Human continuation is the small DM-001 profile-aware Freeze contract/callsite task at exact 481dec0; no R1/assembly/witness rerun, no canonical audit or production mutation is implied by this closeout. This note introduces no new architecture decision or acceptance claim.
