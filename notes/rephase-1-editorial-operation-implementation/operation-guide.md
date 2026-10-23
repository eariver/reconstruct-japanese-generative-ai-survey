# Selected operator flow — current-epoch versioned editorial correction

This documents the implemented isolated/current-epoch operation, not permission to modify Production. Runtime source/contract must be committed and bound before producing authority; the uncommitted review overlay at HEAD409 is not itself a valid producer commit. Synthetic test review/approval records are not genuine review or Human decisions.

## Inputs / order

- Healthy `VALIDATED_DRAFT`, Architecture approved, Preview/freeze/release pending, no exception/foreign or decided authority.
- Existing P1 proposal with new authored input and canonical proposed-reader bytes; P2R retained before-set; actual persisted early scope review; P2V current-before and P3S staged4.
- Manuscript specification and toolchain specification **outside** the unclaimed `P/publication/` root. Use the strict source schemas and actual declared executable/recipe/env. Build auxiliaries stay in owned disposable storage.

The public CLI is a Python module. Examples use repository-relative artifact arguments and the repository's default config:

```sh
python3 -m scripts.survey_editorial_publication_v2 --repo-root "$REPO" prepare-publication --state "$STATE" --proposal "$PROPOSAL" --staged-manifest "$STAGED" --manuscript-spec "$MANUSCRIPT_SPEC" --toolchain-spec "$TOOLCHAIN_SPEC"
```

After prepare, inspect the real PDF and exact manuscript. Obtain independently supplied semantic/visual records and actual deterministic check results at their final repo-contained paths. The operation does not write a genuine PASS for the reviewer. An external review may live outside `publication/`, but all Candidate/seal/target refs must consistently bind its exact path and bytes.

```sh
python3 -m scripts.survey_editorial_publication_v2 --repo-root "$REPO" finalize-publication --state "$STATE" --proposal "$PROPOSAL" --staged-manifest "$STAGED" --deterministic-checks "$CHECKS" --semantic-review "$SEMANTIC" --visual-review "$VISUAL"
python3 -m scripts.survey_editorial_publication_v2 --repo-root "$REPO" validate-prepared-set --state "$STATE" --set "$SET"
python3 -m scripts.survey_editorial_publication_v2 --repo-root "$REPO" activate-publication --state "$STATE" --set "$SET" --reason "$REASON" --executor "$EXECUTOR"
python3 -m scripts.survey_agent_control_v2 --repo-root "$REPO" validate-state --state "$STATE"
```

Finalize creates Candidate then seal; neither is active until the State pointer selects the record. Use normal active-aware direct stage/Preview/Freeze/Release interfaces afterwards. Do not copy the versioned Candidate to the old canonical filename or rebind the Profile.

## Failure / repeat

- Incomplete prepare/finalize: preserve the inert partial set; a new attempt needs a new proposal ID. No same-byte takeover or deletion of unknown outputs.
- Complete orphan activation record with State still exact old: normal activate refuses; explicitly use `resume-activation --state "$STATE" --record "$RECORD"` on the same module only after reviewing the recorded failure. It revalidates the full intent/current-before/set.
- Exact already-active record: `ALREADY_ACTIVE` is a read-only consistency result, not a new approval. Unknown/unreadable/divergent State is retained for explicit investigation, not automatically overwritten or rolled back.
- Second pre-Preview correction: new proposal ID from the **active** authoring/reader/set, same accepted research. Prior immutable versions KEEP; current State COPY. Normal Human decisions remain separate.
- Existing R1/canonical revalidation after versioned activation refuses. Changed-tool/unchanged-reader renewal is the next design task; do not invent an editorial change to bypass this restriction.

Record exact source/head, inputs, commands, raw failures/terminal exits and the distinct genuine review/Human evidence in normal use. The unit's saved test/packaging scripts are historical run evidence, not approved generic replay tools.
