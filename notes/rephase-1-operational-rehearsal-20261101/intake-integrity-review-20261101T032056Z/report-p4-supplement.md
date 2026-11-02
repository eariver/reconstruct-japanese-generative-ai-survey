# P4 supplement — narrow DATA confirmation (10 files) + overlay + X FILE-ref + packages

Review dir (existing): `notes/rephase-1-operational-rehearsal-20261101/intake-integrity-review-20261101T032056Z/`
This file is NEW supplement; original `report.md`, `check_intake_integrity.py`,
`checker.stdout.json`, `check_file_links.py`, `links.stdout.json` untouched
(stable hashes preserved).

## Evidence (NEW only, no overwrite)

- `check_p4_integrity.py` SHA256 `bd5eeb088224cc59667c534ac48b6a91fa2929e25dfbc4eeb9fd37ae3c7b5de2` / 17317B
  stdlib only `hashlib/json/base64/pathlib` (+`sys`). No `assert`. Same LF-strip +
  `validate=True` base64 discipline as V2 checker.
- `p4checker.stdout.json` SHA256 `ca9416b6034c3775cace1802f8f2c0a41679e652eefbac9ef55ae4edeae981b2` / 7367B,
  `p4checker.exit.txt` `0`, `p4checker.stderr.txt` 0B (empty SHA `e3b0c442...`).
  Exit `0` = all 10 P4 payloads + 6+2+2 link checks + package counts PASS, no checker fault.
- Prior evidence still authoritative: `check_intake_integrity.py` `80f6e753...`,
  `checker.stdout.json` `68b0c432...` (6 NEEDS_REPAIR, `exit 1` fail-closed),
  `check_file_links.py` `148e8458...`, `links.stdout.json` `2e3a7258...`
  (`exit 1` for 13 FILE mismatches, since analyzed).
- Bounds: no network, no `git`, no project runtime/import/tests/build/fixtures,
  no source/manifest edits, no P4 overwrite, P3 zeros preserved. Only read
  `...-p4-20261101T031826Z/` responses/manifest/supersede-map + already-captured
  P2/P3 bytes named below. No Production checkout, no root sweep, no Gitlinks.

## P4 transport/content closure (10/10)

P4 manifest 10 results, all `exit 0` + `HTTP 200` + empty `stderr` (verified from
`p4*.exit/headers/stderr.txt`). All 10 bodies `encoding:base64` (blob API, no
`encoding:none`); each `len==reported size` + `sha1(blob len+bytes)==reported blob`
+ `DATA==decoded` + `sha256==manifest`. Content-verified 10/10; zero-byte payloads
are NOT counted as content (P3 zeros remain UNAVAILABLE, below).

### Six exact blob payloads (overlay authoritative, full hashes, no truncation)

