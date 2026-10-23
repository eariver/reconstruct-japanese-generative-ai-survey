# Independent R4D authority review — high/low IO, schema-cache (author-independent)

Fresh AUTHOR-INDEPENDENT implementation source review. Not author / Worker / root.
Scope is ONLY high+low authority/IO/schema-cache as tasked. Another reviewer owns
other consumers/tests; workflow inventory is NOT duplicated here.

No run / import / build / test / network / Git mutation in this review. Only
read-only file reads plus read-only Git verification (`rev-parse`, `status`,
`log`, `remote -v`, `wc -l` for scope sizing) plus this one new review file.
DST was NOT edited. `DST readonly root no editing pending` observed below.

Governing (read):

- `outputs/rephase-1-editorial-operation-contract-decision.md` (d880, all 191 lines, V selection §§1–10).
- `notes/rephase-1-editorial-operation-contract/astra-review-resolution.md` (root resolution, DESIGN BOUNDED COMPLETE, Overriding qualification pointer, §3 next-task).
- `notes/rephase-1-editorial-operation-contract/independent-technical-design-review.md` + `independent-operation-design-review.md` (both DESIGN_BOUNDED_PASS, explicit limits; technical reviewer did NOT re-certify hashes/caches/runtime).
- Implementation root selection: `notes/rephase-1-editorial-operation-implementation/astra-implementation-selection.md` (L/H/C split, frozen low interface, exact 50-row closure, 719-file freeze rule).
- Returns R1–R4 (read as history, NOT adopted as source proof):
  `astra-integration-return-r2.md`, `astra-verification-return-r3.md`,
  `astra-verification-return-r4.md`, `correction-r3/R3-report.md`,
  `correction-r3b/R3c-report.md`, `correction-r4/R4-report.md`,
  `correction-r4c/R4c-report.md`, `correction-r4d/R4d-report.md`.

Old reports remain historical. No wrong-tree / transcription-alias adoption (see §1).

## 1. Source verification (actual, not typed tree)

Stable SOURCE (read-only):

- Root: `/tmp/opencode/jgas-editorial-r4d-20261021T170000Z/candidate-partial-b40de60`
- `git rev-parse HEAD` → `4191503bfe1bd6aadd90a107dc4fd7c601e53f6c` (verified via Git, not typed).
- `git rev-parse HEAD^{tree}` → `8ecd325c762bd70b37b847ad831234245345aa20` (40 chars, from Git).
- `git status --porcelain=v1` → empty (clean). `git log --oneline -3` head line is `4191503 SOURCE snapshot: R4d low full-union anchor projection + P1/P2R/P2V recipe closure, 719 files`.
- `git remote -v` → `https://example.invalid/workerR4d-r4d-snapshot.git` (inert, fetch+push same).
- Manifest `notes/rephase-1-editorial-operation-implementation/correction-r4d/source-manifest-r4d.json` head/tree/count match the Git values above (`count: 719`). Manifest body not re-hashed entry-by-entry here; R4d-report spot-check claim is NOT adopted.
- File count: manifest `count: 719`. Task note `619?` is NOT adopted; actual observed is 719 via manifest + Git log message. No speculation beyond that.
- DST `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60` observed dirty (`M` on 20+ tracked paths incl. workflows/config/schemas/scripts + `??` new editorial modules/schemas/tests + `__pycache__`). DST was NOT edited, NOT used as source. No DST bytes adopted.

## 2. Exact read scope (this reviewer) / unproved

All paths below under the R4d SOURCE root. Sizes via read-only `wc -l` / `wc -c`
(scope sizing only, not execution):

- `scripts/survey_editorial_publication_v2.py` — 3483 lines, read 1–3483 in full
  (7 chunks: 1–450, 451–1050, 1051–1600, 1601–2200, 2201–2800, 2801–3483).
- `scripts/survey_publication_set_v2.py` — 1959 lines, read 1–1959 in full
  (4 chunks: 1–350, 351–750, 751–1200, 1201–1650, 1651–1959).
- `scripts/survey_schema_v2.py` — 185 lines, read 1–185 in full.
- `scripts/survey_agent_control_v2.py` — 2720 lines, targeted ONLY:
  `_validate_checkpoint_record:382–495`, `validate_agent_state:498–561`,
  `_exclusive_create_record_bytes:1922–1962`, `_record_identity_matches:1965–1983`,
  `_atomic_replace_state_bytes:1986–2091`, `revalidate_publication_surface:2093–2171`
  (legacy-refusal + canonical-mode guard). Remainder of agent UNREAD here.
- New strict schemas (read in full):
  `schemas/publication-surface-revalidation.schema.json` (247 lines),
  `schemas/editorial-publication-set-v2.schema.json` (92 lines),
  `schemas/editorial-publication-source-manifest-v2.schema.json` (92 lines),
  `schemas/editorial-publication-build-record-v2.schema.json` (94 lines),
  `schemas/editorial-manuscript-spec-v2.schema.json` (67 lines),
  `schemas/editorial-toolchain-spec-v2.schema.json` (27 lines).
- Grep-only (no full read): `survey_editorial_publication_v2.py` hardlink/nlink/ancestor/symlink/O_NOFOLLOW sites (59 hits),
  `state_path`/canonical-State sites (21 hits); `survey_agent_control_v2.py` fsync/owned/close sites (19 hits).
  `survey_reader_publication_v2.py` / `survey_reader_surface_gate_v2.py` / Weekly/Longform derivation /
  stage / freeze / orchestrator / handoff / human-gate / export / release / P1/P2R/P2V/P3S / R1 /
  tests / workflows / config NOT re-read here (other reviewer + remaining matrix).

