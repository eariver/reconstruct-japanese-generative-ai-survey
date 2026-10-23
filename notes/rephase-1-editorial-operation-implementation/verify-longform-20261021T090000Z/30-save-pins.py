#!/usr/bin/env python3
"""Save actual PDFs/extracted text/page PNG source pins for later independent review (no approval)."""
from __future__ import annotations
import hashlib
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
FIX = Path(os.environ.get("SMOKE_FIX_ROOT", "/tmp/opencode/jgas-editorial-longform-20261021T091000Z/candidate-partial-b40de60"))
OUT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-editorial-operation-implementation/verify-longform-20261021T090000Z/pins")
sys.path.insert(0, str(FIX))
def main() -> int:
    from pypdf import PdfReader
    OUT.mkdir(parents=True, exist_ok=True)
    # First activation PDF + second? Only first exists (second failed before build)
    pdfs = sorted(FIX.rglob("editorial-corrections/*/publication/build/main.pdf"))
    print(f"PDFS={len(pdfs)}", flush=True)
    for pdf in pdfs:
        rel = pdf.relative_to(FIX)
        data = pdf.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        print(f"PIN_PDF {rel} sha={sha} bytes={len(data)} pages={len(PdfReader(str(pdf)).pages)}", flush=True)
        # Extract text
        reader = PdfReader(str(pdf))
        texts = []
        for i, page in enumerate(reader.pages):
            t = page.extract_text() or ""
            texts.append(f"--- page {i+1} chars={len(t)} ---\n{t}")
            # PNG via pymupdf (first 2 pages only to limit size, but save all? save all as PNG)
        joined = "\n".join(texts)
        txt_path = OUT / (f"{pdf.parent.parent.name}-{pdf.parent.name}-extracted.txt")
        txt_path.write_text(joined, encoding="utf-8")
        print(f"PIN_TEXT {txt_path.name} chars={len(joined)} sha={hashlib.sha256(joined.encode()).hexdigest()[:16]}", flush=True)
        # PNGs via pymupdf
        try:
            import fitz
            doc = fitz.open(str(pdf))
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=120)
                png_path = OUT / (f"{pdf.parent.parent.name}-{pdf.parent.name}-p{i+1}.png")
                pix.save(str(png_path))
                print(f"PIN_PNG {png_path.name} bytes={png_path.stat().st_size} sha={hashlib.sha256(png_path.read_bytes()).hexdigest()[:16]}", flush=True)
            doc.close()
        except Exception as exc:
            print(f"PNG_WARN {exc}", flush=True)
    # Also save old canonical + first set pins
    import json
    from scripts import survey_production_v2 as core
    sys.path.insert(0, str(FIX))
    # Save marker + state pointer
    markers = list(FIX.rglob("activation-marker.json"))
    print(f"MARKERS={markers}", flush=True)
    for m in markers:
        print(f"MARKER {m.relative_to(FIX)} {hashlib.sha256(m.read_bytes()).hexdigest()[:16]}", flush=True)
    print("PINS_OK", flush=True)
    return 0
if __name__ == "__main__":
    sys.exit(main())
