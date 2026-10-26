#!/usr/bin/env python3
"""Warmup/hash/import verify + expected recipe TeX local Python/JSON/PDF helpers.
Fresh Python process, fixture-first imports, no stale code. Writes raw JSON.
"""
import sys, hashlib, pathlib, json, subprocess, os
fix = pathlib.Path(sys.argv[1])
evid = pathlib.Path(sys.argv[2])
evid.mkdir(parents=True, exist_ok=True)
out = {}
out["python_version"] = sys.version
out["fix"] = str(fix)
out["head"] = subprocess.run(["git","--no-optional-locks","rev-parse","HEAD"],cwd=str(fix),capture_output=True,text=True).stdout.strip()
out["tree"] = subprocess.run(["git","--no-optional-locks","rev-parse","HEAD^{tree}"],cwd=str(fix),capture_output=True,text=True).stdout.strip()
# pinned hashes
for rel, exp in [
 ("scripts/survey_versioned_renewal_v2.py","9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152"),
 ("scripts/survey_versioned_renewal_history_v2.py","70bcdbb8602dd012cd300eba3e9972735ea5dd29e52cfb76e59cee6605230467"),
 ("scripts/survey_versioned_renewal_source_v2.py","20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306"),
 ("scripts/survey_publication_v2.py","90d90738dc2fc0c57a22f9656659a6e3665d262919b17f259811d035dac3d8c6"),
 ("scripts/survey_reader_publication_v2.py","098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c"),
]:
  data=(fix/rel).read_bytes()
  got=hashlib.sha256(data).hexdigest()
  out[rel]={"bytes":len(data),"sha256":got,"match":got==exp}
# fixture-first import root verify
sys.path.insert(0, str(fix))
from scripts import survey_versioned_renewal_v2 as high
from scripts import survey_versioned_renewal_history_v2 as hist
from scripts import survey_versioned_renewal_source_v2 as src
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
out["import_root_high"]=str(pathlib.Path(high.__file__).resolve())
out["import_root_ok"]=str(pathlib.Path(high.__file__).resolve()).startswith(str(fix.resolve()))
out["high_lines"]=len((fix/"scripts/survey_versioned_renewal_v2.py").read_text().splitlines())
# recipe
recipe=(fix/".latexmkrc").read_bytes().decode()
out["recipe_markers_present"]={m:(m in recipe) for m in ["$pdf_mode","$lualatex","$biber","$max_repeat"]}
# TeX local
texbin=pathlib.Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux")
out["texbin_exists"]=texbin.is_dir()
for exe in ["lualatex","biber","latexmk"]:
  p=texbin/exe
  out[f"tex_{exe}"]={"exists":p.exists(),"is_file":p.is_file() if p.exists() else False}
  if p.exists():
    try:
      cp=subprocess.run([str(p),"--version"],capture_output=True,text=True,timeout=30,env={"PATH":str(texbin)+":/usr/bin:/bin"})
      out[f"tex_{exe}"]["rc"]=cp.returncode
      out[f"tex_{exe}"]["stdout_head"]=(cp.stdout or "")[:500]
    except Exception as e:
      out[f"tex_{exe}"]["error"]=str(e)[:500]
# jsonschema + pypdf helpers
try:
  import jsonschema
  out["jsonschema"]=getattr(jsonschema,"__version__","unknown")
except Exception as e:
  out["jsonschema_error"]=str(e)[:500]
try:
  from pypdf import PdfReader
  out["pypdf_ok"]=True
  # old E PDF pages
  pdf=fix/"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/publication/build/main.pdf"
  out["old_pdf"]={"exists":pdf.exists(),"bytes":pdf.stat().st_size if pdf.exists() else 0,"pages":len(PdfReader(str(pdf)).pages) if pdf.exists() else None}
except Exception as e:
  out["pypdf_error"]=str(e)[:1000]
# State r1
st=json.loads((fix/"sources/2026-W37/production-state.json").read_bytes())
out["state"]={"lifecycle":st.get("lifecycle_state"),"next_action":st.get("next_action"),"provenance":st.get("publication_revalidation_provenance")}
# old r1 record SHA
r1=json.loads((fix/"sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json").read_bytes())
out["r1"]={"kind":r1.get("kind"),"set_sha_preview":str(r1.get("set_ref"))[:200]}
(evid/"warmup.json").write_bytes(json.dumps(out,indent=1).encode())
print(json.dumps(out,indent=1))
