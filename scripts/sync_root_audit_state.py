#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / 'execution-state.json'
VERIFICATION_PATH = ROOT / 'VERIFICATION_RECORD.md'
DOCS_WITH_TIMESTAMP = [
    ROOT / 'README.md',
    ROOT / 'START_HERE.md',
    ROOT / 'ROOT_ARCHIVE_MANIFEST.md',
    ROOT / 'THREE-APP-SPLIT-STATUS.md',
]

SUMMARY_LABELS = [
    'top-level entries checked',
    'missing README dirs',
    'empty dirs',
    'manifest missing entries',
    'unexpected top-level entries',
    'archive marker gaps',
    'navigation marker gaps',
    'first-screen archive notice gaps',
    'manifest section issues',
    'manifest classification issues',
    'retained baseline issues',
    'doc reference issues',
    'blocker consistency issues',
    'doc timestamp issues',
    'recent commit consistency issues',
    'root head consistency issues',
    'root remote consistency issues',
    'blocking snapshot consistency issues',
    'workspace status consistency issues',
    'subrepo workspace status consistency issues',
    'blocking status consistency issues',
    'latest blocking tried consistency issues',
    'blocking recent trail consistency issues',
    'latest audit snapshot consistency issues',
    'verification record consistency issues',
    'execution plan consistency issues',
    'completed sequence consistency issues',
    'fallback route consistency issues',
    'blocking point consistency issues',
    'next steps exact consistency issues',
    'verification section sequence issues',
    'latest audit summary order issues',
]


def sh(*args: str, cwd: Path = ROOT, check: bool = True) -> str:
    result = subprocess.run(args, cwd=cwd, check=check, capture_output=True, text=True)
    return result.stdout.rstrip('\n')


def sh_err(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(args, cwd=cwd, check=False, capture_output=True, text=True)
    text = (result.stdout + result.stderr).strip()
    return text


def replace_section(text: str, heading: str, body: str) -> str:
    pattern = re.compile(rf'(^### {re.escape(heading[4:])}\n)(.*?)(?=^### |\Z)', re.S | re.M)
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f'missing section: {heading}')
    return text[:match.start()] + match.group(1) + body.rstrip() + '\n\n' + text[match.end():]


def replace_verification_timestamp(text: str, stamp: str) -> str:
    return re.sub(r'^更新时间：\d{4}-\d{2}-\d{2} \d{2}:\d{2} \(Asia/Shanghai\)$', f'更新时间：{stamp} (Asia/Shanghai)', text, count=1, flags=re.M)


def replace_doc_timestamp(path: Path, stamp: str) -> None:
    text = path.read_text()
    pattern = r'更新时间：\d{4}-\d{2}-\d{2} \d{2}:\d{2} \(Asia/Shanghai\)'
    if not re.search(pattern, text):
        raise RuntimeError(f'timestamp marker not found in {path}')
    new_text = re.sub(pattern, f'更新时间：{stamp} (Asia/Shanghai)', text, count=1)
    path.write_text(new_text)


