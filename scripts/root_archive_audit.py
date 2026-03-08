#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_NAMES = {'.git', 'node_modules', 'heart-plant', 'heart-plant-admin', 'heart-plant-api'}
MANIFEST = ROOT / 'ROOT_ARCHIVE_MANIFEST.md'

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


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_NAMES for part in path.parts)


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


def main() -> int:
    manifest_text = MANIFEST.read_text(encoding='utf-8')
    entries = top_level_entries()
    missing_readmes = find_missing_readmes()
    empty_dirs = find_empty_dirs()
    manifest_gaps = manifest_missing(entries, manifest_text)
    unexpected = unexpected_entries(entries)
    archive_gaps = archive_marker_gaps()
    navigation_gaps = navigation_marker_gaps()
    manifest_section_issues = manifest_section_gaps(manifest_text)
    manifest_classification_issues = manifest_classification_coverage_gaps()

    print('== Root archive audit ==')
    print(f'root: {ROOT}')
    print(f'top-level entries checked: {len(entries)}')
    print(f'missing README dirs: {len(missing_readmes)}')
    print(f'empty dirs: {len(empty_dirs)}')
    print(f'manifest missing entries: {len(manifest_gaps)}')
    print(f'unexpected top-level entries: {len(unexpected)}')
    print(f'archive marker gaps: {len(archive_gaps)}')
    print(f'navigation marker gaps: {len(navigation_gaps)}')
    print(f'manifest section issues: {len(manifest_section_issues)}')
    print(f'manifest classification issues: {len(manifest_classification_issues)}')

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
    if manifest_section_issues:
        print('\n[manifest section issues]')
        print('\n'.join(manifest_section_issues))
    if manifest_classification_issues:
        print('\n[manifest classification issues]')
        print('\n'.join(manifest_classification_issues))

    failed = bool(
        missing_readmes
        or empty_dirs
        or manifest_gaps
        or unexpected
        or archive_gaps
        or navigation_gaps
        or manifest_section_issues
        or manifest_classification_issues
    )
    if failed:
        print('\nRESULT: FAIL')
        return 1

    print('\nRESULT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
