# GITHUB_UPLOAD_GUIDE.md（历史根目录上传指南 / 已归档）

更新时间：2026-03-09 01:00 (Asia/Shanghai)

本文件对应的是**拆分前/迁移早期**把整个根目录视为主要 GitHub 仓库的上传说明。
当前三端已经拆分为独立仓库，因此这里的很多步骤**不再适合作为默认操作指南**。

## 当前正确的 GitHub 提交流程

请按实际修改位置提交：

- 用户前端改动 → `heart-plant/`
- 管理后台改动 → `heart-plant-admin/`
- 后端 API 改动 → `heart-plant-api/`
- 根目录仅处理迁移文档/历史归档说明

> 也就是说：**默认不要再把根目录当作唯一代码仓库来初始化、提交、推送。**

## 当前状态

- `heart-plant/` 已配置 `origin`
- `heart-plant-admin/` 已配置 `origin`
- `heart-plant-api/` 已配置 `origin`
- 根目录当前**未配置 `origin`**，因此即使提交了文档，也不能直接 `git push origin HEAD`

## 如果你要推送三端仓库

### 用户前端
```bash
cd heart-plant
git status
git add .
git commit -m "docs: ..."   # 或 feat/fix
git push origin HEAD
```

### 管理后台
```bash
cd heart-plant-admin
git status
git add .
git commit -m "docs: ..."   # 或 feat/fix
git push origin HEAD
```

### 后端 API
```bash
cd heart-plant-api
git status
git add .
git commit -m "docs: ..."   # 或 feat/fix
git push origin HEAD
```

## 如果你修改的是根目录文档

当前根目录只建议承载：
- `README.md`
- `START_HERE.md`
- `DEPLOYMENT.md`
- `EXECUTION_PLAN.md`
- `execution-state.json`
- `VERIFICATION_RECORD.md`
- 其他历史说明/归档资料

但请注意：
- 根目录仓库未配置远程 `origin`
- 因此根目录变更目前只能**本地提交留痕**，不能按“推送到对应 GitHub 仓库”完成远端同步
- 若后续需要根目录独立远程仓库，需先补充远程地址再 push

## 为什么归档本文件

旧版上传指南默认：
- 在根目录 `git init`
- 在根目录设置唯一 `origin`
- 把整个项目视为一个仓库整体推送

这与当前三端分离结构不一致，继续照做会带来这些风险：
- 混淆根目录归档区与子仓库开发区
- 误把旧单体代码再次作为主仓库上传
- 让执行记录与实际远程仓库历史错位

## 当前推荐阅读

- 总入口：`README.md`
- 当前状态：`execution-state.json`
- 部署说明：`THREE-APP-DEPLOYMENT.md`
- 验证记录：`VERIFICATION_RECORD.md`

如需保留本文件原始长版命令，可视为历史参考，但不要再作为默认执行手册。