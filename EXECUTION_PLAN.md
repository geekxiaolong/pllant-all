# 三端分离执行清单

## 目标
将当前单体项目拆分为以下三个独立仓库，并保证功能、UI、数据结构与旧版保持一致：

1. `heart-plant`：用户前端
2. `heart-plant-admin`：管理后台
3. `heart-plant-api`：后端 API

## 完成定义
- 三端都能独立启动/构建
- API 可运行并可验证 `/health` 与 `/admin/*`
- 用户前端与管理后台 UI 保持与旧版一致（布局、样式、交互、文案）
- 核心链路完成验证
- 每一阶段产出 GitHub commit

## 任务清单

### A. API 仓库（heart-plant-api）
- [x] A1. 独立建仓并复制后端代码
- [x] A2. 新增 admin 路由模块
- [x] A3. 验证 `deno` 环境
- [x] A4. 启动 API 并验证 `/health`
- [x] A5. 验证 `/admin/users`
- [x] A6. 验证 `/admin/plants`
- [x] A7. 继续拆分 `index.tsx`
- [x] A8. 补更多 `/admin/*` 接口

### B. 用户前端（heart-plant）
- [x] B1. 独立建仓
- [x] B2. 独立入口
- [x] B3. 构建修复（Supabase 配置恢复）
- [x] B4. `npm run build` 验证通过
- [x] B5. 抽公共 API client
- [x] B6. 清理 admin 无关引用
- [x] B7. 本地启动验证
- [x] B8. UI 一致性检查

### C. 管理后台（heart-plant-admin）
- [x] C1. 独立建仓
- [x] C2. 独立入口
- [x] C3. 构建修复（Supabase 配置恢复）
- [x] C4. `npm run build` 验证通过
- [x] C5. 接 admin API
- [x] C6. 清理用户端无关引用
- [x] C7. 本地启动验证
- [x] C8. UI 一致性检查

### D. 共用层与文档
- [x] D1. 仓库说明文档
- [x] D2. 使用文档
- [x] D3. 抽共用类型
- [x] D4. 抽共用 API 封装
- [x] D5. 验证记录文档
- [x] D6. 部署说明文档

## 执行规则
1. 未达到完成定义前不要停止
2. 每完成一步必须验证
3. 如果卡住超过 10 分钟，必须记录阻塞点、已尝试方法、备选方案
4. 每次实质改动都要 commit + push GitHub
5. 以 GitHub commit 和验证结果作为唯一进度凭证
