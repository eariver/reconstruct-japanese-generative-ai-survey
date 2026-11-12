# SP 人間向け Architecture ドラフト r3（案・未承認・条件付き） — efficient-llm-2026

**位置づけ:** AUTHOR r3 DATA案。v2 (`sp-candidate-map-r2.json`) + 独立review `CHANGES_REQUIRED` + `sp-jev-authority-inventory.md` + 新規 archive `BODY_VERSION_CONFIRMED (intake-20261106T001808Z-jev-archive)` に基づく訂正。`sp-four-record-correction-proposal.json` の4-record Delta（D070/D071/D141 archive再束縛＋D142 UNRESOLVED訂正）を前提とする条件付き復元であり、ready canonical ではない。独立re-review・Architecture承認・Human Gate・Draft/PDF・R4は未了。Stateは`EVIDENCE_REVIEWED`のまま。受容済Evidenceの編集はしない。

## r3で直したこと（fetchなし、packet DATAのみ）

- D070/D071/D141: 現行only束縛を archive 束縛に置換提案（original URL＋served timestamp分離、capture timestampをpublicationと偽装しない）。u1 wire gzip＋CDX `6XH5…` MATCH＋decoded `14ae3118…`、u2 wire gzip＋CDX `TUION…` MATCH＋decoded `35770834…`、u3 served `20260920205053` via requested `21091419` 302真実記載（requested-row `E2BRC…` NO-MATCH、served-row `ABQR…` MATCH）を manifest ref 付きで保持。
- D141: archived aliases `->1.13.0` が歴史 valid、Nov `->1.14.0` drift は post-cutoff で衝突なし（back-projectしない）。
- D071: `255-cardinality / score-then-choose` は archive 可視 text に不在のため as-of に使わない（current-onlyに残す）。
- Vendor 報告の mechanism/latency/price/eval条件は vendor として label、独立再現・秘密RLCD推論なし。
- D142: unfetched API に new source id なし。過剰 `VERIFIED` を `UNRESOLVED` に訂正（summary-only＋negative calibration finding）。API詳細なし。
- 15 obligations 維持（O10 LIMITATION、独立 mechanisms/eval 待ち、auto SATなし）。source-backed の境界 rationale のみ改善。
- High producer gap により operation BLOCKED。LOW manual workaround は run しない。

## 対象と読み方（r3条件付き）

- as_of `2026-09-21T16:10:00Z`。Evidence 160、Ledger 165、義務15（O10 LIMITATION）。
- O10 main case は vendor 歴史 scope（u1 09-21T03:30:22Z＋u2 09-21T04:13:55Z＋u3 09-20T20:50:53Z）で条件付き復元。canonical としては HOLD＋LIMITATION が上限。
- PR数値は `pr.json 26122B 3728e08d…` のみ。D119はGenAI-Perf docsで利用可（AIPerf openは別）。D162はlead-only。

## 目次案 r3（63 target / 85 max＋付録A 6独立＝69、p8条件付き復活）

- P1 4pp / P2 6pp / P3 5pp: lineage-only を claim utility で削減。PRIMARYなしを正直に記載。
- P4 10pp: PRIMARY Kimi/Qwen/V41/V32＋D143 Engram deltas。per-figure quarantine。
- P5 10pp: PRIMARY EAGLE＋Snell/s1/ThinkPrune/overthinking。Snell系はO14。
- P6 7pp: PRIMARY D165 existence＋PR-reported numbersのみ。
- P7 6pp: PRIMARY FrugalGPT Table3。D040/D049/D063 HOLD済み。
- P8 5pp 条件付き: SUPPORTING D070/D071/D141 vendor歴史 scope（条件付き）＋D142 HOLD。mechanism/latency/price/evalはvendor報告、再現・RLCD内部・calibrationなしを明示。D071 255はas-of除外。D141 1.13歴史／1.14 drift注記。
- P9 10pp: PRIMARY D030 README@dba1be0＋D032 launch。GLM abstract-only、AIPerf open。
- 付録A 6pp独立: D004/D163＋D040/D049/D063/D153＋D142＋watches/precedents。O10/O04/O08/O11 LIMITATION retained。

## 選ばなかったもの r3

- HOLD canonical 33 → conditional 30（D070/D071/D141のみ条件付きSELECT）。D142はHOLD維持。
- EXCLUDED 5 taskless DROP lawful維持。

## Rootへの正確な修正依頼（受容済み編集なし）

- D141/D142 status・subtarget text 訂正 scope＋body pins は `sp-four-record-correction-proposal.json` records および `sp-essential-gap-map.json` G6相当を参照。D141 alias `->1.13.0` 歴史／`->1.14.0` drift、D142 VERIFIED→UNRESOLVED。
- O10 歴史 authority は archive snapshots (u1/u2/u3) で D070/D071/D141 の body/confirmed まで。D142 body・独立 benchmark/reproduction・RLCD内部は依然 missing のため waive 不可。

## 次に必要なもの

独立re-review（4-record Delta＋supplement 30＋raw staging＋O10/G1/G2 scope）を経て、High producer revision（LOW workaroundではない）＋accepted revision＋7-slot retention/guard/checkpoint/State-switch の pre-code map・Astra・独立 readiness の後にのみ進める。Draft/PDFは承認前作らない。Typed APIは本r3 map後。

*pin・counts・gaps は `sp-candidate-map-r3.json`、Delta・supplement・staging は `sp-four-record-correction-proposal.json`。165 join／160 Matrix＋5 nonmatrix 維持。*
