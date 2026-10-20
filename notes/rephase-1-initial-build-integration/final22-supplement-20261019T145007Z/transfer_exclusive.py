#!/usr/bin/env python3
"""Evidence-only exclusive transfer helper (NOT a shipping writer, NOT a framework).

Behavioral delta vs the old check-then-`shutil.copyfile` witness code: creation uses
`os.open(..., O_CREAT | O_EXCL | O_WRONLY | O_NOFOLLOW)` so an existing destination
refuses with `FileExistsError` atomically at create time (no takeover, no TOCTOU
between a preflight `exists()` check and the write). Old code only checked
`exists()`/`lexists()` first and then copied — never exclusive.

Contract (exactly 3 files, in order `main.pdf`, `main.log`, `main.pdf.sha256`):
- `stage_dir` / `survey_dir` must be real directories (not symlinks); every path
  component prefix must contain no symlink (realpath == abspath check + prefix
  walk) — parent/root no-alias checks. The survey (destination) dir must resolve
  inside the repository root; the staging dir is a disposable build dir outside
  fixture Git by design (noalias-checked, not repo-contained).
- `expected`: {name: sha256} for the 3 files (pins of the exact source bytes).
- Digest convention enforced BEFORE any write: `expected["main.pdf.sha256"]` must
  equal sha256 of (`expected["main.pdf"] + "  main.pdf\\n"` textual digest bytes);
  i.e. the digest file's own pinned bytes must spell `<pdf-sha>  main.pdf`.
- Per-file: source opened `rb` FIRST (an unreadable source leaves no destination
  trace); destination created with `O_CREAT|O_EXCL|O_WRONLY|O_NOFOLLOW` mode
  `0o644` (existing destination refuses atomically — no takeover); streamed
  64 KiB chunks with short-write detection (`os.write` returning short →
  `IOError("short write ...")`); `os.fsync`; `os.close` inside try/finally with
  close-error propagation.
- Postread: every destination sha must equal `expected`; digest line re-checked.
- On ANY exception: optional `on_error(exc, written, survey_dir)` failure callback
  fires first (records partial set), then the exception propagates. Partials are
  NEVER cleaned up by the helper (preserved for inspection).
- Faults are environmental (unreadable source, missing input, pre-existing
  destination) or injected `OSError` via the `on_error`-visible path — never a
  validator stub, never mocked Git/authority.
"""
from __future__ import annotations
import hashlib
import os
from pathlib import Path

ORDER = ("main.pdf", "main.log", "main.pdf.sha256")
DIGEST_LINE = "  main.pdf\n"


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _no_alias(path: Path, label: str) -> Path:
    if os.path.islink(path):
        raise ValueError(f"transfer refused: {label} is a symlink: {path}")
    if os.path.realpath(path) != os.path.abspath(path):
        raise ValueError(f"transfer refused: {label} path contains alias: {path}")
    return path


def transfer_exact(
    repo_root: Path,
    stage_dir: Path,
    survey_dir: Path,
    expected: dict[str, str],
    *,
    on_error=None,
) -> dict[str, str]:
    """Exclusively install exactly the 3 allowed outputs. See module docstring."""
    if set(expected) != set(ORDER):
        raise ValueError("transfer refused: expected pins must cover exactly main.pdf/main.log/main.pdf.sha256")
    repo_root = Path(repo_root).resolve()
    stage_dir = _no_alias(Path(stage_dir), "staging directory")
    survey_dir = _no_alias(Path(survey_dir), "survey directory")
    for label, path in (("staging directory", stage_dir), ("survey directory", survey_dir)):
        if not path.is_dir() or os.path.islink(path):
            raise ValueError(f"transfer refused: {label} is not a real directory: {path}")
        # prefix no-alias walk: no component of the absolute path may be a symlink
        for parent in [path.resolve(), *path.resolve().parents]:
            if str(parent) == parent.anchor:
                break
            if os.path.islink(parent):
                raise ValueError(f"transfer refused: {label} prefix contains symlink: {parent}")
    # repository containment applies to the DESTINATION (survey dir) only: the
    # staging dir is a disposable build dir outside fixture Git by design.
    try:
        survey_dir.resolve().relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"transfer refused: survey directory escapes repository: {survey_dir}") from exc
    want_digest = (expected["main.pdf"] + DIGEST_LINE).encode("utf-8")
    if hashlib.sha256(want_digest).hexdigest() != expected["main.pdf.sha256"]:
        raise ValueError("transfer refused: digest pin does not spell '<pdf-sha>  main.pdf'")
    written: list[str] = []
    try:
        for name in ORDER:
            src = stage_dir / name
            if src.is_symlink() or not src.is_file():
                raise ValueError(f"transfer refused: no built {name} in staging dir")
            dst = survey_dir / name
            with open(src, "rb") as fsrc:
                fd = os.open(dst, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o644)
                try:
                    while True:
                        chunk = fsrc.read(65536)
                        if not chunk:
                            break
                        view = memoryview(chunk)
                        while view:
                            n = os.write(fd, view)
                            if n == 0:
                                raise IOError(f"transfer short write: {name}")
                            view = view[n:]
                    os.fsync(fd)
                finally:
                    try:
                        os.close(fd)
                    except OSError as exc:
                        raise IOError(f"transfer close failed (output may be partial): {name}") from exc
            written.append(name)
        post = {n: _sha256_file(survey_dir / n) for n in ORDER}
        if post != dict(expected):
            raise ValueError(f"transfer postread mismatch: {post} vs {expected}")
        digest_line = (survey_dir / "main.pdf.sha256").read_text(encoding="utf-8")
        if digest_line != expected["main.pdf"] + DIGEST_LINE:
            raise ValueError("transfer refused: digest line not conventional '<sha>  main.pdf'")
        return post
    except Exception as exc:
        if on_error is not None:
            on_error(exc, list(written), survey_dir)
        raise
