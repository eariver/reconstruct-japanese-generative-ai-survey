# P-EAGLEの並列draftは何を速くするのか

vLLMの速度報告は、draftを順番に生成する負担を減らす実装を示す。倍率を読むには、比較対象と運用条件をそろえる必要がある。

AmazonとNVIDIAのチームによる[vLLMの3月13日付報告](https://vllm.ai/blog/2026-03-13-p-eagle)は、P-EAGLEのserving評価を紹介している。元の論文は、UCSCのMude HuiがAWSでのinternship中にAWSの共著者らと行った研究で、2月に公開された。P-EAGLEでは、補助モデル（drafter）が学習した共有hidden stateとmask embeddingを使い、複数のtoken候補を一回のforward passで提案する。本来動かしたい大きなモデル（target）がそれを検証するため、検証を省いて速くする仕組みではない。

報告されたTPS（毎秒token数）は、GPT-OSS 20BをB200 1基のvLLMで動かした場合、公開済みvanilla EAGLE-3 checkpoint比で1.05～1.69倍だった。P-EAGLE側は専用学習した4層drafterで、報告では受理される候補の長さの改善も速度に寄与する。並列生成の順序だけを変えた効果の測定ではない。MT-Bench、HumanEval、SPEED-Bench Codeで、同時実行数1では1.55～1.69倍、64では1.05～1.25倍。最大1.69倍はSPEED-Bench Codeの同時実行数1の値である。両手法ともlinear draftingで提案token数Kを3・5・7と変え、各条件で最大TPSのKをそれぞれ選んだ比較であり、任意の負荷やKで同じ効果が得られるわけではない。

[P-EAGLE論文](https://arxiv.org/abs/2602.01469v1)では、H200と別のtarget・benchmark条件を使い、追加のHCA lossで学習したEAGLE-3を比較対象としている。要約の1.10～1.36倍は表10の全条件の範囲ではない。Qwen3-Coder 30BのHumanEval、同時実行数4、P-EAGLEのK=3では、最適KのEAGLE-3に対するTPSが0.92倍で、遅くなる条件もある。著者は低Kでは4層の一回の処理が1層の逐次処理より重くなり得ると説明する。また、attention mask事前計算や系列内分割は長系列学習のメモリ負荷への対策であり、専用drafterの学習をなくさない。一回のpassという特徴だけでは、学習・検証・計算負担まで小さくなるとは結論できない。

関連研究の[DFlash v1](https://arxiv.org/abs/2602.06036v1)（2月5日付）は、UC San DiegoのJian Chen、Yesheng Liang、Zhijian Liuによる。targetのhidden featuresを各draft層のKVに渡し、block diffusionで並列に提案する。専用drafterを学習する点と、targetの検証を残す点は共通する。論文はSGLangでの評価も含み、B200・FA4・Spec-v2の条件では通常のautoregressive decodingに対して最大5.1倍を報告する。これはQwen3-8BのMath500、同時実行数1の値であり、EAGLE-3比1.69倍と大小比較できない。LLaMA-3.1-8BでEAGLE-3と学習dataをそろえた別のSGLang/Spec-v1評価でもDFlashが上回ったと報告するが、この資料群からP-EAGLEとの同条件の優劣は決められない。

導入時にはheadだけでなくserving設定も確認したい。P-EAGLEの報告はvLLM v0.16.0からの統合を案内する一方、GPT-OSS 20BでEAGLE drafterを使うにはPR #36684のpatchが必要と記す。測定ではfp8 KV cacheとasync schedulingを使い、prefix cachingとchunked prefillを無効にしている。DFlash側も、大blockは大batchなどで検証費用を増やし得るとし、adaptive block-size schedulingを今後の課題としている。掲載TPSから、自分のSLAに対する遅延改善や学習・運用を通じた総費用の削減までは推定できない。

時点については、以上は論文の固定versionと、後日取得した報告本文に基づく。報告の日付は、記載されたheadやpatchがその日に同じ状態で入手できた証明ではない。当時の即時導入可能性と、掲載条件の独立再現は未確認である。