Overlay key is `(ref, repo_path)`. For each path `@774dd39a951c9ac3818e83dfffd4c7666efb0a20`
P3 `DATA.p3a02–07` (0B, `sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)
is SUPERSEDED UNAVAILABLE (preserved, never consumed). P4 `DATA.p4a02–07` is
authoritative. P3 body `sha`/`size` (fixed metadata) == P4 body `sha`/`size`;
P4 `content_sha256` == P2 `discovery-accepted` `raw_ref.sha256` + `byte_count`.

- `p4a02` path `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/flashinfer-ai__flashinfer.json`
  blob-sha1 `90462213d9825c9224a0b169d753f023dcf18537` size `1805968`
  content-sha256 `f75febae2316477e9cd12c4e0a654e83f6d4f90e2def3a47a8a4ad1922946507`
  discovery want identical `f75febae2316477e9cd12c4e0a654e83f6d4f90e2def3a47a8a4ad1922946507` / `1805968`
- `p4a03` path `.../raw/ggml-org__llama.cpp.json`
  blob `62edff35562c0eaa4d175546364b1c2838a11a3a` size `5257525`
  content `80345df9de1fc27f8401efe9bd26cba04297ac9f755eeb41b4f7e231339175d2`
  discovery identical
- `p4a04` path `.../raw/huggingface__transformers.json`
  blob `daa04d862800fc51c3066a2b3e2f53ff96394992` size `1323799`
  content `2a843332a5f95495ac372fa9e947c73a90e5dc93320f6461718c0d65cea8b6f9`
  discovery identical
- `p4a05` path `.../raw/nvidia__tensorrt-llm.json`
  blob `6b093886cc5cf29de0c3ebe55bb907de9c64bad3` size `1854867`
  content `d711b2ebb37cba888013ce125315c90b446721c0f194159fbb9622ca09598f9a`
  discovery identical
- `p4a06` path `.../raw/sgl-project__sglang.json`
  blob `f16c5ec6b2a24a09e7f76dd5fd7ca8e555d30587` size `1839084`
  content `acab64f7e4eb53f3d5bc1dd0cdc12e38af3fe7685d9a9d630c2365cb9ad0c9d2`
  discovery identical
- `p4a07` path `.../raw/vllm-project__vllm.json`
  blob `94aaa50674ab67014d4b0a0030c00af752df7c87` size `3340585`
  content `75f34b036929d41ad2cabb290b8eb647b9776ed0942a7d4d2399edf967a763be`
  discovery identical

P3 `p3a31/34/36/37` via `p3b31/34/36/37` remain verified in P3, NOT superseded here.

### X manifests (2) + tasks (2) — blob-sha1 vs content-sha256 distinguished

`X manifest has no SELF digest field`: neither `DATA.p4x01` nor `DATA.p4x02`
contains its own hash. Validation is transport-level (`body.sha` blob-sha1 +
`body.size` vs decoded bytes) plus external FILE-ref (`discovery-accepted`
`x_source_intake.sha256` content-sha256 vs `DATA` bytes). Both hash functions are
valid for the same bytes; they are NOT comparable to each other.

- W34 `p4x01` repo `sources/2026-W34/external/x/x-source-intake-v2.json`
  ref `774dd39a951c9ac3818e83dfffd4c7666efb0a20`
  body blob-sha1 `113d62e740b111f4eb7af7c2096caf0391ec2f12` size `3913`
  DATA content-sha256 `702881aa75cc09ff3e65f52220e47076c8f67a8c97a36d4e4aea87e41f5a98b2` size `3913`
  decoded bytes yield BOTH `blob1==113d62e7...` AND `sh256==702881aa...`.
  P2 `DATA.p2b02.discovery-accepted-v2.json` `x_source_intake` =
  `{path: sources/2026-W34/external/x/x-source-intake-v2.json, sha256: 702881aa75cc09ff3e65f52220e47076c8f67a8c97a36d4e4aea87e41f5a98b2}`
  MATCHES P4 DATA content-sha256. ROOT concern resolved: `113d62e7...` is blob-sha1,
  `702881aa...` is content-sha256 for the SAME 3913B — no true bytes/ref mismatch,
  no original-API hash mistype. Current fixed-ref bytes valid.
- SP `p4x02` repo `sources/SP-efficient-llm-2026/external/x/x-source-intake-v2.json`
  ref `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`
  body blob-sha1 `638ea4af84eaa87c7e4ab0e1fc22daf7c0acee61` size `5359`
  DATA content-sha256 `3465dc4f4d9d3bce73c33cb16820aa771816fa64a8de850336ef56c46d8275b0` size `5359`
  decoded bytes yield BOTH. P2 `DATA.p2b21.discovery-accepted-v2.json`
  `x_source_intake` `{path: sources/SP-efficient-llm-2026/external/x/x-source-intake-v2.json, sha256: 3465dc4f4d9d3bce73c33cb16820aa771816fa64a8de850336ef56c46d8275b0}`
  MATCHES. `638ea4af...` vs `3465dc4f...` is blob-vs-content, not a mismatch.
- W34 task `p4x03` repo `sources/2026-W34/external/x/weekly-x-2026-W34-r2/grok-task.md`
  ref `774...` blob `2d6c607bdff2fa3e488ce970ed950837cf1b17fb` size `11686`
  content `e97bbd06846955842f86129ed17eb4a6708aa6de337ba9cf997927f33a99a2f0`
  == W34 X-manifest `runs[0].task.{path,sha256}` (`DATA.p4x01...`) verified.
  Result `runs[0].result.raw` `{path: sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/grok-x-result.corrected.md, sha256: 43b0923bbd68ef9d9d9d4bf501a773cd4b4e4cdd881339d9591d97e7951f86ca, byte_count: 23612}`
  == P3 `DATA.p3a51.grok-x-result.corrected.md` 23612B same sha256 (no refetch).
- SP task `p4x04` repo `sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/grok-task.md`
  ref `c8d0...` blob `c9a04eb60831bffb139e049ced285dd1d2fc681b` size `20555`
  content `c1150730c6a0a758c4fd2e85928e593e49484765c4fe68864fe784fdde9220e2`
  == SP X-manifest `runs[0].task` verified.
  Result `runs[0].result.raw` `{path: sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/raw/x-reception-result-r3.md, sha256: b3a8a0404e6d4a1abfaa6bde54c4a6f5d7979ec24870bcd629865f8443377d79, byte_count: 30213}`
  == P3 `DATA.p3a59.x-reception-result-r3.md` 30213B same sha256.

No new publisher fetch, no result recopy. `p4x01/p4x02` production-profile refs
(`a6e3eb30...` W34, `22f2e822...` SP) are FILE refs to already-captured profiles,
not re-validated here beyond path presence.

## Historical FILE links — typed record vs unresolved (no blanket label)

Prior `links.stdout.json` reported 13 FILE mismatches + 119 UNACQUIRED. With P4,
6 github mismatches are CLOSED (above). Remaining split by actual typed evidence
found ONLY in already-captured bytes (no new fetch, no loop):

### Resolved by explicit typed replacement record (NOT assumed supersession)

`DATA.p2c13.publication-surface-revalidation-r1.json` (SP, `reason_class:
REVIEWED_CORE_CHANGE`, `reason: Human Publication Preview r1 REQUEST_CHANGES
repair (Issues #520/#521 + Sol citation-policy)`, `prior_checkpoint:
{sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/DRAFT_COMPLETE.json,
sha256 9d795a31f3df65055824807815d46264031be02e23b5630aea4a0615cd24ca6f}`)
contains `superseded_artifacts[7]` with full `prior_sha256` → `new_sha256` +
`byte_count`, plus `validation` binding new SHAs. This is the typed record for
all 6 `DATA.p2a17.DRAFT_COMPLETE.json` artifact mismatches:

- `publication-pdf` `surveys/special/efficient-llm-2026/main.pdf`
  prior `bc6e280c668a4a17ff98dae58fc574cdce701cce9dd8926eb8b1138e82a46e0b`
  → new `8a9a721ac35b2e5baa2e20162b5a6ba4ae63945d512d985484aeae56073a23c1` (850785B)
- `quality-regression-bundle` `sources/SP-efficient-llm-2026/publication/v2/quality-regression-bundle-v2.json`
  prior `08c0e35848b93e8e27ae6937ea255278dbe760eec96dc32af6f295eed1f0f18d`
  → new `a3f1b649732571dcfe5d713b28352c20f0edee0f90f6b7874ffc2b049130c0a9` (3056B)
- `reader-manuscript` `sources/SP-efficient-llm-2026/publication/v2/reader-manuscript-v2.json`
  prior `f99c3b9353e978aec009871875a0df77d30b7be387b2c90ede15ac44aacbd693`
  → new `cf7aca20714a23ba0b909fb62d79fe644c5e1fbc0d68ebc16b883d0a408f416e` (9657B)
- `reader-surface-gate` `.../reader-surface-gate-v2.json`
  prior `417e49ac28b9e1c8babeac181fb541618a8f23935e61533ac79e5d21bce678a5`
  → new `d5c95b52ca6b0a3e3058ec0b9e17d4aba7563f65ad7ca8822ee9457869bee01e` (4315B)
- `semantic-review` `.../semantic-editorial-review-v2.json`
  prior `c60513eb08a27d8339909dea75d48ea1ddcd6dfe439106a26c8d29465d10c10f`
  → new `6f5e7ff106066fe59ea08ec51d4ea7ccec9574deef327cd78505db023d446c5a` (7521B)
- `validated-source` `surveys/special/efficient-llm-2026/main.tex`
  prior `b09ab3516afaadb5e0f64e21515d2e71dd43cbb926c657e40d48b939dc54b44c`
  → new `87bcb707e13cfde7e3d589271415b66e42385d4c7359f3bb492e9adf2d09fabe` (293777B)
- `visual-review` `.../visual-review-v2.json`
  prior `c4ae1c38c09477dfd003336cf820f9e23267c864861b8292f669a65257d6a222`
  → new `fae79e6739beb225e6c810bf9de2943729853a1b37e792ddc651765425b70487` (4065B)

New SHAs match currently captured `DATA.p2c05/06/07/08`, `DATA.p2b33`,
`DATA.p2a28`, `DATA.p2a30` (850785B PDF). Search of captured `DATA.*.json`
confirms old hashes appear ONLY in `DATA.p2a17` (holder) and `DATA.p2c13`
(replacement record) — no hidden third copy. Do NOT consume DRAFT `prior_*`
as current bytes; consume `new_*` only.

### Unresolved historical references (preserved, NOT invalid, NOT rebound)

- `DATA.p2e11.publication-r1.json` reviewed `publication-candidate`
  `{path: sources/SP-efficient-llm-2026/publication/v2/publication-candidate-v2.json,
  sha256: 76191e9b5f24d6950ce3e80a4f3e19cf79dc4dfc2dee5529488bce23956f787e}`
  vs captured current `DATA.p2c04...`
  file-sha256 `adf22516235c5a5db2a89f9a3facd6d5af559eac0ad564d373fd1b1a7a5e9638`
  (`candidate_sha256` field `6b9fd9059fc068674e63ec1f7e987fa1c2a9e7f4e008f96033909b463bcb62c4`
  is semantic digest, NOT a FILE ref — excluded). Full-text search of P2/P3/P4
  `DATA.*` finds `76191e9b...` ONLY in `DATA.p2e11` (holder); NO explicit
  `prior→new` typed record binds `76191e9b...→adf22516...` in captured bytes.
  Same `REQUEST_CHANGES` context as `p2c13` but candidate itself has no
  `superseded_artifacts` entry. Report as UNRESOLVED historical reference:
  current fixed-ref bytes (`adf22516...`) valid for use, old `r1` reference
  preserved un-rebound; do NOT declare old RELEASED invalid, do NOT rebind old
  acceptance to new bytes. Root execution must use fresh current Profile/acceptance
  and honestly import historical Raw without pretending old chain re-validated.
- 119 UNACQUIRED FILE refs from prior review (sharded evidence/views, screening
  intermediates, collector run metadata, 450/20+ worklogs, TeX log, publisher
  bodies, etc.) remain UNACQUIRED in P4 scope — not invalid, bytes stay at fixed
  refs if genuinely needed (same-ref shards share authorization per P4 README §29
  correction; new publisher URLs still need new permission). W34
  `reader-manuscript`/`main.pdf`/`quality/semantic/visual` links are UNACQUIRED
  in P1/P2/P3-only map but VERIFIED via fixed archives
  (`c453bea798f6d7693d2e92d1dbae3fc7838b24d90df382c2547f3ad033b7c10e` 19652B;
  `e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de` 338722B).
- No other retained exact X bytes found: `702881aa...` appears ONLY in
  `DATA.p2b02` (FILE ref) + P4 `DATA.p4x01` (bytes); `3465dc4f...` ONLY in
  `DATA.p2b21` + P4 `DATA.p4x02`. No duplicate X-manifest copy, no hidden
  replacement record beyond the FILE refs themselves.

## Packages (from captured architectures, no extra corpus)

Parsed `DATA.p2b13.architecture-v2.json` (W34) `packages[]` length `7`,
`DATA.p2b29.architecture-v2.json` (SP) `packages[]` length `9` — matches P4 README
§30 correction (authoritative over packet prose). IDs:

W34 7: `w34-agent-control-plane`, `w34-collaborative-agent-workflows-retrieval`,
`w34-safety-security-governance`, `w34-model-economics-distribution`,
`w34-creative-multimodal-production`, `w34-ecosystem-infrastructure-economics`,
`w34-week-in-review`.

SP 9: `p1-bottleneck`, `p2-scaling-moe`, `p3-attention`, `p4-precision`,
`p5-decode`, `p6-serving`, `p7-routing`, `p8-capstone`, `p9-measure`.

Counts are structural inventory from captured bytes, not quality/cost proof.

## Closure vs unresolved (for root authorization)

- CLOSED transport+content: P1 4/4, P2 145/145, P3 53+4/63 contents+blobs,
  P4 10/10. With P4 overlay, W34 55/55 discovery Raw + SP 25 obs + X
  manifests/tasks/results are byte-verified at fixed refs. P3 zeros stay
  UNAVAILABLE fault evidence; P4 bytes authoritative by `(ref,path)`.
- CLOSED historical via typed record: 6 DRAFT artifact SHAs → 7 new SHAs via
  `DATA.p2c13...` (above). Consumable as `new_*` with provenance.
- UNRESOLVED but PRESERVED: 1 candidate `76191e9b...→adf22516...` (no typed map),
  119 UNACQUIRED paths (bytes at refs, not fetched), archived-only W34
  manuscript/PDF links. Root MAY authorize execution on verified current bytes
  (`P4 6` + `P4 X` + P2/P3 aggregates + archived manuscript/PDF by exact SHA)
  while keeping unresolved historical references un-rebound and explicitly
  disclosed. No old-RELEASED invalidation, no rebind, no quality/corpus/
  cost/vulnerability claim from hashes. Source `138` unchanged.
