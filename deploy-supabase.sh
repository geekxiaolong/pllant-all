#!/bin/bash

set -e

cat <<'EOF'
[Archived root script]

deploy-supabase.sh 曾用于拆分前/迁移早期在根目录部署 Supabase Edge Functions。
当前后端 API 已独立至 ./heart-plant-api，请不要再从根目录执行该脚本。

请改为：
- cd heart-plant-api
- 按该仓库 README/部署文档执行 Supabase CLI、环境变量与发布流程

参考文档：README.md、THREE-APP-DEPLOYMENT.md、heart-plant-api/README.md
EOF
