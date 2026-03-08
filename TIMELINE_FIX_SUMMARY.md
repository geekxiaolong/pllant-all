# Timeline API 404 修复总结（历史归档）

> 归档说明：本文是早期关于 Timeline API 缺失的修复记录，现已转为历史文档。
> 
> 三端分离后的当前工程入口：
> - 用户前端：`./heart-plant`
> - 管理后台：`./heart-plant-admin`
> - 后端 API：`./heart-plant-api`
> 
> 请优先阅读：`README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md`、`VERIFICATION_RECORD.md`。

## 文档用途
- 保留 Timeline 相关接口缺失问题的历史背景
- 便于对照旧单体阶段与三端分离后的接口演进
- 不再作为当前开发任务清单

## 当前状态
- Timeline 相关能力应以 `heart-plant-api` 当前路由实现为准
- 前端页面接入应以 `heart-plant` 当前代码为准
- 根目录文档仅承担导航与归档职责

## 建议阅读路径
1. 看 `heart-plant-api` 中最新 timeline / journal / moments 路由实现
2. 看 `heart-plant` 中对应页面的当前接入方式
3. 仅在需要追溯历史问题来源时回看本文
