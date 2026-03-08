# GITHUB_SETUP.md（历史根目录 GitHub 配置说明 / 已归档）

更新时间：2026-03-09 01:02 (Asia/Shanghai)

本文件原用于把根目录整体初始化并推送到单一 GitHub 仓库。
在当前三端分离结构下，该做法已不再是默认推荐路径。

## 当前正确做法

按改动所在仓库分别处理：
- `heart-plant/`
- `heart-plant-admin/`
- `heart-plant-api/`

根目录仅保留迁移文档、验证记录和历史归档资料。

## 当前注意事项

- 三个子仓库均已配置各自 `origin`
- 根目录未配置 `origin`
- 因此不要再按本文件旧步骤在根目录执行 `git init` / `git remote add origin` / `git push -u origin main`

## 推荐入口

- `README.md`
- `execution-state.json`
- `THREE-APP-DEPLOYMENT.md`
- `VERIFICATION_RECORD.md`

如需保留旧版命令，仅作历史参考，不再作为当前执行手册。