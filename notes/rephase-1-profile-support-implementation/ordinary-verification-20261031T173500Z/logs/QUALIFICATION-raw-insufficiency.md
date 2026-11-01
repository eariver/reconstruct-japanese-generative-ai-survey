# Qualification — raw-evidence insufficiency (append-only, preserves originals)

2026-10-31. Per independent §9.1/9.3/9.5(1): the three `.../173500Z/logs/*-stdout-stderr-exit.txt`
DATA files are 7–8-line hand summaries (command/workdir/env/PID/EXIT + one-line scope note),
NOT captured verbose `unittest -v` streams. No per-test verbose output, no tracebacks,
no before/after inventory hashes, no command stdout were archived there.

Do NOT reconstruct stdout or claim raw 26/26 preserved from those summaries.
Originals preserved as history; this qualification corrects any approximate count
binding. Final verification will be run by a separate evidence worker with direct
subprocess capture after tests are frozen. No broad re-run here beyond the new
focused DERIVED positives/negatives with genuine raw capture (see new logs dir).
