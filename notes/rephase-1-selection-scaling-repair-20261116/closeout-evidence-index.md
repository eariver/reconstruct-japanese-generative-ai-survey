# Closeout evidence index — Selection scaling repair 20261116

技術完了・文書closeout用の bounded indexであり、runtime再証明ではない。
権威は root FULLと独立最終 §§10–11（WITH FINAL-BINDING、後続bindingが正）にあり、本indexは案内のみである。

## 必須

- `astra-closeout-resolution.md` FULL（本unitの verdict・boundary・deviation・nextの正本）
- `astra-repair-resolution.md` FULL、特に §§10–13（source epoch・real・検証/pack・supplement・closeout-only）
- `final-implementation-review.md` §§10–11含む全文＋ `final-implementation-review-machine.json`
  （初回 §§1–9 BLOCKED保存と §§10–11 `BOUNDED_IMPLEMENTATION_PASS` の区別を読むこと）
- `independent-real-output-review.md` §10＋ `independent-real-output-review-machine.json`
  （SP audit 61hex supersede→64hex `ad5474dafb79276d41a580aa48c394757195b7fe53a60bcd3092498254d15449`/1530B）
- `../../outputs/rephase-1-selection-scaling-implementation-assessment.md`（本unit評価、日本語 concise）

## Sourceと配送

- `source-packaging/final-20261116T031000Z/packaging-report.md`＋ `machine.json`
- `complete-selection-scaling-manifest.json` `0dc361cb8284f3465243120b7cea8e20476c3fbe81d90a71ce3028dd43eed150`/187361B
- `complete-selection-scaling-409.patch` `76ac1318cd58311a5a7c0d924ee26b2bdff68dc815e75014a1aacd517e51fd6b`/5691014B
- raw `gen-*`、`indep-*`、`proof-*`、`patch-sha256.txt`、`manifest-sha256.txt`、`gen-counts.json`
- proof `.rephase-1-editorial-runtime/selection-scaling-packaging-20261116T031000Z/proof-copy/candidate-partial-b40de60`
- source `3231a0c280287411513bba359f4d3d2b6703f591` / parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` / tree `ff01b73e6012fd4519fdfb3807186753ff330367`、143=58M85A/774

## 実writerと検証

- `real-rehearsal-20261116T022222Z/README.md`＋ `machine.json`＋ raw `w34-run*`、`w34-run2*`、`sp-run*`、`source-commit*`、`realcopy-rsync*`
- 継続 `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`（W34 836s 45/5、SP 148s 130/9、7+7）
- `verification-20261116T025000Z/README.md`＋ `machine.json`＋ raw batch1（8成功2 ERROR）と batch2（別10成功）
- `implementation-20261116T004649Z/correction-20261116T011405Z/s9-20261116T015500Z/` — final focused22の`run-metadata.json`／`raw-full-stdout.txt`／`raw-full-stderr.txt`／`raw-full-exit.txt`と`independent-correction-review.md`＋machine。先行13／初期11と合算しない。
- `implementation-20261116T004649Z/README.md`の訂正、`independent-first-implementation-review.md`、`initial-draft-snapshot-20261116T011405Z/` — 初期fail-open／helper-test過大主張、config/cache/raw限定と保存source。旧COMPLETE主張は撤回済み。
- `current-proof-20261116T030000Z/README.md`＋ `machine.json`＋ raw（Weekly 70 SAME LOW/runner drift拒否・復元）
- `regression-supplement-20261116T141000Z/report.md`＋ `machine.json`＋ raw（old773 parent 2 ERROR、final774 adapted 4、等価 raw `7ff77fa3…`/`df159445…`、owner errata）

## 補助map（contextのみ、新規certなし）

- `integration-map-final.md`＋ `integration-map-final-machine.json`
- `integration-map-r2.md`、`integration-map.md`＋各 machine
- `current-source-closure-map.md`＋ `current-source-closure-map-machine.json`
- `transitive-dependency-inventory.md`＋ `transitive-dependency-inventory-machine.json`
- `predicate-reuse-resolution-r3.md`＋ machine
- `independent-*-review.md`＋ machine（map/integrated確認）

## 文書closeout

- `closeout-check.md`＋ `closeout-check-machine.json`（scoped links/pins/JSON parseのみ、runtime再certなし）
- 本 `closeout-evidence-index.md`

旧 ae0 active（0/14）と失敗 shadow（W34 0/7 SP 3/7）は保存のみで継続権威ではない。
Whole NOT_READY/DM021+022OPEN/audit未開始/quality-adoption-savings OPEN。
Human Commit Point停止。最終reviewerが本書後に文書bindingを追加する。