UNPROVED in this review (explicit): all runtime success/negative oracles, second
pre-Preview correction, R1×2 anchor/refuse-after, active vs historical readback,
lifecycle Preview/Freeze/Release, export, fault/resume matrix, close/postread
faults, performance, representative quality, measured cost, other-consumer wiring.
No test was run. No fixture was built. No authority was generated.

## 3. Verdict

**BOUNDED source verdict (high+low authority/IO/schema-cache only), subject to
remaining matrix. No CHANGES_REQUIRED real blockers in this scoped read.**

This is NOT a whole-operation PASS, NOT an implementation acceptance, NOT a
Human approval, NOT an audit. It covers ONLY constructibility/invariants actually
read above. Every §4–§8 item below is a source-construct reading, not a runtime
proof. The final matrix on the 4191503 epoch (both routes, repeat, R1×2,
consumer/lifecycle, fault/resume, regressions) plus the separate other-consumer/test
review remain required before any release-ready claim. R4c fixtures (b54a1f2 epoch)
are NOT reblessed as 4191503 evidence here (see §9).

No fixes designed, no new features authored.

## 4. Full-15 seal, Candidate-before-State, State-only selection — constructible

- Low `PUBLICATION_ROLES_15` (`survey_publication_set_v2.py:69–85`) is exactly the
  contract §4.2 15 keys. `validate_seal:445–572` enforces `kind=EDITORIAL_PUBLICATION_SET_V1`,
  `status=SEALED_INERT`, `set_sha256` canonical-excluding-self, exact proposal-namespace
  layout (`<P>/proposal.json`, `<P>/staged-source/staged-source-manifest.json`,
  `<P>/publication/build-record.json`, seal at `<P>/publication/publication-set.json`),
  exact 10 fixed role paths + 2 reviews inside `<P>/publication`, all 15 as
  `{path,sha256,byte_count}` with live SHA+size check, duplicate-path refusal,
  staged-trio mapping (`main/bibliography/style` → `validated-source/bibliography/style`,
  `primary`/`staged_refs` refused), pdf-digest opens-with-PDF-SHA, per-role
  `issue_id` agreement, embedded-ref cross-check vs seal map, receipt/manuscript/bundle/
  candidate/Gate/build cross-bindings. Seal stores NO activation hash, NO before-State
  copy, NO `external_reviews` duplicate map (schema confirms: top keys are
  `schema_version/kind/status/issue_id/research_profile/publication_profile/proposal_ref/
  staged_manifest_ref/build_record_ref/roles/set_sha256`).
- High `_seal_roles:2189–2321` builds exactly `SEAL_ROLES` (same 15), `fr_rel` from
  final-boundary bytes, P1 reader/authoring as original files (not copies),
  validated/bib/style from staged trio, reviews from Candidate binding (not alternate),
  duplicate-path refusal, manuscript/bundle/candidate/Gate/build cross-bindings
  (manuscript primary + BIBLIOGRAPHY/STYLE vs staged, bundle source/PDF vs staged/seal,
  QA result refs pinned, candidate manuscript/source/PDF/bundle vs seal, Gate editorial
  derivation + receipt binding, build outputs/declared-inputs vs seal/staged).
  `finalize_publication:1853–2186` writes seal LAST after fresh P2V + receipt/manuscript/
  build revalidation, then `validate_prepared_set` readback. No permission token returned.
- Candidate finalized BEFORE State: `finalize_publication` builds Candidate via actual
  `publication.build_candidate` to system-temp + exclusive transfer (2100–2137) BEFORE
  seal; `activate_publication:2733–3207` requires `validate_prepared_set` (full seal incl.
  Candidate) BEFORE any record/State write. Activation writes ONLY new exclusive record
  then known-byte State temp+replace updating ONLY `publication_revalidation_provenance`
  (new object copies old + pointer replace). No canonical Candidate/source/QA rewrite.
- Selection is State-pointer only: low `resolve_publication_selection:1624–1800`
  returns derived `{mode,record_ref,set_ref,active_set_ref,activation_record_ref,
  canonical_anchor,canonical7,effective7,candidate_ref,candidate_path,roles}`,
  modes `CANONICAL`/`VERSIONED_ACTIVE`, no fallback (invalid pointer raises, never
  safe-fallback). `resolve_publication_artifact_path:1803–1846` + central
  `resolve_stage_artifact_path:1849–1895` recompute+compare (candidate State-aware,
  others exact template). `resolve_publication_mode:1909–1932` is probe-only;
  `require_active_or_canonical:1935–1948` + `assert_canonical_publication_mode:1951–1959`
  refuse revised mode before writes. No caller-verified dict accepted (all refs reloaded
  + hash-checked from file bytes).

## 5. Raw-first refs, strict JSON/schema branches, no tokens/cycle — constructible with one strictness qualification

- Raw-first: low `resolve_raw_path:162–174` (lexical refusal + ancestor lstat no-follow +
  leaf regular-only), `resolve_raw_dir:177–196`, `_read_bytes_nofollow:199–219`
  (`O_RDONLY|O_NOFOLLOW`, fstat regular, chunked read), `read_repo_bytes`/`sha256_repo_file`.
  High `_lexical_rel:194–208`, `_safe:226–278` (lexical + `core.repo_local_path` + ancestor
  lstat + leaf lstat), `_check_file:281–296`, `_read_bytes_bounded:299–328`
  (`O_RDONLY|O_NOFOLLOW`, size bounds). Writers use `O_CREAT|O_EXCL|O_NOFOLLOW`
  (high `_exclusive_write_bytes:331–434`, agent `xb` exclusive). Symlink/FIFO/socket/dir
  refused on repo-contained reads. Toolchain external executor is the ONLY documented
  symlink-chain exception (high `_resolve_toolchain_executable:121–163`, link→real pin +
  recheck, real must be regular file) — explicitly justified as external executor, NOT repo
  authority. Honest scoping (see §10 for held-vs-lstat wording).
