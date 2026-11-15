# SP prepare-only execution report — FAIL before writes, preserved, no retry

Root §7 ONE SP prepare-only via pinned r3 `dc364727…` + config `e55b0f12…` (r6 `cca74577…`, r5 `cc4ce34d…`, full30 `e2bfb30a…`, routing `d8e10ea0…`, staging `f9780f6a…`, 773 `a7e40c…`, cc1c).
Command (workspace cwd, ABS repo fixes W34 relative bug):
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ABS_REPO python3 notes/.../prepare-normal-high-r3.py --issue SP-efficient-llm-2026 --repo-root ABS_REPO --revision-id sp-repaired-20261112-r1 --config notes/.../prepare-normal-high-config-r3.json --outdir …/prepare-normal-high-r3-SP-20261113T140724Z-outer`
Outer `…-outer.stdout/stderr/exit=2`, inner `…-outer/{argv,stdout,stderr,traceback,exit 2,entry-inventory}`. No Git/network/Production/reconstruct readback, single PID, 1200s timeout.

## Precise exception, where writes stopped
- Exit `2`. `REFUSE: SP D142 pinned drift` at `prepare-normal-high-r3.py:648` during SP routing verification (after `routing keys […]`, after u1/u2/u3 checks, before first-claim literal, before any Raw/request/supplement/R).
- Writes stopped: zero SP files created. Verified absent pre/post: request `…/acceptance-revision-inputs/sp-repaired-20261112-r1.json`, R `…/acceptance-revisions/sp-repaired-20261112-r1`, 4 Raw `sp17-EFF-D070…/D071…/D141…/D142-summary…`, no new supplement. W34 prepared manifest `54de43ed…`/438583 and 4 Raw/request preserved, old States/CP/source unchanged, SP State `180db8c3…`/CP `1233b1f6…` unchanged, no guard/decision/adopt.
- Note: entry inventory records D142 existing `f7eeec68…`/3751 `0o664` matching routing pin; manual post hash/size identical. Refusal is path/pin comparison in wrapper pre-write, not a source mutation. No fix/retry/cleanup per §7 STOP.

## Post-inventory (stdlib)
- Old: W34 State `d7acd29b…`, CP `0979f9f7…`, 4 refs preserved; SP State `180db8c3…`, CP `1233b1f6…`; source 773 `a7e4…`; SP supp dir has no `sp17-EFF*` new files.
- New: none for SP. Outer + inner logs only.
- Code/raw/module binding: operator `dc364727…`, HIGH `f312f02e…`, LOW `7f5fc9e0…`; three archived sources `14ae3118…/253542, 35770834…/307198, 97a5dd74…/350662` FULLDID verified in prior runs (u1/u2/u3 checks passed this run before D142 stop); D142 summary `f7eeec68…`/3751 route `sp17-EFF-D142-summary-captured-20260921.md` + literal `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` mechanically present in retained bytes (prior verification), but this run stopped before literal gate — not claimed as this-run PASS. SEMANTIC still pending, no decision.
