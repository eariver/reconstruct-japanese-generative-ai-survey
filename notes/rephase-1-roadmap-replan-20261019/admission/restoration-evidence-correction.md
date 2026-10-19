# Restoration evidence correction — transcribed observations, not persisted raw

2026-10-19 UTC. Restoration-evidence owner. `integrated-admission-contract-analysis.md` は編集しない。原文書（`restoration-procedure.md` / `restoration-manifest.json` / `README.md` / 当初の4文書）を preserved のまま残し、本書で資格付けを追加する。過去rawの再創作はしない。

工具差異の開示: 本環境に `apply_patch` はないため `Write`/`Read` と `bash` のみ使用した。

## 1. 保存物の正確な範囲

- packet内の4文書（手順書・manifest・README・分析）は `Write` で作成した文書であり、**persisted raw command logs（stdout/stderrの直接保存）でも実行scriptでもない**。
- `restoration-procedure.md` §12の数値exit一覧・各節の `EXIT_*:0` 記載は、**tool観測の転記（transcribed/tool observations）** である。当時の `bash` tool返却を見て書き写したもので、独立したrawファイル・署名付きtranscript・再実行可能なfail-closed rerunnerとして認定できない。
- 旧 `/tmp` 復元・`cp`・`index-pack`・`apply` の各操作を再現するcertified scriptは保存していない。`tar --no-absolute-filenames exit64`・`apply whitespace warning 2行`・`fsck missing` 等の記載も転記であり、rawの再提示ではない。失われたrawは再構成しない。

## 2. 再点検が必要なclaim（本書では遡及修理しない）

- `fsck exit0 / missing 26309`: 当時の `fsck --no-dangling` 出力を `grep -c` した転記であり、raw fsck logは保存していない。`available13 objects` との混同（13 COMMIT chain ≠ all objects）に注意が必要。別途 current verification で `rev-list --missing=print` のexact output/censusを記録する。
- full status形式: `status --porcelain=v1` の21行転記であり、`-z` raw・全untracked census・index diffのrawは保存していない。`index empty` との混同に注意（通常indexはHEAD tracked bytesを持つ）。
- mode一致: `stat 0o664` 21/21の転記であり、reference static pinsとの厳密比較rawは保存していない。reference側に `0o664` 以外があれば虚偽のall664主張になるため、current verificationでactual modes vs referenceを厳密比較する。
- inode独立: `cp` 使用の記述のみで、inode番号の実測rawは保存していない。reconstruct `.git` およびdurable pack inputsとの `device:inode` 比較はcurrent verificationで初めて行う。
- `raw保存/個別exit保存/fail-closed手順認定` としての扱いは不可。以後のread-only current verificationを別packet `admission/current-source-verification-<time>/` に保存し、そちらのraw stdout/stderr/numeric exitをもって証拠とする。

## 3. 本書以降の扱い

- 原文書は修正しない。本書の資格付けが優先するが、原文書の転記内容を遡ってrawに格上げしない。
- 新current verificationは restoration/reapply/Git writes/tests/import を行わない read-only観測のみとし、予期せぬ結果は保存して隠さない。
- checker sourceは reference static pinsを読み、baseline blessing（観測から期待値を計算）をしない inspect-only とする。