- Strict JSON: low `_no_duplicate_object:232–238` + `_parse_json_strict_bytes:241–249` +
  `load_json_strict:265–273` + `load_and_validate_json_strict:282–289` refuse duplicate
  keys before `schema_gate` validation. **Qualification (not a blocker):** high path uses
  `schema_gate.load_and_validate_json` (`survey_schema_v2.py:175–185`, plain `json.loads`
  without duplicate hook) + `core.load_json` for receipt/proposal/staged/State/seal
  (`validate_editorial_receipt:576,628,640`, `validate_prepared_set:2342`). Duplicate keys
  in high-loaded docs would be last-wins, NOT explicitly refused. Mitigated in practice
  by (a) prepare constructs docs programmatically (no duplicates at creation),
  (b) exclusive writes + seal role file-SHA binding (post-creation duplicate tampering
  changes file bytes → seal SHA drift → refused), (c) canonical digest recomputed from
  parsed (last-wins) vs recorded (no-dup) — mismatch if values differ. Still a contract
  strictness gap (low strict, high lenient). Fix would be to route high loads through
  low strict loader or duplicate-refusing parse; NOT claimed as safe-to-ignore, but NOT
  a real unsafe-activation blocker (SHA binding catches).
- Schema branches: `publication-surface-revalidation.schema.json` is `oneOf`
  `legacy_revalidation` / `editorial_activation`, both `additionalProperties:false`,
  legacy `reason_class=REVIEWED_CORE_CHANGE` verbatim shape, editorial exact §4.3 keys
  (`schema_version/kind/issue_id/reason_class/reason/lifecycle/prior_checkpoint/supersedes/
  canonical_anchor/before_state_ref/before_active_digest/before_candidate_ref/set_ref/core/
  executor/recorded_at/establishment`), `supersedes` common edge, `canonical_anchor`
  `{kind,ref}` enum, SHA patterns `^[0-9a-f]{64}$`, commit `^[0-9a-f]{40}$`, dates
  `format:date-time` + `core.parse_instant` checks in code. No top-level required leaking
  across branches. Agent legacy writer refuses `REVIEWED_EDITORIAL_CORRECTION`
  (`revalidate_publication_surface:2109–2114`). Mixed later-legacy-after-editorial refused
  in `derive_canonical_anchor:1004–1006`. No `active_set`/verified-dict/pending boolean
  permission (grep: no such param; all validators reload from file bytes).
- No cycle: receipt schema has NO `seal_path`/`set_ref`; `validate_editorial_receipt`
  never calls seal/activation (imports agent/core/staged/weekly/longform only);
  seal validation never requires activation; activation stores `set_ref` (seal→record→State
  acyclic); Gate requires receipt before itself (high finalize builds Gate with early-scope
  receipt binding, `derivation.route=EDITORIAL_PUBLICATION_V1`). Source proof
  (`_verify_staged:532–549`) is P3S historical only, no P2V/seal.

## 6. Receipt: NEW authoring + FULL accepted + Draft/reader render + closure-50, no repeat skip — constructible

- NEW authoring: `validate_editorial_receipt:657–665` requires authored roles exactly
  `{proposed-publication-authoring,accepted-draft-archive}` + equality to
  `proposal.proposed.authoring_input_ref` (path+sha). New authoring bytes re-read +
  SHA-checked (`786–795`). Route rederivation calls actual
  `weekly.load_derivation` / `longform.load_derivation_for_readback` on NEW authoring
  (`797–878`), NOT old initial input.
- FULL accepted UNCONDITIONAL: both routes normalize receipt `accepted_refs` + ctx
  `accepted_refs` as exact named `{name,path,sha256}` sorted-unique, no-dup, then require
  equality (`806–829` weekly, `879–898` longform). Comment + code state BEFORE-kind only
  locates historical archive refs, NEVER substitutes research equality. Before-receipt
  generic handling (`691–701`) accepts initial (`publication-semantic-input/
  drafting-authored-archive`) OR prior-editorial (`proposed-publication-authoring/
  accepted-draft-archive`, kind must be `EDITORIAL_PUBLICATION_SOURCE_V1`), else
  `BEFORE_AUTHORED` refuse. No `if editorial: skip accepted compare` branch exists.
  Archive path+sha vs ctx `archive_path` bytes + before draft ref enforced
  (`830–846`, `899–912`). Prepare mirrors the same unconditional derivation
  (`1659–1690`).
- Draft/reader canonical render: reviewed input must equal `proposal.proposed.proposed_reader_ref`
  (`713–719`, incl. canonical-SHA equality); scope must bind reviewed input + carry
  `editorial_correction_scope V1/WITHIN_APPROVED_AUTHORITY` + before-reader equality
  (`720–739`, postrender-as-scope refused); staged trio exact `{main,bibliography,style}`
  (`main→primary` mapping, `primary`/`staged_refs` alias refused, `751–775`); weekly
  `surface==reviewed_obj` + `render_main/render_bibliography` vs staged + closure
  (`851–868`); longform FILE==canonical bytes + surface equality + heading/closure + render
  vs staged (`917–935`).
