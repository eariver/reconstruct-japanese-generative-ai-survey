# R1 復元手順 — fail-closed offline actual409+final21（新規作成）

> 工具差異の開示: 本task指示は `apply_patch` 指定だが、本環境に `apply_patch` toolは存在しないため、専用 `Write`/`Read` と `bash` のみで新規作成した。旧runner/scriptの再利用なし、fake-rootなし、layered patchなし、networkなし。

- 作業root: `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z`（新規・事前不在確認済み）
- 復元DB: `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60`（独立DBのみ。このroot以外にDB/indexを作成しない）
- workspace書込み先: `notes/rephase-1-roadmap-replan-20261019/admission/`（新規。旧packet不変）
- 開始workspace HEAD: `eb6b79be1dc6fcd704194c46de1c2f53c7c26e58`（Human commit、開始時cleanはroadmap READMEの記録に従う。今回 `git status` は新規roadmap2件のみ `??` で旧packet変更なしを確認）
- 旧 `/tmp/opencode` copies不在を確認（`ls /tmp/opencode` は空で開始。復元前に `DEST_ABSENT_OK` を確認）

## 0. 固定入力（4 parents + full21 patch + static21）

| 入力 | workspace path | SHA256（実測） | bytes | 期待値一致 |
|---|---|---|---|---|
| b40 tar | `notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz` | `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c` | 5152199 | OK |
| DM001/019 20-pack | `notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-pack.pack` | `2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99` | 46164 | OK |
| W1 7-pack | `notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/w1-222-to-e1705b7.pack` | `97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9` | 57856 | OK |
| DM004 32-pack | `notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/dm004final-e1705b7-to-409b292.pack` | `e3d941653eadf2459a13f1b85b9fbbffd819f0a0ad6bb77eb121b2cba02279bf` | 48240 | OK |
| complete21 patch | `notes/rephase-1-dm021-p3s/evidence-20261018T154812Z-final-packaging/gen-complete21/complete-p3s-21path.patch` | `e449d029c8775ee28ee610f224997a57b0cd68664194c6720a6038ce9a3012fa` | 1233670 | OK |
| R11 static21 | `notes/rephase-1-dm021-p3s/draft-history-r11/static21.json` | `1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5` | — | OK |

全hashは `sha256sum` で実測し、AGENTS/Roadmap/P3Sの固定値と一致。相違時は停止（fail-closed）。今回全一致のため続行。

## 1. tar安全性（展開前、Python tarfile実測）

- `total members: 760`、`Counter({b'0': 760})`（通常fileのみ。初回検査）
- 再検証: `TOTAL:760 BAD:0`（`/`先頭・`..`・symlink/hardlinkゼロ。`top prefixes: {'candidate-partial-b40de60'}` 単一）
- `.git` 74件含むが全て通常file、active hookなし（後述 `.sample` のみ）
- `.git/objects/pack` は `pack-78d27...` + `pack-b2d83...` の2組（`.pack/.idx/.promisor/.rev`）
- `.git/HEAD` は `ref: refs/heads/codex/rephase-candidate-recovery`、`config` originは `https://example.invalid/rephase-candidate-recovery.git`（inert）
- 展開先 `candidate-partial-b40de60` が不在であることを `test ! -e` で確認（`DEST_ABSENT_OK`）

## 2. Git継承環境の無害化

- `env | grep -E '^GIT_'` は空（`NO_GIT_ENV_OK`）。`GIT_DIR/WORK_TREE/INDEX_FILE/CEILING` の継承なし。
- 全 `git -C` は `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` で実行。
- `git config --global --list` は `credential.helper=gh` + `user.name=eariver/user.email` のみ。repo configを上書きしない。
- network操作（fetch/clone/pull/push）を一切実行しない。originは `example.invalid` のまま。

## 3. 展開（失敗rawを隠さない）

