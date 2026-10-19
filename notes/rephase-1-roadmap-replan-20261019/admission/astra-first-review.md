# Astra first review — CHANGES_REQUIRED

初稿 `integrated-admission-contract-analysis.md` は判断入力として保存するが、§§2/3/7の実装提案は採用しない。rootが実sourceのcontroller 1860–2109、Longform receipt606–758、P1 Candidate822–862を直接読んだ結果、次の矛盾がある。

1. **3A/既存変更なしは不成立。** 新State pointerは既存schema/validator/resolverに消費者がなく、receiptはversioned reviewed pathを拒否する。旧P3Sの予算を転用しない。既存consumerを必要に応じて変える一貫した設計が必要。
2. **live 3fileのO_EXCLでは置換できない。** healthy beforeのmain/bib/styleは既に存在する。前後P2Vも「同じbefore」を要求するためlive変更後には使えない。前検証/限定transition中/after public検証を区別し、正確な全write setと失敗時の復旧を決める。State/receipt/QA等を書きながら3file-only/old-live unchangedとも主張できない。
3. **Candidateを混同。** `candidate_selection_gate.py`のSelectionと`publication-candidate-v2.json`は別。P1が保持対象とするobserved unadopted publication Candidate（822–862）を正常ケースから一律排除すると訂正不能が残る。exact retained旧Candidateのsupersessionを検討し、Human承認済み/foreign/driftと区別する。
4. **review/public validator循環が未解決。** current Longform receiptはcanonical reader/archive/receipt path固定（720–730）、strict Stateでderivationをロード（698）、new PDF/QA/semantic/visualを必要とするcontroller（1900–1944）がある。既存validatorを呼ぶという記述だけでは成立しない。review対象pathを維持し、fresh QAをどこで生成してどのchecked contextで検証するかを具体化する。
5. **別State pointerは総コスト比較不足。** 既存revalidation chainへのtruthful reason分岐と独立pointerのconsumer/履歴/retention対応を比較する。historical verifierだけではpublic current readbackにならない。既存record/旧epochのmigration境界も新候補のfixtureから明示する。
6. **fixture commit順が誤る。** 実装source/contractが意味ある独立fixture Gitでcommit済みであることがauthority生成前提。未実装recipeだけを先にcommitしてrenderer basisにしない。ordinary candidate commitの権限とは別。
7. **費用/代案が未検証。** P3Sと同規模という見積りは撤回する。DM021を構造的に解く拡張と、利用者に残すmanual recovery/再reviewの費用を明示する。
8. **復元証拠はtranscript要約。** packetにあるのは4文書だけでraw command logs/実行scriptはない。「raw保存/個別exit保存/fail-closed手順認定」としては扱えない。実際に保存した物とtool観測を区別し、以後の新しいread-only current verificationを別packetへ保存する。過去rawを再創作しない。`fsck exit0/missing26309`、full status形式、mode一致、inode独立のclaimも実観測で再点検する。

統合設計を別Generalへ再委任する。復元担当は過去記述の資格付けと新current観測だけを担当し、runtime変更/テスト/再復元は行わない。これは作者側reviewであり、独立reviewではない。
