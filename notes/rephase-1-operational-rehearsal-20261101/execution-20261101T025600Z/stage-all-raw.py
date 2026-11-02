import json,hashlib,pathlib,shutil,sys
INTAKE=pathlib.Path('notes/rephase-1-operational-rehearsal-20261101')
WORK=pathlib.Path('.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work')
# repo_path -> (intake_dir, gid, local, api_size, api_blob)
index={}
for mf,tag in [(INTAKE/'intake-20261101T023147Z-p2-20261101T024051Z/manifest.json','p2'),
               (INTAKE/'intake-20261101T023147Z-p3-20261101T025459Z/manifest.json','p3'),
               (INTAKE/'intake-20261101T023147Z-p4-20261101T031826Z/manifest.json','p4')]:
  m=json.loads(mf.read_text())
  dname=m['intake_dir']  # e.g. notes/.../intake-...-p2-...
  for r in m.get('results',[]):
    rp=r.get('repo_path')
    if not rp: continue
    # API metadata: for contents API, body file has size/sha; for blob API, body has sha/size
    bodyf=None
    # find body file path: <intake>/<gid>.body.json (dname already includes notes/ prefix)
    bf=pathlib.Path(dname)/(r['gid']+'.body.json')
    api_size=r.get('reported_size'); api_blob=r.get('reported_blob_sha')
    # P4 manifest uses different keys? check
    if api_size is None and bf.exists():
      try:
        b=json.loads(bf.read_text())
        api_size=b.get('size'); api_blob=b.get('sha')
      except Exception: pass
    for df in r.get('data_files',[]):
      index.setdefault(rp,[]).append({'tag':tag,'gid':r['gid'],'local':str(pathlib.Path(dname)/df['local']),'bytes':df.get('bytes'),'sha256':df.get('sha256'),'api_size':api_size,'api_blob':api_blob})
# P4 blob-only results (repo_path null) mapped from supersede-mapping (P3 failed -> P4 verified, same fixed 774 paths)
P4_BLOB_REPOPATH={
 'p4a02':'sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/flashinfer-ai__flashinfer.json',
 'p4a03':'sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/ggml-org__llama.cpp.json',
 'p4a04':'sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/huggingface__transformers.json',
 'p4a05':'sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/nvidia__tensorrt-llm.json',
 'p4a06':'sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/sgl-project__sglang.json',
 'p4a07':'sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/vllm-project__vllm.json',
}
def _index_p4_blobs():
  mf=pathlib.Path('notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p4-20261101T031826Z/manifest.json')
  m=json.loads(mf.read_text()); dname=m['intake_dir']
  for r in m.get('results',[]):
    if r['gid'] in P4_BLOB_REPOPATH:
      rp=P4_BLOB_REPOPATH[r['gid']]
      bf=pathlib.Path(dname)/(r['gid']+'.body.json')
      api_size=r.get('reported_size'); api_blob=r.get('reported_blob_sha')
      try:
        b=json.loads(bf.read_text()); api_size=b.get('size',api_size); api_blob=b.get('sha',api_blob)
      except Exception: pass
      for df in r.get('data_files',[]):
        index.setdefault(rp,[]).append({'tag':'p4','gid':r['gid'],'local':str(pathlib.Path(dname)/df['local']),'bytes':df.get('bytes'),'sha256':df.get('sha256'),'api_size':api_size,'api_blob':api_blob})
_index_p4_blobs()
def need_for(discovery_data):
  recs=[json.loads(l) for l in pathlib.Path(discovery_data).read_text().splitlines()]
  s=set()
  for r in recs:
    src=r.get('source',{})
    for p in src.get('raw_paths',[]) or []: s.add(p)
    loc=src.get('locator')
    if loc and loc.startswith('sources/'): s.add(loc)
  return s
allneed={}
for disc,issue in [(INTAKE/'intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2b01.discovery-v2.jsonl','2026-W34'),
                   (INTAKE/'intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2b20.discovery-v2.jsonl','SP-efficient-llm-2026')]:
  for p in need_for(str(disc)): allneed[p]=issue
# also X result raws (needed for record_result, referenced by X manifests not discovery)
allneed['sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/grok-x-result.corrected.md']='2026-W34'
print(f'total distinct required paths: {len(allneed)}')
ok=0; fail=[]
for rp in sorted(allneed):
  cands=index.get(rp)
  if not cands:
    fail.append((rp,'NO-DATA-SOURCE')); print(f'MISSING SOURCE {rp}'); continue
  # prefer p4 > p3 > p2? take first with bytes>0; never use 0-byte
  cands=[c for c in cands if c['bytes'] and c['bytes']>0]
  if not cands:
    fail.append((rp,'ALL-ZERO')); print(f'ALL-ZERO {rp}'); continue
  c=cands[0]
  b=pathlib.Path(c['local']).read_bytes()
  blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\x00'+b).hexdigest()
  sha=hashlib.sha256(b).hexdigest()
  api_ok = (c['api_size'] is None or len(b)==c['api_size']) and (c['api_blob'] is None or blob==c['api_blob'])
  man_ok = (c['bytes']==len(b) and (c['sha256'] is None or sha==c['sha256']))
  if not (api_ok and man_ok):
    fail.append((rp,f"VERIFY-FAIL local={len(b)}/{blob[:8]}/{sha[:8]} api={c['api_size']}/{str(c['api_blob'])[:8]} man={c['bytes']}/{str(c['sha256'])[:8]}"))
    print(f"VERIFY-FAIL {rp} {c['tag']}/{c['gid']}")
    continue
  dst=WORK/rp
  if dst.exists():
    eb=dst.read_bytes()
    if eb==b: print(f'ALREADY {rp}'); ok+=1; continue
    else: print(f'EXISTS-DIFFERENT {rp} (workdir has different bytes; NOT overwriting)'); fail.append((rp,'EXISTS-DIFFERENT')); continue
  dst.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(c['local'],dst)
  print(f'STAGED {rp} [{c["tag"]}/{c["gid"]}] {len(b)}B')
  ok+=1
print(f'STAGED-OK {ok} FAIL {len(fail)}')
for rp,why in fail: print(f'FAIL {rp}: {why}')