- Tool closure-50: `_editorial_closure_rows:1798–1833` is P3S `_route_code_deps(route)`
  sorted-unique, `path==name`, current-bytes SHA, exact count 50, no discovery.
  `validate_editorial_receipt:939–1026` enforces exact union set (missing/extra refuse),
  per-row path==name + current-bytes + commit-blob double-check, current contract equality,
  commit ancestor + filtered canonical subset via actual route `_verify_head_bytes` /
  `verify_tool_basis` + extra-closure commit check. No old-epoch migration (old 22/27
  via existing helpers preserved). R2 performance-cache interaction is schema-cache only
  (see §10); no State/result caching.

## 7. History anchor, retained COPY/KEEP, active-15 projection — constructible (R4d fix verified in source)

- Canonical anchor: low `derive_canonical_anchor:915–1053` implements §5 cumulative
  (original checkpoint if no legacy, else latest legacy before first activation; repeated
  retain same; later-legacy-after-editorial fail-closed; each legacy cumulative vs ORIGINAL,
  `prior_sha256==original`, never incremental; `supersedes non-publication role` guard).
  `_build_anchor_chain` (high `2495–2542`) + `_walk_chain_backwards` (low `840–868`)
  bound depth-32, cycle on `(path,sha256)`, byte-identical disk check.
- R4d full-union fix present in source: `_full_original_union:1464–1485` (ALL checkpoint
  rows, no 7-filter) + `_anchored_canonical7:1488–1588` legacy branch validates cumulative
  rules over FULL union, NEW `superseded name ∈ PUBLICATION_ROLES_7` guard, live-verifies
  EVERY effective row via `_verified_row_4key` (SHA-before-size), then projects exactly 7.
  No-legacy branch + `_canonical7_from_validation:1407–1433` (internal 3-key, never exported)
  untouched per R4d-report. `derive_canonical_anchor` legacy loop has the same
  superseded-canonical guard (`1026–1029`). `resolve_publication_selection` legacy mode
  (`1693–1766`) cross-checks anchored projection vs head-record cumulative rows (path+sha
  per role). This matches R4d-report diagnosis (upstream `evidence-accepted` preserved rows
  vs 7-only map). Source fix is narrow (low only, no agent wrap) as reported.
- Retained COPY / KEEP: low `_validate_proposal_retention_identity:1134–1245` enforces
  proposal/staged/retention issue/Profile/proposal_id/path/sha graph, `before_state_ref ==
  proposal basis == retained basis`, unique `state:authority COPY_BEFORE_REPLACEMENT` row
  with `retained_dest=<P>/retained/before/<original path>` + COPY bytes/sha/size triple
  check, retained-State parse + Profile ref + unique matching `KEEP_IMMUTABLE` Profile row
  + KEEP bytes/size + Profile/State vs proposal identities + `source_root` + proposal-dir
  derivation. High activate repeats explicit retained pin BEFORE any record write
  (`3019–3090`, COPY vs KEEP branches, no caller trust). First-canonical before-graph
  conservative capture preserved (P1/P2R paths untouched here).
- Active-15 vs canonical-7: low `_verified_active7_from_seal:1591–1621` (seal 7, live SHA
  before size, `origin=ACTIVE`) vs `_anchored_canonical7` (`origin=ORIGINAL`); editorial
  selection returns `canonical7=anchored` + `effective7=active7` + `roles=seal.roles`
  (`1768–1798`); `_recompute_before_digest:1282–1355` derives before-effective7 from
  original / latest-legacy cumulative / prior-seal-7 per supersedes branch + before-Candidate
  PDF binding, then `before_active_digest` (sorted 7 + candidate/null, dup identity/path
  refusal). Agent `_validate_checkpoint_record:404–436` editorial branch uses anchored
  `canonical7` (4-key shape-checked) for `validation` checkpoint only, else `{}`; no
  research rebind.
- Every field path/SHA/size: low `_check_file_ref` exact `{path,sha256,byte_count}` +
  live SHA+size; `_check_authority_ref` exact `{path,sha256}` + live SHA. No arbitrary
  alias: `primary`/`staged_refs` refused in seal/staged/receipt/build paths (low `529–535`,
  `611–614`; high `1136–1137`, `136–137`, `1565–1568`). **Qualifications:** (a) receipt
  `reviewed_reader_input` accepts 2-key OR 3-key (low `626–631`) while seal role is 3-key —
  lenient but size still bound via seal live check; (b) build `declared_inputs` accepts
  `{path,sha256}` OR `{path,sha256,byte_count}` (low `789–790`) with byte equality only if
  present — SHA binds bytes (hence size) regardless; (c) receipt `outputs`/`authored` are
  2-key/3-key per schema, size cross-checked via staged/file reads. None allow path/alias
  substitution.

## 8. R4 orphan/inode/fsync/State-classification — source matches R4 intent

- Orphan fork: high `_next_record_seq:2560–2659` is deterministic `predecessor_seq+1`
  (State pointer, null→1; unknown branch refuses; legacy max listed for declaration only,
  NEVER used as next; collision via lstat before write). `_refuse_if_intent_exists:2662–2730`
  scans `publication-surface-revalidation-rN.json` (lstat, exact naming, skip symlink/non-reg),
  matches exact intent (`issue_id/supersedes/before_state_ref/set_ref/prior_checkpoint` +
  editorial kind/reason), complete records only (unreadable/foreign skipped), raises
  `INTENT_COLLISION` pre-write (ordinary refuses, explicit resume required). Called in
  `activate_publication` after record schema validation, before retained pin/first write
  (`3017`). Legacy writer (`agent.revalidate_publication_surface`) unchanged max+1 (R1-before
  preserved). **Qualification:** intent scan `except Exception: continue` (2706–2711) silently
  skips unreadable/corrupt exact-name files. Same-seq collision still refuses via lstat
  (so same-slot orphan blocks regardless of readability); different-slot same-intent with
  unreadable incumbent could fork. Narrow (requires unreadable exact-name incumbent +
  free next slot); incomplete/unreadable is NOT complete intent per contract, manual recovery
  expected. Note as residual, NOT a real blocker.
