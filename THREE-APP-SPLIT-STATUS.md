# 三端分离开发进度（归档状态说明）

更新时间：2026-03-09 07:21 (Asia/Shanghai)

本文件原本用于记录三端拆分早期的阶段性进度。
目前以 `execution-state.json` 作为**唯一持续更新的执行状态源**，本文件调整为归档摘要，避免与最新状态重复或冲突。

## 当前标准进度入口

请优先查看：
1. `EXECUTION_PLAN.md`：完整任务清单与完成定义
2. `execution-state.json`：当前步骤、阻塞、下一步、最近提交
3. `VERIFICATION_RECORD.md`：已完成的运行/构建/UI 验证记录
4. `THREE-APP-DEPLOYMENT.md`：三端分离后的部署说明

## 已完成的关键里程碑（归档摘要）

- 已拆分出三个独立子仓库：
  - `heart-plant/`：用户前端
  - `heart-plant-admin/`：管理后台
  - `heart-plant-api/`：后端 API
- 两个前端已完成独立入口、构建回归与本地启动回归
- API 已完成 `index.tsx` 进一步路由拆分，并补齐更多 `/admin/*` 接口
- 根目录入口文档已改为三端分离导航，不再将根目录当作单体主入口
- 已补充验证记录与三端部署说明

## 当前剩余阻塞（以 execution-state.json 为准）

1. 缺少 `SUPABASE_SERVICE_ROLE_KEY`，真实写库/对象存储联调无法完成
2. 缺少测试账号或有效 Supabase 登录态，登录后核心页面截图回归无法完成
3. 根目录仓库未配置 `origin`，因此根目录文档提交暂不能直接 push

## 说明

本文件不再滚动维护逐项状态。
如需继续执行任务，请直接按 `execution-state.json -> nextSteps` 续跑。
