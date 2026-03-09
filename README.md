# HeartPlant 三端分离工作区

更新时间：2026-03-09 14:45 (Asia/Shanghai)

这个根目录 **不再作为单体应用直接开发/部署入口**，而是三端拆分后的工作区与历史归档区。

## 当前仓库职责

- `heart-plant/`：用户前端
- `heart-plant-admin/`：管理后台
- `heart-plant-api/`：后端 API（Supabase Edge Function / Deno）
- 根目录：保留旧单体代码、迁移记录、验证文档、部署说明、历史脚本

> 若要继续开发，请优先进入对应子仓库，而不是直接在根目录运行旧单体流程。

## 快速导航

### 开发与验证
- 执行计划：`EXECUTION_PLAN.md`
- 当前进度：`execution-state.json`
- 验证记录：`VERIFICATION_RECORD.md`
- 三端拆分状态：`THREE-APP-SPLIT-STATUS.md`
- 三端部署说明：`THREE-APP-DEPLOYMENT.md`
- 根目录残余清单：`ROOT_ARCHIVE_MANIFEST.md`

### 三个子仓库
- 用户前端：`heart-plant/`
- 管理后台：`heart-plant-admin/`
- 后端 API：`heart-plant-api/`

### 历史单体资料（仅归档参考）
以下文件大多基于拆分前单体结构，**不要再视为当前标准入口**：
- `START_HERE.md`
- `DEPLOYMENT.md`
- `GITHUB_SETUP.md`
- `GITHUB_UPLOAD_GUIDE.md`
- `UPLOAD_TO_GITHUB.md`
- `QUICK_DEPLOY.md`
- `MACOS_QUICKSTART.md`
- `STREAMING_QUICKSTART.md`
- `STREAMING_README.md`
- `WEBRTC_SETUP.md`
- `WEBRTC_DEBUG_GUIDE.md`
- `mediamtx-setup.md`

## 推荐启动方式

### 1) 用户前端
```bash
cd heart-plant
npm install
npm run dev
```

### 2) 管理后台
```bash
cd heart-plant-admin
npm install
npm run dev
```

### 3) API
```bash
cd heart-plant-api
deno task serve
```

## 当前已知限制

1. 真实写库 / 对象存储联调仍依赖 `SUPABASE_SERVICE_ROLE_KEY`
2. 登录后核心页面截图回归仍缺测试账号或有效 Supabase 登录态
3. 根目录 Git 仓库当前未配置 `origin`，因此根目录提交暂不能直接 push

## 建议阅读顺序

1. `execution-state.json`
2. `VERIFICATION_RECORD.md`
3. `THREE-APP-DEPLOYMENT.md`
4. 进入对应子仓库查看其 `README.md` / `USAGE.md`

## 说明

根目录保留旧单体代码，是为了：
- 对照拆分前后的源码与 UI
- 保留历史部署/流媒体/联调资料
- 作为迁移阶段的过渡工作区

后续若三端仓库完全稳定，可继续把历史单体文档集中归档到单独目录。