- Cold partial / ALREADY_ACTIVE / INDETERMINATE:
  - Activate ALREADY_ACTIVE (`2789–2818`) is read-only BEFORE P2V/anchor/seq: requires
    `VERSIONED_ACTIVE` + input seal path/sha == selection `set_ref`, then strict
    `agent.validate_agent_state` (no errors) + `validate_prepared_set`, returns State-pointer
    record path (NOT seal path), `observed=new`. No takeover/fresh approval.
  - Resume ALREADY_ACTIVE (`3256–3274`) requires State pointer path/sha == record path/sha +
    strict State + full set, returns record path. Orphan resume (`3275–3341`) requires
    `supersedes == State pointer` (else `INDETERMINATE`, preserve, no overwrite, `3277–3279`),
    full set + `before_state == current State` + fresh P2V + pre-install drift check, then
    guarded replace + post-install strict selection/record/set checks with
    old/new/unknown observed. Unknown State never overwritten.
  - Partial record (crash during exclusive create): owned partial preserved, never unlinked
    (high `425–428`, agent `_drop_own_temp` identity+bytes gated `2021–2043`); ordinary
    refuses collision; resume requires complete valid record (`validate_activation_record`),
    so partial blocks slot pending explicit manual recovery per contract §7 (never delete
    referenced/possibly-referenced record). Cold resume needs no in-memory owned_id (file
    bytes + State comparison only). Scope matches contract.
- Fsync/owned/close/State-temp:
  - Fsync NO LONGER swallowed: agent `os.fsync` failures raise `AgentControlError`
    (`1942–1945`, `2009–2012`); high `_exclusive_write_bytes` fsync raises `FSYNC_FAILED`
    (`398–401`); disposable build input/recipe fsync raise `FSYNC_FAILED` (`1277–1292`).
    Other `except OSError: return False/preserve` are existence checks, untouched. Verified.
  - Owned inode rechecked immediately pre-State: high activate captures `record_owned_id`
    (fd dev/ino via agent `xb` creation) + `record_bytes`, then before `_atomic_replace_state_bytes`
    rechecks symlink-refuse + `(dev,ino)` equality + byte equality (`3129–3149`),
    same-byte foreign swap refuses (`RECORD_OWNERSHIP/EXPLICIT_RECOVERY`, preserved).
    Agent `_record_identity_matches:1965–1983` pins the same inode+bytes rule.
  - **Close-error MUST-inspect (finding, NOT a blocker):** agent uses `with open(xb)` —
    body `AgentControlError` + `__exit__ close()` OSError would chain (close error surfaces,
    primary as `__context__`), NOT swallowed but potentially masked as outer error; close
    errors propagate as raw `OSError`, NOT `AgentControlError`-classified. High uses
    `os.open` + `finally: try: os.close except OSError: pass` (`429–434`, same in
    `_read_bytes_bounded:324–328`) — close errors SWALLOWED (primary preserved, secondary
    lost). After successful fsync+fd-readback, close-error data-loss risk is negligible
    (durability already ensured + verified via fd), so swallowing does NOT create unsafe
    activation. But contract §9 “every record/State write/close/late-readback failure
    classified” is NOT literally met for close. Disclose as residual: no durability hole,
    but close failures are unclassified (high) / raw-OSError (agent).
  - State temp before/after replace classified: agent `_atomic_replace_state_bytes`
    rechecks live==expected_old before temp, temp exclusive+fsync+identity+readback,
    live recheck + temp identity+bytes recheck immediately before `os.replace`, replace
    failure + post-replace readback classified (`1998–2090`). No global CAS claimed
    (docstrings: exclusive-create + known-byte replace only, single-writer assumption
    explicit in contract §7; code never asserts power-loss atomicity).
- Hardlink/symlink/ancestor honesty: symlink ancestors refused via lstat (low
  `_walk_existing_ancestors:128–146`, high `_safe:238–263` + writer parent walk `351–367`);
  leaf symlink/FIFO refused; opens use `O_NOFOLLOW`; record seq listing + intent scan skip
  symlinks. NO hardlink (`st_nlink`) check anywhere — but NO hardlink-safety claim in
  code comments either (low/high docstrings claim lstat-no-follow + FIFO/dir refusal +
  `O_NOFOLLOW`/`O_EXCL`, NOT link-count pinning). `O_EXCL` refuses pre-existing hardlink
  target + fd-captured inode+readback defeats post-create hardlink aliasing. Honest within
  single-writer scope. **Wording note:** high `_exclusive_write_bytes` comment says
  “Held-ancestor checks” but implements lstat walk + `O_NOFOLLOW`/`O_EXCL`, NOT dirfd-pinned
  `openat2` holding — TOCTOU window between lstat and open remains (mitigated by NOFOLLOW+EXCL
  + owned-identity recheck pre-State). Contract §7 already requires disclosing remaining
  window + fault tests; code does NOT explicitly restate the window at the writer. Note as
  honesty qualification, NOT enforcement hole (no unsafe bypass found).

## 9. Writer recipe/toolchain, review genuineness, source-commit epoch — constructible

