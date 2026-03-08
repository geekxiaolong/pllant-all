# 上传到GitHub说明（历史根目录上传说明 / 已归档）

更新时间：2026-03-09 01:02 (Asia/Shanghai)

这份中文说明基于旧的单体/根目录整体上传流程。
当前已经完成三端拆分，因此不再建议把根目录当作唯一 GitHub 仓库处理。

## 现在应该怎么做

按修改位置分别进入对应仓库：
- `heart-plant/`
- `heart-plant-admin/`
- `heart-plant-api/`

分别执行各自的 `git add / commit / push`。

## 根目录说明

根目录当前主要承载：
- 迁移说明
- 执行计划
- 验证记录
- 历史脚本与历史文档

且根目录尚未配置远程 `origin`，所以这里只适合本地留痕，不适合作为默认推送入口。

## 推荐入口

- `README.md`
- `execution-state.json`
- `THREE-APP-DEPLOYMENT.md`
- `VERIFICATION_RECORD.md`
