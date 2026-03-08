#!/bin/bash

set -e

cat <<'EOF'
[Archived root script]

deploy.sh 曾用于拆分前单体项目的根目录部署流程。
当前工作区已切换为三端分离，请不要再在根目录执行旧部署脚本。

请改为进入对应子仓库操作：
- 用户前端：cd heart-plant && npm run build
- 管理后台：cd heart-plant-admin && npm run build
- 后端 API：cd heart-plant-api && deno task serve / 按该仓库 README 部署

参考文档：README.md、START_HERE.md、THREE-APP-DEPLOYMENT.md
EOF
