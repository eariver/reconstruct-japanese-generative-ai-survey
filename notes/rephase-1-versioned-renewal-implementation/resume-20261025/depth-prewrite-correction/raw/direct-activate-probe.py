import sys
sys.path.insert(0, r'/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-depth-rewrite-20261025T200000Z/fixture-weekly')
from scripts import survey_versioned_renewal_v2 as high
from pathlib import Path
repo=Path(r'/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-depth-rewrite-20261025T200000Z/fixture-weekly')
state_rel=r'sources/2026-W37/production-state.json'
set_rel=r'sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals/high-u33-depth32-full/publication-set.json'
try:
  res=high.activate_renewal(repo, state_rel, set_rel, 'TEST direct activate at cap (valid inert prior chain32)', 'depth-rewrite-test', '2026-10-25T20:00:00Z')
  print('UNEXPECTED_SUCCESS '+str(res))
except Exception as e:
  print('CODE:'+str(getattr(e,'code',type(e).__name__)))
  print('PHASE:'+str(getattr(e,'phase','')))
  print('DISP:'+str(getattr(e,'disposition','')))
  print('DETAIL:'+str(getattr(e,'detail',str(e))[:800]))
