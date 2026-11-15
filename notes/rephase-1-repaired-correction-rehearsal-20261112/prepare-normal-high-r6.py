#!/usr/bin/env python3
"""Thin order-preserving HIGH prepare r6 — W34-r2 reuse + SP-r1 fresh (r7 pins), check-only supported."""
import argparse, copy, hashlib, json, os, re, stat, subprocess, sys, time, traceback
from pathlib import Path
EXP_HEAD="cc1c7fd1cf979e71fda4ae2164828b37bc1b2325"
EXP_TREE="ed2dc4ddd4a9486ccc9d0944bbd48653199b2485"
EXP_INIT480="480823560c0c26ed2e5baa18e0e79a22b2839a27"
EXP_MANIFEST_SHA="a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c"
EXP_MANIFEST_BYTES=202833
EXP_FILES_LEN=773
REVISION_RE=re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
HEX40=re.compile(r"^[0-9a-f]{40}$")
SAFEPATH=re.compile(r"^(?![/\\])(?!.*\.\.)[^\\]+$")
ALLOWED_ENV={"PATH","HOME","LANG","LC_ALL","LC_MESSAGES","TZ","PYTHONDONTWRITEBYTECODE","PYTHONPATH","PWD","TMPDIR","USER","LOGNAME","SHELL"}
PACKET=Path("notes/rephase-1-repaired-correction-rehearsal-20261112")
MANIFEST=Path("notes/rephase-1-supplement-carry-repair-20261106/source-packaging/final-20261107T040903Z/complete-supplement-carry-manifest.json")
CONFIG_R6=PACKET/"prepare-normal-high-config-r6.json"
TOOL_RELS=["scripts/survey_research_authority_v2.py","scripts/survey_prearchitecture_acceptance_v2.py","schemas/dm022-revision-request-v2.schema.json","schemas/dm022-revision-manifest-v2.schema.json","schemas/dm022-revision-proof-v2.schema.json","schemas/dm022-preadoption-report-v2.schema.json","schemas/dm022-supersession-checkpoint-v2.schema.json"]
SEVEN_SLOTS=("candidate-matrix-v2.json","candidate-selection-v2.json","architecture-v2.json","architecture-review-summary-v2.json","architecture-review-attention-v2.json","orchestration/v2/interactive/selection-architecture-input.json","orchestration/v2/interactive/selection-architecture-audit.json")
GUARD_REL="orchestration/v2/acceptance-revision.guard.json"
def sha256_file(p:Path)->str:
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def fail(m:str):
 print(f"REFUSE: {m}",file=sys.stderr);raise SystemExit(2)
def load_strict(p:Path):
 raw=p.read_bytes()
 def hook(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise ValueError(f"dup {k!r} in {p}")
   d[k]=v
  return d
 try:doc=json.loads(raw.decode(),object_pairs_hook=hook)
 except Exception as e:fail(f"{p} strict: {e}")
 return doc,raw,hashlib.sha256(raw).hexdigest(),len(raw)
def check_manifest_all773(repo:Path):
 if hashlib.sha256(MANIFEST.read_bytes()).hexdigest()!=EXP_MANIFEST_SHA:fail("manifest != a7e4")
 m=json.loads(MANIFEST.read_text());files=m.get("files")
 if not isinstance(files,dict) or len(files)!=EXP_FILES_LEN or m.get("intended_files")!=EXP_FILES_LEN:fail("manifest 773 shape")
 for rel,meta in files.items():
  fp=repo/rel;st=os.lstat(fp)
  if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):fail(f"773 type {rel}")
  if sha256_file(fp)!=meta["sha256"] or st.st_size!=meta["bytes"] or oct(stat.S_IMODE(st.st_mode))!=meta["physical_mode"]:fail(f"773 drift {rel}")
  if meta.get("kind")!="file":fail(f"773 kind {rel}")
 for rel in TOOL_RELS:
  if rel not in files:fail(f"tool {rel} not in manifest")
 print("manifest ALL773 OK + tools derived")
