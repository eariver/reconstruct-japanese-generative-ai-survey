# Current source verification — read-only observation (no restoration/reapply/Git writes)

2026-10-19 UTC. Restoration-evidence owner. Design analysis (`integrated-admission-contract-analysis.md`) は編集しない。原文書は `../restoration-evidence-correction.md` の資格付けのまま残す。本packetは新規read-only観測であり、過去rawの再創作ではない。

工具差異: `apply_patch` 不在のため `Write` で新規作成。

## 1. Method (inspect-only, no mutation)

- Target (read-only): `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60`
- Checker: `check_current_source.py` (`d69f39db…`) — reference `static21.json` を読み、観測から期待値を計算しない（no baseline blessing）。Git書込み・復元・再適用・test・importなし。
- Git env: `GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0` + `git --no-optional-locks`。継承 `GIT_*` なし（checker §0で実測 `NO_INHERITED_GIT_ENV`）。
- Raw persistence:
  - `raw_stdout.txt` (`3e7e60be…`, 165 lines) — checker stdout直接保存
  - `raw_stderr.txt` (`e3b0c442…`, 0 bytes) — checker stderr直接保存
  - `exit.txt` (`0`) — checker numeric exit
  - `revlist_missing_print_stdout.txt` (`a183a917…`, 28685 lines) — `rev-list --objects --missing=print 409…` 全出力
  - `revlist_missing_print_stderr.txt` (`e3b0c442…`, 0 bytes), `revlist_missing_print_exit.txt` (`0`)
- Source mutationなし。`.git` 内に新規lock/index/packを作成しない操作のみ使用（rev-parse/status/diff/ls-files/config/remote/rev-list）。

## 2. Exact evidence (current observation; numbers are this packet's raw)

- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` / tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` / `symbolic-ref rc=1` detached=True / shallow=true / git-dir=.git / common-dir=.git（raw §§1）。
- `status --porcelain=v1 -z` rc=0, 1084 bytes, NUL entries 21, parsed M=3 untracked=18（expected 3M18A一致）。`diff HEAD` 3行（上記3M）、`diff --cached` 0行、`ls-files --stage` 32155（通常indexがHEAD tracked bytesを持つ。**index file emptyではない**。旧proof freezeの `index empty` と混同しない）。
- all21: static file sha `1c0e339c…` 一致、entries 21、21/21 OK（sha+bytes+mode per-file一致。reference側が全 `0o664` のため今回全一致だが、blanket all664主張ではなくper-file比較rawによる）。
- durable inputs+patch: tar `faf6792…` 5152199B、20-pack `2c2a8e6f…` 46164B、W1 `97d384fe…` 57856B、DM004 `e3d94165…` 48240B、patch `e449d029…` 1233670B、全一致。
- `.git`: files 83/dirs 48/symlinks 0（aliasesなし）、alternates不在、`config --show-origin` は `.git/config` + `.git/config.worktree` のみ（include/insteadOfなし）、remote `example.invalid` inert、hooks 14件全 `.sample`（active 0）。
- inode sharing (domain明示): restored `*.pack` 5件（dev 45） vs durable inputs 4件 + reconstruct `.git`/`.git/HEAD`（dev 2050）。`dev:ino` 全相違、`INODE_SHARING_FOUND=False`。domain外（全history objects・全worktree files）の無共有は主張しない。
- caches: `__pycache__` 0（cache84歴史不在・再創作なし）。
- missing reachability (current census; prior転記と区別): `rev-list --objects --missing=print 409` rc=0 stderr空、total 28685 / present 2376 / missing(`?`) 26309（全出力別保存）。`rev-list --count` は `13`（commit chain長であり、all-object到達可能性ではない）。**fsckのavailable13 objectsという呼び方はしない。**

## 3. Qualification (retroactive repairなし)

- 旧 `restoration-procedure.md/manifest` の数値exit・`fsck missing26309`・status/mode/inode記述は transcribed/tool observationsであり、本packetで遡ってrawに格上げしない。`../restoration-evidence-correction.md` が優先する。
- prior `fsck missing26309`（転記）と current `rev-list missing26309`（本raw）は数値一致するが別観測である。13はcommit数であり、28685/2376/26309のobject censusと混同しない。
- 予期せぬ結果はなし（checker `failures=0`）。隠蔽なし。非0が出れば保存して報告する方針であり、今回0を成功認定の汎用PASSに流用しない。
- no network: 上記3変数 + inert origin/config + fetchなし。system/global config無効化済み。
