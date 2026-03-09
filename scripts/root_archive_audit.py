#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_NAMES = {'.git', '__pycache__', 'node_modules', 'heart-plant', 'heart-plant-admin', 'heart-plant-api'}
MANIFEST = ROOT / 'ROOT_ARCHIVE_MANIFEST.md'
EXECUTION_STATE = ROOT / 'execution-state.json'
VERIFICATION_RECORD = ROOT / 'VERIFICATION_RECORD.md'
EXECUTION_PLAN = ROOT / 'EXECUTION_PLAN.md'

TOP_LEVEL_EXPECTED = {
    '.gitignore',
    '.vscode',
    'API_FIX_SUMMARY.md',
    'ATTRIBUTIONS.md',
    'DEPLOYMENT.md',
    'DESIGN.md',
    'EXECUTION_PLAN.md',
    'FILES_READY_FOR_GITHUB.md',
    'FIX_SUMMARY.md',
    'GITHUB_SETUP.md',
    'GITHUB_UPLOAD_GUIDE.md',
    'LICENSE',
    'MACOS_QUICKSTART.md',
    'QUICK_DEPLOY.md',
    'README.md',
    'ROOT_ARCHIVE_MANIFEST.md',
    'START_HERE.md',
    'STREAMING_QUICKSTART.md',
    'STREAMING_README.md',
    'THREE-APP-DEPLOYMENT.md',
    'THREE-APP-SPLIT-STATUS.md',
    'TIMELINE_FIX_SUMMARY.md',
    'UPLOAD_TO_GITHUB.md',
    'VERIFICATION_RECORD.md',
    'VIDEO_STATUS_GUIDE.md',
    'WEBRTC_DEBUG_GUIDE.md',
    'WEBRTC_SETUP.md',
    'deploy-supabase.sh',
    'deploy.sh',
    'docker-compose.yml',
    'execution-state.json',
    'git-init.sh',
    'git-push.sh',
    'guidelines',
    'index.html',
    'mediamtx-config-fixed.yml',
    'mediamtx-config.yml',
    'mediamtx-minimal.yml',
    'mediamtx-quickstart.bat',
    'mediamtx-quickstart.sh',
    'mediamtx-setup.md',
    'nginx',
    'package-lock.json',
    'package.json',
    'postcss.config.mjs',
    'quick-upload.bat',
    'quick-upload.sh',
    'scripts',
    'setup-mediamtx-macos.sh',
    'src',
    'start-mediamtx.sh',
    'stream-server',
    'supabase',
    'utils',
    'vite.config.ts',
    'workflows',
    '上传到GitHub说明.md',
}

ARCHIVE_MARKERS = (
    '归档说明（2026-03-09）',
    '归档状态说明',
    '历史归档',
    '已归档',
    'Historical archive notice',
    'Archived root workspace',
    'Archived root script',
    'Archived root workflow',
    'Archived root docker compose',
    'Archived root MediaMTX config',
)

NAV_MARKERS = (
    'README.md',
    'START_HERE.md',
    'THREE-APP-DEPLOYMENT.md',
    'heart-plant/',
    'heart-plant-admin/',
    'heart-plant-api/',
    './heart-plant',
    './heart-plant-admin',
    './heart-plant-api',
)

ARCHIVE_TARGETS = {
    'API_FIX_SUMMARY.md',
    'ATTRIBUTIONS.md',
    'DEPLOYMENT.md',
    'DESIGN.md',
    'FILES_READY_FOR_GITHUB.md',
    'FIX_SUMMARY.md',
    'GITHUB_SETUP.md',
    'GITHUB_UPLOAD_GUIDE.md',
    'MACOS_QUICKSTART.md',
    'QUICK_DEPLOY.md',
    'STREAMING_QUICKSTART.md',
    'STREAMING_README.md',
    'TIMELINE_FIX_SUMMARY.md',
    'UPLOAD_TO_GITHUB.md',
    'VIDEO_STATUS_GUIDE.md',
    'WEBRTC_DEBUG_GUIDE.md',
    'WEBRTC_SETUP.md',
    'mediamtx-setup.md',
    '上传到GitHub说明.md',
    'deploy-supabase.sh',
    'deploy.sh',
    'docker-compose.yml',
    'git-init.sh',
    'git-push.sh',
    'index.html',
    'package.json',
    'postcss.config.mjs',
    'quick-upload.bat',
    'quick-upload.sh',
    'setup-mediamtx-macos.sh',
    'start-mediamtx.sh',
    'vite.config.ts',
    'mediamtx-config.yml',
    'mediamtx-config-fixed.yml',
    'mediamtx-minimal.yml',
    'mediamtx-quickstart.sh',
    'mediamtx-quickstart.bat',
    '.vscode/README.md',
    'guidelines/README.md',
    'LICENSE/README.md',
    'nginx/README.md',
    'src/README.md',
    'src/app/README.md',
    'src/imports/README.md',
    'src/styles/README.md',
    'stream-server/README.md',
    'supabase/README.md',
    'supabase/functions/README.md',
    'supabase/functions/server/README.md',
    'utils/README.md',
    'utils/supabase/README.md',
    'workflows/README.md',
}

MANIFEST_SECTION_EXPECTED = {
    '## 一、当前仍应保留并持续维护的根目录文件': {
        'README.md',
        'START_HERE.md',
        'EXECUTION_PLAN.md',
        'execution-state.json',
        'VERIFICATION_RECORD.md',
        'ROOT_ARCHIVE_MANIFEST.md',
        'THREE-APP-DEPLOYMENT.md',
        'THREE-APP-SPLIT-STATUS.md',
        '.gitignore',
        'package-lock.json',
        '.vscode/settings.json',
        'scripts/README.md',
        'scripts/root_archive_audit.py',
    },
    '### 2.1 历史文档': {
        'DEPLOYMENT.md',
        'DESIGN.md',
        'GITHUB_SETUP.md',
        'GITHUB_UPLOAD_GUIDE.md',
        'UPLOAD_TO_GITHUB.md',
        '上传到GitHub说明.md',
        'FILES_READY_FOR_GITHUB.md',
        'QUICK_DEPLOY.md',
        'MACOS_QUICKSTART.md',
        'API_FIX_SUMMARY.md',
        'ATTRIBUTIONS.md',
        'FIX_SUMMARY.md',
        'TIMELINE_FIX_SUMMARY.md',
        'VIDEO_STATUS_GUIDE.md',
        'STREAMING_README.md',
        'STREAMING_QUICKSTART.md',
        'WEBRTC_SETUP.md',
        'WEBRTC_DEBUG_GUIDE.md',
        'mediamtx-setup.md',
    },
    '### 2.2 历史脚本 / 历史入口守卫': {
        'deploy.sh',
        'deploy-supabase.sh',
        'git-init.sh',
        'git-push.sh',
        'quick-upload.sh',
        'quick-upload.bat',
        'mediamtx-config.yml',
        'mediamtx-config-fixed.yml',
        'mediamtx-minimal.yml',
        'mediamtx-quickstart.sh',
        'mediamtx-quickstart.bat',
        'setup-mediamtx-macos.sh',
        'start-mediamtx.sh',
        'docker-compose.yml',
        'index.html',
        'package.json',
        'postcss.config.mjs',
        'vite.config.ts',
    },
    '### 2.3 历史目录（目录内已有 README 归档说明）': {
        'src/',
        'supabase/',
        'stream-server/',
        'nginx/',
        'guidelines/',
        'utils/',
        'workflows/',
        'LICENSE/',
        '.vscode/',
    },
}

MANIFEST_SECTION_ORDER = list(MANIFEST_SECTION_EXPECTED)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")

ARCHIVE_CLASSIFICATION_TARGETS = {
    'DEPLOYMENT.md': {'DEPLOYMENT.md'},
    'DESIGN.md': {'DESIGN.md'},
    'GITHUB_SETUP.md': {'GITHUB_SETUP.md'},
    'GITHUB_UPLOAD_GUIDE.md': {'GITHUB_UPLOAD_GUIDE.md'},
    'UPLOAD_TO_GITHUB.md': {'UPLOAD_TO_GITHUB.md'},
    '上传到GitHub说明.md': {'上传到GitHub说明.md'},
    'FILES_READY_FOR_GITHUB.md': {'FILES_READY_FOR_GITHUB.md'},
    'QUICK_DEPLOY.md': {'QUICK_DEPLOY.md'},
    'MACOS_QUICKSTART.md': {'MACOS_QUICKSTART.md'},
    'API_FIX_SUMMARY.md': {'API_FIX_SUMMARY.md'},
    'ATTRIBUTIONS.md': {'ATTRIBUTIONS.md'},
    'FIX_SUMMARY.md': {'FIX_SUMMARY.md'},
    'TIMELINE_FIX_SUMMARY.md': {'TIMELINE_FIX_SUMMARY.md'},
    'VIDEO_STATUS_GUIDE.md': {'VIDEO_STATUS_GUIDE.md'},
    'STREAMING_README.md': {'STREAMING_README.md'},
    'STREAMING_QUICKSTART.md': {'STREAMING_QUICKSTART.md'},
    'WEBRTC_SETUP.md': {'WEBRTC_SETUP.md'},
    'WEBRTC_DEBUG_GUIDE.md': {'WEBRTC_DEBUG_GUIDE.md'},
    'mediamtx-setup.md': {'mediamtx-setup.md'},
    'deploy.sh': {'deploy.sh'},
    'deploy-supabase.sh': {'deploy-supabase.sh'},
    'git-init.sh': {'git-init.sh'},
    'git-push.sh': {'git-push.sh'},
    'quick-upload.sh': {'quick-upload.sh'},
    'quick-upload.bat': {'quick-upload.bat'},
    'mediamtx-config.yml': {'mediamtx-config.yml'},
    'mediamtx-config-fixed.yml': {'mediamtx-config-fixed.yml'},
    'mediamtx-minimal.yml': {'mediamtx-minimal.yml'},
    'mediamtx-quickstart.sh': {'mediamtx-quickstart.sh'},
    'mediamtx-quickstart.bat': {'mediamtx-quickstart.bat'},
    'setup-mediamtx-macos.sh': {'setup-mediamtx-macos.sh'},
    'start-mediamtx.sh': {'start-mediamtx.sh'},
    'docker-compose.yml': {'docker-compose.yml'},
    'index.html': {'index.html'},
    'package.json': {'package.json'},
    'postcss.config.mjs': {'postcss.config.mjs'},
    'vite.config.ts': {'vite.config.ts'},
    'src/': {'src/README.md', 'src/app/README.md', 'src/imports/README.md', 'src/styles/README.md'},
    'supabase/': {'supabase/README.md', 'supabase/functions/README.md', 'supabase/functions/server/README.md'},
    'stream-server/': {'stream-server/README.md'},
    'nginx/': {'nginx/README.md'},
    'guidelines/': {'guidelines/README.md'},
    'utils/': {'utils/README.md', 'utils/supabase/README.md'},
    'workflows/': {'workflows/README.md'},
    'LICENSE/': {'LICENSE/README.md'},
    '.vscode/': {'.vscode/README.md'},
}

