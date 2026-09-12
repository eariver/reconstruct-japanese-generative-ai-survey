# P-EAGLEの並列draftは何を速くするのか

vLLMの速度報告は、draftを順番に生成する負担を減らす実装を示す。倍率を読むには、比較対象と運用条件をそろえる必要がある。

[vLLMの3月13日付報告](https://vllm.ai/blog/2026-03-13-p-eagle)は、2月に論文が出たP-EAGLEのserving評価を紹介している。P-EAGLEは、学習した共有hidden stateとmask embeddingを使い、複数のdraft tokenを一回のforward passで提案する。target modelによる検証は引き続き必要で、検証を省いて速くする仕組みではない。

報告されたTPS（毎秒token数）は、GPT-OSS 20BをB200 1基のvLLMで動かした場合、EAGLE-3比で1.05～1.69倍だった。MT-Bench、HumanEval、SPEED-Bench Codeで、同時実行数1では1.55～1.69倍、64では1.05～1.25倍。最大1.69倍はSPEED-Bench Codeの同時実行数1の値であり、どの負荷でも得られる倍率ではない。両手法ともlinear draftingでK=3・5・7を試し、条件ごとに最大TPSのKをそれぞれ選んだ比較である。

[P-EAGLE論文](https://arxiv.org/abs/2602.01469v1)の1.10～1.36倍という結果は、H200と別のtarget・benchmark条件によるEAGLE-3比較であり、今回のB200報告と同一の測定ではない。また、並列予測には専用に学習したdrafterが要る。論文のattention mask事前計算や系列内分割は長系列学習のメモリ負荷に対応する工夫であって、学習作業をなくすものではない。一回のpassで生成できても、draft数を増やした際の計算・メモリや検証の負担まで一定になるとは限らない。

関連研究の[DFlash v1](https://arxiv.org/abs/2602.06036v1)（2月5日付）も、targetのhidden featuresを各draft層のKVに渡し、block diffusionで並列に提案する。専用drafterを学習する点と、targetによる検証を残す点は共通する。DFlashはTransformersだけでなくSGLangでも評価され、B200・FA4・Spec-v2の条件では通常のautoregressive decodingに対して最大5.1倍を報告している。これはQwen3-8BのMath500、同時実行数1の値であり、EAGLE-3比1.69倍と大小比較できない。LLaMA-3.1-8BでEAGLE-3と学習dataをそろえた別評価もあるが、この資料群からP-EAGLEとの同条件の優劣は決められない。

導入時にはheadだけでなくserving設定も確認したい。P-EAGLEの報告はvLLM v0.16.0からの統合を案内する一方、GPT-OSS 20BでEAGLE drafterを使うにはPR #36684のpatchが必要と記す。測定ではfp8 KV cacheとasync schedulingを使い、prefix cachingとchunked prefillを無効にしている。DFlash側も、大blockは大batchなどで検証費用を増やし得るとし、adaptive block-size schedulingを今後の課題としている。掲載TPSから、自分のSLAに対する遅延改善や学習・運用を通じた総費用の削減までは推定できない。

時点については、以上は論文の固定versionと、後日取得した報告本文に基づく。報告の日付は、記載されたheadやpatchがその日に同じ状態で入手できた証明ではない。当時の即時導入可能性と、掲載条件の独立再現は未確認である。
