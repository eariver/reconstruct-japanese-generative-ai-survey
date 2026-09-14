# Re:Phase 1 Evidence

2026-09-15 JST。判断は[方針assessment](../../outputs/rephase-1-direction-assessment.md)。

## 取得と再現

- `evidence.json`: 指定された両baseline、GET観測時点のremote refs、選択sourceの固定commit URL/Git blob SHA-1/raw SHA-256/bytes、限定照合結果。
- `capture.py`: GitHub CLIの`gh api --method GET`だけを使う取得補助。productionのimport/runner/test/workflowを起動しない。
- `.rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/`（ignored）: treeと取得raw。source実行用の完全repositoryではない。

初回は `python -B notes/rephase-1/capture.py observe`、以後 `python -B notes/rephase-1/capture.py <manifest内のpath> ...`。observeは観測recordを新規作成するため、既存Evidenceを更新する目的なく再実行しない。tree APIの`truncated=false`を要求し、rawをtree内Git blob hashへ照合する。旧cacheは同じblobの時だけ流用する。ここでいうGETにはGitHub APIを使用し、通常Git Pull/Push/fetchは使用しない。

## 今回の選択と発見

1. 旧mission/現handoff/assessment等から全体目標と既存Evidenceを確認。旧順序は採用前提にしない。
2. production fixed treeからcurrent config、governance、authority/overlay/bootstrap/final auditを読解。既存の自律進行・独立review・Profile差と、古いcurrent文言が必読入口へ接続される状態を確認。
3. W34 execution indexとStateの不一致、Human Preview r2修復・Freeze記録、W33/SP001の保存Stateを確認。全経路の再実行や品質認定ではない。
4. 関係sourceを静的に確認。#495/#496のPR metadata/bodyはGETで確認し、`evidence.json`へ取得値を保存。PRの試験/品質宣言は著者側報告と区別する。
5. 旧upstream reconciliationの17入力をcurrent treeへ照合。同じ基準の既存probe結果を再利用し、成功済みtest/反例を再実行しない。

source捕捉で一度、未確認のscript名`build_weekly_reader_publication_v2.py`を指定してtree membership assertionで停止した。先行する4ファイルは取得済み。treeと旧manifestで実名`survey_weekly_semantic_publication_v2.py`を確認して続行した。存在しないpathのproduction API取得、productionコード修復/実行はしていない。

local production checkoutへのread-only Git確認ではHEADが旧`f9f3e040`、12 pathに削除表示があり、指定commit objectも存在しなかった。これらを作業基準にせず、checkoutを変更せずfixed-ref APIに切り替えた。削除表示の原因は調べておらず、本調査による削除とはしない。初回の`git status`は内容確認で、通常のGit metadata refreshまで一切起きなかったとは主張しない。

## 限界

treeの全pathが見えたことは全code読解ではない。取得ファイルも目的に必要な節/関数を選んで読んでいる。独立review、full Core/state dependency validation、current cold-start全workflow、公開asset/PDF目視、全source品質、全profile/caller互換、全role時間/token/金額は評価していない。

W33/W34/SP001の`RELEASED`は保存Stateの読解。W34 Release checkpointとHuman Preview approvalはState pointer/raw hashの局所照合だけ。上流#495/#496報告のPASSや旧probe成功を今回のruntime PASSに移さない。

旧Phase 4/5の実験・判断・patchは変更していない。今回の取得/読解/記録/引継ぎもreconstructionの仕事であり、旧資料のArchiveや文書短縮だけで純費用削減が達成されたとは数えない。
