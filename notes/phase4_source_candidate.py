"""One disclosed, manually authored case from fixed repository Raw bytes.

This is not an automatic semantic extractor or independent review. The source
preparation uses BeautifulSoup; claims below were authored after reading S2,
S4, S7 and A6. Output remains an unaccepted research candidate.
"""
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import bs4
from bs4 import BeautifulSoup
import semantic_handoff_probe as p


def make_candidate():
    samples = json.loads((Path(__file__).parent / 'semantic-handoff-probe-results.json').read_text(encoding='utf-8-sig'))
    sample = next(x for x in samples['samples'] if 'arxiv' in x['discovery_id'])
    source = sample['sources'][0]
    raw = p.read(source['path'], p.W34)
    assert hashlib.sha256(raw).hexdigest() == source['sha256']
    soup = BeautifulSoup(raw, 'html.parser')
    for node in soup.select('script,style,nav,header,footer,[hidden],[aria-hidden="true"]'):
        node.decompose()
    selectors = ['#S2', '#S2\\.T1', '#S4', '#S7', '#A6']
    evidence = []
    for selector in selectors:
        nodes = soup.select(selector)
        if len(nodes) != 1:
            raise ValueError(f'non-unique or missing source region: {selector}')
        text = ' '.join(nodes[0].get_text(' ', strip=True).split())
        assert 'Content selection saved.' not in text
        evidence.append({'selector': selector, 'characters': len(text),
                         'normalized_text_sha256': hashlib.sha256(text.encode()).hexdigest()})
    old = p.obj(sample['paths']['card'], p.W34)
    card = copy.deepcopy(old)
    paper = card['artifact']['primary_subject_id']
    sid = card['sources'][0]['source_id']
    card['temporal']['observed_at'] = datetime.now(timezone.utc).isoformat()
    card['sources'][0]['role'] = 'Fixed captured HTML; bounded inspection of sections S2, S4, S7 and A6; external links not fetched.'
    for eid, name in [('policy-gate', 'Self-confidence gate (pre-answer)'), ('policy-frozen', 'Frozen gpt-oss-120b router')]:
        card['entities'].append({'entity_id': eid, 'canonical_name': name, 'entity_type': 'OTHER',
                                 'organization': None, 'canonical_url': None})

    def statement(ident, text, locator, classification='AUTHOR_CLAIM'):
        return {'statement_id': ident, 'text': text, 'subject_id': paper,
                'subject_role': 'PRIMARY_SUBJECT', 'evidence_class': classification,
                'source_ids': [sid], 'context': f'Raw sha256={source["sha256"]}; {locator}; author report, no independent reproduction.'}

    card['claims'] = [
        statement('method-protocols', '著者は主実験で同じgpt-oss-120b solverを用い、直接回答、自己修正、planner/executor/reviewer、共同討議の4方式を各問題で一度ずつ実行して比較した。', '#S2'),
        statement('cost-comparison', '主held-out splitでは自己信頼度gateとfrozen routerの費用効率を比較するが、solve率の信頼区間が重なるためgateの正答率優位とは結論しない。', '#S2.T1; #S4'),
        statement('failure-versus-value', '回答後の失敗予測と、追加protocol固有の価値予測は別の問いであり、前者の有用性だけで完全なprotocol選択器の成立とはしない。', '#S4'),
        statement('archive-link-observation', 'Appendix Fにはcompanion dataset archiveへのリンクと収録物の説明がある。リンク先の実在・内容・再現可能性は今回確認していない。', '#A6'),
    ]
    context = ('Raw sha256=' + source['sha256'] + '; #S2.T1 and #S4; primary held-out n=423, '
               'gpt-oss-120b solver stack; 2000 problem-level bootstrap; deterministic realized runs, '
               'not fresh-run variability. Overlapping solve CIs do not establish solve superiority.')
    card['metrics'] = []
    for eid, other, solve, tokens, solve_ci, tok_ci in [
        ('policy-gate', 'policy-frozen', '78.0', '45.0', '[74.0,81.8]', '[41.6,48.7]'),
        ('policy-frozen', 'policy-gate', '73.8', '71.3', '[69.5,77.5]', '[56.5,86.7]'),
    ]:
        for name, value, unit, ci in [('solve', solve, '%', solve_ci), ('average-tokens', tokens, 'K tokens', tok_ci)]:
            card['metrics'].append({'metric_id': eid + '-' + name, 'name': name, 'value': value, 'unit': unit,
                'context': context + ' 95% CI=' + ci, 'subject_id': eid, 'subject_role': 'RELATED',
                'comparison_subject_ids': [other], 'evidence_class': 'AUTHOR_CLAIM', 'source_ids': [sid]})
    card['limitations'] = [
        statement('scope-boundary', '主router比較は1 solver family・1数学benchmarkに限定され、他benchmark・solverの検査は限定的な頑健性検査であり一般性の証明ではない。', '#S7'),
        statement('oracle-boundary', 'oracleは固定した費用順で過去の実行結果から作る診断量であり、運用可能なpolicyでも各問題の期待効用推定でもない。', '#S7'),
        statement('cost-boundary', '費用の主尺度は記録token数であり、遅延・金額・energy・並列性・正誤以外の回答品質によって運用上の選好は変わり得る。', '#S7'),
        statement('probe-boundary', '回答後probeの確率指標はparse不能30件を除外しており、問題単位のbootstrap区間は再実行時の確率的変動を測らない。', '#S7'),
    ]
    target = card['verification']['targets'][0]
    target['status'] = 'UNRESOLVED'
    target['finding'] = ('Task targetはtriage metadataと途中で切れたabstract要約を含む。S2/S4/S7/A6の上記範囲は読んだが、'
                         'target全体の検証完了は宣言しない。具体的な研究問いの確認と独立reviewが必要。')
    card['verification']['unresolved_questions'] = ['具体的なverification問いの確定', '外部archiveの内容・再現性', '選択read範囲外の内容とomissionの独立review']
    card['verification']['contradictions'] = []
    trace = {'scope': 'MANUALLY_AUTHORED_UNREVIEWED_CANDIDATE_NOT_PRODUCTION',
             'raw_ref': p.W34, 'raw_path': source['path'], 'raw_sha256': source['sha256'],
             'raw_bytes': len(raw), 'parser': 'BeautifulSoup ' + bs4.__version__ + ' / html.parser',
             'regions': evidence, 'truncated': False, 'full_document_consumed': False,
             'not_read': 'Most main sections and appendices outside S2/S4/S7/A6; external dataset/repository links',
             'previous_card_sha256': sample['card_sha256'],
             'independent_review': False}
    return card, trace, raw, p.obj(sample['paths']['task'], p.W34)


if __name__ == '__main__':
    card, trace, _, _ = make_candidate()
    out = Path(__file__).parent
    (out / 'phase4-paper-candidate.json').write_text(json.dumps(card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out / 'phase4-source-trace.json').write_text(json.dumps(trace, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
