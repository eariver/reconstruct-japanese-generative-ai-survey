# r2 application test-contract update rationale

The fixed-base full Core diagnostic exposed one test that still required copied
live candidate and edition status in the authority index. That requirement is
incompatible with r2's reviewed responsibility split.

The proposed test-only update preserves WU-011's immutable Repair Set/Finding
checks, the historical worklog and closure checks, the generic release and Core
scope boundary, the seven-point audit requirements, and the retired pilot CLI
check. It replaces exact live-status assertions with checks that the authority
document:

- identifies itself as an operating-rule index;
- says current main, maintenance, lifecycle and acceptance status live elsewhere;
- keeps unknown evidence unknown;
- links the fixed prior authority as immutable historical context;
- retains generic released-edition immutability and production-scope rules; and
- no longer copies the three former W33/W34/SP001-SP003 live-status sentences.

No r2 candidate code or document byte is changed by this proposal.
