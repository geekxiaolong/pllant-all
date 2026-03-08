#!/bin/bash

set -e

cat <<'EOF'
[Archived root script]

git-push.sh 曾用于拆分前向根目录单体仓库执行统一推送。
当前项目已拆分为三个独立 Git 仓库，根目录不再作为主代码仓库推送入口。

请改为分别进入以下仓库执行 git status / git commit / git push：
- heart-plant/
- heart-plant-admin/
- heart-plant-api/

若需提交根目录归档文档，请先确认该根目录仓库是否配置 origin。
参考文档：README.md、GITHUB_UPLOAD_GUIDE.md、THREE-APP-SPLIT-STATUS.md
EOF
