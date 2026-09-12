"""One-off root repair of independently reviewed r1; retains original files."""
import json
import shutil
from datetime import datetime, timezone
from check import LAB, read, sha, check
from prepare import save

R1=LAB/'r1'; R2=LAB/'r2'
assert not R2.exists(), 'Do not overwrite an existing revision'
R2.mkdir()
for p in R1.glob('*'):
    if p.name not in ('mechanical-check.json','authorship-stage.json'):
        shutil.copyfile(p,R2/p.name)

def item(rows,key,value):
    return next(r for r in rows if r[key]==value)

def claim(sid,text,subject,sources,context,cls='PRIMARY_FACT'):
    return dict(statement_id=sid,text=text,subject_id=subject,subject_role='PRIMARY_SUBJECT',evidence_class=cls,source_ids=sources,context=context)

c1=read(R2/'c1-card.json'); c2=read(R2/'c2-card.json'); c3=read(R2/'c3-card.json')
summary=item(c1['metrics'],'metric_id','p-paper-speed')
summary['name']='abstract/conclusion summary only, not Table10 range'
summary['context']='abstract/§7 author summary 1.10–1.36; not the range of all cells or per-condition best values in Table10. H200/three targets; §5.3 contains smaller gains and low-K slowdowns. No inferred aggregate.'
c1['metrics'].append(dict(metric_id='p-low-depth-slowdown',name='Qwen3-Coder 30B HumanEval output TPS / optimized AR EAGLE-3',value='0.92',unit='ratio',subject_id='peagle',subject_role='PRIMARY_SUBJECT',comparison_subject_ids=['eagle3'],evidence_class='AUTHOR_CLAIM',source_ids=['peagle-paper-v1'],context='Table10 Qwen30B P-EAGLE K=3,C=4, one H200:1066 OTPS vs best AR 1160 (K=5). Also §5.3. Not same-K comparison; not March blog configuration.'))
c1['limitations'].append(claim('p-source-discrepancy','Qwen30B/HumanEval K=3,C=2はTable10の0.94倍と§5.3本文の0.98倍が不一致。要約の1.10–1.36倍も表の全条件範囲ではない。','peagle',['peagle-paper-v1'],'abstract, §5.3/Table10; C4=0.92 is undisputed between table and prose','INFERENCE'))
c1['limitations'].append(claim('p-capacity-limit','論文§5.3は低Kで4層の一回のpassが1層の逐次passより重くなり得ると説明する。並列化だけで高速化が保証されるとはいえない。','peagle',['peagle-paper-v1'],'§5.3 Qwen30B/HumanEval; not attribution of all runtime differences to order alone','AUTHOR_CLAIM'))
c1['claims'] += [
    claim('p-blog-author','vLLM報告のbylineはAmazon and NVIDIA Team。','peagle',['peagle-blog'],'header and acknowledgements; report authorship, not paper authorship'),
    claim('p-paper-author','論文著者はMude Hui、Xin Huang、Jaime Campos Salas、Yue Sun、Nathan Pemberton、Xiang Song、Ashish Khetan、George Karypis。HuiはUCSC所属でAWS internship中の仕事と記載、他著者はAWS所属。','peagle',['peagle-paper-v1'],'title/author affiliations; distinguish from blog team'),
    claim('p-acceptance','報告のP-EAGLEは4層で、vanilla EAGLE-3との測定には受理されるdraftの長さの改善も寄与すると著者は述べる。並列生成順序だけの因果効果を分離した実験ではない。','peagle',['peagle-blog'],'vLLM Benchmarking + acceptance-length discussion; first sentence author report, causal isolation limit is editorial inference','INFERENCE')]
setup=item(c1['claims'],'statement_id','p-blog-setup')
setup['text']='報告の評価はGPT-OSS 20B、B200 1基、vLLM、専用学習した4層P-EAGLE drafter対公開済みvanilla EAGLE-3 checkpoint。両手法はlinear draftingでK=3/5/7を掃引し、各条件でそれぞれ最大TPSのKを選ぶ。'
item(c1['metrics'],'metric_id','p-blog-speed')['context'] += '; baseline specifically publicly available vanilla checkpoint, unlike paper HCA-trained baseline; capacity/training/acceptance also differ'
item(c1['verification']['targets'],'target','performance and comparator conditions')['finding']='blogは公開vanilla checkpointとの各条件best TPS比較で容量/受理長の差もある。paper要約倍率をTable10全条件範囲としない。表/本文の一致するC4低K slowdownは確認、不一致は別targetに保持。'
c1['verification']['contradictions']=['paper Qwen30B/HumanEval K3,C2: Table10 0.94 vs §5.3 0.98; intended value unresolved. Abstract range is a summary, not a lower/upper envelope of Table10.']
c1['verification']['unresolved_questions'].append('paper Table10と§5.3のC2低K倍率の不一致、および要約倍率の集計範囲')
c1['verification']['targets'].append(dict(target='internal source consistency',status='UNRESOLVED',finding='C2 low-K値と要約範囲の不一致/範囲差を保持。本文は一致するC4 cellを用い、根拠なく統合しない。',subject_ids=['peagle'],source_ids=['peagle-paper-v1']))

