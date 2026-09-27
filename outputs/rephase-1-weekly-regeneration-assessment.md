# Weekly regeneration — Astra source/witness assessment

2026-09-28 JST. **Contract analysis and a bounded first/repeat mechanical-refresh witness are complete; an operational refresh writer is not implemented or accepted.** Latest shipping candidate remains **e4c8269**, unchanged. This is Astra author-side review of General execution and Explore search, not independent implementation acceptance or production adoption.

## Result that is supported

For a committed **comment-only** change in the Weekly derivation helper, with accepted/authored inputs, complete reader input, main/bib/style, PDF, manuscript, substantive review bytes and review criteria unchanged, the existing components can connect:

**strict State/derivation → reject old receipt/Gate → construct current-tool receipt → actual Gate CLI → gate-only pending context → existing revalidation CLI → strict State + explicit Gate/receipt readback.**

The corrected supplement demonstrates this first with a null pointer and then with an intact predecessor: r2 supersedes r1; the validation checkpoint and r1 remain unchanged. Runtime schema/authority code was not repaired for this experiment. This disproves the initial inference that every Core commit necessarily blocks historical State validation before new evidence can be generated. It does not establish regeneration for changed source/PDF/content or arbitrary semantic Core changes.

Primary entries:

- [Selected contract/task](rephase-1-weekly-regeneration-decision.md)
- [General corrected source analysis](../notes/rephase-1-weekly-regeneration/contract-analysis.md)
- [Explore build-transfer inventory](../notes/rephase-1-weekly-regeneration/build-transfer-analysis.md)
- [Corrected witness supplement](../notes/rephase-1-weekly-regeneration/witness-report-supplement.md)
- **[Evidence closeout/remaining limitations](../notes/rephase-1-weekly-regeneration/logs/20260927T160625Z/evidence-closeout.md)** — required alongside the earlier reports

## Evidence identity and execution

The original run `20260927T153429Z` is preserved as **partial evidence**. The supplement `20260927T160625Z` uses a new isolated synthetic repository, `/tmp/jgas-rephase-witness-supp-20260927T160625Z`, own Git database and inert origin. Source is a 657-file subset of e4c8269: committed blobs match, with one copied executable-mode difference (`survey_core_execution_bridge_v2.py`, 100755→100644, same bytes). The inventory hash covers **pathnames**, not content. These synthetic commits are not successors to be adopted as shipping candidates.

| Supplement point | Actual commit | Actual tree |
|---|---|---|
| S0 / H0 source basis | `48720ada77088ba16a4a8b1cc55fe76ff62e21b4` | `027e12f10f942eab5f2d4974c5f3b7c4cddcffbf` |
| S1 first comment-only change | `6de6bbb7c9a87d254fafe7474096013ae8b4cc1d` | `2a8386d37c832aa8197f5db2a008933cc2782da1` |
| S2 second comment-only change | `b41c58f2e1ac77cd4acfece08dd701ec2fb9e04d` | `238ddfbfb1632161931972560e8b013218e4869d` |

Root independently read those identities and the final tracked-clean status (untracked synthetic edition artifacts/caches remain). Root also ran read-only `git diff --exit-code HEAD` and `rev-parse HEAD` on preserved e4c8269 and B: both tracked trees match their unchanged heads. No tests were run by root.

The supplement's [first](../notes/rephase-1-weekly-regeneration/logs/20260927T160625Z/s-refresh-first.log), [repeat](../notes/rephase-1-weekly-regeneration/logs/20260927T160625Z/s-refresh-repeat.log) and [negative](../notes/rephase-1-weekly-regeneration/logs/20260927T160625Z/s-negatives.log) phases each have saved numeric **exit 0**. These are phased witness assertions, **not a 32-method regression suite or a full CI run**. CPython 3.12.14, pypdf 6.16.2, jsonschema 4.23.0; commands/cwd/source paths/HEAD/helper hashes/harness hashes are recorded in phase logs.

Actual-current imports are proven by separate commit-only and verification processes; the same-process import-before-commit flaw in the original run is not carried forward. The corrected first/repeat runs exercise actual receipt, accepted-source, Gate and revalidation validators. Real CLI subprocesses emit the Gate and establish records. Constructor/argv adapters and synthetic research/review/PDF fixtures are explicitly labelled; no validator/Git-success stubs are used.

r1 SHA-256 `3f1950007245e319a6ea4e8c3eae27ca80b6612075557bc9496313532a7cfb3c`, recorded `2026-09-27T16:12:03Z`; r2 `b8f828550d1ada0d8022a804122f91df838c11829aa3c88d9736feb264f6e356`, recorded `2026-09-27T16:12:57Z`. [Nine preserved artifacts and manifest](../notes/rephase-1-weekly-regeneration/logs/20260927T160625Z/preserved-artifacts/manifest.json) distinguish run-bound hashes from later current snapshots. Root corrected the manifest's S0 tree transcription against both `w0a-sidecar.json` and actual Git; the original wrong value is retained in its correction field.

## Scope of positive/negative conclusions

