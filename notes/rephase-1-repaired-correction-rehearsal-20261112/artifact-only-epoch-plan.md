# Artifact-only epoch plan (PLAN ONLY, no commit/write yet)

Root §12-13 + `recovery-interface-map.md` + `recovery-interface-map-addendum-20261114Z.md` + W34 resume `RESUME_CLEARED`/`readback PREARCH triplet true` read. SP R1 `694f5e49…` on cc1c cannot adopt (SP Profile tree entry absent); W34 missing blob `155b78cf…` restored, resume completed, guard absent.

## Epoch (dry, not executed)

- Parent `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325` (tree `ed2dc4ddd4a9486ccc9d0944bbd48653199b2485`, parent `e84…`), inert origin, independent DB. No reconstruct writes.
- Stage ONLY 2 unchanged live files (no State/CP/R/Raw/source):
  - `sources/2026-W34/production-profile.json` live SHA256 `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1`/2371B/`0o664`, gitOID `c2990d4fcb81f71a6afac0b14bf93c5b2d9ebb5e` (index/recorded `155b78cfd588eb9300349e4568ee7065ae498477`, working M).
  - `sources/SP-efficient-llm-2026/production-profile.json` live SHA256 `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45`/13748B/`0o664`, gitOID `9251f4872bbcc7e2b412464950e88e02055067f8` (index absent, untracked `sources/SP-…/`).
- Source 773 `a7e40c4711…` identical; initial480 `48082356…`; Profile bytes unchanged (2a8c/aff05). Tool/Contract8 same (HIGH `f312f02e…`, LOW `7f5fc9e0…`, pipeline `3adfbda2…`, quality `b5b955d5…`, W34 research `666f8a06…`/publ `99adff93…`, SP research `0f575e6d…`/publ `a6859559…`); new HEAD/tree change only (W34 `c2990d4f…`, SP `9251f487…` added), beforeState SP same `180db8c3…`.
- W34 own-epoch readback stays cc1c-anchored: R2 `checkpoint/record.json` `73ab28ea…` (triplet true, `original_anchor/parent_checkpoint 0979f9f7…`, completion true), recorded `155b78cf…` reachable via parent cc1c objects; `_verify_own_epoch_commit` reads recorded objects only, never HEAD.
- Old preserved nonadopted/stale: SP R1 manifest `694f5e49092e4ef68c02849f1709ee17c1bcba6fbfee9ffad287f55624eb37d4`/183765B, repo request `sp-repaired-20261112-r1.json` `67fa3d9ebe79e02582e9b1ccbdd3e1cf776ee895a1cc57ae1dc470762ce7d0ce`/389945B, decision `sp-supplied-decision-r1.json` `b7a78bfa7370…`/4875B. Do NOT rewrite `expected_head`; new SP request/R2 (`sp-repaired-20261112-r2`) after epoch pins NEW HEAD/tree + same 160 records/r8 closure/4 existing Raw (`253542/307198/350662/3751` FULL-DID, no re-copy)/supp `ff3ba77555de8df0b9c9066ac70b1bef4032d49017baca6e7391133afbd5f5fe`/31530B.

## Dry commit (exact 2 paths only)

```
git -C <ABS_NEW_REPO> add --sparse -- sources/2026-W34/production-profile.json sources/SP-efficient-llm-2026/production-profile.json
git -C <ABS_NEW_REPO> -c user.name=artifact-only-epoch -c user.email=artifact-epoch@example.invalid commit -m "Artifact-only profile-data epoch: live W34 2a8c + SP aff05 on cc1c; source773 same, no State/CP/R/raw/source"
```

Pre: HEAD `cc1c…`, `diff --cached` empty, status scoped M W34-profile + other rehearsal M preserved + `?? sources/SP-…/` + `?? sources/*/research/` + R2 paths absent (`…/sp-repaired-20261112-r2.json` NOENT, `…/sp-repaired-20261112-r2/` NOENT), SP R1/request/decision present, 773/State/CP/Gates/old-accepted/canonical Ledger/Comp bytes unchanged, hooks `.sample` present (no bypass), `user.name`/`HOME` unchanged, sparse-checkout file unchanged, no `--allow-empty/--no-verify`, no global `--sparse-index`/`core.ignore` change.
Post (future): new HEAD child of cc1c, tree has `c2990d4f…`+`9251f487…`, 2 paths committed (W34 M, SP A), all else preserved, W34 `a858…` State + SP `180db8…` + R1/R2 refs verified, readback still cc1c-anchored.

No object restore/commit/State/source/prep/adopt now. Details: `artifact-only-epoch-config.json`, `artifact-only-epoch-data.json`.
