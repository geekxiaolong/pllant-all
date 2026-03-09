# START_HERE（已切换为三端分离导航）

更新时间：2026-03-09 14:35 (Asia/Shanghai)

如果你是第一次回到这个工作区，请先记住一件事：

> **根目录不再是旧单体项目的主入口。现在请按三端分离方式工作。**

## 先看哪里

### 如果你要继续执行拆分任务
1. 打开 `EXECUTION_PLAN.md`
2. 查看 `execution-state.json`
3. 阅读 `VERIFICATION_RECORD.md`
4. 根据任务进入对应子仓库

### 如果你要启动项目
- 用户前端：`heart-plant/`
- 管理后台：`heart-plant-admin/`
- 后端 API：`heart-plant-api/`

## 最常用命令

### 用户前端
```bash
cd heart-plant
npm install
npm run dev
```

### 管理后台
```bash
cd heart-plant-admin
npm install
npm run dev
```

### API
```bash
cd heart-plant-api
deno task serve
```

## 当前主文档

- 根目录说明：`README.md`
- 根目录残余清单：`ROOT_ARCHIVE_MANIFEST.md`
- 三端部署：`THREE-APP-DEPLOYMENT.md`
- 验证记录：`VERIFICATION_RECORD.md`
- 进度状态：`execution-state.json`

## 哪些文档是旧资料

下面这些文档仍可参考，但主要服务于拆分前单体或流媒体联调历史：
- `DEPLOYMENT.md`
- `GITHUB_SETUP.md`
- `GITHUB_UPLOAD_GUIDE.md`
- `QUICK_DEPLOY.md`
- `STREAMING_QUICKSTART.md`
- `STREAMING_README.md`
- `WEBRTC_SETUP.md`
- `WEBRTC_DEBUG_GUIDE.md`
- `mediamtx-setup.md`

## 当前阻塞提醒

- 缺 `SUPABASE_SERVICE_ROLE_KEY`：真实写库/存储联调无法完成
- 缺测试账号或有效登录态：登录后核心页面截图回归无法完成
- 根目录 Git 未配置 `origin`：根目录文档提交后暂不能 push

如果以上阻塞未解除，优先继续做：
- 根目录历史单体文档与说明清理
- 三端仓库 README / 部署说明收口
- 可离线完成的代码整理与验证