RETAINED_ACTIVITY_PATHS = {
    '.vscode/settings.json',
    'scripts/root_archive_audit.py',
    'scripts/README.md',
}

RETAINED_ROOT_DOC_TARGETS = {
    'README.md',
    'START_HERE.md',
    'EXECUTION_PLAN.md',
    'execution-state.json',
    'VERIFICATION_RECORD.md',
    'ROOT_ARCHIVE_MANIFEST.md',
    'THREE-APP-DEPLOYMENT.md',
    'THREE-APP-SPLIT-STATUS.md',
}

RETAINED_TOP_LEVEL_DIRS = {
    '.vscode',
    'scripts',
}

DOC_REFERENCE_REQUIREMENTS = {
    'README.md': {
        'START_HERE.md',
        'execution-state.json',
        'VERIFICATION_RECORD.md',
        'ROOT_ARCHIVE_MANIFEST.md',
        'THREE-APP-DEPLOYMENT.md',
    },
    'START_HERE.md': {
        'README.md',
        'execution-state.json',
        'VERIFICATION_RECORD.md',
        'ROOT_ARCHIVE_MANIFEST.md',
        'THREE-APP-DEPLOYMENT.md',
    },
    'ROOT_ARCHIVE_MANIFEST.md': {
        'README.md',
        'START_HERE.md',
        'execution-state.json',
        'VERIFICATION_RECORD.md',
        'THREE-APP-DEPLOYMENT.md',
        'scripts/root_archive_audit.py',
        '.vscode/settings.json',
    },
    'THREE-APP-SPLIT-STATUS.md': {
        'EXECUTION_PLAN.md',
        'execution-state.json',
        'VERIFICATION_RECORD.md',
        'THREE-APP-DEPLOYMENT.md',
    },
    'THREE-APP-DEPLOYMENT.md': {
        'DEPLOYMENT.md',
        'heart-plant',
        'heart-plant-admin',
        'heart-plant-api',
        'SUPABASE_SERVICE_ROLE_KEY',
    },
    'DEPLOYMENT.md': {
        'THREE-APP-DEPLOYMENT.md',
        'heart-plant/',
        'heart-plant-admin/',
        'heart-plant-api/',
        'SUPABASE_SERVICE_ROLE_KEY',
    },
}

BLOCKER_PHRASES = {
    'service_role': {
        'execution_state': ('SUPABASE_SERVICE_ROLE_KEY',),
        'required_docs': {
            'README.md': ('SUPABASE_SERVICE_ROLE_KEY',),
            'START_HERE.md': ('SUPABASE_SERVICE_ROLE_KEY',),
            'ROOT_ARCHIVE_MANIFEST.md': ('SUPABASE_SERVICE_ROLE_KEY',),
            'THREE-APP-SPLIT-STATUS.md': ('SUPABASE_SERVICE_ROLE_KEY',),
            'THREE-APP-DEPLOYMENT.md': ('SUPABASE_SERVICE_ROLE_KEY',),
        },
    },
    'login_state': {
        'execution_state': ('测试账号', 'Supabase 登录态'),
        'required_docs': {
            'README.md': ('测试账号', 'Supabase 登录态'),
            'START_HERE.md': ('测试账号', '登录态'),
            'ROOT_ARCHIVE_MANIFEST.md': ('测试账号', 'Supabase 登录态'),
            'THREE-APP-SPLIT-STATUS.md': ('测试账号', 'Supabase 登录态'),
            'VERIFICATION_RECORD.md': ('测试账号', '登录态'),
        },
    },
    'git_origin': {
        'execution_state': ('origin',),
        'required_docs': {
            'README.md': ('origin',),
            'START_HERE.md': ('origin',),
            'ROOT_ARCHIVE_MANIFEST.md': ('origin',),
            'THREE-APP-SPLIT-STATUS.md': ('origin',),
        },
    },
}

BLOCKER_SECTION_REQUIREMENTS = {
    'README.md': {
        'heading': '## 当前已知限制',
        'markers': (
            'SUPABASE_SERVICE_ROLE_KEY',
            '测试账号',
            'Supabase 登录态',
            'origin',
        ),
    },
    'START_HERE.md': {
        'heading': '## 当前阻塞提醒',
        'markers': (
            'SUPABASE_SERVICE_ROLE_KEY',
            '测试账号',
            '登录态',
            'origin',
        ),
    },
    'ROOT_ARCHIVE_MANIFEST.md': {
        'heading': '## 五、当前仍未解除的硬阻塞',
        'markers': (
            'SUPABASE_SERVICE_ROLE_KEY',
            '测试账号',
            'Supabase 登录态',
            'origin',
        ),
    },
    'THREE-APP-SPLIT-STATUS.md': {
        'heading': '## 当前剩余阻塞（以 execution-state.json 为准）',
        'markers': (
            'SUPABASE_SERVICE_ROLE_KEY',
            '测试账号',
            'Supabase 登录态',
            'origin',
        ),
    },
    'THREE-APP-DEPLOYMENT.md': {
        'heading': '## 8. 当前已知风险',
        'markers': (
            'SUPABASE_SERVICE_ROLE_KEY',),
    },
    'DEPLOYMENT.md': {
        'heading': '## 当前已知前置条件',
        'markers': (
            'SUPABASE_SERVICE_ROLE_KEY',
            '测试账号',
            '登录态',
        ),
    },
    'VERIFICATION_RECORD.md': {
        'heading': '## 剩余风险',
        'markers': (
            'SUPABASE_SERVICE_ROLE_KEY',
            '测试账号',
            '登录态',
        ),
    },
}

FIRST_SCREEN_LINE_LIMIT = 20
VERIFICATION_TIMESTAMP_RE = re.compile(r'^更新时间：(?P<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \(Asia/Shanghai\)$', re.MULTILINE)
LATEST_AUDIT_SUMMARY_HEADING = '### 22. 最近一轮归档审计摘要（机读对照）'
LATEST_AUDIT_SUMMARY_TIMESTAMP_PREFIX = '- timestamp: '
LATEST_AUDIT_SUMMARY_LABELS = (
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
    'blocking status consistency issues',
    'latest blocking tried consistency issues',
    'blocking recent trail consistency issues',
    'verification record consistency issues',
    'execution plan consistency issues',
    'completed sequence consistency issues',
    'fallback route consistency issues',
    'blocking point consistency issues',
)


DOC_TIMESTAMP_REQUIREMENTS = {
    'README.md': 'execution-state.json',
    'START_HERE.md': 'execution-state.json',
    'ROOT_ARCHIVE_MANIFEST.md': 'execution-state.json',
    'THREE-APP-SPLIT-STATUS.md': 'execution-state.json',
    'VERIFICATION_RECORD.md': 'execution-state.json',
}

STATE_SYNC_MARKERS = (
    'execution-state.json',
    'VERIFICATION_RECORD.md',
    'latestAudit',
    '阻塞项',
)

VERIFICATION_RECORD_STATE_SYNC_HEADING = '### 25. execution-state / fallback 阻塞同步显式校验'
VERIFICATION_RECORD_STATE_SYNC_MARKERS = (
    'execution-state.json',
    'VERIFICATION_RECORD.md',
    'latestAudit',
    '阻塞项',
    'blocking.fallback',
    'nextSteps',
    'RESULT: PASS',
)

RECENT_COMMIT_REPOS = {
    'heart-plant': ROOT / 'heart-plant',
    'heart-plant-admin': ROOT / 'heart-plant-admin',
    'heart-plant-api': ROOT / 'heart-plant-api',
    'workspace-root': ROOT,
}

