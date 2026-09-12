"""Root-authored manuscript from frozen local package fields; no Raw reads."""
import json
from datetime import datetime, timezone
from check import LAB, sha, check
from prepare import save

D=LAB/'r1'
package=json.loads((D/'package.lab.json').read_text(encoding='utf-8'))
cards={r['candidate_id']:r['evidence_card'] for r in package['evidence_inputs']}

def ref(cid,kind,eid):
    card=cards[cid]
    table,key={'CLAIM':('claims','statement_id'),'LIMITATION':('limitations','statement_id'),
               'METRIC':('metrics','metric_id'),'EVENT':('events','event_id')}[kind]
    rows=card['temporal']['events'] if table=='events' else card[table]
    row=next(r for r in rows if r[key]==eid)
    return dict(evidence_task_id=card['evidence_task_id'],kind=kind,evidence_id=eid,subject_id=row['subject_id'],subject_role=row['subject_role'])

def refs(cid,kind,*ids):
    return [ref(cid,kind,x) for x in ids]

def block(bid,text,evidence,mode='MIXED'):
    return dict(block_id=bid,block_type='PARAGRAPH',text=text,attribution_mode=mode,evidence_refs=evidence)

assert not (D/'draft.json').exists(), 'Never overwrite a frozen draft'
draft=dict(schema_version='2.0-rc1',issue_id=package['issue_id'],research_profile='WEEKLY',publication_profile='WEEKLY_MAGAZINE',
    package_id=package['package_id'],draft_version='v1.0',status='DRAFT',
    basis=dict(draft_package_sha256=sha(D/'package.lab.json'),prompt_id='article-drafting-v2',prompt_sha256=sha(LAB/'contracts/config/prompts/article-drafting-v2.md')),
    runner=dict(provider='OpenAI',model='GPT-6 Astra (session binding; exact billing model/usage unavailable)',invocation='root direct canonical-field authorship with local hash assembly',generated_at=datetime.now(timezone.utc).isoformat(),run_reference='notes/phase-4c/protocol.md'),
    headline='P-EAGLEの並列draftは何を速くするのか',
    deck='vLLMの速度報告は、draftを順番に生成する負担を減らす実装を示す。倍率を読むには、比較対象と運用条件をそろえる必要がある。',
    deck_attribution_mode='MIXED',deck_evidence_refs=refs('c1','CLAIM','p-method','p-blog-setup')+refs('c1','LIMITATION','p-bound'),
    blocks=[
        block('b1','[vLLMの3月13日付報告](https://vllm.ai/blog/2026-03-13-p-eagle)は、2月に論文が出たP-EAGLEのserving評価を紹介している。P-EAGLEは、学習した共有hidden stateとmask embeddingを使い、複数のdraft tokenを一回のforward passで提案する。target modelによる検証は引き続き必要で、検証を省いて速くする仕組みではない。',refs('c1','EVENT','p-report','p-paper')+refs('c1','CLAIM','p-method')),
        block('b2','報告されたTPS（毎秒token数）は、GPT-OSS 20BをB200 1基のvLLMで動かした場合、EAGLE-3比で1.05～1.69倍だった。MT-Bench、HumanEval、SPEED-Bench Codeで、同時実行数1では1.55～1.69倍、64では1.05～1.25倍。最大1.69倍はSPEED-Bench Codeの同時実行数1の値であり、どの負荷でも得られる倍率ではない。両手法ともlinear draftingでK=3・5・7を試し、条件ごとに最大TPSのKをそれぞれ選んだ比較である。',refs('c1','METRIC','p-blog-speed','p-peak')+refs('c1','CLAIM','p-blog-setup'),'ATTRIBUTED'),
        block('b3','[P-EAGLE論文](https://arxiv.org/abs/2602.01469v1)の1.10～1.36倍という結果は、H200と別のtarget・benchmark条件によるEAGLE-3比較であり、今回のB200報告と同一の測定ではない。また、並列予測には専用に学習したdrafterが要る。論文のattention mask事前計算や系列内分割は長系列学習のメモリ負荷に対応する工夫であって、学習作業をなくすものではない。一回のpassで生成できても、draft数を増やした際の計算・メモリや検証の負担まで一定になるとは限らない。',refs('c1','METRIC','p-paper-speed')+refs('c1','CLAIM','p-paper-setup','p-training')+refs('c1','LIMITATION','p-pass-cost')),
        block('b4','関連研究の[DFlash v1](https://arxiv.org/abs/2602.06036v1、2月5日付)も、targetのhidden featuresを各draft層のKVに渡し、block diffusionで並列に提案する。専用drafterを学習する点と、targetによる検証を残す点は共通する。DFlashはTransformersだけでなくSGLangでも評価され、B200・FA4・Spec-v2の条件では通常のautoregressive decodingに対して最大5.1倍を報告している。これはQwen3-8BのMath500、同時実行数1の値であり、EAGLE-3比1.69倍と大小比較できない。LLaMA-3.1-8BでEAGLE-3と学習dataをそろえた別評価もあるが、この資料群からP-EAGLEとの同条件の優劣は決められない。',refs('c2','EVENT','d-paper')+refs('c2','CLAIM','d-method','d-training','d-serving','d-eagle-serving')+refs('c2','METRIC','d-serving-speed')+refs('c2','LIMITATION','d-compare')),
        block('b5','導入時にはheadだけでなくserving設定も確認したい。P-EAGLEの報告はvLLM v0.16.0からの統合を案内する一方、GPT-OSS 20BでEAGLE drafterを使うにはPR #36684のpatchが必要と記す。測定ではfp8 KV cacheとasync schedulingを使い、prefix cachingとchunked prefillを無効にしている。DFlash側も、大blockは大batchなどで検証費用を増やし得るとし、adaptive block-size schedulingを今後の課題としている。掲載TPSから、自分のSLAに対する遅延改善や学習・運用を通じた総費用の削減までは推定できない。',refs('c1','CLAIM','p-integration','p-config')+refs('c2','LIMITATION','d-verification-cost')+refs('c1','LIMITATION','p-bound')),
        block('b6','時点については、以上は論文の固定versionと、後日取得した報告本文に基づく。報告の日付は、記載されたheadやpatchがその日に同じ状態で入手できた証明ではない。当時の即時導入可能性と、掲載条件の独立再現は未確認である。',refs('c1','LIMITATION','p-time','p-bound')+refs('c2','LIMITATION','d-time'),'INFERENCE')],
    must_cover_coverage=[dict(requirement=r,block_ids=ids) for r,ids in zip(package['package']['must_cover_requirements'],[['b1','b4','b6'],['b1','b3','b4'],['b2','b3'],['b4','b5'],['b5','b6']])],
    boundary_dispositions=[dict(boundary=b,handling=h,block_ids=ids,rationale=why) for b,h,ids,why in zip(package['package']['boundaries'],
        ['EXPLICITLY_STATED','EXPLICITLY_STATED','EXPLICITLY_STATED','RESPECTED_BY_OMISSION'],
        [['b2','b3','b4'],['b1','b6'],['b1','b3','b5'],[]],
        ['分母と測定環境を明記して順位を留保','日付の意味と取得履歴の限界を明示','検証・専用学習・計算負担を明示し品質向上を主張しない','後日C3をpackage根拠にも本文にも取り込まない。採否理由はselectionへ保持'])],
    profile_extensions=dict(lab_only=True,historical_page_state='UNATTESTED'),publication_extensions={})
# Link syntax is authored here, independent of factual content.
draft['blocks'][3]['text']=draft['blocks'][3]['text'].replace('https://arxiv.org/abs/2602.06036v1、2月5日付)', 'https://arxiv.org/abs/2602.06036v1)（2月5日付）')
save(D/'draft.json',draft)
(D/'manuscript.md').write_text('# '+draft['headline']+'\n\n'+draft['deck']+'\n\n'+'\n\n'.join(b['text'] for b in draft['blocks'])+'\n',encoding='utf-8')
result=check('r1')
save(D/'mechanical-check.json',dict(checked_at=datetime.now(timezone.utc).isoformat(),checker_sha256=sha(LAB/'check.py'),result=result))
save(LAB/'r1-freeze.json',dict(frozen_at=datetime.now(timezone.utc).isoformat(),scope='LOCAL_FILES_NOT_PRODUCTION_ACCEPTANCE',
    reviewer_expectations_unread=True,source_expectations_sha256='8b129b38f6ea899eebe2df2f50943f5a4e966f0ceecf1a78b79abb695741a817',
    files=[dict(path=str(p.relative_to(LAB)).replace('\\','/'),sha256=sha(p)) for p in sorted(D.glob('*'))]))
print(json.dumps(result))