- Real fixed recipe + external toolchain pin + allowlisted env + full logs + exclusive build3:
  `FIXED_RECIPE_STEPS` + `EXPECTED_ARGV_*` + `REQUIRED_RECIPE_MARKERS` + `REQUIRED_BLOCKING_LOG_PATTERNS`
  + `ALLOWED_ENV_KEYS` + `CONTROLLED_SYSTEM_PATH_SUFFIX` (high `60–118`); toolchain spec
  validated exact argv (must EQUAL expected tuple, not token membership), recipe allowlist,
  env allowlist (PATH/PYTHONPATH/LD_LIBRARY_PATH/GIT_* refused), recipe `.latexmkrc` markers
  (`1033–1094`); disposable build copies trio via bounded reads, `O_EXCL|O_NOFOLLOW` creates,
  fixed cmds with absolute exe/companion (no shell string, no `-e`, no output-root override),
  versions/link+real+sha recorded, pre/post source+recipe unchanged checks, real PDF/log gates
  (regular, non-empty, `pypdf` pages≥1), blocking-pattern scan over combined logs+`main.log`,
  full raw preserved (no rmtree/truncation), exclusive build3 transfer with pinned-bytes +
  final readback (`1129–1400`, `1461–1496`). `build_sha256` INCLUDES input/output refs,
  excludes ONLY itself (map-resolution “excluding outputs” correctly rejected).
- Body completeness / genuine review operational-only: manuscript spec requires
  `FULFILLED`-only coverage/requirements with locations/detail (schema const + code
  `1116–1125`); deterministic checks via existing `quality.validate_checks` (no family PASS
  by schema, `1951–1955`); supplied semantic/visual reviews validated typed + PASS required
  (`2021–2038`, `2416–2431`), Gate editorial derivation with early-scope binding
  (`2039–2088`, `2304–2310`), Candidate via actual builder + validator (`2088–2137`).
  Runtime NEVER synthesizes PASS (prepare ends at receipt/manuscript/build-record;
  finalize consumes persisted review files only). Genuineness/provenance/independence remain
  operational evidence per contract §3 (synthetic fixtures visibly separate) — correctly NOT
  inferred from schema.
- Meaningful source commit before authority, no old-epoch rebless (source scope):
  R4d SOURCE is a real commit (4191503, 719 files, inert origin, clean). Receipt
  `current_tools` pins `repository_commit_sha` (ancestor-of-HEAD + control-root + closure
  verified, `984–1020`) + contract equality, so old-epoch receipts do NOT auto-migrate.
  R4d-report reuses R4c fixtures (b54a1f2 epoch) without rebuild, justified ONLY by
  no-legacy-branch-untouched argument — that fixture-epoch carry-forward is NOT adopted
  here; final-matrix epoch on 4191503 (parameterized fixture scripts rerun) remains required
  (see §3 UNPROVED). No source rebless in code (no pending-bypass, no old-epoch acceptance).

## 10. Schema-cache (Gate) — constructible, matches R2 authorization

`survey_schema_v2.py` (185 lines, fully read) implements EXACTLY the R2-authorized bounded
repair: content-keyed cache of immutable compiled validators + metaschema check ONLY.

- Every call still safe-checks path (`is_symlink`/regular), reads current bytes, parses
  FRESH JSON, validates FRESH instance+format via (possibly reused) compiled validator
  (`load_schema:126–143`, `validate_instance:146–172`). No State/authority/result caching
  (`_CACHE` holds ONLY compiled `Draft202012Validator`, keyed per §10).
- Key includes ALL resolution inputs: absolute resolved path + content-SHA + jsonschema
  version + draft id + format id (`_cache_key:82–83`, `_CACHE_KEY` use `106`). Changed bytes
  at same path miss (different SHA → `check_schema` + recompile). Same bytes hit skips ONLY
  redundant metaschema+compile. Bounded LRU-64, stdlib only, no new scripts imports
  (`_CACHE_MAX:41`, P3S closure unchanged claim holds for this module).
- External refs NEVER cached: `_has_external_ref:61–79` covers `$ref` + `$dynamicRef` +
  `$recursiveRef` not starting with `#` (recursive walk of dicts+lists), re-check+recompile
  every call (`95–100`). Internal `#/...` (incl. `#/$defs/...`) safe to cache (same-file
  content in key). Covers dynamic/recursive as tasked. No stale external-registry.
- **Qualification:** file-level `is_symlink` check does NOT walk ancestors (parent-dir
  symlink not refused here); hardlink not checked. Mitigated by callers’ raw-first
  ancestor walks + `O_NOFOLLOW` reads for authority files, but schema file itself loaded
  via `read_bytes` (follow) after `is_symlink`/`is_file` (TOCTOU). Narrow (requires
  schema-dir alias swap mid-call); cache key uses `resolve()` (follows) + content-SHA, so
  swap causes miss (safe direction), NOT stale hit. Honest bound, NOT a blocker.

## 11. Current-State-path consideration (tasked)

Public write APIs (`prepare/finalize/activate/resume`) take `state_path` as repo-relative
path (lexical + `_safe` containment only, NO canonical-path allowlist). Read-only validators
(`validate_editorial_receipt`, `validate_prepared_set`, `verify_activation_history`)
likewise accept ANY repo-contained State file that strictly validates — a retained COPY
(`<P>/retained/before/...`) or cloned State file WOULD validate as “strict State” if
supplied. This is GIGO, NOT a permission bypass: read-only returns NO token, and write
paths enforce `proposal basis state_ref path+sha == supplied State path + expected_old bytes`
(activate `2829–2835`, resume `3285–3288`) + retained COPY/KEEP pin + fresh P2V + pre-write
drift checks, so retained/cloned State CANNOT be installed as current via these APIs
(path mismatch refuses). Historical private paths (P2R retained COPY, P2V snapshots) are
read via THEIR OWN recorded refs inside retention/proof, NEVER as `state_path` substitute.
No historical-private-path-as-current Authority found. Note as operating discipline
(caller must pass live canonical State), NOT a code blocker. If root wants hard
canonical-path pinning in read-only APIs, that is a NEW design constraint (do NOT author
here per task).

