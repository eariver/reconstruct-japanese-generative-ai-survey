"""Linux-only experimental working-set / no-replace publication boundary.
Layers on phase7 Card byte binding. No Raw cache; no whole-repository snapshot.
"""
from phase7_byte_binding import bind_card_bytes

WRAPPER = '''
def _publish_evidence_directory(source: Path, target: Path) -> None:
    # Experimental Linux primitive: never replace even an existing empty directory.
    import ctypes
    import errno
    import sys
    if sys.platform != "linux":
        raise OSError(errno.ENOTSUP, "Evidence staged publication requires Linux renameat2")
    libc = ctypes.CDLL(None, use_errno=True)
    rename = getattr(libc, "renameat2", None)
    if rename is None:
        raise OSError(errno.ENOTSUP, "renameat2 unavailable")
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(-100, os.fsencode(source), -100, os.fsencode(target), 1) != 0:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code), str(target))


def accept_evidence_results(
    repo_root: Path, package_path: Path, results_dir: Path,
    accepted_root: Path, implementation_sha: str,
) -> Path:
    import tempfile
    # Reject known symlink components; this is not protection against a hostile
    # same-user process replacing directories after this check.
    def regular(path: Path) -> bytes:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Evidence input must be a regular non-symlink file: {path}")
        return path.read_bytes()
    if package_path.parent.is_symlink() or results_dir.is_symlink():
        raise ValueError("Evidence input directory must not be a symlink")
    package_bytes = regular(package_path)
    package = json.loads(package_bytes.decode("utf-8"))
    metas = package.get("tasks")
    if not isinstance(metas, list):
        raise ValueError("Evidence working set requires tasks")
    names = []
    for meta in metas:
        rel = Path(meta["path"])
        if len(rel.parts) != 2 or rel.parts[0] != "tasks" or rel.name != task_filename(meta["evidence_task_id"]):
            raise ValueError("Evidence working-set task path invalid")
        names.append(rel.name)
    if len(names) != len(set(names)):
        raise ValueError("Evidence working-set task paths duplicated")
    task_dir = package_path.parent / "tasks"
    if task_dir.is_symlink():
        raise ValueError("Evidence task directory must not be a symlink")
    tasks = _exact_regular_files(task_dir, set(names), "Evidence input task set")
    cards = _exact_regular_files(results_dir, set(names), "Evidence input result set")
    destination = Path(os.path.abspath(accepted_root))
    repository = Path(os.path.abspath(repo_root))
    if not destination.is_relative_to(repository):
        raise ValueError("Evidence accepted root outside repository")
    for parent in [destination, *destination.parents]:
        if parent.is_symlink():
            raise ValueError("Evidence accepted destination contains symlink")
        if parent == repository:
            break
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".evidence-working-", dir=destination.parent) as td:
        working = Path(td)
        captured = working / "input"
        (captured / "tasks").mkdir(parents=True)
        (working / "cards").mkdir()
        (captured / "package.json").write_bytes(package_bytes)
        for meta, name in zip(metas, names):
            task_bytes = regular(tasks[name])
            if hashlib.sha256(task_bytes).hexdigest() != meta["sha256"]:
                raise ValueError("Evidence captured Task SHA drift")
            (captured / "tasks" / name).write_bytes(task_bytes)
            (working / "cards" / name).write_bytes(regular(cards[name]))
        staged = _accept_evidence_results_from_working_set(
            repo_root, captured / "package.json", working / "cards",
            working / "accepted", implementation_sha)
        # Verify the completed output, including live upstream basis, before publication.
        validate_evidence_acceptance(repo_root, staged, implementation_sha)
        target = destination / staged.parent.name
        existing = target / "evidence-accepted.json"
        if target.exists() or target.is_symlink():
            if target.is_symlink() or not existing.is_file():
                raise ValueError("incomplete or linked existing Evidence run")
            validate_evidence_acceptance(repo_root, existing, implementation_sha)
            return existing
        destination.mkdir(parents=True, exist_ok=True)
        try:
            _publish_evidence_directory(staged.parent, target)
        except FileExistsError:
            if target.is_symlink() or not existing.is_file():
                raise ValueError("conflicting Evidence run appeared during publication")
            validate_evidence_acceptance(repo_root, existing, implementation_sha)
        return existing

'''

def staged_acceptance(source):
    source = bind_card_bytes(source)
    anchor = 'def accept_evidence_results(\n'
    assert source.count(anchor) == 1
    source = source.replace(anchor, 'def _accept_evidence_results_from_working_set(\n')
    return source + WRAPPER
