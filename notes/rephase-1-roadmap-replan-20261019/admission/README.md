# R1 admission packet — 復元 + 統合契約分析

**Current overriding disposition:** [Astra可否判断](../../../outputs/rephase-1-integrated-admission-feasibility-decision.md)で原案・`integrated-admission-correction.md`の両案をNO-GOとした。[独立review必須§9](../independent-roadmap-decision-review.md)は不採用/再計画/次taskのみ支持する。以下の「提案決定」は元Worker返却であり実装指示ではない。

**Mandatory evidence qualification:** [restoration-evidence-correction.md](restoration-evidence-correction.md)を読む。以下の「失敗raw・数値exit保存」は転記/tool観測の意味に限定され、復元当時rawは保存されていない。[新current観測](current-source-verification-20261019T000525Z/README.md)とdecision§2のchecker/inode比較domainを区別する。

再計画後最初のtask（R1: checked editorial admission / normal-lifecycle return統合契約）のWorker成果。root architecture reviewerの判断入力であり、Worker自身の独立reviewではない。

- 全体計画: `outputs/rephase-1-completion-roadmap-20261019.md`
- R1 task契約: `notes/rephase-1-roadmap-replan-20261019/README.md`
- 復元手順（失敗raw・数値exit保存）: `restoration-procedure.md`
- 復元manifest（固定hash・同一性・限定）: `restoration-manifest.json`
- 統合契約分析（本文・日本語）: `integrated-admission-contract-analysis.md`
- 復元DB（独立・inert・detached409+final21）: `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60`
  - `HEAD 409b292756dd1277b9dfae87679934c0d2ce251c` detached / `tree 8ce3699861505f32d1d60bdc185d4d4f635aedb2`
  - `status 21行=3M18A` / `final21 21/21 OK vs static21 1c0e339c` / `__pycache__ 0`（cache84再創作なし）
  - `fsck missing 26309` を隠さない。candidate commitなし、networkなし、旧packet不変。

工具差異: `apply_patch` 不在のため `Write` で新規作成（手順書に明示）。

## rootへの読所・判断依頼

1. `integrated-admission-contract-analysis.md` §§1–7（actual-source根拠・DM022境界・3案比較・次vertical task具体形・採否提案）
2. `restoration-procedure.md` §§6–9（409系譜13・clean409前提・DIRECT適用・21/21検証・missing26309）
3. 実source hotspots（復元DB内。workspaceではない）:
   - `scripts/survey_agent_control_v2.py:726 _collect_pending_rows / :1931 revalidation→Gate`
   - `scripts/survey_reader_surface_gate_v2.py:1174 Longform receipt / 698 strict healthy-State readback`（P3S contract§2の指摘行。復元DBで再確認要）
   - `scripts/survey_production_v2.py::transition_state`（単調前進・同State拒否。DM022 intake §§15–59）
   - `scripts/survey_human_gate_v2.py::invalidate_pending_gate`（pending Gate + Architecture checkpoint条件）
   - `scripts/survey_editorial_correction_proposal_v2.py`（P1 prepare/stage。reason/recordの現起点）
   - `scripts/survey_editorial_retention_v2.py`（P2R COPY→KEEP。retained権威）
   - `scripts/survey_editorial_current_authority_v2.py`（P2V SCOPE_BOUND。live/current観測）
   - `scripts/survey_editorial_staged_source_v2.py:574/794/964/1032/1095/1113/1134`（P2V×2・manifest-last・所有4file）
   - `schemas/editorial-* / longform-* / reader-surface-*`（7+?の契約面。特に `editorial-staged-source-manifest-v2` と既存Gate/receipt schemaの差）
4. 提案決定: 本文§7の ** bounded coherent extension（checked editorial admission最小一貫拡張）を条件付き選択、helper-only追加・現状維持・broad authority置換は不採用** の採否。fresh作者別設計reviewへ回付し、R2 vertical taskのscope固定を求める。Workerは独立PASSを宣言しない。
