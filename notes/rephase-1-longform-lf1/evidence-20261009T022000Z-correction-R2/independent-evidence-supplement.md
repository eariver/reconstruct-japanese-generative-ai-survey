# Independent evidence supplement (closeout, no rerun)

2026-10-09. Closeout-only: read exact files listed below, no probes, code,
source edits, subagents, or network. Prior `independent-final-resolution.md`
(BOUNDED_PASS) stands unless contradicted here — it is not.

## 1. v1 numeric claim: QUALIFIED (defect confirmed, deviation disclosed)

Preserved `proof-postdrift-shell.log:26` (`runner_shell_exit:0`) is `tee`'s
status from a piped invocation, evidencing nothing about the runner — must
never be cited as guard proof. `RUNNER_EXIT:3` (:43) is a real observed digit
from a second unpiped invocation, but that rerun overwrote `proof-postdrift.log`,
so v1 has no single unbroken argv→transcript→exit capture. My resolution cited
"exit 3" from this packet without flagging the overwrite; that citation is
hereby narrowed to "observed digit inside a reconstructed narrative," not a
numeric proof. The author's `evidence-qualification.md` §§1–2 disclosure is
accurate against the preserved bytes, including the first-transcript loss
despite the preserve instruction — recorded as a transcript deviation, not
excused.

## 2. v2 numeric proof: CONFIRMED (direct capture)

`proof-postdrift-v2/prove_postdrift.py` (subprocess argv, `.returncode`
recorded, no shell pipe in capture path; exclusive `open(...,'x')`) on a NEW
disposable (`...-v2-20261009T025927Z`, old one never reused): `capture.log:61`
`returncode=3`, all CHECKs PASS (env-absent, candidate pre clean 3-path overlay,
disposable HEAD/tree/status/inert/no-alternates/no-multilink/zero shared
inodes, runner-log `unittest_exit:0` + `OUTCOME=POSTGUARD_FAILED`, canary in
disposable only, candidate post identical/canary-free, disposable removed).
Runner pins are the unmodified final hashes; child is one fast pure test, the
31-method suite untouched. v2 closes the v1 numeric gap. Residual: the script's
own process exit is attested by the qualification doc, not re-executed here.

## 3. Claim scopes (accepted bounds, no promotion)

- Alias sentinel `'{"malformed": true}'` is VALID JSON, not an Evidence card;
  test force is pre-validator directory-alias refusal + never-ran/never-read
  spies (byte-identical after), not a parser trap.
- Derived style mutation is schema-const evidence only (no renderer/style
  engine); `_kicker` ordinal/total/suffix are helper unit checks, with
  loader-level kicker order covered by the two-package chain test.
- Multi-DID: non-constructibility is limited to this fixture-producer family
  (per-task single-DID cards). The `multiple accepted Evidence cards` code guard
  has NO executed real-card test in the 31-run — code-present only, not proved;
  loader evidence is the duplicate-shape checks plus the ambiguity /
  equal-timestamp resolver pair.

## 4. Verdict

Source BOUNDED_PASS unchanged. Final overlay hashes immutable, 31-run
unaffected. Only additions: qualification doc + v2 proof + this supplement.