item(c2['metrics'],'metric_id','d-transformers')['context']='§5.1/Table1; Qwen3-4B/8B instruct, thinking disabled, Transformers/H200, temp0; Table1 model means4.91/4.86 over vanilla AR. No resolved EAGLE-3 ratio asserted; §5.1 prose/tree16 correspondence is inconsistent with ratios of displayed means and remains unresolved.'
c2['claims'].append(claim('d-authors','DFlashの著者はUC San DiegoのJian Chen、Yesheng Liang、Zhijian Liu。','dflash',['dflash-paper-v1'],'title/author affiliations'))
item(c2['claims'],'statement_id','d-eagle-serving')['text'] += ' この設定の掲載評価でDFlashがEAGLE-3を上回ったと著者は報告する。'
c2['limitations'].append(claim('d-source-discrepancy','§5.1本文は平均4.9倍がEAGLE-3 tree16比2.4倍に相当と記すが、Table1のgreedyモデル別meanはDFlash4.91/4.86、tree16が1.81/1.76、tree60が2.08/2.02。掲載mean比から本文のtree16対応は再現できず、意図した集計/分母は不明。','dflash',['dflash-paper-v1'],'§5.1/Table1; no silent correction to tree60; ratio-of-means is not proven intended aggregation','INFERENCE'))
item(c2['verification']['targets'],'target','performance and comparator conditions')['finding']='AR分母のmean約4.9とTable3 peak5.1、および各backend/scheduling条件を確認。本文の対tree16比は確定扱いせず、別の未解決targetで保持。'
c2['verification']['contradictions']=['§5.1 4.9x AR corresponds to2.4x EAGLE-3(16) is not directly reconciled with Table1 displayed means; intended aggregation/denominator unresolved.']
c2['verification']['unresolved_questions'].append('§5.1とTable1のEAGLE-3比の集計/分母の対応')
c2['verification']['targets'].append(dict(target='internal source consistency',status='UNRESOLVED',finding='§5.1 proseのtree16対応を削除/確定せず保持。表のmean比から意図した集計や正しい分母を推定しない。',subject_ids=['dflash'],source_ids=['dflash-paper-v1']))
c3['claims'].append(claim('h-author','hidden-state抽出報告のbylineはFynn Schmitt-Ulms。','hidden-extract',['hidden-states-blog'],'header'))

for cid,card in [('c1',c1),('c2',c2),('c3',c3)]:
    task=read(R2/f'{cid}-task.json')
    task['verification_targets']=[t['target'] for t in card['verification']['targets']]
    save(R2/f'{cid}-task.json',task)
    card['basis']['task_sha256']=sha(R2/f'{cid}-task.json')
    save(R2/f'{cid}-card.json',card)
    view=read(R2/f'{cid}-view.json')
    view['evidence_sha256']=sha(R2/f'{cid}-card.json')
    save(R2/f'{cid}-view.json',view)

package=read(R2/'package.lab.json')
for row in package['evidence_inputs']:
    row['evidence_card']=read(R2/(row['candidate_id']+'-card.json'))
    row['evidence_sha256']=sha(R2/(row['candidate_id']+'-card.json'))
save(R2/'package.lab.json',package)

def ref(cid,kind,eid):
    card={'c1':c1,'c2':c2}[cid]
    table,key={'CLAIM':('claims','statement_id'),'LIMITATION':('limitations','statement_id'),'METRIC':('metrics','metric_id'),'EVENT':('events','event_id')}[kind]
    row=item(card['temporal']['events'] if table=='events' else card[table],key,eid)
    return dict(evidence_task_id=card['evidence_task_id'],kind=kind,evidence_id=eid,subject_id=row['subject_id'],subject_role=row['subject_role'])