def inventory(repo:Path,issue:str,allow_exact:set,r1_req:str="",r1_root:str="",ancestor_exact:set=None):
 if ancestor_exact is None:ancestor_exact=set()
 m=json.loads(MANIFEST.read_text())["files"];inv_f={}
 for rel in m:
  fp=repo/rel;st=os.lstat(fp)
  if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):fail(f"inv type {rel}")
  inv_f[rel]=[sha256_file(fp),st.st_size,oct(stat.S_IMODE(st.st_mode))]
 src=repo/f"sources/{issue}";extra={};dirs={}
 for p in sorted(src.rglob("*")):
  try:st=os.lstat(p)
  except FileNotFoundError:continue
  s=p.relative_to(repo).as_posix()
  # kind first (inspect actual path kind before policy test)
  if stat.S_ISLNK(st.st_mode):fail(f"inv symlink {s}")
  is_dir=stat.S_ISDIR(st.st_mode);is_reg=stat.S_ISREG(st.st_mode)
  if not is_dir and not is_reg:fail(f"inv special {s}")
  if "/research/v2/acceptance-revision" in s:
   if s in allow_exact or s in ancestor_exact or (r1_req and s==r1_req) or (r1_root and (s==r1_root or s.startswith(r1_root+"/"))):pass
   else:fail(f"future R non-R1 research: {s}")
  if is_dir:dirs[s]=oct(stat.S_IMODE(st.st_mode))
  elif is_reg:
   if s not in inv_f:extra[s]=[sha256_file(p),st.st_size,oct(stat.S_IMODE(st.st_mode))]
 try:os.lstat(src/GUARD_REL);fail("guard present")
 except FileNotFoundError:pass
 for slot in SEVEN_SLOTS:
  try:os.lstat(src/slot);fail(f"slot present {slot}")
  except FileNotFoundError:pass
 return {"files773":inv_f,"extra":extra,"dirs":dirs,"allow_exact":sorted(allow_exact)}
class Tee:
 def __init__(self,*fs):self.files=fs
 def write(self,d):
  for f in self.files:f.write(d)
 def flush(self):
  for f in self.files:f.flush()
def resolve_in(repo:Path,rel:str)->Path:
 if not SAFEPATH.fullmatch(rel) or rel.startswith("/") or ".." in Path(rel).parts:fail(f"unsafe {rel!r}")
 ap=repo/rel
 try:ap.resolve().relative_to(repo.resolve())
 except Exception:fail(f"escapes repo {rel!r}")
 return ap
