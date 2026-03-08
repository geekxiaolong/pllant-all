# UPLOAD_TO_GITHUB.md（历史根目录上传说明 / 已归档）

更新时间：2026-03-09 01:02 (Asia/Shanghai)

本文件描述的是拆分前把根目录整体上传到单一 GitHub 仓库的流程。
当前项目已拆为三端独立仓库，因此这里改为归档说明。

## 当前提交原则

- 用户前端改动：在 `heart-plant/` 提交并推送
- 管理后台改动：在 `heart-plant-admin/` 提交并推送
- API 改动：在 `heart-plant-api/` 提交并推送
- 根目录改动：仅本地留痕，除非后续为根目录单独配置远程仓库

## 当前限制

根目录仓库目前没有 `origin`，因此不能继续按旧文档中的根目录 `git push -u origin main` 执行。

## 建议查看

- `README.md`
- `START_HERE.md`
- `execution-state.json`
- `THREE-APP-DEPLOYMENT.md`

旧版长篇 GitHub 上传命令请视为历史背景，不再作为默认操作。