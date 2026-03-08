#!/bin/bash

set -e

cat <<'EOF'
[Archived root script]

quick-upload.sh 曾用于把根目录单体项目快速上传到 GitHub。
当前项目已拆分为 heart-plant / heart-plant-admin / heart-plant-api 三个独立仓库。

请不要再在根目录执行旧上传流程。
请进入目标子仓库，按其远程仓库配置独立提交和推送。

参考文档：README.md、UPLOAD_TO_GITHUB.md、THREE-APP-SPLIT-STATUS.md
EOF
