# 根工作区残余清单（历史归档总览）

更新时间：2026-03-09 06:58 (Asia/Shanghai)

## 归档说明（2026-03-09）

`/Users/mac/植物记 (2)` 当前是 **HeartPlant 三端分离后的历史归档根工作区**。
它不再承担单体应用的开发、构建、部署职责。

当前真正持续开发的仓库只有：
- `heart-plant/`：用户前端
- `heart-plant-admin/`：管理后台
- `heart-plant-api/`：后端 API

本清单用于回答两个问题：
1. 根目录里还保留了什么；
2. 哪些文件仍值得看，哪些只是历史资料或归档守卫。

## 一、当前仍应保留并持续维护的根目录文件

这些文件仍是当前三端分离工作区的有效导航或执行凭据：

- `README.md`：根工作区总入口与三端导航
- `START_HERE.md`：回到工作区后的最短阅读路径
- `EXECUTION_PLAN.md`：原始执行清单（计划面）
- `execution-state.json`：**唯一持续更新的执行状态源**
- `VERIFICATION_RECORD.md`：构建、运行、UI、回归验证记录
- `ROOT_ARCHIVE_MANIFEST.md`：根工作区残余资产总表，也是后续归档巡检的基准清单
- `THREE-APP-DEPLOYMENT.md`：三端分离后的部署说明
- `THREE-APP-SPLIT-STATUS.md`：历史状态摘要（只作归档索引）
- `.gitignore`：根工作区忽略规则，避免误把三端子仓库再次纳入根仓库提交
- `package-lock.json`：根工作区最小归档锁文件，避免误保留旧单体依赖树
- `.vscode/settings.json`：仅用于将根目录显示为“历史归档工作区”，降低误操作风险
- `scripts/README.md`：归档巡检脚本目录说明，约束该目录仅承载根工作区维护脚本
- `scripts/root_archive_audit.py`：根工作区归档巡检脚本，可重复校验顶层残余资产、目录 README 覆盖和空目录状态

## 二、当前仍保留但仅作为历史资料参考的文件

这些文件已经改为“归档说明”或“归档守卫”，保留目的主要是：
- 追溯拆分前背景
- 给旧链接/旧脚本一个明确落点
- 阻止误执行历史单体流程

### 2.1 历史文档
- `DEPLOYMENT.md`
- `DESIGN.md`
- `GITHUB_SETUP.md`
- `GITHUB_UPLOAD_GUIDE.md`
- `UPLOAD_TO_GITHUB.md`
- `上传到GitHub说明.md`
- `FILES_READY_FOR_GITHUB.md`
- `QUICK_DEPLOY.md`
- `MACOS_QUICKSTART.md`
- `API_FIX_SUMMARY.md`
- `ATTRIBUTIONS.md`
- `FIX_SUMMARY.md`
- `TIMELINE_FIX_SUMMARY.md`
- `VIDEO_STATUS_GUIDE.md`
- `STREAMING_README.md`
- `STREAMING_QUICKSTART.md`
- `WEBRTC_SETUP.md`
- `WEBRTC_DEBUG_GUIDE.md`
- `mediamtx-setup.md`

### 2.2 历史脚本 / 历史入口守卫
- `deploy.sh`
- `deploy-supabase.sh`
- `git-init.sh`
- `git-push.sh`
- `quick-upload.sh`
- `quick-upload.bat`
- `mediamtx-config.yml`
- `mediamtx-config-fixed.yml`
- `mediamtx-minimal.yml`
- `mediamtx-quickstart.sh`
- `mediamtx-quickstart.bat`
- `setup-mediamtx-macos.sh`
- `start-mediamtx.sh`
- `docker-compose.yml`
- `index.html`
- `package.json`
- `postcss.config.mjs`
- `vite.config.ts`

### 2.3 历史目录（目录内已有 README 归档说明）
- `src/`
- `supabase/`
- `stream-server/`
- `nginx/`
- `guidelines/`
- `utils/`
- `workflows/`
- `LICENSE/`
- `.vscode/`

## 三、如何判断一个根目录文件还能不能执行

### 可以继续当“当前入口”使用的
只限以下几类：
- 导航文档
- 执行状态文件
- 验证记录
- 三端部署说明
- 根目录只读型配置（如 `.gitignore`、`.vscode/settings.json`）

### 不应再当“当前系统入口”使用的
凡是满足以下任一条件，均视为历史归档：
- 文件头明确写有 `归档说明（2026-03-09）`
- 文件内容包含 `Archived root workspace`
- 脚本输出 `Archived root script`
- workflow 标注 `Archived root workflow`

## 四、推荐操作路径

### 需要开发用户端
```bash
cd heart-plant
npm run dev
```

### 需要开发管理后台
```bash
cd heart-plant-admin
npm run dev
```

### 需要开发 API
```bash
cd heart-plant-api
deno task serve
```

### 需要续跑拆分任务
按以下顺序阅读：
1. `execution-state.json`
2. `VERIFICATION_RECORD.md`
3. `THREE-APP-DEPLOYMENT.md`
4. 再进入对应子仓库

## 五、当前仍未解除的硬阻塞

1. 缺少 `SUPABASE_SERVICE_ROLE_KEY`，因此真实写库 / 对象存储联调尚不能完成
2. 缺少测试账号或有效 Supabase 登录态，因此登录后核心页面截图回归尚不能完成
3. 根工作区 Git 仓库尚未配置可用 `origin`，因此根目录提交目前仍无法 push

## 六、维护约定

后续若继续清理根工作区，请遵守：
- 新发现的历史目录：补 `README.md` 归档说明
- 新发现的历史入口脚本：改为归档守卫，不再执行旧流程
- 新发现的根目录说明文档：在文件头追加归档说明，并指回三端子仓库
- `execution-state.json` 中的 `currentStep` / `nextSteps` 必须同步更新

## 结论

根目录现在的角色只有两个：
- 作为三端分离的导航与验证中枢
- 作为拆分前单体资料的归档承载层

**所有实际开发、运行、构建、部署，都应回到三个子仓库中进行。**
