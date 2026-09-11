"""Experimental Card-only byte binding, layered on phase5 structural hardening.
Not a production patch: package/task/Raw closure and publication atomicity remain outside scope.
"""
from phase5_stage_probe import harden

def bind_card_bytes(source):
    source = harden(source)
    source = source.replace('def _load_factual_card(path: Path) -> dict[str, Any]:',
                            'def _decode_factual_card(data: bytes) -> dict[str, Any]:')
    source = source.replace('json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)',
                            'json.loads(data.decode("utf-8"), object_pairs_hook=unique_object)')
    anchor = 'def validate_evidence_card(\n'
    source = source.replace(anchor, 'def _load_factual_card(path: Path) -> dict[str, Any]:\n'
        '    return _decode_factual_card(path.read_bytes())\n\n\n' + anchor)
    start = source.index('def accept_evidence_results(')
    end = source.index('\ndef validate_evidence_acceptance(', start)
    part = source[start:end]
    part = part.replace('    entries: list[dict[str, Any]] = []',
        '    entries: list[dict[str, Any]] = []\n    captured_cards: dict[str, bytes] = {}')
    part = part.replace('        card = _load_factual_card(result_path)',
        '        card_bytes = result_path.read_bytes()\n'
        '        card = _decode_factual_card(card_bytes)\n'
        '        captured_cards[result_path.name] = card_bytes')
    part = part.replace('"sha256": core.sha256_file(result_path)',
        '"sha256": hashlib.sha256(card_bytes).hexdigest()')
    part = part.replace('        shutil.copy2(files[basename], run_dir / "results" / basename)',
        '        (run_dir / "results" / basename).write_bytes(captured_cards[basename])')
    source = source[:start] + part + source[end:]
    old = '        if row.get("filename") != name or core.sha256_file(result_files[name]) != row.get("sha256"):'
    assert source.count(old) == 1
    source = source.replace(old, '        card_bytes = result_files[name].read_bytes()\n'
        '        if row.get("filename") != name or hashlib.sha256(card_bytes).hexdigest() != row.get("sha256"):')
    source = source.replace('        card = _load_factual_card(result_files[name])',
        '        card = _decode_factual_card(card_bytes)')
    return source