draft=read(R2/'draft.json')
draft['draft_version']='v1.1'; draft['status']='REVISED'
draft['basis']['draft_package_sha256']=sha(R2/'package.lab.json')
draft['runner']['generated_at']=datetime.now(timezone.utc).isoformat()
b1,b2,b3,b4,b5,b6=draft['blocks']
b1['text']='AmazonとNVIDIAのチームによる[vLLMの3月13日付報告](https://vllm.ai/blog/2026-03-13-p-eagle)は、P-EAGLEのserving評価を紹介している。元の論文は、UCSCのMude HuiがAWSでのinternship中にAWSの共著者らと行った研究で、2月に公開された。P-EAGLEでは、補助モデル（drafter）が学習した共有hidden stateとmask embeddingを使い、複数のtoken候補を一回のforward passで提案する。本来動かしたい大きなモデル（target）がそれを検証するため、検証を省いて速くする仕組みではない。'
b1['evidence_refs'] += [ref('c1','CLAIM','p-blog-author'),ref('c1','CLAIM','p-paper-author')]
b2['text']='報告されたTPS（毎秒token数）は、GPT-OSS 20BをB200 1基のvLLMで動かした場合、公開済みvanilla EAGLE-3 checkpoint比で1.05～1.69倍だった。P-EAGLE側は専用学習した4層drafterで、報告では受理される候補の長さの改善も速度に寄与する。並列生成の順序だけを変えた効果の測定ではない。MT-Bench、HumanEval、SPEED-Bench Codeで、同時実行数1では1.55～1.69倍、64では1.05～1.25倍。最大1.69倍はSPEED-Bench Codeの同時実行数1の値である。両手法ともlinear draftingで提案token数Kを3・5・7と変え、各条件で最大TPSのKをそれぞれ選んだ比較であり、任意の負荷やKで同じ効果が得られるわけではない。'
b2['evidence_refs'].append(ref('c1','CLAIM','p-acceptance'));b2['attribution_mode']='MIXED'
b3['text']='[P-EAGLE論文](https://arxiv.org/abs/2602.01469v1)では、H200と別のtarget・benchmark条件を使い、追加のHCA lossで学習したEAGLE-3を比較対象としている。要約の1.10～1.36倍は表10の全条件の範囲ではない。Qwen3-Coder 30BのHumanEval、同時実行数4、P-EAGLEのK=3では、最適KのEAGLE-3に対するTPSが0.92倍で、遅くなる条件もある。著者は低Kでは4層の一回の処理が1層の逐次処理より重くなり得ると説明する。また、attention mask事前計算や系列内分割は長系列学習のメモリ負荷への対策であり、専用drafterの学習をなくさない。一回のpassという特徴だけでは、学習・検証・計算負担まで小さくなるとは結論できない。'
b3['evidence_refs'] += [ref('c1','METRIC','p-low-depth-slowdown'),ref('c1','LIMITATION','p-capacity-limit'),ref('c1','LIMITATION','p-source-discrepancy')]
b4['text']='関連研究の[DFlash v1](https://arxiv.org/abs/2602.06036v1)（2月5日付）は、UC San DiegoのJian Chen、Yesheng Liang、Zhijian Liuによる。targetのhidden featuresを各draft層のKVに渡し、block diffusionで並列に提案する。専用drafterを学習する点と、targetの検証を残す点は共通する。論文はSGLangでの評価も含み、B200・FA4・Spec-v2の条件では通常のautoregressive decodingに対して最大5.1倍を報告する。これはQwen3-8BのMath500、同時実行数1の値であり、EAGLE-3比1.69倍と大小比較できない。LLaMA-3.1-8BでEAGLE-3と学習dataをそろえた別のSGLang/Spec-v1評価でもDFlashが上回ったと報告するが、この資料群からP-EAGLEとの同条件の優劣は決められない。'
b4['evidence_refs'].append(ref('c2','CLAIM','d-authors'))
save(R2/'draft.json',draft)
(R2/'manuscript.md').write_text('# '+draft['headline']+'\n\n'+draft['deck']+'\n\n'+'\n\n'.join(b['text'] for b in draft['blocks'])+'\n',encoding='utf-8')
result=check('r2')
save(R2/'mechanical-check.json',dict(checked_at=datetime.now(timezone.utc).isoformat(),checker_sha256=sha(LAB/'check.py'),result=result))
save(R2/'repair-record.json',dict(author='root',review_findings_sha256=sha(LAB/'review/r1-findings.md'),
    source_first_expectations_sha256=sha(LAB/'review/source-expectations.md'),completed_at=datetime.now(timezone.utc).isoformat(),
    dispositions={
        'R1':'ACCEPTED: summary scoped, undisputed slowdown added, disputed C2 value retained unresolved, Card→package→b3 repaired',
        'R2':'ACCEPTED: source-specific authorship added to all Cards and selected report/research reader passages',
        'R3':'ACCEPTED: unnecessary tree16 correspondence removed from metric; source conflict retained and targeted as unresolved; no invented correction or manuscript number',
        'R4':'ACCEPTED: public vanilla checkpoint and 4-layer/acceptance qualifications added; no order-only causal attribution',
        'O1':'ACCEPTED: same-data rival direction and separate SGLang/Spec-v1 conditions stated',
        'O2':'ACCEPTED: drafter/target and K defined briefly'},
    source_rereads=['P-EAGLE Table10 headers/Qwen30B rows and §5.3','DFlash Table1 means and §5.1 context','P-EAGLE/DFlash author blocks; existing blog header/benchmark context'],
    unresolved_source_conflicts=['P-EAGLE C2 low-K table/text value','DFlash intended aggregation/denominator'],
    active_seconds=None,tokens=None,production_changes=False))
save(LAB/'r2-freeze.json',dict(frozen_at=datetime.now(timezone.utc).isoformat(),parent_freeze_sha256=sha(LAB/'r1-freeze.json'),
    scope='LOCAL_REPAIR_NOT_PRODUCTION_ACCEPTANCE',files=[dict(path=str(p.relative_to(LAB)).replace('\\','/'),sha256=sha(p)) for p in sorted(R2.glob('*'))]))
print(json.dumps(result))