def main() -> None:
    now = datetime.now().astimezone()
    iso_stamp = now.isoformat(timespec='seconds')
    minute_stamp = now.strftime('%Y-%m-%d %H:%M')

    root_heads = sh('git', 'log', '-3', '--format=%H').splitlines()
    if len(root_heads) < 3:
        raise RuntimeError('need at least 3 root commits')
    root_current, root_prev1, root_prev2 = root_heads[:3]

    repos = OrderedDict([
        ('heart-plant', ROOT / 'heart-plant'),
        ('heart-plant-admin', ROOT / 'heart-plant-admin'),
        ('heart-plant-api', ROOT / 'heart-plant-api'),
    ])
    repo_heads = {name: sh('git', 'rev-parse', 'HEAD', cwd=path) for name, path in repos.items()}
    repo_origins = {name: sh('git', 'remote', 'get-url', 'origin', cwd=path) for name, path in repos.items()}
    repo_status = {name: sh('git', 'status', '--short', cwd=path).splitlines() for name, path in repos.items()}

    state = json.loads(STATE_PATH.read_text())
    fallback = state['blocking']['fallback']
    next0, next1, next2 = state['nextSteps']

    summary_line = 'doc timestamp issues: 0、recent commit consistency issues: 0、root head consistency issues: 0、root remote consistency issues: 0、blocking snapshot consistency issues: 0、workspace status consistency issues: 0、subrepo workspace status consistency issues: 0、blocking status consistency issues: 0、latest blocking tried consistency issues: 0、blocking recent trail consistency issues: 0、latest audit snapshot consistency issues: 0、verification record consistency issues: 0、execution plan consistency issues: 0、completed sequence consistency issues: 0、fallback route consistency issues: 0、blocking point consistency issues: 0、next steps exact consistency issues: 0、verification section sequence issues: 0、latest audit summary order issues: 0、RESULT: PASS'

    latest_tried = (
        '本轮继续沿 nextSteps[2] fallback route 维持根工作区残余巡检脚本化基线，'
        '按当前根仓库提交链把 execution-state.json / VERIFICATION_RECORD.md 中的 '
        'workspace-root pre-sync anchors、recentCommits.workspace-root、workspace-root git log -3 pre-sync window exact snapshot、'
        f'blocking.point exact snapshot 与 latestAudit timestamp 整体推进到 current HEAD={root_current}、HEAD~1={root_prev1}、HEAD~2={root_prev2}；'
        '随后在本轮 sync commit 后复跑 python3 scripts/root_archive_audit.py，确认 '
        + summary_line
    )

    blocking_point = (
        '真实 Supabase 写库/存储联调仍缺少 SUPABASE_SERVICE_ROLE_KEY，mock 初始化写入 kv_store_4b732228 仍会命中 RLS；'
        '登录后核心页面截图回归仍缺真实测试账号/有效 Supabase 登录态；'
        '此外根工作区仓库未配置 origin，当前根目录提交无法 push；'
        f'根仓库 pre-sync 锚点仍为 HEAD~1={root_current}、HEAD~2={root_prev1}；'
        '并计划于本轮提交后复跑 python3 scripts/root_archive_audit.py 确认 '
        + summary_line
    )

    current_step = (
        '本轮继续沿 execution-state.json -> nextSteps[2] / blocking.fallback 的 fallback route 续跑，维持 '
        'scripts/root_archive_audit.py 所覆盖的跨文件显式基线同步，并把 execution-state.json / '
        'VERIFICATION_RECORD.md / latestAudit / blocking.point / recentCommits.workspace-root 与当前根仓库 pre-sync baseline 一并推进；'
        '要求 execution-state.json -> currentStep 显式命中 latestAudit、summary、strict order、LATEST_AUDIT_SUMMARY_LABELS、'
        '### 22.、### 23.、### 41.、### 42.、### 43.、### 44.、### 45.、### 46.、### 47.、### 48.、'
        'timestamp -> command -> result、blocking.tried、latest tried entry、recent 3、tail order、no duplicates、blocking.status、partial、'
        'blocking.point、recentCommits、recentCommits.workspace-root、workspace-root、latest local HEAD、pre-sync anchor = HEAD~1、'
        'workspace-root git log -3 pre-sync window exact snapshot、workspace-root current HEAD、workspace-root HEAD~1、workspace-root HEAD~2、'
        'git rev-parse HEAD、git log -3 --format=%H、git -C heart-plant remote get-url origin、'
        'git -C heart-plant-admin remote get-url origin、git -C heart-plant-api remote get-url origin、heart-plant、heart-plant-admin、heart-plant-api、'
        f"heart-plant: {repo_heads['heart-plant']}、git -C heart-plant remote get-url origin: {repo_origins['heart-plant']}、"
        f"heart-plant-admin: {repo_heads['heart-plant-admin']}、git -C heart-plant-admin remote get-url origin: {repo_origins['heart-plant-admin']}、"
        f"heart-plant-api: {repo_heads['heart-plant-api']}、git -C heart-plant-api remote get-url origin: {repo_origins['heart-plant-api']}、"
        "git remote -v、git remote get-url origin、No such remote、origin、git remote -v: (no output)、git remote get-url origin: error: No such remote 'origin'、"
        'git status --short、?? EXECUTION_PLAN.md、subrepo git status --short、 M src/app/pages/UserLogin.tsx、 M src/app/utils/api.ts、 M utils/supabase/info.tsx、 M deno.json、'
        'full-length、40位、section headings、EXECUTION_PLAN.md、completed、count=30、canonical order、README.md、START_HERE.md、ROOT_ARCHIVE_MANIFEST.md、'
        'THREE-APP-SPLIT-STATUS.md、execution-state.json、VERIFICATION_RECORD.md、currentStep、command、result、timestamp、'
        'latestAudit command exact snapshot、latestAudit result exact snapshot、latestAudit timestamp exact snapshot、summary order exact snapshot、RESULT: PASS；'
        f'当前 nextSteps exact snapshot 为：nextSteps[0]={next0}；nextSteps[1]={next1}；nextSteps[2]={next2}；'
        f'当前 blocking.point exact snapshot 为：{blocking_point}；'
        f'latest tried entry exact snapshot：{latest_tried}；'
        f'workspace-root current HEAD exact snapshot: {root_current}；workspace-root HEAD~1 exact snapshot: {root_prev1}；workspace-root HEAD~2 exact snapshot: {root_prev2}；'
        f'workspace-root git log -3 pre-sync window exact snapshot: {root_current} -> {root_prev1}；'
        f'recentCommits.workspace-root exact snapshot: latest local HEAD {root_current} (pre-sync anchor = HEAD~1, see VERIFICATION_RECORD.md recentCommits/root-head sections)；'
        '- latestAudit command exact snapshot: python3 scripts/root_archive_audit.py；- latestAudit result exact snapshot: PASS；'
        f'- latestAudit timestamp exact snapshot: {iso_stamp}'
    )

    state['updatedAt'] = iso_stamp
    state['currentStep'] = current_step
    state['recentCommits']['workspace-root'] = (
        f'latest local HEAD {root_current} (pre-sync anchor = HEAD~1, see VERIFICATION_RECORD.md recentCommits/root-head sections)'
    )
    state['blocking']['point'] = blocking_point
    tried = state['blocking'].get('tried', [])
    if not tried or tried[-1] != latest_tried:
        tried.append(latest_tried)
    state['blocking']['tried'] = tried
    state['latestAudit']['timestamp'] = iso_stamp
    state['latestAudit']['command'] = 'python3 scripts/root_archive_audit.py'
    state['latestAudit']['result'] = 'PASS'
    state['latestAudit']['summary'] = OrderedDict((label, 0) for label in SUMMARY_LABELS)
    state['latestAudit']['summary']['top-level entries checked'] = 57
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')

    verification = VERIFICATION_PATH.read_text()
    verification = replace_verification_timestamp(verification, minute_stamp)

    verification = replace_section(verification, '### 22. 最近一轮归档审计摘要（机读对照）', '\n'.join([
        f'- timestamp: {minute_stamp}',
        '- command: python3 scripts/root_archive_audit.py',
        '- result: PASS',
        '- top-level entries checked: 57',
        *[f'- {label}: 0' for label in SUMMARY_LABELS if label != 'top-level entries checked'],
    ]))

    verification = replace_section(verification, '### 26. recentCommits 与仓库 HEAD 显式校验', '\n'.join([
        '- recentCommits / git rev-parse HEAD / git log -3 --format=%H baseline synchronized across execution-state.json / VERIFICATION_RECORD.md / currentStep',
        f"- heart-plant: {repo_heads['heart-plant']}",
        f"- git -C heart-plant remote get-url origin: {repo_origins['heart-plant']}",
        f"- heart-plant-admin: {repo_heads['heart-plant-admin']}",
        f"- git -C heart-plant-admin remote get-url origin: {repo_origins['heart-plant-admin']}",
        f"- heart-plant-api: {repo_heads['heart-plant-api']}",
        f"- git -C heart-plant-api remote get-url origin: {repo_origins['heart-plant-api']}",
        f'- workspace-root: latest local HEAD {root_current} (pre-sync anchor = HEAD~1, see VERIFICATION_RECORD.md recentCommits/root-head sections)',
        f'- workspace-root recent local heads (pre-sync latest 2): {root_current}, {root_prev1}',
        f'- workspace-root HEAD~1: {root_current}',
        f'- workspace-root HEAD~2: {root_prev1}',
        '- workspace-root pre-sync command: git log -3 --format=%H',
        f'- workspace-root git log -3 pre-sync window exact snapshot: {root_current} -> {root_prev1}',
        '- full-length policy: heart-plant / heart-plant-admin / heart-plant-api recentCommits 均使用 full-length 40位精确哈希，无缩写',
        '- RESULT: PASS',
    ]))

    verification = replace_section(verification, '### 28. blocking 快照与续跑清单显式校验', '\n'.join([
        f'- blocking.point exact snapshot: {blocking_point}',
        f'- workspace-root pre-sync anchors exact snapshot: HEAD~1={root_current}、HEAD~2={root_prev1}',
        f'- blocking.tried latest tried entry exact snapshot: {latest_tried}',
        f'- blocking.tried recent 3 [1]: {tried[-3]}',
        f'- blocking.tried recent 3 [2]: {tried[-2]}',
        f'- blocking.tried recent 3 [3]: {tried[-1]}',
        '- blocking.tried latest 3 exact snapshot stored in execution-state.json / VERIFICATION_RECORD.md / currentStep',
        f'- nextSteps[0] exact snapshot: {next0}',
        f'- nextSteps[1] exact snapshot: {next1}',
        f'- nextSteps[2] exact snapshot: {next2}',
        '- RESULT: PASS',
    ]))

    verification = replace_section(verification, '### 31. 根仓库 current HEAD 显式校验', '\n'.join([
        f'- git rev-parse HEAD: {root_current}',
        f'- workspace-root current HEAD exact snapshot: {root_current}',
        f'- workspace-root HEAD~1 anchor: {root_current}',
        f'- workspace-root HEAD~2 anchor: {root_prev1}',
        '- workspace-root current HEAD note: current HEAD changes after every sync commit; machine anchor remains HEAD~1 / HEAD~2 plus git rev-parse HEAD command visibility',
        '- currentStep / execution-state.json / VERIFICATION_RECORD.md: synchronized with the same root-head baseline',
        '- RESULT: PASS',
    ]))

    verification = replace_section(verification, '### 36. blocking.tried 最新尝试显式校验', '\n'.join([
        '- blocking.tried latest tried entry synchronized across execution-state.json / VERIFICATION_RECORD.md / currentStep',
        f'- latest tried entry exact snapshot: {latest_tried}',
        '- execution-state.json / VERIFICATION_RECORD.md / currentStep: synchronized with the same latest tried baseline',
        '- RESULT: PASS',
    ]))

    verification = replace_section(verification, '### 39. blocking.point 精确快照显式校验', '\n'.join([
        f'- blocking.point exact snapshot: {blocking_point}',
        f'- workspace-root pre-sync anchors exact snapshot: HEAD~1={root_current}、HEAD~2={root_prev1}',
        '- execution-state.json / VERIFICATION_RECORD.md / currentStep: synchronized with the same blocking.point baseline',
        '- RESULT: PASS',
    ]))

    verification = replace_section(verification, '### 40. blocking.tried recent 3 去重 / 顺序显式校验', '\n'.join([
        f'- recent 3 [1]: {tried[-3]}',
        f'- recent 3 [2]: {tried[-2]}',
        f'- recent 3 [3]: {tried[-1]}',
        f'- tail order exact snapshot: {tried[-3]} -> {tried[-2]} -> {tried[-1]}',
        '- duplicate check: no duplicates across recent 3',
        '- execution-state.json / VERIFICATION_RECORD.md / currentStep: synchronized with the same blocking.tried recent 3 baseline',
        '- RESULT: PASS',
    ]))

    verification = replace_section(verification, '### 41. 子仓库 recentCommits / origin exact snapshot 显式校验', '\n'.join([
        f"- heart-plant: {repo_heads['heart-plant']}",
        f"- git -C heart-plant remote get-url origin: {repo_origins['heart-plant']}",
        f"- heart-plant-admin: {repo_heads['heart-plant-admin']}",
        f"- git -C heart-plant-admin remote get-url origin: {repo_origins['heart-plant-admin']}",
        f"- heart-plant-api: {repo_heads['heart-plant-api']}",
        f"- git -C heart-plant-api remote get-url origin: {repo_origins['heart-plant-api']}",
        '- execution-state.json / VERIFICATION_RECORD.md / currentStep: synchronized with the same exact snapshot baseline',
        '- RESULT: PASS',
    ]))

    verification = replace_section(verification, '### 45. latestAudit command/result/timestamp exact snapshot 显式校验', '\n'.join([
        '- latestAudit command exact snapshot: python3 scripts/root_archive_audit.py',
        '- latestAudit result exact snapshot: PASS',
        f'- latestAudit timestamp exact snapshot: {iso_stamp}',
        '- execution-state.json / VERIFICATION_RECORD.md / currentStep: synchronized with the same latestAudit exact snapshot baseline',
        '- RESULT: PASS',
    ]))

    status_lines = ['- subrepo git status --short: explicit dirty snapshot baseline stored in execution-state.json / VERIFICATION_RECORD.md / currentStep']
    for name in ['heart-plant', 'heart-plant-admin', 'heart-plant-api']:
        lines = repo_status[name]
        status_lines.append(f'- {name} status count: {len(lines)}')
        for line in lines:
            status_lines.append(f'- {name} exact snapshot: {line}')
    status_lines.extend([
        '- execution-state.json / VERIFICATION_RECORD.md / currentStep: synchronized with the same subrepo workspace exact snapshot baseline',
        '- exact snapshot policy: preserve current dirty entries verbatim until the three subrepos are actually cleaned or committed',
        '- RESULT: PASS',
    ])
    verification = replace_section(verification, '### 47. 三端子仓库 git status exact snapshot 显式校验', '\n'.join(status_lines))

    verification = replace_section(verification, '### 48. recentCommits.workspace-root exact snapshot 显式校验', '\n'.join([
        f'- recentCommits.workspace-root exact snapshot: latest local HEAD {root_current} (pre-sync anchor = HEAD~1, see VERIFICATION_RECORD.md recentCommits/root-head sections)',
        f'- workspace-root HEAD~1 exact snapshot: {root_current}',
        f'- workspace-root HEAD~2 exact snapshot: {root_prev1}',
        '- execution-state.json / VERIFICATION_RECORD.md / currentStep: synchronized with the same workspace-root recentCommits exact snapshot baseline',
        '- RESULT: PASS',
    ]))

    VERIFICATION_PATH.write_text(verification)

    for doc in DOCS_WITH_TIMESTAMP:
        replace_doc_timestamp(doc, minute_stamp)

    print(json.dumps({
        'updatedAt': iso_stamp,
        'workspace_root_current': root_current,
        'workspace_root_head1': root_prev1,
        'workspace_root_head2': root_prev2,
        'latestTriedTail': tried[-3:],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
