# Phase 5 — current Coreとの照合と保守判断

日付: 2026-09-15 JST  
状態: **BOUNDED ROOT REVIEW COMPLETE / PARTIAL UPSTREAM SUPERSESSION / NO ADOPTION / NO CONDITIONAL 5-C**

## 1. 判断

productionの関連改修を取り込み対象として照合した結果、**旧Freeze/Release候補を一括でreview・適用する入口は廃止する。Releaseの必須report生成は上流で実装済み、Freezeの二つの不整合は残存、reader gateは実装済みだが対象範囲と出力への結び付けに再現可能な不足がある。** 次はこの残差に限定した保守と検証であり、新architecture B、意味層、conditional 5-C A/Bではない。

開始reconstruct local HEAD/remote mainはHuman指定`b8bdf9821a48d22b2db840458b1b385f1c744bdb`と一致・clean。production mainをGETで確認し`774dd39a951c9ac3818e83dfffd4c7666efb0a20`を固定した。前回main `3e3eebe0cda3a32ac88ae764d279b37768f6bfca`から8 commits / 16 changed files。今回compareは前回の300-file打切りとは別で、返却上限に達していない。変更script/schemaを全て取得し、関係する関数を限定読解した。全Core/全変更testを読解・実行したとは言わない。

[Evidence](../notes/phase-5-upstream-reconciliation/README.md)、[固定入力](../notes/phase-5-upstream-reconciliation/inputs.json)、[限定probe結果](../notes/phase-5-upstream-reconciliation/probe-results.json)。production成果はproduction側の成果であり、reconstruct候補の採用・独立review済みという意味ではない。

## 2. 旧候補と計画の処遇

| 対象 | current production | Phase 5の処遇 |
|---|---|---|
| Release helperのCORE_STAGE_CONTRACT欠落 | #495でreport生成、COREと外部reconciliationのdual reviewを実装。controllerにもrelease record/merge artifactの照合を追加 | 欠落修復の重複実装・旧producer置換は不要。旧候補を採用済みとは言わない |
| Freeze artifact集合 | stage validatorは2種類を要求しextraを拒否。schemaの既存visual-review-record要求と不一致のまま | 旧候補のこの問題設定は存続。current reader gateを保つ限定差分が必要 |
| Human approvalの型 | `_prior_artifacts`は全checkpoint pointerをStage Checkpointとして読むまま。実W34のpublication_previewはHuman approval | typed authority解決が引き続き必要。単純skipや最新Candidate推測は修復にしない |
| FROZENのlocal semantics / retry | current producerは独自にreportを構築。旧候補の共通stage検証・timestamp保持と同一ではない | 旧候補の成功をcurrentへ移さない。full workflow retryは未実証のまま。今は別の全面再実装へ広げない |
| pre-TeX reader review | #496でstructured input、persisted semantic review、下流gateを実装 | 「入口を新規実装する」計画は既に古い。§3の範囲/結合を先に直す。前回reader計画を再執筆したり重複gateを足したりしない |

current Release helperは既存reportの比較に`recorded_at`を含めるため、同じ外部recordでも時刻を変えた再呼出しは旧候補のようにbytes保持で再利用する設計ではない。この差はsource inspectionであり、今回はRelease helper/Actions再試行を実行していない。上流のState/release検証を「検証なしの偽PASS」とは扱わない。current schema/controllerはhistorical FROZENにもdual reviewを要求する。実W34は既に両方を持ち、新schemaを通った。未検査の旧号全般の互換は保留する。

旧[候補patchと試験](../notes/phase-5-runtime-repair/README.md)は歴史Evidenceとしてそのまま保持。新sourceへそのまま適用するとreader gate等の変更との整合を失い得るため、次の実装の完成物ではない。

## 3. current reader gateで確認できた仕事の差

### R1 — review対象と現在の本文との結合

`evaluate_reader_surface_gate`と`validate_reader_surface_gate`は、persisted semantic reviewとその対象ファイルのhash/存在/issue/profileを検証する。一方、reviewされたstructured inputから現在のTeXが導出されたことは検証していない。下流stage呼出しもexpected issue/profileだけを渡し、現在のmanuscript authorityをgateへ照合入力として渡さない。

current上流test helperの合成reviewを使い、structured inputとreviewを保存したまま、manuscriptのprimary TeXを別の正常な読者文章へ変え、manifestの参照hashも更新した。gate生成と再検証は両方PASSした。review済みファイル自体をdriftさせる対照は拒否された。**個々のhash検証は働くが、両者の内容関係を保証しない**という限定反例である。無関係なreviewを新たに偽造して検証を迂回した実験ではない。review判断自体はfixtureで、実reviewではない。

これは新gateの局所的な受容であり、全stage advanceや最終editorial/PDF/Human Gateを通過する実証ではない。後段reviewが誤りを見つけ得ることと、早期reviewを再利用するbasisが正しいことは別。修復では、採用する現在のmanuscriptとgateのsurface集合を照合し、review対象の完全なreader projectionと実際のrender入力/出力との導出関係を検証する必要がある。hash欄をもう一つ追加するだけでは足りない。

### R2 — pre-TeX review対象から落ちる読者フィールド