- 初回 `tar --no-absolute-filenames -xzf ... -C <newroot>` は `EXIT_EXTRACT:64`（`tar: 未知のオプション '--no-absolute-filenames'`）。本失敗を隠さず記録し、別名再実行とした。
- 再実行 `tar -xzf <tar> -C <newroot>`（portable flags、事前安全性確認済みのため安全）は `EXIT_EXTRACT_RETRY:0`。
- 展開直後 `ls` は `AGENTS.md/README.md/config/docs/schemas/scripts/specials/templates/tests` + `.git/{COMMIT_EDITMSG/HEAD/config/config.worktree/description/hooks/index/info/logs/objects/refs/shallow}` を確認（`EXIT_LIST2:0/EXIT_GITLS:0`）。

## 4. 独立DBの初期同一性・隔離

- `rev-parse HEAD` = `b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`（`EXIT:0`）
- `rev-parse --is-shallow-repository` = `true`（`EXIT:0`）、`.git/shallow` = `774dd39a951c9ac3818e83dfffd4c7666efb0a20` のみ
- `log --oneline -5` は `b40de60` + `774dd39`（shallow2件。`EXIT:0`）
- `status --porcelain=v1` は空（clean。`EXIT:0`）
- `remote -v` は fetch/pushとも `example.invalid`（inert。`EXIT:0`）
- `objects/info/alternates` は不在（`ls/cat EXIT:1/2`。no alternates/no sharing。`objects/info/` 自体不在）
- `hooks/` は14件全て `*.sample` のみ（active hookなし。`EXIT:0`）
- `objects/pack/*.promisor` あり（partial/promisor。欠落26309の前提。後述fsckで明示）
- copyは `cp`（hardlink/`ln`不使用）。別DB・別inodeの独立copy。

## 5. 後継3packの導入（新規fail-closed手順。旧restore_chain.py/runner不使用）

- `cp` で `successor-20.pack/w1-7.pack/dm004-32.pack` を `objects/pack/` へ（`EXIT_CP*:0`）。`sha256sum` でcopy後も4hash一致（`EXIT_SHACOPY:0`）。
- `git -C <repo> index-pack <pack>` を3件実行（各 `EXIT_IDX*:0`）。出力は各packのcanonical id（`c99020.../5c4d19.../116b05...`）。thin-fix不要。
- `verify-pack -v` は全て `ok`（`EXIT_VERIFY*:0`）:
  - `successor-20.idx`: 20 objects（`grep -c ^[0-9a-f]{40}` =20。内訳 `non delta:9/chain1:10/chain2:1`。commits `222a37e/ff6c67f/490414c`）
  - `w1-7.idx`: 7 objects（`non delta:7`。commit `e1705b7`）
  - `dm004-32.idx`: 32 objects（`non delta:12/chain1:13/chain2:7`。commits `409b292/34f934e/c4aa3b5/6ffed32/22598f1/d80b5ee/3dc4288`）
- AGENTSの `20(3c/9t/8b)/7(1c/3t/3b)/32(7c/16t/9b)` と一致。

## 6. actual409の確定

- `cat-file -t 409b292756dd1277b9dfae87679934c0d2ce251c` = `commit`（`EXIT:0`）
- `rev-parse 409^{tree}` = `8ce3699861505f32d1d60bdc185d4d4f635aedb2`（`EXIT:0`）
- `log --oneline 409` は13件（`409/34f/c4aa/6ff/225/d80b/3dc/e170/222/ff/490/b40/774`。`EXIT:0`、`rev-list --count`=13）
- `checkout --detach 409b292...` は `HEAD is now at 409b292 ...`（`EXIT:0`）
- 直後 `rev-parse HEAD` = `409b292756dd1277b9dfae87679934c0d2ce251c`、`HEAD^{tree}` = `8ce369...`（各 `EXIT:0`）
- `status --porcelain=v1` は空（clean409。`EXIT:0`）
- `fsck --no-dangling` は `EXIT:0` だが `missing blob` を26309件出力（`grep -c ^missing` =26309）。 inherited missingを隠さない。`rev-list --objects --missing=print 409` はavailable13件を正常列挙（`EXIT:0`）。full-history/runtime backupの主張はしない。

## 7. clean409事前確認（DIRECT適用の前提）

