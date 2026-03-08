#!/bin/bash

set -e

cat <<'EOF'
[Archived root script]

git-init.sh 曾用于拆分前把根目录整体初始化并推送到单个 GitHub 仓库。
当前项目已拆分为三个独立仓库，根目录仅保留历史归档与导航资料。

请不要再在根目录执行 git init / git remote add origin 的单体流程。
请分别进入以下子仓库管理远程仓库：
- heart-plant/
- heart-plant-admin/
- heart-plant-api/

参考文档：README.md、GITHUB_SETUP.md、THREE-APP-SPLIT-STATUS.md
EOF
