"""One historical-package editorial specimen; no new production authority.

The Japanese boundary wording is root-authored from embedded canonical Cards,
not a new source investigation. The four historical body blocks are unreviewed
carry-forward. This is a trial record, not another production authoring format.
"""
import copy
import json
from pathlib import Path

LAB = Path(__file__).resolve().parent
ROOT = LAB.parents[1]
REF = 'c1703f772837317b81735cd4cc851c715fff1a3b'
FIXED = ROOT / '.phase-4-inputs' / REF
PID = 'w34-collaborative-agent-workflows-retrieval'
PACKAGE = FIXED / f'sources/2026-W34/draft/v2/packages/{PID}/draft-package.json'
ORIGINAL = PACKAGE.with_name('draft-result.json')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def author():
    original, package = read(ORIGINAL), read(PACKAGE)
    draft = copy.deepcopy(original)
    draft['status'] = 'DRAFT'
    draft['draft_version'] = 'v1.1'
    draft['runner'] = dict(provider='OpenAI', model='Astra / root',
        invocation='Phase 4-E LAB ONLY: root-authored boundary wording; historical body carry-forward, not independently reviewed or admitted',
        generated_at=read(LAB/'observation.json')['observed_at'],
        run_reference='notes/phase-4e/README.md')
    draft['blocks'] = [b for b in draft['blocks'] if b['block_type'] != 'CLAIM_BOUNDARY']
    # One readable note per subject. Exact canonical refs are retained below.
    wording = {
        'mistral-agentic-search': 'Mistral Agentic SearchのFinanceBench／OfficeQA Proの数値は、既定の構成を使ったMistral自身の報告である。今回確認された資料には独立した再現検証がなく、提供範囲や料金についても発表記事を超える詳細は確認されていない。',
        'slack-code': 'Slack Codeの企業向け展開や利用プランは、発表の「本日提供開始」を超える詳細が確認されていない。エージェントの出力品質やレビュー負担に関する説明も提供元の主張であり、今回の資料にはそれを測定した結果はない。',
        'chatgpt-messages-plugin': 'Messages連携の対応機種やWork／Codexでの利用範囲について、二次報道にある詳細は取得した一次資料で別途確認されていない。Appleの推奨・承認を示すものとも扱わない。端末上の自動操作という仕組みの説明も二次報道によるもので、取得した一次資料では確認されていない。',
        'copilot-jetbrains-enterprise': 'JetBrains向けCopilotの資料の9月8日という日付は取得日であり、ページの発表日ではない。対象週との対応は変更記録の文脈と当時の観測に基づく。変更記録を超える展開時期や利用プランの詳細は確認されていない。',
        'chatgpt-computer-history': 'ChatGPTの操作履歴の基本機能を記した8月14日の記録は日付のみで、対象期間の開始時刻との前後関係を確定できない。この週の変更として扱うのは8月20日の拡張である。プライバシー上の性質は記録の説明を超えて独立検証されていない。',
        'grok-bot-expansion': 'Grok Botの現在の案内ページは編集後の8月26日付であり、8月21日時点の本文を示す資料としては扱わない。8月21日の出来事としての時期は、当時の公式X投稿の観測と同日付の二次資料に基づく。現在のページにある無料試用や企業向け順番待ちの詳細には、8月21日後の編集内容が含まれる可能性がある。',
        'replit-gpt56-luna': 'ReplitのFree Modeの対象者や利用上限、GPT-5.6 Lunaの詳しい性能は今回の資料では確認されていない。値下げが無償提供を可能にしたという因果の説明は提供元のものであり、監査によって確かめられた結果ではない。',
        'antigravity-enterprise': 'Google Cloudの記事は8月21日付だが公開時刻がなく、22:00 UTCの締切以前だったかは確定できない。一方、8月20日のAntigravityの記事もバンドル提供を伝えている。Standard／Plus／新興市場向けの条件を超える個別の加入資格については管理画面での確認が必要である。',
        'copilot-slack': 'Slack向けCopilotの9月8日という日付は資料の取得日であり、対象週との対応は変更記録の文脈と当時の観測に基づく。機能の説明は取得した本文で確認できる範囲に限る。',
        'runway-mcp-workflows': 'RunwayのMCPによるワークフロー操作について、変更記録には品質や限界を評価する記述がない。機能の追加から品質の向上までは判断しない。',
        'copilot-teams': 'Teams向けCopilotの9月8日という日付は資料の取得日であり、対象週との対応は変更記録の文脈と当時の観測に基づく。機能の説明は取得した本文で確認できる範囲に限る。',
        'kimi-code-cli': 'Kimi Code CLIの新しい道具については機能の説明があるが、振る舞いや品質への効果を示す記述はない。機能の追加からその効果までは判断しない。',
    }
    block_by_subject, blocks_by_limitation = {}, {}
    for item in package['evidence_inputs']:
        card = item['evidence_card']
        subject = card['limitations'][0]['subject_id']
        bid = 'scope-' + subject
        block_by_subject[subject] = bid
        refs = []
        for row in card['limitations']:
            refs.append(dict(evidence_task_id=item['evidence_task_id'], kind='LIMITATION',
                evidence_id=row['statement_id'], subject_id=row['subject_id'], subject_role=row['subject_role']))
            blocks_by_limitation.setdefault(row['text'], []).append(bid)
        draft['blocks'].append(dict(block_id=bid, block_type='CLAIM_BOUNDARY', text=wording[subject],
            attribution_mode='INFERENCE', evidence_refs=refs))
    aggregate = {
        'maker-reported benchmark figures for Agentic Search': [block_by_subject['mistral-agentic-search']],
        'Grok Bot Aug 21 / Aug 26 chronology provenance': [block_by_subject['grok-bot-expansion']],
        'GitHub Slack/Teams claim-text capture limitations where applicable':
            [block_by_subject['copilot-slack'], block_by_subject['copilot-teams']],
    }
    internal = 'regional processing is NOT part of this package after Selection r2; it belongs to Package 4'
    dispositions = []
    for boundary in package['package']['boundaries']:
        if boundary == internal:
            dispositions.append(dict(boundary=boundary, handling='RESPECTED_BY_OMISSION', block_ids=[],
                rationale='内部の配置制約として保持する。本文にはregional processingを追加せず、Selection修復の経緯も掲載しない。元Architectureと他packageの配置は変更しない。'))
        else:
            ids = blocks_by_limitation.get(boundary) or aggregate[boundary]
            dispositions.append(dict(boundary=boundary, handling='EXPLICITLY_STATED', block_ids=ids,
                rationale='名指しblockに日本語で制約を述べ、当該subjectの既存LIMITATION参照を保持する。原資料の再検証や独立した品質合格を意味しない。'))
    draft['boundary_dispositions'] = dispositions
    cover_blocks = [
        ['p2-slack-collab'],
        ['p2-search-retrieval', 'scope-mistral-agentic-search'],
        ['p2-slack-collab', 'p2-search-retrieval', 'p2-ide-enterprise'],
        ['p2-grok', 'scope-grok-bot-expansion'],
        ['p2-slack-collab', 'scope-copilot-slack', 'scope-copilot-teams'],
    ]
    assert len(cover_blocks) == len(draft['must_cover_coverage'])
    for row, ids in zip(draft['must_cover_coverage'], cover_blocks):
        row['block_ids'] = ids
    save(LAB/'draft-result.lab.json', draft)
    lines = ['# Phase 4-E: 境界表現の著者案', '',
        '**LAB / NOT INDEPENDENTLY REVIEWED / NOT ADMITTED**', '',
        '既存の4本文blockは未再reviewの歴史入力。以下はcanonical Cards内の制約から作った日本語案で、出典の再調査ではない。', '']
    for block in draft['blocks'][4:]:
        lines += ['## ' + block['block_id'], '', block['text'], '']
    (LAB/'boundary-wording.lab.md').write_bytes(('\n'.join(lines)).encode('utf-8'))
    print('Authored LAB DRAFT: 12 subject notes, 22 explicit boundary mappings, 1 internal omission; historical body unchanged')


if __name__ == '__main__':
    author()