- `apply --stat` は `21 files changed, 21116 insertions(+), 10 deletions(-)`（`EXIT_STAT:0`）
- `apply --check` は `EXIT_CHECK:0`（stderr空）
- 21 pathの事前存在: `ABSENT 18 / EXISTS 3`（Python実測。`EXIT:0`）。EXISTS3は `schemas/reader-surface-gate-v2.schema.json/schemas/reader-surface-semantic-review-v2.schema.json/scripts/survey_reader_surface_gate_v2.py`（3M）。`status` cleanにより3MはHEAD一致。
- cache84は歴史的実体不在のため再創作しない。`find -name __pycache__` =0件（`EXIT:0`）。applied copyは21行のみ（active105との混同をしない。supplement§5準拠）。

## 8. DIRECT適用（layered patchなし）

- `git apply <complete-p3s-21path.patch>` は `EXIT_APPLY:0`。ただし下記warningを隠さない:
  - `complete-p3s-21path.patch:17857: trailing whitespace.` / `new blank line at EOF.` / `warning: 2 lines add whitespace errors.`
- 直後 `status --porcelain=v1` は21行（`EXIT:0`、`wc -l`=21）:
  - `M 3`（上記3M） + `?? 18`（18A）。`3M18A` でP3S assessmentと一致。cacheなし。
- HEAD/tree不変（`HEAD=409b292/tree=8ce36998` 各 `EXIT:0`）。candidate commitなし（detachedのまま）。

## 9. final21検証（R11 static21 1c0e339c基準）

- Python `hashlib.sha256+len+stat(0o777)` を21件全数実測。結果 `VERIFY21: ok 21/21 fail 0`（`EXIT_VERIFY21:0`）。内訳はmanifest別表。全 `0o664` 一致。
- 代表3A: module `7059166e.../126181B`、schema `4fa61723.../5627B`、test `a3bb0f23.../147845B` がstatic21と一致。
- `find __pycache__` 0件のため、applied21=21とactive105（21+84）の区別を維持。cache84のbyte再証明は主張しない（P2R `cache-inventory-static.json` が別権威。今回re-hashなし）。

## 10. 隔離・不変の最終確認

- `config` はinertのまま（`example.invalid`。`EXIT:0`）、`alternates` 不在（`EXIT:2`）、active hookなし。
- `index` はHEADのtracked bytes（`ls-files --stage | wc -l`=32155。temporary-indexではない通常index。proofの `index empty` との混同をしない）。
- `/usr/bin/python3 --version` = `Python 3.14.4`（実行は検証のみ。P3S runtime実装/test実行なし）。
- workspace `git status` は `?? notes/rephase-1-roadmap-replan-20261019/ + ?? outputs/rephase-1-completion-roadmap-20261019.md` のみ。旧packet変更なし。
- 本復元で旧 `/tmp` を上書きせず、新rootのみ使用。GEN DB/temp indexのpacket外配置原則を維持（本復元はGEN再実行なし）。

## 11. 残る限定（成功の誤用禁止）

- `fsck missing 26309` を含むpartial/shallow/promisor制約、unbundled runtime、no-CAS/crash/true-approval/migration/adoptionは残る。
- 本復元+patch適用はsource準備のみ。26-methodの再実行・full-suite・PDF build・真正review/Human判断の証拠ではない。
- `git apply --check/apply` の数値exitは個別に保存したが、`apply --check` のstdout空と `apply` のwhitespace warning2行を隠さない。成功の診断隠蔽なし。

## 12. 生数値exit一覧（要約。再実行は別名・別root）

`TAR_HASH:0/20PACK:0/W1:0/DM004:0/PATCH:0/STATIC21:0/TAR_SAFETY:0/DEST:0/MKDIR:0/ENV:0/EXTRACT:64→RETRY:0/HEAD_b40:0/SHALLOW:true:0/STATUS_clean:0/REMOTE:0/ALT:1(不在正常)/HOOKS:0/CP:0/SHACOPY:0/IDX20:0/IDXW1:0/IDXDM004:0/VERIFY20:0/VERIFYW1:0/VERIFYDM004:0/CAT409:0/TREE409:0/LOG409:0/COUNT13:0/CHECKOUT:0/HEAD409:0/TREE409:0/STATUS409:0/FSCK:0(missing26309)/STAT:0/CHECK:0/APPLY:0(warn2)/STATUS21:0/VERIFY21:0/CACHE0:0/PY:0`
