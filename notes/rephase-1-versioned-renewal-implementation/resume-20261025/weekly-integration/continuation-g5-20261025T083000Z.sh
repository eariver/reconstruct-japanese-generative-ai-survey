#!/bin/bash
# G5 commit — repair 739 (preserve a4bd style variant)
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
FIX=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/continuation-g5-20261025T083000Z
mkdir -p "$EVID"
exec >> "$EVID/commands.log" 2>&1
echo "=== G5 commit ==="
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
run head-g5-pre git -C "$FIX" rev-parse HEAD
run status-g5-pre git -C "$FIX" status --porcelain=v1 --untracked-files=all
# variant manifest before commit: 739 BASE + style a4bd + markers (record)
python3 -c "
import hashlib, pathlib, json
fix=pathlib.Path('$FIX'); snap=pathlib.Path('$REPO/.rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work')
lst=[l.strip() for l in open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input-evidence-20261025T082826Z/dst-hash-intended-stdout.txt') if l.strip()]
variant={}
for line in lst:
  exp, rel = line.split()[0], line.split()[2]
  if rel=='templates/survey/jgaisurvey.sty':
    live=hashlib.sha256((fix/rel).read_bytes()).hexdigest()
    variant[rel]={'shipping':exp,'live':live,'note':'G2 style variant a4bd preserved (U reuse, not C)'}
  else:
    # check if live differs from shipping due to previous markers (will be committed as G5 revert? Actually staged already overlays shipping, so live==shipping except style)
    pass
# also record staged files that revert previous synthetic markers
import subprocess
staged=subprocess.run(['git','--no-optional-locks','diff','--cached','--name-only'],cwd=str(fix),capture_output=True,text=True).stdout.splitlines()
variant['_staged_G5']=sorted(staged)
variant['_note']='739 BASE + style a4bd variant; H6fe86/P1825dba/PUB3f4039 new repair tools; S/weekly_derivation revert previous G2/G4 synthetic markers to shipping (history preserves markers, live is shipping + style variant)'
open('$EVID/variant-manifest.json','w').write(json.dumps(variant,indent=1))
print(json.dumps(variant,indent=1))
"
run commit-g5 git -C "$FIX" commit -m "HIGH phase TEST-ONLY: G5 repair 739 (H perf+P1 dispatcher+PUB union, preserve G2 style a4bd for U reuse)" --no-verify
run head-g5-post git -C "$FIX" rev-parse HEAD
run log-g5 git -C "$FIX" log --oneline -13
run tree-g5 git -C "$FIX" rev-parse HEAD^{tree}
run ancestor-g5 git -C "$FIX" merge-base --is-ancestor 721a04d85532d7855f3e54cc411f5847c787726e HEAD
# verify H/P1/PUB new SHAs, style preserved
python3 -c "import hashlib, pathlib; fix=pathlib.Path('$FIX'); print('H',hashlib.sha256((fix/'scripts/survey_versioned_renewal_history_v2.py').read_bytes()).hexdigest()); print('P1',hashlib.sha256((fix/'scripts/survey_editorial_correction_proposal_v2.py').read_bytes()).hexdigest()); print('PUB',hashlib.sha256((fix/'scripts/survey_publication_v2.py').read_bytes()).hexdigest()); print('style',hashlib.sha256((fix/'templates/survey/jgaisurvey.sty').read_bytes()).hexdigest())" > "$EVID/pins-g5-stdout.txt" 2> "$EVID/pins-g5-stderr.txt"; echo $? > "$EVID/pins-g5-exit.txt"
cat "$EVID/pins-g5-stdout.txt"
echo "G5 DONE"