Weekly publisherのstructured inputへの引数はclosing synthesis、final summary paragraphs、package headline/deck/blocks、cover headline/deck。実renderが出力するcover anchors、frontmatter heading/lede/scope_notes、final summary headingは含まれていない。section kickerも同じ引数集合にはない。

実projection/render関数で`frontmatter.lede`だけを`Discovery observation ...`へ変更すると、TeXは変わるがreview対象JSONのhashは同じだった。この文はlexical scannerに直接渡すとblockingになる。main内のpre-TeX lexicalリストにもfrontmatterは含まれない。後段TeX lintが止め得ても、Humanが指定したpre-TeX境界での早期検出にはならず、semantic reviewもこのフィールドをその入力から読めない。

probeは空のpackage列でprojection/renderの差だけを検証し、全Weekly edition/CLIを実行していない。全Specialのrender入力網羅性は未調査。修復時は実renderが消費する可変読者フィールドを一つのprojectionへ集約し、lint/review/renderでそれを共有する。本文を再著述する別artifactや新Human Gateは要らない。

### R3 — audit説明を読者本文として停止する

`validate_manuscript_surface`とgate生成器は`architecture_coverage[].detail`をreader proseとしてlintする。TeX/Bibを変えず、このmanifest内のcoverage説明だけに`Discovery observation`を記すとblockingになった。実renderが読まないaudit説明への拒否である。エラー位置もmanifestではなくProduction Profile pathを指す。

Human carry-forwardの狭いreader-field lintと、監査用説明の読者化は別。非読者フィールドをscopeから外し、実際に読者へ出る位置へfindingを結び付けるのが保守方針である。許可済み内部説明を無理に言い換える仕事や、恒久例外の追加管理へ移すことは改善に数えない。W34のHuman受容済みdebtを再生成しない。

## 4. 次に行う限定保守と終了条件

**次の既定作業はcurrentに対する残差の修復候補をreconstructで作ること。旧patch一式の独立review、reader実運用trial、追加の網羅監査は先行させない。** 根拠は、現時点で失敗/誤受容の具体例があり、ここで独立reviewやtrialを増やしても既知不整合の再発見と引継ぎを増やすため。

1. **Freezeの二つの残差**を先に扱う。current reader gateと上流Release producerを保持し、schema-required visualを承認済みCandidateへbindして受理、Human approvalは専用型からexact Candidateへ解決する。旧候補の限定部分と既存negativeを再利用し、現sourceでの正常系とauthority drift拒否を確認する。既存Git-aware fixtureは独立Git rootでのみ実行する。
2. **readerのR1–R3**を同じ保守単位で混ぜず、別の限定差分として扱う。全readerフィールドの単一projection、現在のmanuscriptへの結合、audit-field除外を揃え、上記反例が正しく拒否/受容へ変わることを確認する。Weeklyだけを直してSpecial generalityを認定せず、少なくとも既存LONGFORM_SPECIALの対応入口を確認する。current semantic reviewのpersisted record、drift検出、下流admissionを弱めない。
3. その具体物の独立reviewが必要になった時点で、限定scopeに対する新しい明示許可を得る。productionへの投稿/適用/採用は別のHuman authorization。今回それらを求めるために停止したのではなく、**upstream照合と根拠付き残差処遇が揃った判断面で終了**する。

各修復単位は再現失敗、修復後正常系/負例、関連回帰、維持したauthority、残るcaller/historical/費用の限界をreview可能にしたところで止める。Actions全体やfull canonical baselineを前提に膨張させない。currentに新しい上流修復が来たら、まず当該残差だけ照合する。Issue open indexの取得では5件が返ったが、全Issue本文/閉鎖Issue/PR reviewを監査したわけではない。新Issue/コメントは投稿していない。

## 5. 全体目標への含意と保留

今回の仕事はarchitecture選択の追加A/Bではなく、すでに実装されたquality/authority境界を有効に働かせるための接続検証である。支持できる改善対象は、Freezeの決定的な停止による手動復旧、早期reviewから抜ける本文の後段修復、audit説明への誤停止と例外管理。必要なsource固有の検証、編集判断、独立review、最終PDF/visual/Human判断を省略・他roleへ移転する提案ではない。

新gateには入力作成、review record、後段report、各消費者の整合、歴史互換の保守もかかる。上流に実装されたというだけでtotal lifecycle workが減ったとは言えず、今回の取得・読解・probe修正・記録・引継ぎ費も含む純削減はunknown。5-Bの「除ける同一比較条件再構成の支持例なし」と部分的非識別性は維持。新意味層、恒久telemetry、renderer/citation/cache等の保留を再開する根拠にはしない。

current W34 mainは実StateでRELEASED / next null。release checkpoint raw hashをState pointerと照合し、新schemaで受容された。W34 branch、public asset、PDFのfresh取得/品質review、全State依存閉包の検証はしていない。旧観測のbranch FROZENをcurrent mainへ混同しない。Human承認や既存Releaseは変更しない。

全号publication quality、Special/歴史の一般性、独立review、current workflow全実行、net savings、architecture adoptionは未実証。Phase 4はclosed、conditional 5-Cは未開始。通常Pull/Push/最終commitはHuman。