RECENT_COMMIT_REQUIRED_MARKERS = {
    'currentStep': ('recentCommits', 'git rev-parse HEAD', 'git log -3 --format=%H', 'HEAD~1', 'HEAD~2', 'git -C heart-plant remote get-url origin', 'git -C heart-plant-admin remote get-url origin', 'git -C heart-plant-api remote get-url origin', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('recentCommits', 'git rev-parse HEAD', 'git log -3 --format=%H', 'HEAD~1', 'HEAD~2', 'git -C heart-plant remote get-url origin', 'git -C heart-plant-admin remote get-url origin', 'git -C heart-plant-api remote get-url origin', 'RESULT: PASS'),
}

VERIFICATION_RECORD_RECENT_COMMITS_HEADING = '### 26. recentCommits 与仓库 HEAD 显式校验'
VERIFICATION_RECORD_RECENT_COMMITS_MARKERS = (
    'recentCommits',
    'git rev-parse HEAD',
    'git log -3 --format=%H',
    'HEAD~1',
    'HEAD~2',
    'git -C heart-plant remote get-url origin',
    'git -C heart-plant-admin remote get-url origin',
    'git -C heart-plant-api remote get-url origin',
    'heart-plant',
    'heart-plant-admin',
    'heart-plant-api',
    'workspace-root',
    'RESULT: PASS',
)

ROOT_REMOTE_REQUIRED_MARKERS = {
    'currentStep': ('git remote -v', 'git remote get-url origin', 'No such remote', 'origin'),
    'VERIFICATION_RECORD.md': ('git remote -v', 'git remote get-url origin', 'No such remote', 'origin', 'RESULT: PASS'),
}

VERIFICATION_RECORD_ROOT_HEAD_HEADING = '### 31. 根仓库 current HEAD 显式校验'
VERIFICATION_RECORD_ROOT_HEAD_MARKERS = (
    'git rev-parse HEAD',
    'workspace-root current HEAD',
    'workspace-root HEAD~1',
    'currentStep',
    'RESULT: PASS',
)

ROOT_HEAD_REQUIRED_MARKERS = {
    'currentStep': ('git rev-parse HEAD', 'workspace-root current HEAD', 'workspace-root HEAD~1', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('git rev-parse HEAD', 'workspace-root current HEAD', 'workspace-root HEAD~1', 'RESULT: PASS'),
}

VERIFICATION_RECORD_ROOT_REMOTE_HEADING = '### 27. 根仓库 origin 缺失显式校验'
VERIFICATION_RECORD_ROOT_REMOTE_MARKERS = (
    'git remote -v',
    'git remote get-url origin',
    'No such remote',
    'origin',
    'RESULT: PASS',
)



BLOCKING_SNAPSHOT_REQUIRED_MARKERS = {
    'currentStep': ('blocking.point', 'blocking.tried', 'nextSteps', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('blocking.point', 'blocking.tried', 'nextSteps', 'RESULT: PASS'),
}

VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING = '### 28. blocking 快照与续跑清单显式校验'
VERIFICATION_RECORD_BLOCKING_SNAPSHOT_MARKERS = (
    'blocking.point',
    'blocking.tried',
    'nextSteps',
    'SUPABASE_SERVICE_ROLE_KEY',
    '测试账号',
    'origin',
    'RESULT: PASS',
)

WORKSPACE_STATUS_ALLOWED_SHORT = ('?? EXECUTION_PLAN.md',)
WORKSPACE_STATUS_REQUIRED_MARKERS = {
    'currentStep': ('git status --short', '?? EXECUTION_PLAN.md', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('git status --short', '?? EXECUTION_PLAN.md', 'RESULT: PASS'),
}

VERIFICATION_RECORD_WORKSPACE_STATUS_HEADING = '### 29. 根工作区 git status 显式校验'
VERIFICATION_RECORD_WORKSPACE_STATUS_MARKERS = (
    'git status --short',
    '?? EXECUTION_PLAN.md',
    'clean tracked files',
    'RESULT: PASS',
)

BLOCKING_STATUS_REQUIRED_MARKERS = {
    'currentStep': ('blocking.status', 'partial', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('blocking.status', 'partial', 'RESULT: PASS'),
}

VERIFICATION_RECORD_BLOCKING_STATUS_HEADING = '### 32. blocking.status 显式校验'
VERIFICATION_RECORD_BLOCKING_STATUS_MARKERS = (
    'blocking.status',
    'partial',
    'SUPABASE_SERVICE_ROLE_KEY',
    '测试账号',
    'origin',
    'RESULT: PASS',
)

BLOCKING_POINT_REQUIRED_MARKERS = {
    'currentStep': ('blocking.point', 'SUPABASE_SERVICE_ROLE_KEY', '测试账号', 'origin', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('blocking.point', 'SUPABASE_SERVICE_ROLE_KEY', '测试账号', 'origin', 'RESULT: PASS'),
}

VERIFICATION_RECORD_BLOCKING_POINT_HEADING = '### 39. blocking.point 精确快照显式校验'
VERIFICATION_RECORD_BLOCKING_POINT_MARKERS = (
    'blocking.point',
    'SUPABASE_SERVICE_ROLE_KEY',
    '测试账号',
    'origin',
    'currentStep',
    'execution-state.json',
    'VERIFICATION_RECORD.md',
    'RESULT: PASS',
)

VERIFICATION_RECORD_BLOCKING_RECENT_TRAIL_HEADING = '### 40. blocking.tried recent 3 去重 / 顺序显式校验'
VERIFICATION_RECORD_BLOCKING_RECENT_TRAIL_MARKERS = (
    'blocking.tried',
    'recent 3',
    'no duplicates',
    'tail order',
    'execution-state.json',
    'VERIFICATION_RECORD.md',
    'currentStep',
    'RESULT: PASS',
)
BLOCKING_RECENT_TRAIL_REQUIRED_MARKERS = {
    'currentStep': ('blocking.tried', 'recent 3', 'no duplicates', 'tail order', 'execution-state.json', 'VERIFICATION_RECORD.md', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('blocking.tried', 'recent 3', 'no duplicates', 'tail order', 'execution-state.json', 'VERIFICATION_RECORD.md', 'RESULT: PASS'),
}

VERIFICATION_RECORD_LATEST_BLOCKING_TRIED_HEADING = '### 36. blocking.tried 最新尝试显式校验'
VERIFICATION_RECORD_LATEST_BLOCKING_TRIED_MARKERS = (
    'blocking.tried',
    'latest tried entry',
    'currentStep',
    'VERIFICATION_RECORD.md',
    'execution-state.json',
    'RESULT: PASS',
)
LATEST_BLOCKING_TRIED_REQUIRED_MARKERS = {
    'currentStep': ('blocking.tried', 'latest tried entry', 'execution-state.json', 'VERIFICATION_RECORD.md', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('blocking.tried', 'latest tried entry', 'execution-state.json', 'VERIFICATION_RECORD.md', 'RESULT: PASS'),
}

PLAN_TASK_RE = re.compile(r'^- \[([ xX])\]\s+([A-D]\d+)\.\s+(.*)$')
VERIFICATION_RECORD_EXECUTION_PLAN_HEADING = '### 33. EXECUTION_PLAN 完成状态显式校验'
VERIFICATION_RECORD_EXECUTION_PLAN_MARKERS = (
    'EXECUTION_PLAN.md',
    'execution-state.json',
    'completed',
    'A1',
    'A8',
    'B8',
    'C8',
    'D6',
    'RESULT: PASS',
)
EXECUTION_PLAN_REQUIRED_MARKERS = {
    'currentStep': ('EXECUTION_PLAN.md', 'completed', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('EXECUTION_PLAN.md', 'completed', 'RESULT: PASS'),
}

VERIFICATION_RECORD_COMPLETED_SEQUENCE_HEADING = '### 34. completed 顺序 / 去重 / 总数显式校验'
VERIFICATION_RECORD_COMPLETED_SEQUENCE_MARKERS = (
    'execution-state.json',
    'completed',
    'count=30',
    'no duplicates',
    'canonical order',
    'A1',
    'D6',
    'RESULT: PASS',
)
COMPLETED_SEQUENCE_REQUIRED_MARKERS = {
    'currentStep': ('execution-state.json', 'completed', 'count=30', 'no duplicates', 'canonical order', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('execution-state.json', 'completed', 'count=30', 'no duplicates', 'canonical order', 'RESULT: PASS'),
}

VERIFICATION_RECORD_FALLBACK_ROUTE_HEADING = '### 35. currentStep / fallback route 显式校验'
VERIFICATION_RECORD_FALLBACK_ROUTE_MARKERS = (
    'currentStep',
    'blocking.fallback',
    'nextSteps[2]',
    'fallback route',
    'execution-state.json',
    'VERIFICATION_RECORD.md',
    'latestAudit',
    'RESULT: PASS',
)
FALLBACK_ROUTE_REQUIRED_MARKERS = {
    'currentStep': ('blocking.fallback', 'nextSteps[2]', 'fallback route', 'execution-state.json', 'VERIFICATION_RECORD.md', 'latestAudit', 'RESULT: PASS'),
    'VERIFICATION_RECORD.md': ('blocking.fallback', 'nextSteps[2]', 'fallback route', 'execution-state.json', 'VERIFICATION_RECORD.md', 'latestAudit', 'RESULT: PASS'),
}


def parse_execution_plan_tasks(text: str) -> dict[str, bool]:
    tasks: dict[str, bool] = {}
    for line in text.splitlines():
        match = PLAN_TASK_RE.match(line.strip())
        if not match:
            continue
        checked, task_id, _ = match.groups()
        tasks[task_id] = checked.lower() == 'x'
    return tasks


def expected_task_ids() -> list[str]:
    return [f'{prefix}{idx}' for prefix, end in [('A', 8), ('B', 8), ('C', 8), ('D', 6)] for idx in range(1, end + 1)]


def execution_plan_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')
    plan_text = EXECUTION_PLAN.read_text(encoding='utf-8', errors='ignore')
    plan_tasks = parse_execution_plan_tasks(plan_text)

    expected_tasks = expected_task_ids()
    for task_id in expected_tasks:
        if task_id not in plan_tasks:
            gaps.append(f'EXECUTION_PLAN missing task checkbox :: {task_id}')

    completed = state.get('completed')
    if not isinstance(completed, list):
        return gaps + ['execution-state completed missing or invalid']
    completed_set = {item for item in completed if isinstance(item, str)}

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_EXECUTION_PLAN_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing execution plan section :: '
            f'{VERIFICATION_RECORD_EXECUTION_PLAN_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_EXECUTION_PLAN_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD execution plan marker missing :: {marker}')

    current_step = state.get('currentStep', '')
    for marker in EXECUTION_PLAN_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing execution plan marker :: {marker}')

    for marker in EXECUTION_PLAN_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing execution plan marker :: {marker}')

    for task_id in expected_tasks:
        if task_id not in completed_set and plan_tasks.get(task_id) is True:
            gaps.append(f'EXECUTION_PLAN task checked but not in execution-state completed :: {task_id}')
        if task_id in completed_set and plan_tasks.get(task_id) is not True:
            gaps.append(f'EXECUTION_PLAN task not checked but execution-state completed includes it :: {task_id}')
        if section_text:
            marker = f'- {task_id}: done'
            if task_id in completed_set and marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD execution plan section missing completed marker :: {marker}')

    extra_completed = sorted(completed_set - set(expected_tasks))
    for task_id in extra_completed:
        gaps.append(f'execution-state completed contains unexpected task id :: {task_id}')

    return gaps


def completed_sequence_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    expected_tasks = expected_task_ids()
    completed = state.get('completed')
    if not isinstance(completed, list):
        return ['execution-state completed missing or invalid for sequence check']

    if len(completed) != len(expected_tasks):
        gaps.append(
            'execution-state completed count mismatch :: '
            f'count={len(completed)} expected={len(expected_tasks)}'
        )

    duplicate_items = sorted({item for item in completed if completed.count(item) > 1})
    for item in duplicate_items:
        gaps.append(f'execution-state completed duplicate task id :: {item}')

    non_string_items = [repr(item) for item in completed if not isinstance(item, str)]
    for item in non_string_items:
        gaps.append(f'execution-state completed contains non-string item :: {item}')

    completed_strings = [item for item in completed if isinstance(item, str)]
    if completed_strings != expected_tasks:
        gaps.append(
            'execution-state completed canonical order mismatch :: '
            f'actual={completed_strings} expected={expected_tasks}'
        )

    current_step = state.get('currentStep', '')
    for marker in COMPLETED_SEQUENCE_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing completed sequence marker :: {marker}')

    for marker in COMPLETED_SEQUENCE_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing completed sequence marker :: {marker}')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_COMPLETED_SEQUENCE_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing completed sequence section :: '
            f'{VERIFICATION_RECORD_COMPLETED_SEQUENCE_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_COMPLETED_SEQUENCE_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD completed sequence marker missing :: {marker}')
        expected_line = '- canonical sequence: ' + ', '.join(expected_tasks)
        if expected_line not in section_text:
            gaps.append(f'VERIFICATION_RECORD completed sequence marker missing :: {expected_line}')

    return gaps


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_NAMES for part in path.parts)


def fallback_route_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    blocking = state.get('blocking', {})
    fallback = blocking.get('fallback', '')
    next_steps = state.get('nextSteps')
    current_step = state.get('currentStep', '')

    if not isinstance(fallback, str) or not fallback.strip():
        gaps.append('execution-state blocking.fallback missing or empty for fallback route check')
        fallback = ''

    fallback_step = ''
    if not isinstance(next_steps, list) or len(next_steps) < 3:
        gaps.append('execution-state nextSteps[2] missing for fallback route check')
    else:
        fallback_step = next_steps[2]
        if not isinstance(fallback_step, str) or not fallback_step.strip():
            gaps.append('execution-state nextSteps[2] empty for fallback route check')
            fallback_step = ''

    if fallback and fallback_step and fallback != fallback_step:
        gaps.append('execution-state blocking.fallback and nextSteps[2] mismatch for fallback route check')

    for marker in FALLBACK_ROUTE_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing fallback route marker :: {marker}')

    for marker in FALLBACK_ROUTE_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing fallback route marker :: {marker}')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_FALLBACK_ROUTE_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing fallback route section :: '
            f'{VERIFICATION_RECORD_FALLBACK_ROUTE_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_FALLBACK_ROUTE_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD fallback route marker missing :: {marker}')
        if fallback and f'- blocking.fallback / nextSteps[2] snapshot: {fallback}' not in section_text:
            gaps.append('VERIFICATION_RECORD fallback route section missing exact fallback snapshot line')

    return gaps


def find_missing_readmes() -> list[str]:
    missing: list[str] = []
    for path in ROOT.rglob('*'):
        if not path.is_dir() or path == ROOT or should_skip(path.relative_to(ROOT)):
            continue
        if not any(path.iterdir()):
            continue
        if not (path / 'README.md').exists():
            missing.append(str(path.relative_to(ROOT)))
    return sorted(missing)


def find_empty_dirs() -> list[str]:
    empty: list[str] = []
    for path in ROOT.rglob('*'):
        if not path.is_dir() or should_skip(path.relative_to(ROOT)):
            continue
        if path == ROOT:
            continue
        try:
            next(path.iterdir())
        except StopIteration:
            empty.append(str(path.relative_to(ROOT)))
    return sorted(empty)


def top_level_entries() -> list[str]:
    return sorted(p.name for p in ROOT.iterdir() if p.name not in EXCLUDED_NAMES)


def manifest_missing(entries: list[str], manifest_text: str) -> list[str]:
    return sorted(name for name in entries if name not in manifest_text)


def unexpected_entries(entries: list[str]) -> list[str]:
    return sorted(set(entries) - TOP_LEVEL_EXPECTED)


def has_any_marker(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)


def archive_marker_gaps() -> list[str]:
    missing: list[str] = []
    for rel in sorted(ARCHIVE_TARGETS):
        path = ROOT / rel
        if not path.exists():
            missing.append(f'{rel} :: missing file')
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        if not has_any_marker(text, ARCHIVE_MARKERS):
            missing.append(f'{rel} :: missing archive marker')
    return missing


def navigation_marker_gaps() -> list[str]:
    missing: list[str] = []
    for rel in sorted(ARCHIVE_TARGETS):
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        if not has_any_marker(text, NAV_MARKERS):
            missing.append(f'{rel} :: missing navigation marker')
    return missing


def first_screen_archive_notice_gaps() -> list[str]:
    missing: list[str] = []
    for rel in sorted(ARCHIVE_TARGETS):
        path = ROOT / rel
        if not path.exists():
            missing.append(f'{rel} :: missing file')
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        snippet = '\n'.join(text.splitlines()[:FIRST_SCREEN_LINE_LIMIT])
        if not has_any_marker(snippet, ARCHIVE_MARKERS):
            missing.append(f'{rel} :: first-screen archive marker missing (top {FIRST_SCREEN_LINE_LIMIT} lines)')
            continue
        if not has_any_marker(snippet, NAV_MARKERS):
            missing.append(f'{rel} :: first-screen navigation marker missing (top {FIRST_SCREEN_LINE_LIMIT} lines)')
    return missing


def extract_manifest_section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.find(heading)
    if start == -1:
        return ''
    start += len(heading)
    if next_heading:
        end = text.find(next_heading, start)
        if end != -1:
            return text[start:end]
    match = re.search(r'^#{1,6}\s+', text[start:], re.MULTILINE)
    end = start + match.start() if match else len(text)
    return text[start:end]


def parse_manifest_sections(text: str) -> dict[str, set[str]]:
    parsed: dict[str, set[str]] = {}
    for index, heading in enumerate(MANIFEST_SECTION_ORDER):
        next_heading = MANIFEST_SECTION_ORDER[index + 1] if index + 1 < len(MANIFEST_SECTION_ORDER) else None
        section_text = extract_manifest_section(text, heading, next_heading)
        entries: set[str] = set()
        for line in section_text.splitlines():
            stripped = line.lstrip()
            if not stripped.startswith('- '):
                continue
            match = INLINE_CODE_RE.search(stripped)
            if match:
                entries.add(match.group(1))
        parsed[heading] = entries
    return parsed


def manifest_section_gaps(manifest_text: str) -> list[str]:
    gaps: list[str] = []
    parsed = parse_manifest_sections(manifest_text)
    for heading in MANIFEST_SECTION_ORDER:
        expected = MANIFEST_SECTION_EXPECTED[heading]
        actual = parsed.get(heading, set())
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        if not actual:
            gaps.append(f'{heading} :: missing section or no parsed bullet entries')
            continue
        for item in missing:
            gaps.append(f'{heading} :: missing entry {item}')
        for item in unexpected:
            gaps.append(f'{heading} :: unexpected entry {item}')
    return gaps


def manifest_classification_coverage_gaps() -> list[str]:
    gaps: list[str] = []
    retained = MANIFEST_SECTION_EXPECTED['## 一、当前仍应保留并持续维护的根目录文件']
    archive_section_entries = set().union(
        MANIFEST_SECTION_EXPECTED['### 2.1 历史文档'],
        MANIFEST_SECTION_EXPECTED['### 2.2 历史脚本 / 历史入口守卫'],
        MANIFEST_SECTION_EXPECTED['### 2.3 历史目录（目录内已有 README 归档说明）'],
    )

    overlap = sorted(retained & archive_section_entries)
    for item in overlap:
        gaps.append(f'classification overlap :: {item} appears in both retained and archive baselines')

    uncovered_manifest_entries = sorted(archive_section_entries - set(ARCHIVE_CLASSIFICATION_TARGETS))
    for item in uncovered_manifest_entries:
        gaps.append(f'archive manifest baseline uncovered :: {item}')

    classified_archive_targets = set().union(*ARCHIVE_CLASSIFICATION_TARGETS.values())
    missing_archive_target_coverage = sorted(ARCHIVE_TARGETS - classified_archive_targets)
    for item in missing_archive_target_coverage:
        gaps.append(f'archive audit target not mapped from manifest classification :: {item}')

    unexpected_archive_target_mapping = sorted(classified_archive_targets - ARCHIVE_TARGETS)
    for item in unexpected_archive_target_mapping:
        gaps.append(f'archive classification mapped non-audit target :: {item}')

    retained_misclassified = sorted(retained & classified_archive_targets)
    for item in retained_misclassified:
        gaps.append(f'retained baseline collides with archive audit target :: {item}')

    for manifest_item, targets in sorted(ARCHIVE_CLASSIFICATION_TARGETS.items()):
        for target in sorted(targets):
            if target not in ARCHIVE_TARGETS:
                continue
            path = ROOT / target
            if not path.exists():
                gaps.append(f'archive classification target missing on disk :: {manifest_item} -> {target}')

    return gaps


def retained_baseline_gaps(manifest_text: str) -> list[str]:
    gaps: list[str] = []
    retained = MANIFEST_SECTION_EXPECTED['## 一、当前仍应保留并持续维护的根目录文件']

    top_level_retained = {item for item in retained if '/' not in item}
    nested_retained = retained - top_level_retained

    missing_top_level_allowlist = sorted(top_level_retained - TOP_LEVEL_EXPECTED)
    for item in missing_top_level_allowlist:
        gaps.append(f'retained baseline not allowed by top-level expected set :: {item}')

    archive_collisions = sorted(top_level_retained & ARCHIVE_TARGETS)
    for item in archive_collisions:
        gaps.append(f'retained top-level entry collides with archive audit target :: {item}')

    manifest_missing_root_docs = sorted(RETAINED_ROOT_DOC_TARGETS - top_level_retained)
    for item in manifest_missing_root_docs:
        gaps.append(f'retained manifest missing root doc target :: {item}')

    manifest_missing_activity_paths = sorted(RETAINED_ACTIVITY_PATHS - nested_retained)
    for item in manifest_missing_activity_paths:
        gaps.append(f'retained manifest missing activity path :: {item}')

    referenced_dirs = {item.split('/', 1)[0] for item in nested_retained}
    missing_activity_dirs = sorted(RETAINED_TOP_LEVEL_DIRS - referenced_dirs)
    for item in missing_activity_dirs:
        gaps.append(f'retained manifest missing activity directory reference :: {item}/')

    for item in sorted(RETAINED_ACTIVITY_PATHS):
        if not (ROOT / item).exists():
            gaps.append(f'retained activity path missing on disk :: {item}')

    root_text_targets = {
        'README.md': ROOT / 'README.md',
        'START_HERE.md': ROOT / 'START_HERE.md',
        'ROOT_ARCHIVE_MANIFEST.md': ROOT / 'ROOT_ARCHIVE_MANIFEST.md',
        'scripts/README.md': ROOT / 'scripts/README.md',
    }
    required_mentions = {
        'README.md': ('ROOT_ARCHIVE_MANIFEST.md', 'execution-state.json', 'VERIFICATION_RECORD.md'),
        'START_HERE.md': ('ROOT_ARCHIVE_MANIFEST.md', 'execution-state.json', 'VERIFICATION_RECORD.md'),
        'ROOT_ARCHIVE_MANIFEST.md': ('scripts/root_archive_audit.py', '.vscode/settings.json'),
        'scripts/README.md': ('ROOT_ARCHIVE_MANIFEST.md',),
    }
    for rel, markers in required_mentions.items():
        text = root_text_targets[rel].read_text(encoding='utf-8', errors='ignore')
        for marker in markers:
            if marker not in text:
                gaps.append(f'retained activity/navigation marker missing :: {rel} -> {marker}')

    return gaps


def doc_reference_gaps() -> list[str]:
    gaps: list[str] = []
    for rel, markers in sorted(DOC_REFERENCE_REQUIREMENTS.items()):
        path = ROOT / rel
        if not path.exists():
            gaps.append(f'doc reference source missing on disk :: {rel}')
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        for marker in sorted(markers):
            if marker not in text:
                gaps.append(f'doc reference missing :: {rel} -> {marker}')
    return gaps


def extract_heading_section(text: str, heading: str) -> str:
    start_match = re.search(rf'^{re.escape(heading)}\s*$', text, re.MULTILINE)
    if not start_match:
        return ''
    start = start_match.end()
    next_match = re.search(r'^#{1,6}\s+', text[start:], re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end]


def blocker_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    blocking_point = state.get('blocking', {}).get('point', '')

    for blocker_key, spec in sorted(BLOCKER_PHRASES.items()):
        expected_state_markers = spec['execution_state']
        if not all(marker in blocking_point for marker in expected_state_markers):
            gaps.append(
                'execution-state blocker marker missing :: '
                f'{blocker_key} -> required={expected_state_markers}'
            )
        for rel, markers in sorted(spec['required_docs'].items()):
            path = ROOT / rel
            if not path.exists():
                gaps.append(f'blocker doc missing on disk :: {blocker_key} -> {rel}')
                continue
            text = path.read_text(encoding='utf-8', errors='ignore')
            if not all(marker in text for marker in markers):
                gaps.append(
                    'blocker doc marker missing :: '
                    f'{blocker_key} -> {rel} requires {markers}'
                )

    for rel, spec in sorted(BLOCKER_SECTION_REQUIREMENTS.items()):
        path = ROOT / rel
        if not path.exists():
            gaps.append(f'blocker section doc missing on disk :: {rel}')
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        section_text = extract_heading_section(text, spec['heading'])
        if not section_text:
            gaps.append(f'blocker section heading missing :: {rel} -> {spec["heading"]}')
            continue
        for marker in spec['markers']:
            if marker not in section_text:
                gaps.append(
                    'blocker section marker missing :: '
                    f'{rel} -> {spec["heading"]} requires {marker}'
                )
    return gaps


def doc_timestamp_gaps(state_stamp: str) -> list[str]:
    gaps: list[str] = []
    if not state_stamp:
        return ['execution-state updatedAt missing/invalid; cannot validate doc timestamps']

    for rel, source in sorted(DOC_TIMESTAMP_REQUIREMENTS.items()):
        path = ROOT / rel
        if not path.exists():
            gaps.append(f'doc timestamp source missing on disk :: {rel}')
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        match = VERIFICATION_TIMESTAMP_RE.search(text)
        if not match:
            gaps.append(f'doc timestamp missing :: {rel} -> 更新时间')
            continue
        doc_stamp = match.group('stamp')
        if doc_stamp != state_stamp:
            gaps.append(
                'doc timestamp mismatch :: '
                f'{rel}={doc_stamp} vs {source}={state_stamp}'
            )
    return gaps


def verification_record_summary_section_gaps(
    verification_text: str,
    latest_audit: dict,
    expected_summary: dict[str, int],
    expected_timestamp: str,
) -> list[str]:
    gaps: list[str] = []
    latest_audit_section = extract_heading_section(verification_text, LATEST_AUDIT_SUMMARY_HEADING)
    if not latest_audit_section:
        return [
            'VERIFICATION_RECORD missing latest audit summary section :: '
            f'{LATEST_AUDIT_SUMMARY_HEADING}'
        ]

    state_summary = latest_audit.get('summary')
    if not isinstance(state_summary, dict):
        return ['execution-state latestAudit.summary missing or invalid']

    for label in LATEST_AUDIT_SUMMARY_LABELS:
        state_value = state_summary.get(label)
        if not isinstance(state_value, int):
            gaps.append(f'execution-state latestAudit.summary invalid :: {label}')
            continue
        expected_value = expected_summary[label]
        if state_value != expected_value:
            gaps.append(
                'execution-state latestAudit.summary mismatch :: '
                f'{label} expected {expected_value} got {state_value}'
            )
        marker = f'- {label}: {expected_value}'
        if marker not in latest_audit_section:
            gaps.append(f'VERIFICATION_RECORD audit summary marker missing :: {marker}')

    latest_timestamp = latest_audit.get('timestamp')
    if latest_timestamp is None:
        gaps.append('execution-state latestAudit.timestamp missing')
    else:
        try:
            latest_audit_stamp = datetime.fromisoformat(latest_timestamp).strftime('%Y-%m-%d %H:%M')
        except ValueError:
            gaps.append(f'execution-state latestAudit.timestamp invalid isoformat :: {latest_timestamp}')
            latest_audit_stamp = ''
        if latest_audit_stamp and latest_audit_stamp != expected_timestamp:
            gaps.append(
                'execution-state latestAudit.timestamp mismatch :: '
                f'expected {expected_timestamp} got {latest_audit_stamp}'
            )
        marker = f'{LATEST_AUDIT_SUMMARY_TIMESTAMP_PREFIX}{expected_timestamp}'
        if marker not in latest_audit_section:
            gaps.append(f'VERIFICATION_RECORD audit summary marker missing :: {marker}')

    latest_result = latest_audit.get('result')
    if latest_result != 'PASS':
        gaps.append(f'execution-state latestAudit.result invalid :: {latest_result}')
    if '- result: PASS' not in latest_audit_section:
        gaps.append('VERIFICATION_RECORD audit summary marker missing :: - result: PASS')

    latest_command = latest_audit.get('command')
    if latest_command != 'python3 scripts/root_archive_audit.py':
        gaps.append(f'execution-state latestAudit.command invalid :: {latest_command}')
    if '- command: python3 scripts/root_archive_audit.py' not in latest_audit_section:
        gaps.append(
            'VERIFICATION_RECORD audit summary marker missing :: '
            '- command: python3 scripts/root_archive_audit.py'
        )

    return gaps


def state_sync_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    fallback = state.get('blocking', {}).get('fallback', '')
    if not isinstance(fallback, str) or not fallback.strip():
        gaps.append('execution-state blocking.fallback missing or empty')
    else:
        for marker in STATE_SYNC_MARKERS:
            if marker not in fallback:
                gaps.append(f'execution-state blocking.fallback missing marker :: {marker}')

    next_steps = state.get('nextSteps')
    if not isinstance(next_steps, list) or len(next_steps) < 3:
        gaps.append('execution-state nextSteps missing fallback continuation entry')
        fallback_step = ''
    else:
        fallback_step = next_steps[2]
        if not isinstance(fallback_step, str) or not fallback_step.strip():
            gaps.append('execution-state nextSteps[2] missing or empty')
            fallback_step = ''
        else:
            for marker in STATE_SYNC_MARKERS:
                if marker not in fallback_step:
                    gaps.append(f'execution-state nextSteps[2] missing marker :: {marker}')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_STATE_SYNC_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing state sync section :: '
            f'{VERIFICATION_RECORD_STATE_SYNC_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_STATE_SYNC_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD state sync marker missing :: {marker}')

    if fallback and fallback_step and fallback != fallback_step:
        gaps.append('execution-state blocking.fallback and nextSteps[2] mismatch')

    return gaps


def git_status_short(path: Path) -> list[str]:
    result = subprocess.run(
        ['git', 'status', '--short'],
        cwd=path,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or 'unknown git error'
        raise RuntimeError(stderr)
    return [line.rstrip() for line in result.stdout.splitlines() if line.strip()]


def git_head(path: Path) -> str:
    result = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        cwd=path,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or 'unknown git error'
        raise RuntimeError(stderr)
    return result.stdout.strip()


def git_recent_heads(path: Path, limit: int = 2) -> list[str]:
    result = subprocess.run(
        ['git', 'log', f'-{limit}', '--format=%H'],
        cwd=path,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or 'unknown git error'
        raise RuntimeError(stderr)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def git_origin_url(path: Path) -> str:
    result = subprocess.run(
        ['git', 'remote', 'get-url', 'origin'],
        cwd=path,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or 'unknown git error'
        raise RuntimeError(stderr)
    return result.stdout.strip()


def root_head_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    try:
        root_head = git_head(ROOT)
        recent_heads = git_recent_heads(ROOT, limit=3)
    except RuntimeError as exc:
        return [f'root head lookup failed :: {exc}']

    if len(recent_heads) < 2:
        return [f'root recent head lookup returned too few commits :: {recent_heads}']

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_ROOT_HEAD_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing root head section :: '
            f'{VERIFICATION_RECORD_ROOT_HEAD_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_ROOT_HEAD_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD root head marker missing :: {marker}')
        head_minus_one_marker = f'- workspace-root HEAD~1 anchor: {recent_heads[1]}'
        if head_minus_one_marker not in section_text:
            gaps.append(f'VERIFICATION_RECORD root head marker missing :: {head_minus_one_marker}')
        current_head_note = '- workspace-root current HEAD note: current HEAD changes after every sync commit; machine anchor remains HEAD~1 plus git rev-parse HEAD command visibility'
        if current_head_note not in section_text:
            gaps.append(f'VERIFICATION_RECORD root head marker missing :: {current_head_note}')

    current_step = state.get('currentStep', '')
    for marker in ROOT_HEAD_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing root head marker :: {marker}')
    if recent_heads[1] not in current_step:
        gaps.append(f'execution-state currentStep missing root HEAD~1 hash :: {recent_heads[1]}')

    for marker in ROOT_HEAD_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing root head marker :: {marker}')

    recent_commits = state.get('recentCommits', {})
    workspace_root_record = recent_commits.get('workspace-root', '') if isinstance(recent_commits, dict) else ''
    head_match = re.search(r'([0-9a-f]{40})', workspace_root_record)
    if not head_match:
        gaps.append('execution-state recentCommits workspace-root missing pre-sync hash for root head check')
    elif head_match.group(1) != recent_heads[1]:
        gaps.append(
            'execution-state recentCommits workspace-root not aligned with HEAD~1 during root head check :: '
            f'recorded={head_match.group(1)} expected={recent_heads[1]} current={root_head}'
        )

    return gaps


def root_remote_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_ROOT_REMOTE_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing root remote section :: '
            f'{VERIFICATION_RECORD_ROOT_REMOTE_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_ROOT_REMOTE_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD root remote marker missing :: {marker}')

    current_step = state.get('currentStep', '')
    for marker in ROOT_REMOTE_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing root remote marker :: {marker}')

    for marker in ROOT_REMOTE_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing root remote marker :: {marker}')

    blocking_point = state.get('blocking', {}).get('point', '')
    if 'origin' not in blocking_point or '未配置' not in blocking_point:
        gaps.append('execution-state blocking.point missing explicit root origin blocker')

    remote_v = subprocess.run(
        ['git', 'remote', '-v'],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    remote_get = subprocess.run(
        ['git', 'remote', 'get-url', 'origin'],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    if remote_v.returncode != 0:
        stderr = remote_v.stderr.strip() or remote_v.stdout.strip() or 'unknown git error'
        gaps.append(f'git remote -v failed unexpectedly :: {stderr}')
    elif remote_v.stdout.strip():
        gaps.append(f'root git remote unexpectedly configured :: {remote_v.stdout.strip()}')

    expected_error = "error: No such remote 'origin'"
    actual_error = (remote_get.stderr.strip() or remote_get.stdout.strip())
    if remote_get.returncode == 0:
        gaps.append(f'root origin unexpectedly configured :: {remote_get.stdout.strip()}')
    elif expected_error not in actual_error:
        gaps.append(
            'git remote get-url origin unexpected stderr :: '
            f'{actual_error or 'missing stderr'}'
        )

    if section_text:
        if '- git remote -v: (no output)' not in section_text:
            gaps.append('VERIFICATION_RECORD root remote marker missing :: - git remote -v: (no output)')
        if f'- git remote get-url origin: {expected_error}' not in section_text:
            gaps.append(
                'VERIFICATION_RECORD root remote marker missing :: '
                f'- git remote get-url origin: {expected_error}'
            )

    return gaps



def blocking_snapshot_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    current_step = state.get('currentStep', '')
    for marker in BLOCKING_SNAPSHOT_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing blocking snapshot marker :: {marker}')

    for marker in BLOCKING_SNAPSHOT_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing blocking snapshot marker :: {marker}')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing blocking snapshot section :: '
            f'{VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_BLOCKING_SNAPSHOT_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD blocking snapshot marker missing :: {marker}')

    blocking = state.get('blocking', {})
    point = blocking.get('point', '')
    tried = blocking.get('tried')
    next_steps = state.get('nextSteps')

    required_point_markers = ('SUPABASE_SERVICE_ROLE_KEY', '测试账号', 'origin')
    for marker in required_point_markers:
        if marker not in point:
            gaps.append(f'execution-state blocking.point missing marker :: {marker}')
        if section_text and marker not in section_text:
            gaps.append(f'VERIFICATION_RECORD blocking snapshot section missing point marker :: {marker}')

    if not isinstance(tried, list) or not tried:
        gaps.append('execution-state blocking.tried missing or empty')
    else:
        recent_slice = tried[-3:]
        for item in recent_slice:
            if not isinstance(item, str) or not item.strip():
                gaps.append('execution-state blocking.tried contains blank item')
                continue
            if section_text and item not in section_text:
                gaps.append(f'VERIFICATION_RECORD blocking snapshot section missing tried item :: {item}')

    if not isinstance(next_steps, list) or len(next_steps) < 3:
        gaps.append('execution-state nextSteps missing blocking snapshot coverage')
    else:
        for marker in ('SUPABASE_SERVICE_ROLE_KEY', '测试账号', 'execution-state.json', 'VERIFICATION_RECORD.md'):
            if marker not in next_steps[0] and marker not in next_steps[1] and marker not in next_steps[2]:
                gaps.append(f'execution-state nextSteps missing marker across continuation plan :: {marker}')
        if section_text:
            for index, step in enumerate(next_steps[:3]):
                if step not in section_text:
                    gaps.append(f'VERIFICATION_RECORD blocking snapshot section missing nextSteps[{index}] entry')

    return gaps


def recent_commit_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    recent_commits = state.get('recentCommits')
    if not isinstance(recent_commits, dict):
        return ['execution-state recentCommits missing or invalid']

    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')
    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_RECENT_COMMITS_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing recent commit section :: '
            f'{VERIFICATION_RECORD_RECENT_COMMITS_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_RECENT_COMMITS_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD recent commit marker missing :: {marker}')

    current_step = state.get('currentStep', '')
    for marker in RECENT_COMMIT_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing recent commit marker :: {marker}')

    for marker in RECENT_COMMIT_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing recent commit marker :: {marker}')

    for repo_name, repo_path in sorted(RECENT_COMMIT_REPOS.items()):
        if repo_name not in recent_commits:
            gaps.append(f'execution-state recentCommits missing repo :: {repo_name}')
            continue
        recorded = recent_commits[repo_name]
        if not isinstance(recorded, str) or not recorded.strip():
            gaps.append(f'execution-state recentCommits invalid value :: {repo_name}')
            continue
        try:
            actual = git_head(repo_path)
        except RuntimeError as exc:
            gaps.append(f'git head lookup failed :: {repo_name} -> {exc}')
            continue
        if repo_name == 'workspace-root':
            if 'latest local HEAD' not in recorded:
                gaps.append(
                    'execution-state recentCommits workspace-root marker missing :: '
                    f'recorded={recorded}'
                )
            head_match = re.search(r'([0-9a-f]{40})', recorded)
            if not head_match:
                gaps.append(
                    'execution-state recentCommits workspace-root hash missing :: '
                    f'recorded={recorded}'
                )
            else:
                recorded_head = head_match.group(1)
                try:
                    recent_heads = git_recent_heads(repo_path, limit=3)
                except RuntimeError as exc:
                    gaps.append(f'git recent head lookup failed :: {repo_name} -> {exc}')
                else:
                    if len(recent_heads) < 2:
                        gaps.append(
                            'git recent head lookup returned too few commits :: '
                            f'{repo_name} recent={recent_heads}'
                        )
                    elif recorded_head != recent_heads[1]:
                        gaps.append(
                            'execution-state recentCommits workspace-root must match HEAD~1 :: '
                            f'recorded={recorded_head} expected={recent_heads[1]} recent={recent_heads}'
                        )
        elif not actual.startswith(recorded):
            gaps.append(
                'execution-state recentCommits mismatch :: '
                f'{repo_name} recorded={recorded} actual={actual}'
            )
        if section_text:
            if repo_name == 'workspace-root':
                if '- workspace-root:' not in section_text:
                    gaps.append('VERIFICATION_RECORD recent commit marker missing :: - workspace-root:')
                window_match = re.search(r'- workspace-root recent local heads \(pre-sync latest 2\): ([0-9a-f]{40}), ([0-9a-f]{40})', section_text)
                if not window_match:
                    gaps.append(
                        'VERIFICATION_RECORD recent commit marker missing :: '
                        '- workspace-root recent local heads (pre-sync latest 2): <head1>, <head2>'
                    )
                else:
                    recorded_window = [window_match.group(1), window_match.group(2)]
                    try:
                        recent_heads = git_recent_heads(repo_path, limit=3)
                    except RuntimeError as exc:
                        gaps.append(f'git recent head lookup failed :: {repo_name} -> {exc}')
                    else:
                        if len(recent_heads) < 3:
                            gaps.append(
                                'git recent head lookup returned too few commits :: '
                                f'{repo_name} recent={recent_heads}'
                            )
                        else:
                            expected_window = recent_heads[1:3]
                            if recorded_window != expected_window:
                                gaps.append(
                                    'VERIFICATION_RECORD workspace-root recent head window mismatch :: '
                                    f'recorded={recorded_window} expected={expected_window} recent={recent_heads}'
                                )
                            head1_marker = f'- workspace-root HEAD~1: {recent_heads[1]}'
                            if head1_marker not in section_text:
                                gaps.append(f'VERIFICATION_RECORD recent commit marker missing :: {head1_marker}')
                            head2_marker = f'- workspace-root HEAD~2: {recent_heads[2]}'
                            if head2_marker not in section_text:
                                gaps.append(f'VERIFICATION_RECORD recent commit marker missing :: {head2_marker}')
            else:
                expected_marker = f'- {repo_name}: {actual}'
                if expected_marker not in section_text:
                    gaps.append(f'VERIFICATION_RECORD recent commit marker missing :: {expected_marker}')
                try:
                    origin_url = git_origin_url(repo_path)
                except RuntimeError as exc:
                    gaps.append(f'git origin lookup failed :: {repo_name} -> {exc}')
                else:
                    expected_origin_command = f'- git -C {repo_name} remote get-url origin: {origin_url}'
                    if expected_origin_command not in section_text:
                        gaps.append(
                            'VERIFICATION_RECORD recent commit origin marker missing :: '
                            f'{expected_origin_command}'
                        )

    return gaps


def workspace_status_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_WORKSPACE_STATUS_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing workspace status section :: '
            f'{VERIFICATION_RECORD_WORKSPACE_STATUS_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_WORKSPACE_STATUS_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD workspace status marker missing :: {marker}')

    current_step = state.get('currentStep', '')
    for marker in WORKSPACE_STATUS_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing workspace status marker :: {marker}')

    for marker in WORKSPACE_STATUS_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing workspace status marker :: {marker}')

    status_lines = git_status_short(ROOT)
    unexpected = [line for line in status_lines if line not in WORKSPACE_STATUS_ALLOWED_SHORT]
    if unexpected:
        for line in unexpected:
            gaps.append(f'root git status unexpected dirty entry :: {line}')

    expected_line = WORKSPACE_STATUS_ALLOWED_SHORT[0]
    if expected_line not in status_lines:
        gaps.append(f'root git status missing expected entry :: {expected_line}')

    if section_text:
        if f'- git status --short: {expected_line}' not in section_text:
            gaps.append(
                'VERIFICATION_RECORD workspace status marker missing :: '
                f'- git status --short: {expected_line}'
            )
        if '- tracked files: clean tracked files' not in section_text:
            gaps.append(
                'VERIFICATION_RECORD workspace status marker missing :: '
                '- tracked files: clean tracked files'
            )

    return gaps



def blocking_recent_trail_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    blocking = state.get('blocking', {})
    tried = blocking.get('tried')
    if not isinstance(tried, list) or len(tried) < 3:
        return ['execution-state blocking.tried needs at least 3 entries for recent trail check']

    recent_slice = tried[-3:]
    normalized_slice: list[str] = []
    for item in recent_slice:
        if not isinstance(item, str) or not item.strip():
            gaps.append('execution-state blocking.tried recent 3 contains blank item')
            continue
        normalized_slice.append(item)

    if len(normalized_slice) == 3 and len(set(normalized_slice)) != 3:
        gaps.append('execution-state blocking.tried recent 3 duplicate entries :: ' + ' | '.join(normalized_slice))

    current_step = state.get('currentStep', '')
    for marker in BLOCKING_RECENT_TRAIL_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing blocking recent trail marker :: {marker}')

    for marker in BLOCKING_RECENT_TRAIL_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing blocking recent trail marker :: {marker}')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_BLOCKING_RECENT_TRAIL_HEADING)
    if not section_text:
        gaps.append('VERIFICATION_RECORD missing blocking recent trail section :: ' f'{VERIFICATION_RECORD_BLOCKING_RECENT_TRAIL_HEADING}')
        return gaps

    for marker in VERIFICATION_RECORD_BLOCKING_RECENT_TRAIL_MARKERS:
        if marker not in section_text:
            gaps.append(f'VERIFICATION_RECORD blocking recent trail marker missing :: {marker}')

    for idx, item in enumerate(normalized_slice, start=1):
        expected_marker = f'- recent 3 [{idx}]: {item}'
        if expected_marker not in section_text:
            gaps.append(f'VERIFICATION_RECORD blocking recent trail marker missing :: {expected_marker}')

    if normalized_slice:
        expected_order = f"- tail order exact snapshot: {' -> '.join(normalized_slice)}"
        if expected_order not in section_text:
            gaps.append(f'VERIFICATION_RECORD blocking recent trail marker missing :: {expected_order}')

    if '- duplicate check: no duplicates across recent 3' not in section_text:
        gaps.append('VERIFICATION_RECORD blocking recent trail marker missing :: - duplicate check: no duplicates across recent 3')

    snapshot_section = extract_heading_section(verification_text, VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING)
    if not snapshot_section:
        gaps.append('VERIFICATION_RECORD missing blocking snapshot section for recent trail cross-check :: ' f'{VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING}')
    else:
        for item in normalized_slice:
            if item not in snapshot_section:
                gaps.append(f'VERIFICATION_RECORD blocking snapshot section missing recent trail item :: {item}')

    return gaps


def latest_blocking_tried_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    blocking = state.get('blocking', {})
    tried = blocking.get('tried')
    if not isinstance(tried, list) or not tried:
        return ['execution-state blocking.tried missing or empty for latest tried check']

    latest_entry = tried[-1]
    if not isinstance(latest_entry, str) or not latest_entry.strip():
        return ['execution-state blocking.tried latest entry missing or blank']

    current_step = state.get('currentStep', '')
    for marker in LATEST_BLOCKING_TRIED_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing latest blocking.tried marker :: {marker}')
    if latest_entry not in current_step:
        gaps.append('execution-state currentStep missing latest blocking.tried exact entry')

    for marker in LATEST_BLOCKING_TRIED_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing latest blocking.tried marker :: {marker}')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_LATEST_BLOCKING_TRIED_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing latest blocking.tried section :: '
            f'{VERIFICATION_RECORD_LATEST_BLOCKING_TRIED_HEADING}'
        )
        return gaps

    for marker in VERIFICATION_RECORD_LATEST_BLOCKING_TRIED_MARKERS:
        if marker not in section_text:
            gaps.append(f'VERIFICATION_RECORD latest blocking.tried marker missing :: {marker}')

    exact_marker = f'- latest tried entry exact snapshot: {latest_entry}'
    if exact_marker not in section_text:
        gaps.append(f'VERIFICATION_RECORD latest blocking.tried marker missing :: {exact_marker}')

    snapshot_section = extract_heading_section(verification_text, VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING)
    if not snapshot_section:
        gaps.append(
            'VERIFICATION_RECORD missing blocking snapshot section for latest tried cross-check :: '
            f'{VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING}'
        )
    elif latest_entry not in snapshot_section:
        gaps.append('VERIFICATION_RECORD blocking snapshot section missing latest blocking.tried entry')

    return gaps


def blocking_point_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    point = state.get('blocking', {}).get('point', '')
    current_step = state.get('currentStep', '')
    if not isinstance(point, str) or not point.strip():
        return ['execution-state blocking.point missing or empty']

    for marker in BLOCKING_POINT_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing blocking.point marker :: {marker}')
    for marker in BLOCKING_POINT_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing blocking.point marker :: {marker}')

    if point not in current_step:
        gaps.append('execution-state currentStep missing exact blocking.point snapshot')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_BLOCKING_POINT_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing blocking point section :: '
            f'{VERIFICATION_RECORD_BLOCKING_POINT_HEADING}'
        )
        return gaps

    for marker in VERIFICATION_RECORD_BLOCKING_POINT_MARKERS:
        if marker not in section_text:
            gaps.append(f'VERIFICATION_RECORD blocking.point marker missing :: {marker}')

    exact_marker = f'- blocking.point exact snapshot: {point}'
    if exact_marker not in section_text:
        gaps.append('VERIFICATION_RECORD blocking.point exact snapshot mismatch')

    blocking_snapshot_section = extract_heading_section(verification_text, VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING)
    if not blocking_snapshot_section:
        gaps.append(
            'VERIFICATION_RECORD missing blocking snapshot section :: '
            f'{VERIFICATION_RECORD_BLOCKING_SNAPSHOT_HEADING}'
        )
    elif exact_marker not in blocking_snapshot_section:
        gaps.append('VERIFICATION_RECORD blocking snapshot section missing exact blocking.point snapshot')

    return gaps


def blocking_status_consistency_gaps() -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    blocking = state.get('blocking', {})
    status = blocking.get('status')
    point = blocking.get('point', '')
    if status != 'partial':
        gaps.append(f'execution-state blocking.status invalid :: {status}')

    current_step = state.get('currentStep', '')
    for marker in BLOCKING_STATUS_REQUIRED_MARKERS['currentStep']:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing blocking.status marker :: {marker}')

    for marker in BLOCKING_STATUS_REQUIRED_MARKERS['VERIFICATION_RECORD.md']:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD missing blocking.status marker :: {marker}')

    section_text = extract_heading_section(verification_text, VERIFICATION_RECORD_BLOCKING_STATUS_HEADING)
    if not section_text:
        gaps.append(
            'VERIFICATION_RECORD missing blocking status section :: '
            f'{VERIFICATION_RECORD_BLOCKING_STATUS_HEADING}'
        )
    else:
        for marker in VERIFICATION_RECORD_BLOCKING_STATUS_MARKERS:
            if marker not in section_text:
                gaps.append(f'VERIFICATION_RECORD blocking status marker missing :: {marker}')
        status_marker = f'- blocking.status: {status}'
        if status_marker not in section_text:
            gaps.append(f'VERIFICATION_RECORD blocking status marker missing :: {status_marker}')

    for marker in ('SUPABASE_SERVICE_ROLE_KEY', '测试账号', 'origin'):
        if marker not in point:
            gaps.append(f'execution-state blocking.point missing blocker for blocking.status context :: {marker}')

    return gaps


def verification_record_consistency_gaps(expected_summary: dict[str, int]) -> list[str]:
    gaps: list[str] = []
    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    verification_text = VERIFICATION_RECORD.read_text(encoding='utf-8', errors='ignore')

    updated_at = state.get('updatedAt', '')
    current_step = state.get('currentStep', '')
    latest_audit = state.get('latestAudit', {})
    match = VERIFICATION_TIMESTAMP_RE.search(verification_text)
    if not match:
        gaps.append('verification record timestamp missing :: VERIFICATION_RECORD.md -> 更新时间')
        verification_stamp = ''
    else:
        verification_stamp = match.group('stamp')

    try:
        state_stamp = datetime.fromisoformat(updated_at).strftime('%Y-%m-%d %H:%M')
    except ValueError:
        gaps.append(f'execution-state updatedAt invalid isoformat :: {updated_at}')
        state_stamp = ''

    if state_stamp and verification_stamp and state_stamp != verification_stamp:
        gaps.append(
            'verification timestamp mismatch :: '
            f'execution-state.json={state_stamp} vs VERIFICATION_RECORD.md={verification_stamp}'
        )

    required_current_step_markers = (
        'execution-state.json',
        'VERIFICATION_RECORD.md',
        'python3 scripts/root_archive_audit.py',
        'RESULT: PASS',
    )
    for marker in required_current_step_markers:
        if marker not in current_step:
            gaps.append(f'execution-state currentStep missing marker :: {marker}')

    required_verification_markers = (
        'execution-state.json',
        'python3 scripts/root_archive_audit.py',
        'RESULT: PASS',
        '更新时间：',
    )
    for marker in required_verification_markers:
        if marker not in verification_text:
            gaps.append(f'VERIFICATION_RECORD marker missing :: {marker}')

    if '最近一轮归档审计记录同步校验' not in verification_text:
        gaps.append('VERIFICATION_RECORD missing latest audit section :: 最近一轮归档审计记录同步校验')

    latest_audit_timestamp = latest_audit.get('timestamp')
    if latest_audit_timestamp != updated_at:
        gaps.append(
            'execution-state latestAudit.timestamp mismatch :: '
            f'updatedAt={updated_at} vs latestAudit.timestamp={latest_audit_timestamp}'
        )

    gaps.extend(
        verification_record_summary_section_gaps(
            verification_text,
            latest_audit,
            expected_summary,
            state_stamp,
        )
    )

    return gaps


def main() -> int:
    manifest_text = MANIFEST.read_text(encoding='utf-8')
    entries = top_level_entries()
    missing_readmes = find_missing_readmes()
    empty_dirs = find_empty_dirs()
    manifest_gaps = manifest_missing(entries, manifest_text)
    unexpected = unexpected_entries(entries)
    archive_gaps = archive_marker_gaps()
    navigation_gaps = navigation_marker_gaps()
    first_screen_notice_gaps = first_screen_archive_notice_gaps()
    manifest_section_issues = manifest_section_gaps(manifest_text)
    manifest_classification_issues = manifest_classification_coverage_gaps()
    retained_issues = retained_baseline_gaps(manifest_text)
    doc_reference_issues = doc_reference_gaps()
    blocker_consistency_issues = blocker_consistency_gaps()
    recent_commit_issues = recent_commit_consistency_gaps()
    root_head_issues = root_head_consistency_gaps()
    root_remote_issues = root_remote_consistency_gaps()
    blocking_snapshot_issues = blocking_snapshot_consistency_gaps()
    workspace_status_issues = workspace_status_consistency_gaps()
    blocking_status_issues = blocking_status_consistency_gaps()
    latest_blocking_tried_issues = latest_blocking_tried_consistency_gaps()
    blocking_recent_trail_issues = blocking_recent_trail_consistency_gaps()
    execution_plan_issues = execution_plan_consistency_gaps()
    completed_sequence_issues = completed_sequence_consistency_gaps()
    fallback_route_issues = fallback_route_consistency_gaps()
    blocking_point_issues = blocking_point_consistency_gaps()

    state = json.loads(EXECUTION_STATE.read_text(encoding='utf-8'))
    updated_at = state.get('updatedAt', '')
    try:
        state_stamp = datetime.fromisoformat(updated_at).strftime('%Y-%m-%d %H:%M')
    except ValueError:
        state_stamp = ''
    doc_timestamp_issues = doc_timestamp_gaps(state_stamp)
    state_sync_issues = state_sync_gaps()

    summary_counts = {
        'top-level entries checked': len(entries),
        'missing README dirs': len(missing_readmes),
        'empty dirs': len(empty_dirs),
        'manifest missing entries': len(manifest_gaps),
        'unexpected top-level entries': len(unexpected),
        'archive marker gaps': len(archive_gaps),
        'navigation marker gaps': len(navigation_gaps),
        'first-screen archive notice gaps': len(first_screen_notice_gaps),
        'manifest section issues': len(manifest_section_issues),
        'manifest classification issues': len(manifest_classification_issues),
        'retained baseline issues': len(retained_issues),
        'doc reference issues': len(doc_reference_issues),
        'blocker consistency issues': len(blocker_consistency_issues),
        'doc timestamp issues': len(doc_timestamp_issues),
        'recent commit consistency issues': len(recent_commit_issues),
        'root head consistency issues': len(root_head_issues),
        'root remote consistency issues': len(root_remote_issues),
        'blocking snapshot consistency issues': len(blocking_snapshot_issues),
        'workspace status consistency issues': len(workspace_status_issues),
        'blocking status consistency issues': len(blocking_status_issues),
        'latest blocking tried consistency issues': len(latest_blocking_tried_issues),
        'blocking recent trail consistency issues': len(blocking_recent_trail_issues),
        'verification record consistency issues': 0,
        'execution plan consistency issues': len(execution_plan_issues),
        'completed sequence consistency issues': len(completed_sequence_issues),
        'fallback route consistency issues': len(fallback_route_issues),
        'blocking point consistency issues': len(blocking_point_issues),
    }
    verification_record_issues = state_sync_issues + verification_record_consistency_gaps(summary_counts)
    summary_counts['verification record consistency issues'] = len(verification_record_issues)

    print('== Root archive audit ==')
    print(f'root: {ROOT}')
    for label in LATEST_AUDIT_SUMMARY_LABELS:
        print(f'{label}: {summary_counts[label]}')

    if missing_readmes:
        print('\n[missing README dirs]')
        print('\n'.join(missing_readmes))
    if empty_dirs:
        print('\n[empty dirs]')
        print('\n'.join(empty_dirs))
    if manifest_gaps:
        print('\n[manifest missing entries]')
        print('\n'.join(manifest_gaps))
    if unexpected:
        print('\n[unexpected top-level entries]')
        print('\n'.join(unexpected))
    if archive_gaps:
        print('\n[archive marker gaps]')
        print('\n'.join(archive_gaps))
    if navigation_gaps:
        print('\n[navigation marker gaps]')
        print('\n'.join(navigation_gaps))
    if first_screen_notice_gaps:
        print('\n[first-screen archive notice gaps]')
        print('\n'.join(first_screen_notice_gaps))
    if manifest_section_issues:
        print('\n[manifest section issues]')
        print('\n'.join(manifest_section_issues))
    if manifest_classification_issues:
        print('\n[manifest classification issues]')
        print('\n'.join(manifest_classification_issues))
    if retained_issues:
        print('\n[retained baseline issues]')
        print('\n'.join(retained_issues))
    if doc_reference_issues:
        print('\n[doc reference issues]')
        print('\n'.join(doc_reference_issues))
    if blocker_consistency_issues:
        print('\n[blocker consistency issues]')
        print('\n'.join(blocker_consistency_issues))
    if doc_timestamp_issues:
        print('\n[doc timestamp issues]')
        print('\n'.join(doc_timestamp_issues))
    if recent_commit_issues:
        print('\n[recent commit consistency issues]')
        print('\n'.join(recent_commit_issues))
    if root_head_issues:
        print('\n[root head consistency issues]')
        print('\n'.join(root_head_issues))
    if root_remote_issues:
        print('\n[root remote consistency issues]')
        print('\n'.join(root_remote_issues))
    if blocking_snapshot_issues:
        print('\n[blocking snapshot consistency issues]')
        print('\n'.join(blocking_snapshot_issues))
    if workspace_status_issues:
        print('\n[workspace status consistency issues]')
        print('\n'.join(workspace_status_issues))
    if blocking_status_issues:
        print('\n[blocking status consistency issues]')
        print('\n'.join(blocking_status_issues))
    if latest_blocking_tried_issues:
        print('\n[latest blocking tried consistency issues]')
        print('\n'.join(latest_blocking_tried_issues))
    if blocking_recent_trail_issues:
        print('\n[blocking recent trail consistency issues]')
        print('\n'.join(blocking_recent_trail_issues))
    if verification_record_issues:
        print('\n[verification record consistency issues]')
        print('\n'.join(verification_record_issues))
    if execution_plan_issues:
        print('\n[execution plan consistency issues]')
        print('\n'.join(execution_plan_issues))
    if completed_sequence_issues:
        print('\n[completed sequence consistency issues]')
        print('\n'.join(completed_sequence_issues))
    if fallback_route_issues:
        print('\n[fallback route consistency issues]')
        print('\n'.join(fallback_route_issues))
    if blocking_point_issues:
        print('\n[blocking point consistency issues]')
        print('\n'.join(blocking_point_issues))

    failed = bool(
        missing_readmes
        or empty_dirs
        or manifest_gaps
        or unexpected
        or archive_gaps
        or navigation_gaps
        or first_screen_notice_gaps
        or manifest_section_issues
        or manifest_classification_issues
        or retained_issues
        or doc_reference_issues
        or blocker_consistency_issues
        or doc_timestamp_issues
        or recent_commit_issues
        or root_head_issues
        or root_remote_issues
        or blocking_snapshot_issues
        or workspace_status_issues
        or blocking_status_issues
        or latest_blocking_tried_issues
        or blocking_recent_trail_issues
        or verification_record_issues
        or execution_plan_issues
        or completed_sequence_issues
        or fallback_route_issues
        or blocking_point_issues
    )
    if failed:
        print('\nRESULT: FAIL')
        return 1

    print('\nRESULT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