- The two new receipts preserve exact `accepted_refs` and `authored_refs` lists and replay against current source. Gate derivation references the new receipt; success is not merely a new timestamp.
- Equality/criteria guards belong to the **experimental harness**, not a shipping refresh command. Ordinary State validation is intentionally historical-checkpoint consistency, not complete generated-derivation replay. Explicit Gate/receipt and review checks are necessary.
- Windowed delta assertions cover receipt-only change, Gate-only change, and new revalidation-record + State change. Earlier pre-snapshot verification is not delta-covered; exclusions are `.git`, `.witness-evidence` instrumentation and caches. Supplement sidecars retain assertion outcomes/hashes, not the in-memory full snapshots. Do not claim whole-operation atomicity.
- Observed negatives: changed reader surface → receipt drift; changed accepted Architecture → checkpoint/approval mismatch; an added applicable review-contract check with unchanged review bytes → `Publication Review check family differs from bound Profile`; malformed prior pointer → predecessor authority SHA mismatch. No-op revalidation is also rejected. A FAIL review in the original run is separate from the corrected **criteria** mutation.
- N1/N2's reusable harness oracle catches its own sentinel via broad `Exception`; its green alone is insufficient. Root instead reviewed the saved actual `ValueError`/`AgentControlError` messages. N3 has a specific message assertion; N4 catches the runtime error type. These scripts must not be promoted verbatim into accepted regression tests.
- Under the changed review contract, strict State still returns `[]`; the actual review validator rejects. This is consistent with historical checkpoint validation and shows why State-only verification cannot justify review reuse.

## Retained failures and procedural/evidence limitations

1. Initial setup failures, residue/no-overwrite collisions, State-watchlist mismatch and missing restore/finally are preserved. An original fixture-only `reset --hard` and broad `git clean` were **procedure deviations**, not implicitly authorized repairs. The failed intermediate commit remains in that fixture's reflog; raw shell transcripts are missing. The supplement used a fresh fixture and did not repeat those operations. No production or preserved-candidate mutation was observed.
2. The supplement's first pre-write missing-directory harness failure and an output-guard refusal were disclosed; the first traceback was tool-captured but not durably file-saved. Do not call the execution history clean.
3. The supplement failed to retain the original S0/H0 Gate **bytes** before the first replacement. Its hash in the checkpoint is not an archive. Later receipt/Gate versions and immutable r1/r2 are preserved; original missing bytes are not recreated. Thus the selected **full retention/operational writer safety condition remains unmet**, even though the first/repeat runtime connection is demonstrated.
4. The original `receipt_old_sha256` field was a parsed-object hash, not raw-byte hash. Supplement/closeout identify the distinction. Do not mix original-run H0 receipt (`ca04815b…`) with supplement-run H0 receipt (`4d98b3c7…`); use the artifact manifest's full hashes, not the closeout table's abbreviated/transcribed suffix.
5. Supplement sidecar/plog guards do not protect every sub-log/exit path on an interrupted retry. **Do not auto-run either saved harness.** Any justified later test must use a fresh fixture/log target and corrected explicit-failure oracles. No repeat solely to polish evidence.
6. No Candidate-stage publication-candidate validation, TeX compile, real visual/Human review, production transfer, Windows/Actions execution, full multi-file rollback or independent witness audit is claimed. The 32-method CLI PASS remains its earlier exact-head result, not a result from this analysis.

## Build/application decisions retained

Explore's inventory confirms the configured Weekly repository PDF is `survey_root/main.pdf`. `main.log`/`main.pdf.sha256` are allowed optional local outputs; the workflow checks its log but uploads PDF+digest only. An in-tree artifact→canonical-PDF transfer/real preflight producer was not found in the bounded search. Reference hashes do not execute or prove PDF preflight. The older semantic-quality helper has a mismatched handler literal/preview path and is not a second current canonical route. Existing semantic/visual reviewer responsibility remains distinct.

Because this witness leaves rendered/PDF bytes unchanged, these build gaps are not prerequisites to its narrow observation. They remain prerequisites to a changed-output/full-application claim. Whole candidate **NOT_READY**, step 4/B3 OPEN, canonical seven-point audit unstarted; no lifecycle savings measured.

## Next bounded task — operational mechanical-refresh contract, before code

Do not rerun the positive witness or create a generic classifier/report CLI. General should return a **small concrete interface/path inventory for a mechanical-only receipt/Gate refresh operation** in the existing Weekly/Gate/agent owners, using this witness as function evidence. Root must resolve the writer protocol before code:

1. Entry only at pre-decision VALIDATED_DRAFT with exact immutable validation/predecessor authority. Old receipt/Gate may be stale only in current-tool replay; their old byte identities must still be connected to actual checkpoint/active revalidation authority. No arbitrary rehashed stale input gets accepted.
2. Explicitly guard same accepted/authored refs, exact complete reader bytes, main/bib/style/PDF/manuscript/review/QA bytes, current clean tools and unchanged substantive review requirements. Determine the minimal criterion/control closure from existing code; unsupported criteria or output changes stop. No synthetic PASS, history reconstruction or upstream reopening.
3. Define owned writes **receipt, Gate, existing revalidation record and State pointer only**, and retain both superseded receipt AND Gate bytes before any replacement. Recheck observed bytes before replacing; preserve existing pointer/record authority. Evidence retention is inert provenance, not another approval ledger.
4. Define failure states exactly: existing revalidation rollback covers its record/State, not receipt/Gate. Either restore only this operation's unchanged owned writes after failure using captured bytes, or specify a durable fail-closed resumable pending state. A generic transaction framework and blanket file deletion are not selected. Do not promise atomic publication from the current witness.
5. Propose the smallest runtime/test path set and meaningful first/repeat/criteria/upstream/concurrent-drift/retention/no-write oracles. Replace the witness's broad exception and stale-import flaws; preserve existing initial-publication guard semantics. Return the contract for Astra decision before runtime edits. If a real new authority/schema/history mechanism is necessary, return the concrete blocker.

This is a new operational contract task, not permission to ship the experimental harness. Scope remains same-byte refresh; changed-content/build regeneration and Special/DM/optional findings transport keep their separate dispositions. Independent implementation review follows only after a future exact candidate exists.
