# Addendum — four research-artifact refs (corrects setup README §54 wording, no raw overwrite)

Setup `setup-20261112T125743Z/README.md` §54 lists under “Successor four refs” three checkpoint file hashes (ISSUE `3c64e…`/`5b991…`, DISCOVERY `4d322…`/`481d96…`, CANDIDATES `0979f9…`/`1233b1…`). Those are Discovery/Screening/Evidence checkpoint refs, not the four research-artifact refs. Raw preserved; this addendum only.

Correct four artifact refs are in Evidence checkpoint `CANDIDATES_NORMALIZED.json` `artifacts[]` (independent `setup-independent-review.md` §4, re-verified OLD vs NEW identical, file bytes match):

W34 (`CANDIDATES_NORMALIZED.json` `0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a`):
- `edition-views-acceptance` `sources/2026-W34/evidence/v2/views/accepted/574b96ff3ce87f7f2e46fcd78724bf1fbfcdad590e009be1500f03446697b5c5/edition-views-accepted.json` `3777133cc09d0189ab97cc1d8ff1f8b420108d43880f69f1745356508b8acfce` 159498B
- `evidence-acceptance` `sources/2026-W34/evidence/v2/accepted/5ca6f31033dcaed6a153f0eb6f838f18bc9bdd1674a19a941f8c8378f88e4e48/evidence-accepted.json` `edf21e4de5f7ab8db2d5189f45abc8cc6d0cf6475e532b20bcc56b0ce5660218` 126592B
- `materiality-ledger` `sources/2026-W34/materiality-ledger-v2.json` `f089cc4eedb49a81b4b925c1219f22a77237d16f28fdee73f20a3744e725e91d` 186202B
- `profile-completeness` `sources/2026-W34/profile-completeness-v2.json` `e8c432dd6275e81df5286cb8c0d55d99e27aa0812c52a114d870dddaf0d2795f` 71532B LIMITED

SP (`CANDIDATES_NORMALIZED.json` `1233b1f6ca3301d6430d4d157788d0a45a613c9ce1e1563e7c06fe11d73993f0`):
- `edition-views-acceptance` `sources/SP-efficient-llm-2026/evidence/v2/views/accepted/5e722402c7e8df6077f87f0da33b2b53355f22ae3f306482dedbd27350b7145f/edition-views-accepted.json` `1557fef75b4b737379a0e84eea983d9151b7148077f65da018206a2fae2b0341` 64222B
- `evidence-acceptance` `sources/SP-efficient-llm-2026/evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/evidence-accepted.json` `65784e69559f9379412935fa5e7671beddee59b46b8fdb28a848d450e2b68ce0` 49237B
- `materiality-ledger` `sources/SP-efficient-llm-2026/materiality-ledger-v2.json` `b7c85b4eb009249b355445f94a4041d4374990fccb07c38595b61c1e770c8c60` 66850B
- `profile-completeness` `sources/SP-efficient-llm-2026/profile-completeness-v2.json` `d67f7f8363407b30d58dbe2dbe562b3666ea9483f9f16303859cfe459ab5e805` 33683B LIMITED

Next HIGH requests must bind these eight (before_checkpoint evidence/materiality/completeness + profile_ref/discovery_ref/screening_ref SizedRefs), not checkpoint file hashes. No raw overwritten.
