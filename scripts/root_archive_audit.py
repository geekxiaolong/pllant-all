#!/usr/bin/env python3
from __future__ import annotations

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
    missing = []
    for name in entries:
        if name not in manifest_text:
            missing.append(name)
    return missing


def unexpected_entries(entries: list[str]) -> list[str]:
    return sorted(set(entries) - TOP_LEVEL_EXPECTED)


def main() -> int:
    manifest_text = MANIFEST.read_text(encoding='utf-8')
    entries = top_level_entries()
    missing_readmes = find_missing_readmes()
    empty_dirs = find_empty_dirs()
    manifest_gaps = manifest_missing(entries, manifest_text)
    unexpected = unexpected_entries(entries)

    print('== Root archive audit ==')
    print(f'root: {ROOT}')
    print(f'top-level entries checked: {len(entries)}')
    print(f'missing README dirs: {len(missing_readmes)}')
    print(f'empty dirs: {len(empty_dirs)}')
    print(f'manifest missing entries: {len(manifest_gaps)}')
    print(f'unexpected top-level entries: {len(unexpected)}')

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

    failed = bool(missing_readmes or empty_dirs or manifest_gaps or unexpected)
    if failed:
        print('\nRESULT: FAIL')
        return 1

    print('\nRESULT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
