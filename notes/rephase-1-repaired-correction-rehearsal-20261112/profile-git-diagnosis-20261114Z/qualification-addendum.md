# Qualification addendum — scope of the local Git database probe

This addendum qualifies, without modifying, `diagnostic-report.md` and `diagnostic-machine.json` in this packet. It is written only from the existing command transcript and raw files. No new search, Git, or network was performed.

## 1. Exact local Git areas visited

- **Authorized scoped repo:** `/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work/.git`. Commands: `rev-parse`, `for-each-ref`, `config --local -l`, `remote -v`, `ls-tree`, `ls-files`, `status`, `cat-file -t/-e/--batch/--batch-check`, `show`, and `verify-pack -v` on the active repo packs only.
- **Broad runtime/proof loop (scope deviation):** `find .rephase-1-editorial-runtime -maxdepth 6 -type d -name .git`, then `-maxdepth 12`, followed by `git -C <dir> cat-file -e 155b78cfd588eb9300349e4568ee7065ae498477` for each. It visited **542 `.git` directories**. This set included the active candidate-work repo plus proof-copy/gen-copy and other runtime/synthetic-fixture/proof DBs; the loop did not individually classify them.
- **Input-capture loop (scope deviation):** `find .rephase-1-inputs .phase-5-inputs -maxdepth 12 -type d -name .git`, followed by the same `git -C <dir> cat-file -e` check. It visited **2 DBs**: `.rephase-1-inputs/integration-r2/.git` and `.phase-5-inputs/runtime-repair-candidate/.git`.
- **Active pack index check:** `git verify-pack -v .git/objects/pack/*.idx` on the active cc1c repo only.
- **Known-capture file/hash scans:** `find notes .rephase-1-editorial-runtime -path '*/sources/2026-W34/production-profile.json'` with sha1/sha256 computation, plus `grep -rIl` for `155b78cf` and the expected sha256 over notes. These are known-capture file scans, not a filesystem-wide proof.

## 2. What was not read

- **No** `git -C` was run against the reconstruct repository root or its `.git`. Reconstruct Git history, refs, and objects were not read.
- **No** Production checkout, remote, network, or external clone was read.
- The fixed-774 **plain input capture** `.rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/production-profile.json` and its `tree.json` were read; this is a source capture, not a Production checkout.
- Other local object stores outside the roots above, external/previous environments, and remote/upstream availability remain **unknown**.

## 3. Quarantined conclusion

The original “544 local Git DBs probed / zero hits / no other exact copy” wording is **scope-limited and must not be used as a global absence claim**. The broad loops exceeded the authorized exact-cc1c-plus-known-fixed-captures scope and touched other fixture/proof DBs by `cat-file -e` existence checks. That result is not needed for recovery.

No zero-readback claim is made. The existence checks and standard Git reads can read object metadata; only the active cc1c repo's needed blobs were batch-read for content. The 542/2 DB classifications are command-record facts, not an audited inventory.

## 4. Retained verified facts for root

- The `cc1c` tree records `sources/2026-W34/production-profile.json` as blob `155b78cfd588eb9300349e4568ee7065ae498477`; that blob is **missing in the active cc1c repo** (`cat-file -e` exit 1; batch header `… missing`).
- The exact already-authorized fixed-774 plain capture is `.rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/production-profile.json`: sha256 `a6e3eb3006dde95da008876486cbfc7fdce75f507f7efcd6b0fcaba5e154b21a`, Git blob `155b78cfd588eb9300349e4568ee7065ae498477`, 2371B. Its bytes hash to the cc1c tree OID. **No object restore was performed.**
- Helper-name correction retained: no `_verify_recorded_epoch` symbol exists; the actual source symbol is `_verify_own_epoch_commit` (`scripts/survey_research_authority_v2.py:639-799`).
- No global absence or availability claim; no object restore, commit, config, State, guard, source edit, test, project import, or network action.

## 5. Unknowns

- Availability of the object in reconstruct `.git`, Production checkout, remote/full upstream, and any local store outside the probed roots.
- Whether any of the 542/2 visited DBs is relevant beyond the recorded `cat-file -e` result; they were not individually audited or content-extracted by this diagnosis.
