"""One-off lab authorship record; not a proposed production authoring interface.

All semantic values below are authored by root. Helpers only serialize canonical
fields and bind files. Do not run again over a frozen revision.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from check import LAB, sha
from prepare import save

D = LAB/'r1'
ISSUE = 'lab-phase4c-weekly-2026-03-09'
NOW = datetime.now(timezone.utc).isoformat()
SOURCE = {r['source_id']:r for r in json.loads((LAB/'source-manifest.json').read_text(encoding='utf-8'))['sources']}

def entity(eid, name, kind, url=None):
    return dict(entity_id=eid,canonical_name=name,entity_type=kind,organization=None,canonical_url=url)

def statement(sid,text,subject,sources,context,cls='AUTHOR_CLAIM',role='PRIMARY_SUBJECT'):
    return dict(statement_id=sid,text=text,subject_id=subject,subject_role=role,evidence_class=cls,source_ids=sources,context=context)

def metric(mid,name,value,subject,comparators,sources,context):
    return dict(metric_id=mid,name=name,value=value,unit='ratio',subject_id=subject,subject_role='PRIMARY_SUBJECT',comparison_subject_ids=comparators,evidence_class='AUTHOR_CLAIM',source_ids=sources,context=context)

def source(sid,title,date,kind,role):
    r=SOURCE[sid]
    return dict(source_id=sid,url=r['final_url'],source_class=kind,title=title,published_at=date,accessed_at=r['captured_at_utc'],role=role)

def event(eid,date,subject,sid):
    return dict(event_id=eid,event_type='SOURCE_PUBLICATION_LABEL',event_date=date,subject_id=subject,subject_role='PRIMARY_SUBJECT',source_ids=[sid])

def write_candidate(cid, entities, artifact, sources, events, claims, metrics, limitations, findings, unresolved, materiality):
    task_id='lab-p4c-'+cid
    targets=list(findings)
    task=dict(schema_version='2.0-rc1',issue_id=ISSUE,evidence_task_id=task_id,discovery_ids=['lab-'+cid],
        source_records=[dict(SOURCE[s['source_id']],lab_only=True) for s in sources],verification_targets=targets,
        screening_basis=dict(screening_acceptance_sha256=sha(D/'lab-screening.json'),decisions=[dict(discovery_id='lab-'+cid,decision='INSPECT',scope_tags=['parallel-drafting','temporal-eligibility'])]))
    save(D/f'{cid}-task.json',task)
    card=dict(schema_version='2.0-rc1',issue_id=ISSUE,evidence_task_id=task_id,
        basis=dict(task_sha256=sha(D/f'{cid}-task.json'),screening_acceptance_sha256=sha(D/'lab-screening.json'),
            prompt_sha256=sha(LAB/'contracts/config/prompts/evidence-verification-v2.md'),result_contract_sha256=sha(LAB/'contracts/schemas/evidence-v2-card.schema.json')),
        status='PARTIAL',entities=entities,artifact=artifact,temporal=dict(observed_at=NOW,events=events),sources=sources,
        claims=claims,metrics=metrics,limitations=limitations,
        verification=dict(targets=[dict(target=k,status=v[0],finding=v[1],subject_ids=[artifact['primary_subject_id']],source_ids=v[2]) for k,v in findings.items()],unresolved_questions=unresolved,contradictions=[]))
    save(D/f'{cid}-card.json',card)
    save(D/f'{cid}-view.json',dict(schema_version='2.0-rc1',issue_id=ISSUE,research_profile='WEEKLY',evidence_task_id=task_id,
        evidence_sha256=sha(D/f'{cid}-card.json'),materiality=dict(status=materiality[0],rationale=materiality[1]),
        scope_dimensions=['speculative-inference','speed-interpretation'],profile_annotations=dict(lab_only=True,window_start='2026-03-09T00:00:00Z',window_end_exclusive='2026-03-16T00:00:00Z',historical_webpage_state='UNATTESTED')))

if __name__ == '__main__':
    assert not D.exists(), 'Do not overwrite a frozen/started revision'
    save(D/'lab-screening.json',dict(scope='LAB_INSPECTION_INPUT_SELECTION_ONLY_NOT_PRODUCTION_ACCEPTANCE',
        protocol_sha256=sha(LAB/'protocol.md'),preflight_sha256=sha(LAB/'preflight.md'),source_manifest_sha256=sha(LAB/'source-manifest.json'),
        decisions=[dict(discovery_id='lab-'+c,decision='INSPECT',reason='Assess relevance and time; no predetermined editorial disposition') for c in ('c1','c2','c3')]))
    p='peagle'; b=['peagle-blog']; paper=['peagle-paper-v1']
    write_candidate('c1',[
        entity(p,'P-EAGLE','FRAMEWORK','https://arxiv.org/abs/2602.01469v1'),entity('eagle3','EAGLE-3','FRAMEWORK'),
        entity('gptoss20b','GPT-OSS 20B','MODEL'),entity('gptoss120b','GPT-OSS 120B','MODEL'),entity('qwen3coder','Qwen3-Coder 30B','MODEL'),entity('vllm','vLLM','FRAMEWORK')],
        dict(primary_subject_id=p,artifact_type='FRAMEWORK',canonical_name='P-EAGLE',canonical_url='https://arxiv.org/abs/2602.01469v1'),
        [source('peagle-blog','P-EAGLE: Faster LLM inference with Parallel Speculative Decoding in vLLM','2026-03-13','PRIMARY_OFFICIAL','serving-report'),source('peagle-paper-v1','P-EAGLE: Parallel-Drafting EAGLE with Scalable Training','2026-02-01','PRIMARY_PAPER','technical-background')],
        [event('p-report','2026-03-13',p,'peagle-blog'),event('p-paper','2026-02-01',p,'peagle-paper-v1')],
        [statement('p-method','学習済みの共有hidden stateとmask embeddingを使い、複数draft tokenを一回のforward passで提案する。採否を決めるtarget modelの検証は残る。',p,b+paper,'paper §2; blog Our Approach / Implementation'),
         statement('p-training','並列予測専用のdrafterが必要。論文は長系列学習のattention mask事前計算と、依存関係を保つ系列内分割でメモリ負荷に対応する。',p,paper,'§2–3; training is not free or removed'),
         statement('p-blog-setup','報告の評価はGPT-OSS 20B、B200 1基、vLLM、4層drafter。両手法ともlinear draftingでK=3/5/7を掃引し、各条件でそれぞれ最大TPSのKを選ぶ。',p,b,'vLLM Benchmarking; concurrency 1/2/4/8/16/32/64; MT-Bench/HumanEval/SPEED-Bench Code'),
         statement('p-config','掲載設定はfp8 KV cache、async schedulingを使用し、prefix cachingとchunked prefillを無効にする。',p,b,'benchmark launch command; recipe-specific, not general requirements'),
         statement('p-integration','報告はvLLM v0.16.0からの統合と対応学習済みheadを案内する一方、GPT-OSS 20BでEAGLE drafterをserveするにはPR #36684のpatchが必要としている。',p,b,'opening / benchmark Note; captured page statement, not verified release history'),
         statement('p-paper-setup','論文のserving表はH200 1基、concurrency 2/4、3種のtargetと異なるbenchmark条件でAR EAGLE-3と比較する。baselineにはHCA lossも用いる。',p,paper,'§5.1–5.3, Table 10; no conflation with March blog')],
        [metric('p-blog-speed','P-EAGLE / EAGLE-3 TPS','1.05–1.69',p,['eagle3'],b,'GPT-OSS20B/B200/vLLM; methods individually optimized K; c1 1.55–1.69, c64 1.05–1.25; Figures 4–6, not raw AR ratio'),
         metric('p-peak','SPEED-Bench Code TPS ratio','1.69',p,['eagle3'],b,'Figure 6: c=1, B200 1 GPU/GPT-OSS20B, best K per method; code workload, not universal max latency reduction'),
         metric('p-paper-speed','paper reported best serving speedup over AR EAGLE-3','1.10–1.36',p,['eagle3'],paper,'abstract and §5.3/Table10; H200; three targets; not same experiment as blog')],
        [statement('p-time','取得は2026-09-12。表示された報告日やversionから、ページ全文・head・patchの3月時点の正確な公開状態までは証明できない。',p,b+paper,'manifest capture versus source labels; no immutable blog commit checked','INFERENCE'),
         statement('p-bound','単一GPUと掲載workloadのTPS改善は、任意構成の応答遅延、総費用、モデル品質の改善、DFlashとの優劣を証明しない。',p,b+paper,'inference from tested scope; no independent reproduction','INFERENCE'),
         statement('p-pass-cost','forward passの回数が一定でも、K増加時の検証・draft batch・計算/メモリ負荷がゼロになるわけではない。',p,b+paper,'blog batch expansion/CUDA graph range; paper §3 and §5; distinguish sequential overhead','INFERENCE')],
        {'method and verifier':('VERIFIED','共有学習parameterを使うparallel drafterでありtarget verificationを残す。',b+paper),
         'performance and comparator conditions':('VERIFIED','blogは各条件のbest TPS同士。paperのH200条件と区別。',b+paper),
         'training and deployment prerequisites':('VERIFIED','専用head、長系列学習、version/patch記載を取得本文で確認。',b+paper),
         'historical availability':('UNRESOLVED','報告日表示はあるが3月当時の同一bytes/patch公開を追跡していない。',b)},
        ['3月当時のblog本文・head・patchのimmutable公開履歴','掲載条件の独立再現と実運用SLA/総費用'],
        ('MATERIAL','週内3月13日付のserving報告が問いの中心。方法の新規発表日や当時の即時導入可能性は主張しない。'))
    p='dflash'; s=['dflash-paper-v1']
    write_candidate('c2',[entity(p,'DFlash','FRAMEWORK','https://arxiv.org/abs/2602.06036v1'),entity('eagle3','EAGLE-3','FRAMEWORK'),entity('ar','vanilla autoregressive decoding','OTHER'),entity('qwen38b','Qwen3-8B','MODEL'),entity('sglang','SGLang','FRAMEWORK')],
        dict(primary_subject_id=p,artifact_type='PAPER',canonical_name='DFlash: Block Diffusion for Flash Speculative Decoding',canonical_url='https://arxiv.org/abs/2602.06036v1'),
        [source('dflash-paper-v1','DFlash: Block Diffusion for Flash Speculative Decoding','2026-02-05','PRIMARY_PAPER','competing-method-background')],[event('d-paper','2026-02-05',p,'dflash-paper-v1')],
        [statement('d-method','DFlashはtargetの複数層のhidden featuresを各draft層のKVへ渡し、block diffusionで一回のpassから複数tokenを提案しtargetが検証する。',p,s,'§3–4.1; distinct conditioning from P-EAGLE'),
         statement('d-training','target生成応答で専用drafterを学習する。埋め込みとLM headを共有・固定し、draft transformerを更新。hidden featuresのoffline保存量は抽出層数に比例する。',p,s,'§4.2, §5, §5.4.3, Appendix A.1; training/storage costs remain'),
         statement('d-serving','論文にはTransformersだけでなくSGLang/FA4、B200 1基、Spec-v2 scheduling overlapでconcurrency 1–32を調べたserving評価がある。',p,s,'§5.3/Table3; Qwen3-4B/8B/Coder30B; baseline vanilla AR'),
         statement('d-eagle-serving','別のLLaMA-3.1-8B評価ではEAGLE-3と同じ学習dataと公式checkpointを用いて比較し、tree draftingに対応するSpec-v1を両者に用いる。',p,s,'§5.4.1/Table4; single B200 Flashinfer; do not conflate with §5.3')],
        [metric('d-transformers','mean greedy decoding speedup','4.9',p,['ar'],s,'§5.1/Table1; Qwen3 instruct, thinking disabled, Transformers/H200, temp0; corresponding 2.4x over EAGLE-3 tree16; headline over6x is not mean'),
         metric('d-serving-speed','reported peak SGLang speedup','5.1',p,['ar'],s,'§5.3/Table3; Qwen3-8B Math500, concurrency1, single B200/FA4/Spec-v2; denominator vanilla AR, not EAGLE-3 or P-EAGLE')],
        [statement('d-verification-cost','大blockはcompute-bound/大batchで検証費用を増やし得る。小さくする選択はあるがadaptive block-size schedulingは今後の課題。',p,s,'§5.4.4','AUTHOR_CLAIM'),
         statement('d-compare','この固定source群にP-EAGLEと同条件の直接比較はなく、異なる分母・model・backend・workloadの倍率から優劣は決められない。',p,s,'§5–5.4.1 compared with P-EAGLE corpus','INFERENCE'),
         statement('d-time','v1本文の表示は2月5日。後続v2の結果・採択statusは根拠にしない。source取得は9月であり、blog同様の公開履歴attestationは実施していない。',p,s,'version-pinned HTML watermark and manifest','INFERENCE')],
        {'method and verifier':('VERIFIED','target feature conditioningとparallel diffusion draft、target検証を確認。',s),
         'performance and comparator conditions':('VERIFIED','AR分母/対EAGLE比、Transformers/SGLang、異なるscheduling設定を区別。',s),
         'training and source-specific limits':('VERIFIED','専用学習、hidden state保存、大block検証費用、adaptive scheduling未実装。',s),
         'direct P-EAGLE rank':('UNRESOLVED','固定sourceに同条件直接比較なし。',s)},
        ['P-EAGLEとの同条件直接比較','両手法の実運用費用とSLAを含む再現'],
        ('CONTEXT','2月の背景研究だが問いに直接関係し、P-EAGLEだけが並列draft/serving可能という誤解を防ぐ。週内新着とはしない。'))
    p='hidden-extract'; s=['hidden-states-blog']
    write_candidate('c3',[entity(p,'vLLM hidden-state extraction','PRODUCT','https://vllm.ai/blog/2026-03-30-extract-hidden-states')],
        dict(primary_subject_id=p,artifact_type='INTEGRATION',canonical_name='vLLM hidden-state extraction',canonical_url='https://vllm.ai/blog/2026-03-30-extract-hidden-states'),
        [source('hidden-states-blog','Extracting hidden states from vLLM','2026-03-30','PRIMARY_OFFICIAL','temporal-eligibility-test')],[event('h-report','2026-03-30',p,'hidden-states-blog')],
        [statement('h-design','報告はdummy draft modelとKV connectorを再利用するhidden-state抽出を説明し、PR #33736とvLLM >=0.18.0に言及する。',p,s,'opening and Design Insights','PROJECT_CLAIM'),
         statement('h-training-use','hidden-state生成の既存方式にはTransformersとのずれやvLLM patchのmaintenance負荷があると説明する。',p,s,'Motivation; author diagnosis, not measured J-GAS costs','PROJECT_CLAIM')],[],
        [statement('h-limit','執筆時のconnectorはdiskへ保存する例示実装で、dummy methodとconnectorを併用する必要がある。',p,s,'Usage and Limitations','PROJECT_CLAIM'),
         statement('h-date','表示される報告日は3月30日。PRのmerge/release履歴を確認していないため、この日を機能が初めて存在した日とも、3月15日までに利用可能だった証拠とも扱えない。',p,s,'publication label vs implementation chronology','INFERENCE')],
        {'source publication label':('VERIFIED','3月30日表示を確認。',s),
         'implementation and prerequisites':('VERIFIED','dummy model/KV connector、versionへの言及を確認。',s),
         'availability before cutoff':('UNRESOLVED','この後日報告だけではcutoff以前の実装・公開を立証できない。',s)},
        ['PR/リリースのcutoff以前の公開履歴'],
        ('HOLD','問いには関係するが3月30日付sourceは週のcutoff後。過去公開履歴の追加調査は今回の結論に不可欠ではないため行わず、本文根拠には入れない。'))
    assignments=[
        dict(candidate_id='c1',disposition='SELECTED',rationale='週内日付のserving報告を中心に、方法の新発表や歴史的即時導入可能性へ昇格せず紹介。',architecture_usage='PRIMARY',publication_role='報告の主題',architecture_role='P-EAGLE serving conditions',profile_extensions={'lab_only':True}),
        dict(candidate_id='c2',disposition='SELECTED',rationale='2月の背景研究として比較の限界と別の並列draft/serving経路を示す。新着記事にはせず同じ本文を支える。',architecture_usage='SUPPORTING',publication_role='関連研究の比較背景',architecture_role='substantive alternative and non-ranking boundary',profile_extensions={'lab_only':True}),
        dict(candidate_id='c3',disposition='HOLD',rationale='後日sourceから週内利用可能性を補えない。以前に存在しなかったとは結論しない。将来の別期間/歴史調査なら再評価。',architecture_usage='NONE',publication_role=None,architecture_role=None,profile_extensions={'lab_only':True})]
    save(D/'selection.lab.json',dict(scope='LAB_CANONICAL_FIELDS_NOT_ESTABLISHED_PRODUCTION_SELECTION',
        assignments=assignments,summary=dict(candidate_count=3,disposition_counts={'SELECTED':2,'HOLD':1},selected_count=2)))
    requirements=['週内の報告と以前の研究を区別する','並列draftと検証・学習負担を説明する','P-EAGLEの倍率とbaseline/条件を保持する','DFlashの実質的代案と比較不能条件を示す','導入条件と未実証を伝える']
    boundaries=['異条件の倍率で順位をつけない','報告日を公開/導入可能日の証明にしない','一回のpassを無費用や品質向上へ変換しない','cutoff後のC3を週内根拠にしない']
    save(D/'package.lab.json',dict(scope='LAB_CANONICAL_FIELDS_NO_ARCHITECTURE_APPROVAL_OR_ADMISSION',
        issue_id=ISSUE,package_id='lab-p4c-article',selection_sha256=sha(D/'selection.lab.json'),protocol_sha256=sha(LAB/'protocol.md'),
        package=dict(title='並列draftの速度報告をどう読むか',purpose='掲載評価の範囲と導入条件を区別し、読者が比較検証の条件を把握する',drafting_order=1,primary_candidate_ids=['c1'],supporting_candidate_ids=['c2'],must_cover_requirements=requirements,boundaries=boundaries),
        evidence_inputs=[dict(candidate_id=c,architecture_usage=u,evidence_task_id='lab-p4c-'+c,evidence_sha256=sha(D/f'{c}-card.json'),evidence_card=json.loads((D/f'{c}-card.json').read_text(encoding='utf-8'))) for c,u in [('c1','PRIMARY'),('c2','SUPPORTING')]],
        drafting_constraints=dict(language='ja',raw_sources_forbidden=True,unknowns_remain_unknown=True,citation_granularity='EVENT_CLAIM_METRIC_LIMITATION')))
    save(D/'authorship-stage.json',dict(evidence_and_package_written_at=NOW,root_roles=['source-reader','evidence-author','editor','mechanical-binding-author'],active_seconds=None,tokens=None,
        reviewer_expectations_unread=True,source_expectations_sha256='8b129b38f6ea899eebe2df2f50943f5a4e966f0ceecf1a78b79abb695741a817'))
    print('r1 Task/Card/View/Selection fields/Package fields written; no draft yet')
