# Phase 5 — runtime修復候補のEvidence

[判断](../../outputs/astra-phase-5-runtime-repair-assessment.md)。conditional 5-Cではなく、固定Coreの二つのproducer/consumer不整合に対するreconstruct-only候補。

## 再開時に必要なもの

- [candidate.patch](candidate.patch): production source二つ＋既存producer単体テストの変更。まだproductionへ適用していない。
- [test_runtime_repair.py](test_runtime_repair.py): 追加の実validator接続テスト。fixtureの研究本文/QA/Human決定は合成入力。
- [candidate-files](candidate-files.json): patch前後のexact source SHA。
- [baseline結果](baseline-results.json) / [raw log](baseline-test.txt): 3 profile条件でschema-required VISUALがunexpectedになった。最終追加testと同じfixture classのAST hashを照合。
- [初回関連回帰結果](test-results.json): 58件中52件PASS、6件はGit-aware fixtureのroot設定不足でerror。成功結果へ上書きしない。
- [Git-aware再実行](git-aware-results.json): 独立Git rootとfixture-only originを用いて同じ系統8件を再確認し全PASS。source/test bytesは初回と同一。
- [check.py](check.py) / [check結果](check.json): 固定入力、patch、両test runのcode hash、追加test、baselineの同一classをoffline照合。

## 固定入力と再現

production mainは開始時のGETで`3e3eebe0cda3a32ac88ae764d279b37768f6bfca`。reconstructは`f5dffe5c3c748a545437b21f1e43a145a041ba4d`でlocal/remote一致・clean。[baseline metadata](baseline.json)、[個別GET](inputs.json)、[固定support bytes](support-inputs.json)。codeの主な根拠:

- [stage validator](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_stage_validation_v2.py)
- [release checkpoint producer](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_release_checkpoint_v2.py)
- [controller](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_agent_control_v2.py)
- [current Release workflow](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/.github/workflows/survey-production-v2-release.yml)

ignored cacheは`.phase-5-inputs/runtime-repair-baseline/`と`runtime-repair-candidate/`。archive全体を再取得する必要はない。cacheが失われた場合、上の固定refとsupport manifestのpathから必要なcode/schema/config/contract/test bytesをGETで復元する。publication実データの復元やW34再実行は不要。

再現する場合は、まず**独立した使い捨てGit repository**をreconstructのignored領域に用意する。親reconstructのGitを継承させない。fixture-onlyのorigin URL（今回`https://example.invalid/isolated-test-only.git`、接続しない）を設定し、固定support snapshotとpatch・追加testを含めたテスト用commitを置く。これは成果のfinal commitとは別のテスト前提。実production/ユーザーのbranchをここへ結び付けない。

テスト用commitの準備ではcopyにpatchを適用し、追加testを`tests/test_runtime_repair.py`へ置く。Linux/WSLでconfigが指定するjsonschema 4.23.0 / pypdf 6.16.2を使い、そのrootから次を実行する（`<evidence>`は本directoryの絶対path）:

```text
python3 <evidence>/run_tests.py candidate <evidence>/new-test-results.json
```

現在保存した全回帰を理由なく反復しない。問題がGit-aware fixtureだけなら`candidate`の代わりに`git-aware`で該当系統のみ実行できる。baselineの既知失敗だけを見るmodeは`baseline`。既存cacheの確認はreconstruct rootから`python notes/phase-5-runtime-repair/check.py`。

## テスト環境の修正履歴

初回はisolated filesystem copyだけを作り、Git rootの隔離をしていなかった。既存Human revisionテストは独自indexでfixture commit objectsを作り、`refs/remotes/origin/test/revalidation`を作成/更新/cleanupする。そのため親reconstructのobject databaseへfixture objectsが書かれた。通常index/HEAD/mainは変わっておらず、対象refは終了時に不在。refの実行前値は記録していないが、reconstruct remoteにも同名branchは現在存在しない。不要objectの一括削除/GCは行わない。

独立Gitを作った最初の再実行ではorigin未設定も判明したため、その実行を中断し、接続しないfixture-only originを設定した。codeのguardをskipしたり、Humanのreachable-commit規則を弱めて通したのではない。設定後の8件全PASS結果をgit-aware-resultsへ保存した。これらの調査/修正/再実行費を候補の費用から除外しない。

## 境界

新規testは実State/schema/publication/approval/stage/controller検証を通すが、上流research/独立editorial判断はfixture。Actions外部処理は実行せず、既に成功した外部Releaseの固定recordを入力する。独立review、実W34/歴史全data、Windows native実行、全dispatch/retry、全品質/純lifecycle savingは未実証。旧決定・旧Evidenceを上書きしていない。

productionに対する操作はread-only取得のみ。追加agentなし。reconstruct成果のGit Pull/Push/最終commitはHuman。
