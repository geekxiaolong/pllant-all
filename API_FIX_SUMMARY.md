# API 通信问题修复总结（历史归档）

> 归档说明：本文记录的是**拆分前/早期迁移阶段**的 API 通信修复背景，保留用于排障追溯。
> 
> 当前项目已调整为三端分离，请勿再把根目录当作单体主工程继续开发或部署：
> - 用户前端：`./heart-plant`
> - 管理后台：`./heart-plant-admin`
> - 后端 API：`./heart-plant-api`
> 
> 当前入口请优先查看：`README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md`、`VERIFICATION_RECORD.md`。

## 文档用途
- 仅作为历史问题修复记录
- 可用于对照迁移前后的接口问题来源
- 不再作为当前实施步骤或部署说明

## 当前状态
- 公共 API URL / Header 封装已在三端分离仓库中落地
- 根目录仅保留归档与导航说明，不再作为主开发入口
- 如需继续排查接口问题，请到对应子仓库查看最新实现与提交记录

## 建议阅读路径
1. 先看 `THREE-APP-DEPLOYMENT.md` 了解三端职责
2. 再到对应仓库查看最新代码：
   - `heart-plant/src`
   - `heart-plant-admin/src`
   - `heart-plant-api/supabase/functions/server`
3. 历史修复背景需要追溯时，再回看本文
