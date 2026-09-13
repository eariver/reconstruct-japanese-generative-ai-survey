# Phase 5 — publication review境界の実例確認

開始基準: reconstruct `4504d4c1c52d9fcda75e20803b72d470c67a74be`（local/remote一致、clean）。2026-09-14 JST。Phase 5-Bと条件付き5-C A/B非開始は保持する。本単位は別の実例調査であり、5-C費用試験ではない。

問い: W34のHuman Preview r2で求めた修復について、既存の原稿完了判定とreviewはどの版・読者向け要素を対象にし、何を検出できず、どんな追加仕事が生じたか。current mainのShared Core修復で既に除かれた原因と、残る編集判断を分けて、次の改善投資を選べるか。

current ref/State差分にr2 REQUEST_CHANGES→Core修復→用語/書誌再生成→r3 APPROVEが現れたため、この一件を選ぶ。r1や関連Issueは因果/要求範囲を確定する必要がある部分だけ読む。全W34品質再監査、過去全修復、PDF全号読解、新規小記事実験はしない。

必要Evidence: Humanの対象版と要求、直前のreview/bundle・宣言したcoverage、修復の差分とworklog、現在のCore実装が変えた決定的境界、現在のcanonical approvalとCandidateの局所binding。記録上の宣言、実際に読んだ証拠、rootが再確認した内容を区別する。

停止面: 一件の原因と既存責務・出力境界・追加仕事の関係を説明でき、候補策が同じ仕事の移転か、必要な新判断/機械処理かを区別できた時。不可視のLLM認知/active time/料金はunknown。正確なversion/hashだけでreview実効性や完全品質を認定しない。証拠が区別できなければその限界で止める。既存修復の作り直しやreviewer追加を結論に固定しない。

productionはGETのみ。承認/Freeze/Releaseを実行しない。追加agentなし（5-Bの一体許可は完了）。通常Pull/Push/最終commitはHuman。取得補助は既存`notes/phase-5b/capture.py`をimportし、DESTのみ本directoryへ指定する。5-B frozen artifactは変更しない。
