# SP D165 binding correction r5 — rationale (input-only, no active writes)

Root re-review (`sp-evidence-rereview-20261105T003000Z-qual-addendum-20261105T010000Z.md` Q3)
holds prior BOUNDED_PROCEED but narrows D165: bound `sp17-pr27742.json`
26122B `3728e08d…` contains all cited numericals (verified counts:
4.0068×1/4.0126×1/98.0×1/QSA×4/PLE×2/97.7×1/bit-identical×2/jaccard×1/
0.975×1/UD-IQ1×1/2.84×1/qwen4exp×5/converter×1); packet commits/comments
(`4143b4ad…`/`c1b1f7d5…`/`541bd239…`) are chronology corroboration only,
not staged task-bound authority. Card phrase “per commit messages” is struck
as authority.

Smallest fix: `sp-corrected-input-r5-D165fix-20261105.json` 355643B
`697a4ed0…` changes ONLY `EFF-D165 claims[0].context` (bound-body report +
packet-as-context disclaimer) and `verification[0].finding` (same facts,
numericals bound to pr.json, packet 65+144 as context-only, binds staged Raw
`sp17-pr27742.json` only). All facts/status/claims preserved; 159 other
records + completeness identical; 160/15 counts unchanged. No new fetch,
no schema/source change.

Prior SP semantic PASS is HELD for this final artifact fix; do not cite it
as unqualified PASS until re-review of the corrected card. Next (after
root+independent review): input-only preflight stages 1 NEW input, then
same-stage retry against current canonical `253cb2ea…`/`18a05292…` (still
CAND unaccepted) with original backups preserved.
