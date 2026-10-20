# Initial real-build integration — Astra assessment

2026-10-20 JST closeout. **Roadmap R2 BOUNDED COMPLETE:** initial generated Weekly＋THEMATIC/LONGFORM_SPECIALを実LuaLaTeXで生成し、PDF/log/digestの明示転送、公開receipt/Gate/QA/Candidate/Stateと合成承認付きFreeze/Releaseの接続を実証した。実visual欠陥1件を共有styleの1行で修復。作者別内容/visual点検と独立実装/evidence reviewを完了した。

必須: [root closeout](../notes/rephase-1-initial-build-integration/astra-closeout-resolution.md)、[独立final resolution §§2–6](../notes/rephase-1-initial-build-integration/independent-final-resolution.md)、[postfix visual resolution](../notes/rephase-1-initial-build-integration/independent-postfix-visual-resolution.md)。**複数runの範囲付き証拠**であり、一括full-suite/真正Human承認/Production受入れではない。

## 1. 得られた成果

| 境界 | 実結果 | 受入れ範囲 |
|---|---|---|
| source/runtime | available409＋final21から独立fixture。TeXLive2026/LuaHBTeX1.24.0/latexmk4.88/biber2.22を一時領域に用意。Python3.14.4＋jsonschema4.23.0/pypdf6.16.2 | workflow Python3.12・実Actions同等の認定ではない |
| initial生成 | actual accepted-chain producer→DRAFT_COMPLETE→2pass CLI→generated trio/receipt | 研究データ・上流承認は明示synthetic。真正研究資料の再評価ではない |
| real PDF | Weekly5pp/61151B、Special5pp/79156B（修正後最終run）。実compiler/log・3出力hashを保存 | placeholder資料の描画。単一DID・短い内容という限界 |
| public integration | strict receipt replay、exact manuscript/Gate、bounded deterministic checks、Candidate、合成Preview→profiled Freeze→RELEASEDを両routeで確認 | 74harness milestonesはtest件数ではない。意味/visual/Human承認fixtureは実判断と区別 |
| 拒否 | 元25負例、両stageのGate拒否補足、転送control | exact errorと観測範囲ごとに採用。先行validator拒否、失敗setup、修復control有無を区別 |
| transfer補強 | same evidence-only helperでO_EXCL/O_NOFOLLOW、正/衝突/欠落PDF/部分失敗/新target復旧 | 新helper経路はVALIDATED_DRAFTまで。旧check-then-copyのRELEASED結果と合成して一括runとはしない |
| source保存 | full22patch、独立clean409への直接apply、22pins/status一致 | partialDB/runtime非同梱。汎用safe-runner認定なし |

Final fixture source commitsはWeekly`51b0e42b…`、Special`9917a6ff…`（synthetic snapshot ancestry）。Final PDF SHAは[packet最終records](../notes/rephase-1-initial-build-integration/final22-integration-20261019T135318Z/README.md)のWeekly`899f0f2a…`とSpecial`71a2c98a…`、Specialは`attempt6`が正。原21fixtureのPDFや失敗attemptと混ぜない。

## 2. 実内容・visualの判断

[pre-TeX](../notes/rephase-1-initial-build-integration/independent-pretex-inspection.md)と[postbuild](../notes/rephase-1-initial-build-integration/independent-postbuild-inspection.md)は作者別の実読解/画像点検である。元・修正後とも各route全5ページ、合計10ページを点検した。

- reader入力からの描画、文字、引用、TOC、表、PDF表示は限定確認できた。
- **両synthetic editionのProduction semantic品質はNO-GO。** `Target Model`、`example.invalid`、薄い本文、単一DIDで4family欄を埋めたplaceholder等をpublishable researchに昇格させない。
- Special Technical Noteの白文字/薄灰色headerは実欠陥として修復。`technicalnote`だけ`coltitle=SurveyInk`を追加し、独立postfix画像確認で可読性改善・内容/他box不変を確認。
- pagination/余白は短いfixtureの影響が大きい。Longformの明示改頁はcover/frontmatter/referencesであり「毎section改頁」は広すぎた。代表的な長さでのlayout評価、row引用の見え方、bibliography日付localeは残す。
- Manuscriptのfulfilled requirement、postrender/densityのschema-valid PASSはsynthetic type入力。独立報告のNO-GOをこれらのPASSへ付替えていない。