## 12. Remaining matrix (NOT covered, must NOT be read as PASS)

- Other-consumer wiring + tests (separate reviewer): Reader `_validate_manifest_semantics:207–219`/
  `build_manuscript_manifest`, Gate `_derivation_for_manuscript`/builder/CLI, Weekly/Longform
  receipt dispatch, stage `_prior_artifacts`/VALIDATED/RELEASE_CANDIDATE checks, agent
  `_validate_stage_artifacts`, `validate_state_semantics:784–809`, `approve_publication_preview`,
  `build_profiled_freeze`, config/orchestrator/handoff/human-gate/export/release/P1/P2V/P2R/P3S/R1/
  wrapper/semantic-writer/build-workflow changes per contract §8. NOT reviewed here.
- Runtime matrix on 4191503: both routes, repeat pre-Preview, R1×2 anchor/refuse-after, active vs
  historical readback, artifact-only commits under closure predicates, full §9 negatives
  (wrong seal/manuscript/Candidate, old-Candidate-after, inert-not-adopted, unknown branch,
  research change, old-authored/new-reader, equal-SHA-different-path, stale/failed/missing reviews,
  build failure/drift, seal role/unknown/dup, anchor error/cycle/depth/sequence, State/predecessor
  drift, approved/foreign Candidate, canonical-writer-after, every write/close/late-readback fault
  with observed delta + resume/healthy control), closure/regression enumeration, operator
  procedure/cost. R4d authoritative runs cited in R4d-report (legacy 31/31, P1 9/9, retention 25/25,
  current-authority 14/14, staged 26/26, agent 5/5, state 2/2, low 18/18, cache 6/6, fault 4/4)
  are Worker claims, NOT re-executed or adopted here.
- Close-error classification + duplicate-key strictness in high path + held-wording + intent-scan
  unreadable-skip + schema-ancestor scope ( §§5/8/10 qualifications) are disclosed residuals;
  none is a real unsafe-activation blocker in this read, but final fault/negative matrix must
  keep them in scope (do NOT close by assertion).

---

**Stop. No code/test/build/fixture/source changes made. No fixes designed. Ordinary
Commit/Push Human-owned. This file is the ONLY write in this review unit.**

---

## Appendix A — Overriding addendum (R5 disposition; preserves §§1–12 above)

Status: this appendix OVERRIDES the §3 verdict and the “not a blocker / GIGO /
negligible-risk” treatment in §§5, 8 (close), 11. All §§1–12 recorded excerpts,
line numbers, and scope statements are PRESERVED as the evidence basis; nothing
above is rewritten. No DST re-read, no fix-closure claim, no new source
verification in this addendum (source currently being corrected; fixes by other
worker, later fresh resolution).

Read for this addendum (no new source reads):

- Root `astra-verification-return-r5.md` (all 15 lines): rejects non-blocking
  duplicate/close treatment; selects corrections 1–3 (in this reviewer’s scope)
  plus 4–5 (other reviewer, NOT duplicated here).
- Contract §§4/7/9 as recorded in §2 governing (d880, re-read §§4/7/9 text only
  for this addendum; citations below).

### A.1 Duplicate-key strictness (§4) — original §5 qualification OVERRIDDEN

Contract §4, first paragraph (exact): “All new records use strict objects
(`additionalProperties:false`), duplicate-key refusal and exact lowercase
SHA256/commit formats.” No hash-binding exception, no fresh-vs-tamper
distinction, no high/low split.

Own recorded excerpts (preserved from §§2/5): high `validate_editorial_receipt`
loads via `schema_gate.load_and_validate_json` (:576) and `core.load_json`
(:628, :640); high `validate_prepared_set` loads seal via
`schema_gate.load_and_validate_json` (:2342). `survey_schema_v2.py:175–185`
(fully read) is plain `json.loads(path.read_text(...))` with NO duplicate hook;
`validate_instance` takes the already-parsed (last-wins) object. Low path alone
refuses (`_no_duplicate_object:232–238`, `load_json_strict`, strict seal/record
loads). I independently agree with root: a HIGH fresh-supplied record
(receipt / seal-as-loaded-by-high / manuscript-spec / toolchain-spec / supplied
semantic-visual reviews / deterministic-checks payload / QA bundle as loaded by
high) containing a duplicate key WITH a self-consistent fresh SHA/digest CAN
pass last-wins in the high path. My original “seal file-SHA drift catches it”
covers ONLY the post-creation tamper case (bytes changed after an honest seal);
it does NOT cover the fresh-malformed-supply case (record FIRST presented with
duplicates + matching fresh hash/digest, seal role SHA computed FROM those
duplicate-containing bytes at finalize, canonical digest recomputed FROM parsed
last-wins). Nested duplicates likewise pass (no recursive duplicate walk in
high loads). Contract mandates refusal BEFORE schema/digest/semantic checks.
Hash binding does not excuse it. Prior §5 “mitigated, not a blocker” is
withdrawn. **CHANGES_REQUIRED** (R5 item 1, this scope only): strict parsing for
all new high-level records/spec inputs + supplied review/QA dependencies before
schema/digest/semantic checks, nested refusal, shared strict parser without
caching authority/success, legacy JSON still valid, plus duplicate-with-fresh-hash
negative oracles (not only stale-SHA tamper). Other-worker fix + later fresh
resolution to verify; no retroactive claim here.