def main():
 ap=argparse.ArgumentParser(description="Thin order-preserving HIGH prepare r6 (W34-r2 reuse, SP-r1 fresh).")
 ap.add_argument("--issue",required=True,choices=["2026-W34","SP-efficient-llm-2026"])
 ap.add_argument("--repo-root",required=True)
 ap.add_argument("--revision-id",required=True)
 ap.add_argument("--config",default=str(CONFIG_R6))
 ap.add_argument("--outdir",required=True)
 ap.add_argument("--check-only",action="store_true",help="read-only preflight then early return before ANY writes")
 a=ap.parse_args();issue,rev=a.issue,a.revision_id
 if not Path("notes/rephase-1-repaired-correction-rehearsal-20261112").exists():fail("must run from workspace root")
 repo=Path(a.repo_root)
 if not repo.is_absolute():fail("repo-root must be ABSOLUTE")
 repo=repo.resolve()
 if not REVISION_RE.fullmatch(rev) or any(c.isupper() for c in rev):fail(f"revision {rev!r}")
 cfg0,_,_,_=load_strict(Path(a.config))
 if cfg0["issues"][issue]["revision_id"]!=rev:fail("--revision-id != cfg spec")
 out=Path(a.outdir)
 try:out.mkdir(parents=True,exist_ok=False)
 except FileExistsError:fail(f"outdir exists {out}")
 stdout_f=open(out/"stdout.txt","w");stderr_f=open(out/"stderr.txt","w")
 o_out,o_err=sys.stdout,sys.stderr;sys.stdout,sys.stderr=Tee(o_out,stdout_f),Tee(o_err,stderr_f)
 def w(n:str,d:str):(out/n).write_text(d)
 w("argv.txt"," ".join(sys.argv));w("env-whitelist.txt","\n".join(f"{k}={os.environ.get(k,'')}" for k in sorted(ALLOWED_ENV)));w("pid.txt",str(os.getpid()));w("wall-start.txt",time.strftime("%Y%m%dT%H%M%SZ",time.gmtime()));w("cwd.txt",os.getcwd())
 exit_code=2
 try:
  check_manifest_all773(repo)
  env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
  head=subprocess.run(["git","rev-parse","HEAD"],cwd=repo,check=True,capture_output=True,text=True,env=env).stdout.strip()
  tree=subprocess.run(["git","rev-parse","HEAD^{tree}"],cwd=repo,check=True,capture_output=True,text=True,env=env).stdout.strip()
  if head!=EXP_HEAD or tree!=EXP_TREE:fail("HEAD/tree != cc1c/ed2dc4")
  cfg,_,cfg_h,cfg_n=load_strict(Path(a.config));w("config-pinned.txt",f"{a.config} {cfg_h} {cfg_n}\n(no post reseal)")
  spec=cfg["issues"][issue]
  if spec["revision_id"]!=rev:fail("revision != spec")
  # prechecks per mode (no writes yet)
  if issue=="2026-W34":
   if rev!="w34-repaired-20261112-r2":fail("W34 requires r2")
   r1_req="sources/2026-W34/research/v2/acceptance-revision-inputs/w34-repaired-20261112-r1.json";r1_root="sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r1"
   exp_r1={"sources/2026-W34/research/v2/acceptance-revision-inputs/w34-repaired-20261112-r1.json":"057e186fbda8df8f58fd400def30cf5a6a80ba1d310f161f1854882619f1e5a3","sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r1/revision-manifest.json":"54de43edc49a24e2fd8ffaf02144a83c5812a2c59290eb1d3a914709e8583da2"}
   for p in [r1_req,r1_root+"/revision-manifest.json"]:
    if sha256_file(repo/p)!=exp_r1[p]:fail(f"R1 pinned drift {p}")
   for r in spec["reuse_raw"]:
    fp=repo/r["path"]
    if fp.is_symlink() or not fp.is_file():fail(f"reuse Raw type {r['path']}")
    if sha256_file(fp)!=r["sha256"] or fp.stat().st_size!=r["bytes"]:fail(f"reuse Raw drift {r['path']}")
    if oct(stat.S_IMODE(fp.stat().st_mode))!="0o664":fail(f"reuse Raw mode {r['path']}")
   print("W34 r2 reuse verified")
   allow_exact={r1_req,r1_root+"/revision-manifest.json"}|{r["path"] for r in spec["reuse_raw"]}
   ancestor_exact={"sources/2026-W34/research","sources/2026-W34/research/v2","sources/2026-W34/research/v2/acceptance-revision-inputs","sources/2026-W34/research/v2/acceptance-revisions",r1_root}
   r1_req_v,r1_root_v=r1_req,r1_root
  else:
   if rev!="sp-repaired-20261112-r1":fail("SP requires r1")
   for key in ("records_r7","routing_r7","staging_r7"):
    pin=spec.get(key)
    if not pin or pin.get("forthcoming"):fail(f"SP {key} forthcoming (must bind actual r7, no hold)")
    if sha256_file(Path(pin["path"]))!=pin["sha256"] or Path(pin["path"]).stat().st_size!=pin["bytes"]:fail(f"SP {key} drift")
   for p in [spec["request_rel"],spec["rev_root_rel"]+"/revision-manifest.json"]+[r["future_raw_path"] for r in spec["new_raw"]]:
    if (repo/p).exists() or (repo/p).is_symlink():fail(f"SP must be new absent {p}")
   s142=spec["true_s142"]
   for src in s142["sources"]:
    pp=Path(src["path"])
    if pp.is_symlink() or not pp.is_file():fail(f"S142 type {src['path']}")
    if sha256_file(pp)!=s142["sha256"] or pp.stat().st_size!=s142["bytes"]:fail(f"S142 drift {src['path']}")
   if s142["sha256"]!="f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662":fail("S142 must be true ...18672662")
   print("SP r7 + true S142 OK")
   allow_exact=set();ancestor_exact=set();r1_req_v,r1_root_v="",""
  entry=inventory(repo,issue,allow_exact,r1_req_v,r1_root_v,ancestor_exact);w("entry-inventory.json",json.dumps(entry,indent=2,sort_keys=True))
  st,_,_,_=load_strict(repo/f"sources/{issue}/production-state.json")
  if st["lifecycle_state"]!="EVIDENCE_REVIEWED" or st["implementation"]["repository_commit_sha"]!=EXP_INIT480:fail("State shape")
  if st["human_gates"]!={"architecture_review":"pending","publication_preview":"pending"} or st["human_gate_provenance"]!={"architecture_review":None,"publication_preview":None}:fail("Human shape")
  if st["exception_gate"]["status"]!="inactive":fail("guard shape")
  import sys as _s;_s.path.insert(0,str(repo.resolve()))
  try:
   from scripts import survey_production_v2 as core
   from scripts import survey_schema_v2 as gate
   from scripts import survey_evidence_v2 as ev
   from scripts import survey_prearchitecture_acceptance_v2 as high
   cfg_obj=core.load_json(repo/str(core.DEFAULT_CONFIG))
   live_contract,live_tools=high._contract_and_tools(repo,cfg_obj,st)
   m_all=json.loads(MANIFEST.read_text())["files"]
   for e in live_tools:
    meta=m_all.get(e["path"])
    if meta is None or e["sha256"]!=meta["sha256"]:fail(f"live tool {e['path']} != manifest")
   if set(e["path"] for e in live_tools)!=set(TOOL_RELS):fail("live tool set != 7")
   # actual patch keys (no guess)
   if issue=="2026-W34":patch,_,_,_=load_strict(Path(spec["patch"]["path"]));changed=patch.get("changed_record_ids");base_rel=spec["base_interactive"]["path"]
   else:patch,_,_,_=load_strict(Path(spec["records_r7"]["path"]));changed=patch.get("changed_ids");base_rel=spec["base_interactive"]["path"]
   if not isinstance(changed,list) or len(changed)!=4:fail("changed !=4")
   base,_,_,_=load_strict(repo/base_rel)
   if len(base["records"])!=(409 if issue=="2026-W34" else 160):fail("base count")
   runner=base["runner"]
   for k in ["provider","model","invocation","generated_at"]:
    if k not in runner:fail(f"runner missing {k}")
   by_base={r["discovery_id"]:r for r in base["records"]}
   if set(changed)-set(by_base):fail("changed not in base")
   full_map={}
   for r in base["records"]:
    did=r["discovery_id"]
    if did in set(changed):full_map[did]=copy.deepcopy([x for x in patch["new_records"] if x["discovery_id"]==did][0])
    else:full_map[did]=copy.deepcopy(r)
   full=[full_map[r["discovery_id"]] for r in base["records"]]
   for r in base["records"]:
    did=r["discovery_id"]
    if did not in set(changed):
     if list(full_map[did]["entity"].keys())!=list(r["entity"].keys()):fail(f"entity order {did}")
     if json.dumps(full_map[did],indent=2,ensure_ascii=False).encode()+b"\n"!=json.dumps(r,indent=2,ensure_ascii=False).encode()+b"\n":fail(f"unaffected serialized {did}")
   # REAL prospective unaffected cards with REAL task meta (no fake/dummy)
   pkg,_,_,_=load_strict((repo/base_rel).parent/"package.json")
   if len(pkg.get("tasks",[]))!=(409 if issue=="2026-W34" else 160):fail("package cardinality")
   tmap={}
   for t in pkg["tasks"]:
    if len(t.get("discovery_ids",[]))!=1:fail("package task shape")
    # actual JSON fields: evidence_task_id/path/sha256/discovery_ids (+supplement ids W34)
    for k in ["evidence_task_id","path","sha256","discovery_ids"]:
     if k not in t:fail(f"package task missing {k} actual {sorted(t.keys())}")
    if not HEX40.fullmatch(t["evidence_task_id"].split(":")[-1]) and len(t["evidence_task_id"])==0:fail("task id")
    tmap[t["discovery_ids"][0]]=t
   if set(tmap)!=set(by_base):fail("package IDs != base IDs")
   prof,_,_,_=load_strict(repo/f"sources/{issue}/production-profile.json")
   # nonDROP: affected must not be DROP via screening decisions
   scr_acc,_,_,_=load_strict(repo/spec["screening_ref"]["path"])
   dec={d["discovery_id"]:d.get("decision") for d in scr_acc.get("decisions",[]) if isinstance(d,dict)}
   for did in changed:
    if dec.get(did)=="DROP":fail(f"affected DROP {did}")
   # task-file verification_targets exact (non-empty exact, no guess)
   for r in [x for x in full if x["discovery_id"] in set(changed)]:
    did=r["discovery_id"];t=tmap[did];tf=(repo/base_rel).parent/t["path"]
    if tf.is_symlink() or not tf.is_file():fail(f"task file type {did}")
    if sha256_file(tf)!=t["sha256"]:fail(f"task file sha {did}")
    tdoc,_,_,_=load_strict(tf)
    # actual task fields
    for k in ["evidence_task_id","discovery_ids","source_records","verification_targets","screening_basis"]:
     if k not in tdoc:fail(f"task {did} missing {k} actual {sorted(tdoc.keys())}")
    exp_targets=tdoc.get("verification_targets")
    if not isinstance(exp_targets,list) or len(exp_targets)==0:fail(f"task {did} targets empty")
    if set(x.get("target") for x in r.get("verification",[]))!=set(exp_targets):fail(f"{did} targets != task exact")
   # effective R/E: screening package basis == disc + file sha/size; screening == pin == SCP
   scr_pkgs=list((repo/f"sources/{issue}/screening/v2/accepted").glob("*/package.json"))
   if len(scr_pkgs)!=1:fail("screening package !=1")
   scr_pkg,_,_,_=load_strict(scr_pkgs[0])
   if scr_pkg.get("basis",{}).get("discovery_path")!=spec["discovery_ref_effective"]["path"]:fail("effective != screening basis (W34 439 vs root 369)")
   if sha256_file(repo/spec["discovery_ref_effective"]["path"])!=spec["discovery_ref_effective"]["sha256"]:fail("effective DS drift")
   if sha256_file(repo/spec["screening_ref"]["path"])!=spec["screening_ref"]["sha256"]:fail("screening drift")
   # completeness 7-field + residual/closure + no-fake-SAT
   if issue=="2026-W34":comp,_,_,_=load_strict(repo/"sources/2026-W34/profile-completeness-v2.json");obligs,resid,clos=comp["obligations"],comp["residual_limitations"],comp["closure"]
   else:comp5,_,_,_=load_strict(Path(spec["completeness_r5"]["path"]));obligs,resid,clos=comp5["obligations"],comp5["residual_limitations"],comp5["closure"]
   if len(obligs)!=(3 if issue=="2026-W34" else 15):fail("obligations count")
   for o in obligs:
    for k in ["obligation_id","dimension","description","status","discovery_ids","evidence_task_ids","rationale"]:
     if k not in o:fail(f"obligation {o.get('obligation_id')} missing {k}")
   sats=[o["obligation_id"] for o in obligs if o["status"]=="SATISFIED"]
   if issue=="2026-W34" and set(sats)!={"weekly:carry-over"}:fail(f"W34 SAT {sats}")
   if issue!="2026-W34" and set(sats)!={"EFF-O01","EFF-O07"}:fail(f"SP SAT {sats}")
   # routing FullDID/safePath/pinned + UTF8 literal byte checks BEFORE writes
   if issue=="2026-W34":
    rout,_,_,_=load_strict(Path("notes/rephase-1-repaired-correction-rehearsal-20261112/w34-repaired-raw-routing-map.json"))
    entries=rout.get("entries")
    if not isinstance(entries,dict) or len(entries)!=4:fail("W34 routing entries")
    raw_jobs=[]
    for did,e in entries.items():
     for k in ["source_file","bytes","sha256","future_raw_path"]:
      if k not in e:fail(f"W34 routing {did} missing {k} actual {sorted(e.keys())}")
     fut=e["future_raw_path"]
     if did not in fut or "w34-event-arxiv-2608-" not in fut or not SAFEPATH.fullmatch(fut):fail(f"W34 FULLDID {did}")
     src=Path(e["source_file"])
     if src.is_symlink() or not src.is_file():fail(f"W34 src type {did}")
     try:src.resolve().relative_to(repo.resolve())
     except Exception:fail(f"W34 src escapes {did}")
     if sha256_file(src)!=e["sha256"] or src.stat().st_size!=e["bytes"]:fail(f"W34 pinned {did}")
     raw_jobs.append((did,src,e["sha256"],e["bytes"],fut))
   else:
    rout,_,_,_=load_strict(Path(spec["routing_r7"]["path"]))
    for k in ["u1","u2","u3","d142_summary_routing"]:
     if k not in rout:fail(f"SP routing missing {k} actual {sorted(rout.keys())}")
    intake=Path("notes/rephase-1-selection-architecture-20261105/intake-20261106T001808Z-jev-archive")
    mapping=[("u1","EFF-D070","u1.snapshot.decoded.html",253542,"14ae31184b253b736ff8be423fafbe5ff82d1f75cf66b600bad8b8c9152aa443"),("u2","EFF-D071","u2.snapshot.decoded.html",307198,"357708348b9884d004669d6df45100986676f5ab900a75e76304fb19cae05bf2"),("u3","EFF-D141","u3.snapshot.body.bin",350662,"97a5dd74ed1e9ba006d21759c14615a7c0a485c4db161dc00a2d0b1e4d651b69")]
    raw_jobs=[]
    for rk,did,fn,exp_len,exp_sha in mapping:
     fut=rout[rk].get("future_raw_path")
     if not isinstance(fut,str) or "EFF-D" not in fut or not SAFEPATH.fullmatch(fut):fail(f"SP {rk} FULLDID")
     src=intake/fn
     if src.is_symlink() or not src.is_file():fail(f"SP {rk} type")
     if sha256_file(src)!=exp_sha or src.stat().st_size!=exp_len:fail(f"SP {rk} pinned")
     raw_jobs.append((did,src,exp_sha,exp_len,fut))
    d142=rout["d142_summary_routing"]
    for k in ["existing_file","existing_sha256","existing_bytes","future_raw_path","first_claim_literal"]:
     if k not in d142:fail(f"SP d142 missing {k}")
    fut142=d142["future_raw_path"]
    if "EFF-D142" not in fut142 or not SAFEPATH.fullmatch(fut142):fail("SP D142 FULLDID")
    src142=Path(d142["existing_file"])
    if src142.is_symlink() or not src142.is_file():fail("SP D142 type")
    try:src142.resolve().relative_to(repo.resolve())
    except Exception:fail("SP D142 escapes")
    if sha256_file(src142)!=d142["existing_sha256"] or src142.stat().st_size!=d142["existing_bytes"]:fail("SP D142 pinned")
    raw_jobs.append(("EFF-D142",src142,d142["existing_sha256"],d142["existing_bytes"],fut142))
   for r in [x for x in full if x["discovery_id"] in set(changed)]:
    did=r["discovery_id"];first=(r.get("claims") or [{}])[0].get("text","")
    if not first:fail(f"{did} first empty")
    cand=[j for j in raw_jobs if j[0]==did]
    if len(cand)!=1:fail(f"{did} raw job")
    if first.encode("utf-8") not in cand[0][1].read_bytes():fail(f"{did} literal UTF8 byte NOT in retained")
   print(f"routing/literal UTF8 OK BEFORE writes")
   # prospective unaffected cards byte-eq with REAL meta (no fake)
   n_eq=0
   for r in base["records"]:
    did=r["discovery_id"]
    if did in set(changed):continue
    t=tmap[did];tf=(repo/base_rel).parent/t["path"]
    if sha256_file(tf)!=t["sha256"]:fail(f"task sha {did}")
    tdoc,_,_,_=load_strict(tf)
    # constructor args: repo_root/Path task:dict meta:dict{sha256,byte_count} package:dict record:dict runner:dict; return dict
    meta={"sha256":t["sha256"],"byte_count":tf.stat().st_size}
    card=ev.build_research_card_content(repo,tdoc,meta,pkg,copy.deepcopy(r),runner)
    if not isinstance(card,dict) or card.get("evidence_task_id")!=tdoc.get("evidence_task_id"):fail(f"card return {did}")
    old_raw=((repo/base_rel).parent/"results"/(t["path"].split("/")[-1])).read_bytes()
    if core.json_bytes(card)!=old_raw:fail(f"unaffected card byte {did}")
    n_eq+=1
   print(f"prospective unaffected cards byte-eq {n_eq}")
   w("prospective-byte-eq.txt",str(n_eq))
   # SP payload schema precheck before Raw (no FULL Raw validator claim before files)
   if issue!="2026-W34":
    f30,_,_,_=load_strict(Path(spec["supplement_full30_r4"]["path"]))
    if len(f30.get("sources",[]))!=30:fail("full30 !=30")
    gate.validate_instance(f30,repo/"schemas/evidence-authority-supplement-v2.schema.json",label="supplement planned")
    print("SP payload schema prechecked (FULL Raw validator only after files via HIGH)")
   if a.check_only:
    w("wall-end.txt",time.strftime("%Y%m%dT%H%M%SZ",time.gmtime()));w("exit.txt","0")
    print(f"CHECK-ONLY OK {issue} prospective {n_eq}")
    exit_code=0
    return
   # ---- writes start here (never in check-only) ----
   if issue=="2026-W34":
    req_rel=spec["request_rel"];rev_root=spec["rev_root_rel"]
    if (repo/req_rel).exists():fail("W34 request must be new")
    if (repo/rev_root).exists():fail("W34 R must be new")
    supp={"path":spec["supplement_manifest_explicit"]["path"],"sha256":spec["supplement_manifest_explicit"]["sha256"],"byte_count":spec["supplement_manifest_explicit"]["byte_count"]}
    chk=repo/supp["path"]
    if sha256_file(chk)!=supp["sha256"]:fail("W34 ce6f drift")
   else:
    for job in spec["new_raw"]:
     if "src" in job:src=Path(job["src"])
     elif "src_is_repo" in job:src=repo/job["src_is_repo"]
     else:fail("SP new_raw src")
     if src.is_symlink() or not src.is_file():fail(f"SP src type {job['future_raw_path']}")
     dst=resolve_in(repo,job["future_raw_path"])
     if dst.exists() or dst.is_symlink():fail(f"SP Raw new {job['future_raw_path']}")
     for anc in [dst.parent]+list(dst.parent.parents):
      if str(anc)=="/":break
      try:st_a=os.lstat(anc)
      except FileNotFoundError:continue
      if stat.S_ISLNK(st_a.st_mode):fail(f"SP Raw ancestor symlink {anc}")
      if anc==repo:break
     data=src.read_bytes()
     if hashlib.sha256(data).hexdigest()!=job["sha256"] or len(data)!=job["bytes"]:fail(f"SP Raw pin {job['future_raw_path']}")
     fd=os.open(str(dst),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o664)
     with os.fdopen(fd,"wb") as f:f.write(data)
     st_n=os.lstat(dst)
     if oct(stat.S_IMODE(st_n.st_mode))!="0o664":fail("SP Raw mode (no broad perms)")
    f30,_,_,_=load_strict(Path(spec["supplement_full30_r4"]["path"]))
    out_rel=f"sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r7-sp17-{time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())}.json"
    resolve_in(repo,out_rel)
    if (repo/out_rel).exists():fail("SP supp new absent")
    try:built=ev.build_evidence_authority_supplement(repo,issue,repo/"sources/SP-efficient-llm-2026",repo/spec["discovery_ref_effective"]["path"],repo/spec["screening_ref"]["path"],f30["sources"],repo/out_rel,supplement_id=f"r7-sp17-EFF-DID-{time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())}")
    except Exception as e:fail(f"SP builder failed (own output may be deleted) {e}")
    ev.validate_evidence_authority_supplement(repo,built,expected_issue_id=issue,expected_source_root=repo/"sources/SP-efficient-llm-2026",expected_discovery_path=repo/spec["discovery_ref_effective"]["path"],expected_screening_acceptance_path=repo/spec["screening_ref"]["path"])
    st_o=(repo/out_rel).stat();supp={"path":out_rel,"sha256":sha256_file(repo/out_rel),"byte_count":st_o.st_size}
    req_rel=spec["request_rel"];rev_root=spec["rev_root_rel"]
    if (repo/req_rel).exists():fail("SP request new absent")
    if (repo/rev_root).exists():fail("SP R new absent")
   # request assembly order-preserving (NO sort_keys) via core.json_bytes
   disc=spec["discovery_ref_effective"];scr=spec["screening_ref"];cp=st["checkpoint_provenance"]
   req={"schema_version":"2.0-rc1","issue_id":issue,"revision_id":rev,"research_profile":("WEEKLY" if issue=="2026-W34" else "THEMATIC"),"before_state":{"path":f"sources/{issue}/production-state.json","sha256":sha256_file(repo/f"sources/{issue}/production-state.json"),"byte_count":(repo/f"sources/{issue}/production-state.json").stat().st_size},"before_checkpoint":{"evidence":cp["evidence"],"materiality":cp["materiality"],"completeness":cp["completeness"]},"profile_ref":{"path":f"sources/{issue}/production-profile.json","sha256":sha256_file(repo/f"sources/{issue}/production-profile.json"),"byte_count":(repo/f"sources/{issue}/production-profile.json").stat().st_size},"discovery_ref":disc,"screening_ref":scr,"work":{"expected_head":EXP_HEAD,"expected_tree":EXP_TREE},"affected_ids":list(changed),"supplement_manifest":supp,"records":full,"completeness":{"obligations":obligs,"residual_limitations":resid,"closure":clos},"runner":runner,"tool_pins":{"repository_commit_sha":EXP_HEAD,"orchestrator_version":"survey-production-core-v2/0.15-postintegration-transport-thematic","contract":live_contract,"tool_shas":live_tools},"recorded_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"executor":f"general / Muse Spark 1.3 / prepare-normal-high-r6 {issue} {rev}"}
   gate.validate_instance(req,repo/"schemas/dm022-revision-request-v2.schema.json",label="revision request")
   for r in full:ev.validate_research_record_content(r,prof)
   parsed=json.loads(core.json_bytes(req).decode())
   for x,y in zip(req["records"],parsed["records"]):
    if list(x["entity"].keys())!=list(y["entity"].keys()):fail("entity order after core_json")
   req_abs=resolve_in(repo,req_rel)
   req_abs.parent.mkdir(parents=True,exist_ok=True)
   fd=os.open(str(req_abs),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o664)
   with os.fdopen(fd,"wb") as f:f.write(core.json_bytes(req))
   if oct(stat.S_IMODE(os.lstat(req_abs).st_mode))!="0o664":fail("request mode")
   print(f"request staged {req_rel}")
   from scripts.survey_prearchitecture_acceptance_v2 import prepare_revision
   res=prepare_revision(repo,Path(f"sources/{issue}/production-state.json"),Path(req_rel),rev)
   if "manifest_ref" not in res:fail("HIGH manifest invalid")
   print(f"HIGH OK {res['manifest_ref']}")
   (out/"manifest-ref.json").write_text(json.dumps(res["manifest_ref"],indent=2,sort_keys=True))
   # post: old extra incl R1 unchanged; only declared new R/request/staging; preserve R1 candidate
   post_f={};post_e={};post_d={}
   m_all=json.loads(MANIFEST.read_text())["files"]
   for rel in m_all:
    fp=repo/rel;st_p=os.lstat(fp);post_f[rel]=[sha256_file(fp),st_p.st_size,oct(stat.S_IMODE(st_p.st_mode))]
   src2=repo/f"sources/{issue}"
   for p in sorted(src2.rglob("*")):
    try:st_p=os.lstat(p)
    except FileNotFoundError:continue
    s=p.relative_to(repo).as_posix()
    if stat.S_ISLNK(st_p.st_mode):fail(f"post symlink {s}")
    elif stat.S_ISDIR(st_p.st_mode):post_d[s]=oct(stat.S_IMODE(st_p.st_mode))
    elif stat.S_ISREG(st_p.st_mode):
     if s not in post_f:post_e[s]=[sha256_file(p),st_p.st_size,oct(stat.S_IMODE(st_p.st_mode))]
    else:fail(f"post special {s}")
   (out/"post-inventory.json").write_text(json.dumps({"files773":post_f,"extra":post_e,"dirs":post_d},indent=2,sort_keys=True))
   for k,v in entry["files773"].items():
    if post_f.get(k)!=v:fail(f"old 773 changed {k}")
   for k,v in entry["dirs"].items():
    if post_d.get(k)!=v:fail(f"old dir mode changed {k}")
   for k,v in entry["extra"].items():
    if post_e.get(k)!=v:
     # W34 R1 retained + reuse Raw are old extra and must be unchanged; SP has no old R
     fail(f"old extra changed {k}")
   if issue=="2026-W34":
    allowed={spec["request_rel"]}
    for k in post_e:
     if k not in entry["extra"] and k not in allowed and not k.startswith(spec["rev_root_rel"]+"/"):fail(f"unexpected W34 new {k} (only r2 request/R)")
   else:
    allowed={spec["request_rel"]}|{j["future_raw_path"] for j in spec["new_raw"]}
    for k in post_e:
     if k in entry["extra"]:continue
     ok=k in allowed or k.startswith(spec["rev_root_rel"]+"/") or (k.startswith("sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r7-sp17-") and k.endswith(".json"))
     if not ok:fail(f"unexpected SP new {k}")
   print("post inventory OK")
   w("wall-end.txt",time.strftime("%Y%m%dT%H%M%SZ",time.gmtime()));w("exit.txt","0");exit_code=0
  finally:
   try:_s.path.remove(str(repo.resolve()))
   except ValueError:pass
 except SystemExit as e:
  exit_code=int(e.code) if isinstance(e.code,int) else 2
  try:w("traceback.txt",traceback.format_exc());w("exit.txt",str(exit_code))
  except Exception:pass
  raise
 except Exception:
  try:w("traceback.txt",traceback.format_exc());w("exit.txt","2")
  except Exception:pass
  print("REFUSE: preserved, no retry/cleanup",file=sys.stderr);raise SystemExit(2)
 finally:
  try:sys.stdout,sys.stderr=o_out,o_err;stdout_f.close();stderr_f.close()
  except Exception:pass
  try:(out/"exit-code.txt").write_text(str(exit_code))
  except Exception:pass
 raise SystemExit(exit_code)
if __name__=="__main__":main()