## 3. 最終候補と復元

- 実candidate: `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`
- HEAD **409b292756dd1277b9dfae87679934c0d2ce251c**、tree **8ce3699861505f32d1d60bdc185d4d4f635aedb2**、未commit **22paths=4M18A**。旧21は不変、新変更は共有style1行のみ。
- style SHA256 **035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec**、6569B。
- 完全patch **[complete22-409-clean.patch](../notes/rephase-1-initial-build-integration/source-packaging/complete22-409-clean.patch)**: **7c82ec47eb82dc56210b82063fe04c583d29cd36df5ce19f48297ebd4f000334**,1233999B。4parent inputs→actual clean409へDIRECT適用。21patchは内包済み。
- [保存patch適用証拠](../notes/rephase-1-initial-build-integration/source-packaging/README.md): check/apply各0、22SHA/bytes/mode/status一致。stderrの2line whitespace warningsも保存。旧final22-manifestの73文字hash誤記はcomplete22-manifest/static21で訂正。
- Missing26309/runtime非同梱、source/fixture/proofのidentity区別を保持。源candidate commitもreconstruct commitも作成していない。

## 4. 費用と制約

TeX環境に約1GBの初期導入が必要だった。最終選択2buildの所要は約21.0秒/23.9秒だが、これは**初期setup・失敗・再build・fixture生成・review時間を含む全費用ではない**。総work/LLM/Human費の削減は未測定。

確実に得た改善は、許される3source/3output境界を弱めず、実compile→転送→公開admissionを実物で接続できると分かったこと、および見出しcontrast欠陥を発見・修復したこと。専用helperや手書き再開手順の実Production廃止はまだ行っていない。

旧transferは排他ではなかった。補足helperは観測用であり、sourceの事前fd固定・ancestor保持・CAS・crashatomicity等は備えない。元負例のno-write/修復の範囲は一様でなく、VALIDATED Gate負例はlate-file-swap fault injection。原rawの一部削除、`git clean`、専用editor指示逸脱を[必須root resolution](../notes/rephase-1-initial-build-integration/astra-closeout-resolution.md)に残す。新greenで過去をcleanにしない。

## 5. 次taskと全体の残り

**次の単位: R3 — 実build/外部review入力を組み込んだeditorial correctionの統合契約・実装選択。** Human continuation後にGeneralへactual final22で委任しAstraが決定する。

1. 今回確定したgenerated trio→disposable build→PDF/log/digest→各QA/公開consumerを、訂正前/後のversioned review target・authored input・State/receipt/Gate/Candidateへ対応付ける。入力に外部のpersisted semantic/visual判断を要求し、runtimeがPASSを生成する案を拒否。
2. **canonical replacement＋durable checked context**と**immutable versioned publication set＋reason-tagged active-role解決**を、具体caller/歴史行/失敗復旧/必要review/作業除去で比較する。既存Profile差替えやreason enumだけで解決すると仮定しない。先の2案NO-GOを再提出しない。
3. 最小の利用可能な訂正操作として、reader変更→実build/QA→公開readback→fresh Candidate→通常Preview/Freeze/Releaseまでのauthorityとwrite/保持集合を決める。既存未承認Candidate、同一reader機械refreshとの順序、部分失敗からの再開も含む。孤立した新helperを終了物にしない。
4. 選択設計が成立した時だけ、その具体的差分とactual accepted fixture/real-build oracleに基づく実装へ進む。境界の不成立なら根拠付き採否を返す。任意のpath数制限や新Human Gateは設けない。

並行して残る全体義務: 必要Special/Retrospective/manual/direct-primaryの適用範囲と代表的資料での品質確認、DM016/017 upstream Profile、**DM022のpre-Architecture accepted-upstream訂正**の必要対応、固定候補/七観点audit、Human採用/実運用、総費用判定/旧経路廃止。今回2routeの成功へ完成線を縮めない。

**whole NOT_READY / step4・B3 OPEN / audit未開始 / DM021・DM022 OPEN。Human Commit Pointで停止。** 通常Commit/Push・Production採用はHuman-owned。