### A.2 Close-error classification (§§7/9) — original §8 “negligible-risk” OVERRIDDEN

Contract §7 table (exact): “close/postreplace validation failure | report primary
plus secondary errors and observed old/new/unknown disposition. Never delete
referenced/possibly referenced record.” §9 required negatives (exact):
“every record/State write/close/late-readback failure classified with immediate
observed delta and explicit resume/healthy control.” No durability-risk qualifier,
no fsync-sufficiency exception.

Own recorded excerpts (preserved from §8): high `finally: try: os.close(fd)
except OSError: pass` (`_exclusive_write_bytes:429–434`, same pattern
`_read_bytes_bounded:324–328`); agent `with open(record_path,"x+b") as fh`
(`:1939–1962`) / `with open(tmp,"xb") as fh` (`:2006–2019`) where a body
`AgentControlError` + `__exit__ close()` OSError chains/masks (close surfaces as
raw `OSError`, unclassified as `AgentControlError`, primary relegated to
`__context__`). I independently agree with root: “data already fsynced/verified
via fd, so close loss is negligible” does NOT fulfill the explicit observed +
primary-plus-secondary classification condition. Unclassified/swallowed close is
non-conformance regardless of estimated risk. Prior §8 close finding (“residual,
not a blocker”) is withdrawn. **CHANGES_REQUIRED** (R5 item 2, this scope only):
surface/classify every observed close error in new high read/write boundaries +
shared record/State writer, preserve primary + attach secondary close/readback
errors, no `except: pass`, no close-success-from-fsync inference, preserve
partial/foreign/possibly-referenced bytes + old/new/unknown observations (no
power-loss atomicity promised). Other-worker fix + later fresh fault-oracle
resolution; no retroactive claim here.

### A.3 Canonical current State for receipt/set validators (§§4.1/6/7) — original §11 GIGO treatment OVERRIDDEN

Contract readings I accept as controlling (exact phrases): §4.1 “verifies current
contract/tool closure and actual current accepted research via strict current
State plus ordinary route loaders”; “A private historical proof path does not
claim current eligibility.” §6 public signatures
`validate_editorial_receipt(root, receipt_path, state_path)`,
`validate_prepared_set(root, state_path, set_path)` with “path arguments
repo-contained,” “no caller-verified objects”; `validate_prepared_set` “verifies
current research/tool requirements”; §7 ALREADY_ACTIVE “validate strict active
State and full set”; sole write is record + State pointer (§7); `verify_activation_history(root,
record_path)` is the EXPLICIT separate historical API (takes NO state_path;
returns historical classification, “no current eligibility claim here” per own
recorded high `:3344–3386`).

Own recorded excerpts (preserved from §11): high state_path handling is lexical +
`_safe` containment only (`:499, :573–575, :1420, :1868, :2335, :2764–2767,
:3227`); NO canonical-path derivation from validated Profile/config. Hence a
retained COPY (`<P>/retained/before/...`) or cloned State file that strictly
validates WOULD be accepted as “strict State” by `validate_editorial_receipt` /
`validate_prepared_set`. My original framing (“GIGO, no token, write paths check
basis equality, so not a blocker; canonical pinning would be NEW design”) is
withdrawn as a verdict: the ordinary receipt/set APIs EXPLICITLY claim CURRENT
validation, and the contract already provides the separate history API for
historical inspection. Labelling an unfulfilled explicit-current condition as
Pass/GIGO is not permitted. I agree canonical-State loading (live State derived
from validated Profile/config, NOT silent acceptance of a historical
retained/copied `state_path`) clarifies — not extends — the existing
strict-current-State requirement; it adds no approval role/token and does not
require the set already be active. **CHANGES_REQUIRED, conditional-pending**
(R5 item 3, this scope only): receipt/set validators load canonical current
State; historical inspection stays on the explicit separate API. Other-worker fix
+ later fresh resolution (incl. retained-State-decoy negatives); no retroactive
claim here. R5 items 4 (export State-location enumeration) + 5
(orchestrator/handoff SHA compare) are OUT of this reviewer’s scope (other
reviewer owns consumers/workflows; §12 preserved, NOT duplicated).

### A.4 Precise scope of this addendum + amended verdict

Scope: UNCHANGED from §2 (high 3483 + low 1959 + schema-cache 185 fully read;
agent §§382–561/1922–2171 targeted; 6 new schemas fully read; all else UNREAD,
other reviewer’s). No new measurements, no DST bytes, no fixture/test evidence
adopted or re-executed. Evidence = preserved §§1–12 excerpts + contract/R5 texts
cited above.

Amended verdict (overrides §3): **qualified CHANGES_REQUIRED** — the scoped
high/low/cache source as read at 4191503 does NOT yet satisfy explicit contract
§4 duplicate-refusal (high loads), §§7/9 close classification, and §§4.1/6/7
canonical-current-State for public receipt/set validators. Pending: other-worker
corrections per R5 items 1–3 + duplicate-with-fresh-hash negatives + close-fault
oracles with primary+secondary/observed-delta + retained-decoy current-State
negatives + later FRESH author-independent resolution on the new untouched SOURCE
snapshot. Whole-operation NOT_READY unchanged; R5 items 4–5 + §9 full matrix +
consumer/lifecycle/quality/cost remain with the owning reviewers/matrix. No PASS,
no fix-closure, no new-feature authorship in this unit.
