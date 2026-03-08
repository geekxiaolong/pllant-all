# 三端分离验证记录

更新时间：2026-03-09 01:35 (Asia/Shanghai)

## 本轮目标
- 完成 B8：用户端 UI 一致性检查
- 完成 C8：管理后台 UI 一致性检查
- 补充可追溯验证记录，作为后续部署前回归依据

## 运行环境
- 用户端：`heart-plant`，Vite 本地启动
- 管理后台：`heart-plant-admin`，Vite 本地启动
- API：`heart-plant-api`，`deno task serve`
- 浏览器回归：本机 `http://localhost`

## 实际验证

### 1. 用户端登录页可访问
访问：`http://localhost:3001/#/login`

页面快照检查结果：
- 标题：`心植 HeartPlant`
- 副标题：`IoT Social App`
- 输入框：邮箱、密码
- 主按钮：`进入心植世界`
- 次按钮：`还没有账号？立即加入`
- 版本文案：`HeartPlant v2.0.4`

结论：登录页布局、文案、视觉层级正常，未出现拆分后缺样式或白屏。

### 2. 管理后台登录页可访问
访问：`http://localhost:3002/#/admin/login`

页面快照检查结果：
- 标题：`心植管理系统`
- 副标题：`HEARTPLANT MANAGEMENT CONSOLE`
- 输入框：管理员邮箱、密码
- 主按钮：`安全登录`
- 返回按钮：`← 返回系统门户`

结论：管理后台登录页布局、文案、视觉层级正常，未出现拆分后缺样式或白屏。

### 3. 源码级 UI 一致性校验
将拆分仓库中的同名页面/组件/样式与原单体项目对应文件逐一做 `diff`。

#### 用户端一致性结果
完全一致：
- `Home.tsx`
- `PlantAdoption.tsx`
- `DiscoverPlants.tsx`
- `Achievements.tsx`
- `JournalDetailPage.tsx`
- `MoodDetailPage.tsx`
- `Notifications.tsx`
- `Layout.tsx`
- `ThemeContext.tsx`
- `AuthContext.tsx`
- 全部样式文件（`theme.css`、`custom.css`、`index.css`、`tailwind.css`、`fonts.css`）

存在 diff 的页面：
- `Interaction.tsx`
- `Moments.tsx`
- `Profile.tsx`
- `Following.tsx`
- `UserProfile.tsx`
- `MoodRecordPage.tsx`
- `JournalWritePage.tsx`
- `UserLogin.tsx`
- `AdoptionCeremony.tsx`
- `PlantProfileDetail.tsx`

差异性质：
- 差异主要为将原来硬编码的 Supabase Functions URL 替换为 `apiUrl(...)` 和 `buildApiHeaders(...)`
- 未发现布局结构、样式 class、文案资源被重写

结论：用户端 UI 差异属于 API 接入层替换，不属于视觉或交互层回归风险。

#### 管理后台一致性结果
完全一致：
- `AdminLogin.tsx`
- `DashboardLayout.tsx`
- `PlantLibrary.tsx`
- `OperationLogs.tsx`
- `StreamTest.tsx`
- `NetworkDiagnostic.tsx`
- `VideoStatus.tsx`
- `AdminGuard.tsx`
- `ThemeContext.tsx`
- `AuthContext.tsx`
- 全部样式文件（`theme.css`、`custom.css`、`index.css`、`tailwind.css`、`fonts.css`）

存在 diff 的页面：
- `DashboardHome.tsx`
- `AddPlant.tsx`
- `EditPlant.tsx`
- `Monitoring.tsx`
- `GrowthDiary.tsx`
- `GrowthDiaryDetail.tsx`
- `PlantTimeline.tsx`
- `AdoptedPlants.tsx`

差异性质：
- 差异主要为 API 请求地址统一改为 `apiUrl(...)`，请求头统一改为 `buildApiHeaders(...)`
- 未发现后台布局、导航结构、视觉 class、主要文案被重写

结论：管理后台 UI 差异同样主要属于 API 封装替换，不属于样式或结构偏差。

### 4. API 本地回归状态
`heart-plant-api` 已成功启动，`localhost:8000` 可监听。

当前已知问题：
- mock 初始化写入 `kv_store_4b732228` 时仍触发 RLS
- 根因仍是缺少 `SUPABASE_SERVICE_ROLE_KEY`，不影响本轮 UI 一致性检查

### 5. 登录后核心页面截图回归尝试
本轮继续尝试补做“登录后核心页面截图回归”，实际操作如下：
- 本地重新拉起三端：
  - API：`DEV_ADMIN_BYPASS_TOKEN=local-dev-admin deno task serve`
  - 用户端：`npm run dev -- --host 127.0.0.1`
  - 管理后台：`npm run dev -- --host 127.0.0.1`
- 浏览器访问：
  - 用户端：`http://127.0.0.1:3000/#/`
  - 管理后台：`http://127.0.0.1:3001/#/admin`
- 在浏览器中手动写入 `sb-dkszigraljeptpeiimzg-auth-token`，构造本地 session
- 通过页面内 `supabase.auth.getSession()` 二次确认：伪造 session 已可被读取
- 尝试将 hash 切换到 `#/` 与 `#/admin`，期望直接进入登录后页面继续抓图

结果：
- 用户端仍停留在登录页
- 管理后台仍停留在登录页
- 未能进入真实登录后业务页面，因此本轮无法产出“登录后核心页面截图”证据

判断：
- `DEV_ADMIN_BYPASS_TOKEN` 只解决 API 鉴权绕过，不等价于合法 Supabase JWT
- 前端路由守卫 / 登录态恢复流程不接受该伪造 token 作为真实登录凭据
- 在缺少真实测试账号或可用 service role 的前提下，无法完成登录后页面截图回归

### 6. 根工作区历史流媒体/部署文档归档清理
本轮继续清理仍可能误导为“根目录单体入口”的历史文档，在以下文件头部追加了明确归档说明，并统一指回三端分离主入口：
- `STREAMING_README.md`
- `WEBRTC_SETUP.md`
- `WEBRTC_DEBUG_GUIDE.md`
- `mediamtx-setup.md`
- `STREAMING_QUICKSTART.md`
- `QUICK_DEPLOY.md`

验证方式：
- 对上述 6 个文件执行 `head -n 4`，确认文件头都包含 `归档说明（2026-03-09）`
- 执行 `grep -R "归档说明（2026-03-09）" ...`，确认 6 个目标文件均命中

结论：流媒体与快速部署相关历史文档已统一标记为归档参考，降低后续误把根工作区继续当作单体主入口的风险。

### 7. 根工作区剩余单体入口继续归档封口
本轮继续处理仍可能把根目录误当成“可直接运行单体工程”的入口，完成以下收口：
- `DESIGN.md`：补充历史归档说明，明确当前仅用于设计追溯，不再作为当前目录结构/部署入口说明
- `deploy.sh`
- `deploy-supabase.sh`
- `git-init.sh`
- `git-push.sh`
- `quick-upload.sh`
- `quick-upload.bat`
- `package.json`

处理方式：
- 所有根目录 shell / bat 历史脚本统一改为输出归档提示，不再继续执行旧单体流程
- 根目录 `package.json` 中的 `dev` / `build` 改为直接提示“请到子仓库执行”，避免误拉起旧 Vite 单体

验证方式：
- `sed -n '1,12p'` 检查各文件头部归档提示
- `grep -nE '归档说明（2026-03-09）|\[Archived root script\]|Archived root workspace' ...` 命中全部目标文件
- 执行 `npm run dev`，确认输出归档提示并中止，不再启动旧单体开发服务器
- 执行 `bash ./deploy.sh`，确认仅输出归档提示，不再进入旧部署流程

结论：
- 根工作区剩余高风险“旧单体执行入口”已继续封口
- 后续即便误在根目录执行常见脚本，也会被明确引导到三端子仓库

### 8. 为 src 目录树补齐目录级归档说明
本轮继续处理根工作区中“文件已归档、但目录层级仍像现行源码入口”的残留认知风险，新增以下目录说明：
- `src/README.md`
- `src/app/README.md`
- `src/styles/README.md`
- `src/imports/README.md`

处理方式：
- 在每个目录放置统一的归档说明，明确这些目录属于拆分前单体历史结构
- 在说明中统一指回 `README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md`
- 明确告知当前开发应进入 `heart-plant/`、`heart-plant-admin/`、`heart-plant-api/`

验证方式：
- `grep -nH "归档说明（2026-03-09）\|Archived root workspace" src/README.md src/app/README.md src/styles/README.md src/imports/README.md`
- `git status --short` 确认本轮新增文件仅为 4 份目录级 README（另有未跟踪的 `EXECUTION_PLAN.md` 为外部计划文件）

结论：
- 进入 `src/` 及其关键子目录时，现已能在目录层级直接看到“三端分离后这里是历史归档”的提示
- 根工作区剩余源码树的误判风险进一步下降

## 本轮结论
- B8 用户端 UI 一致性检查：通过
- C8 管理后台 UI 一致性检查：通过
- 本轮未发现拆分导致的登录页白屏、样式缺失、页面文案错乱或布局结构异常
- 同名页面 diff 的主要差异均集中在 API 调用封装替换，不属于 UI 回归
- 根工作区剩余历史单体设计文档与脚本入口已进一步归档封口，降低误操作风险

## 剩余风险
1. 受登录态限制，用户端/后台登录后深层业务页面尚未做完整人工点点点回归
2. 真实写库、上传、签名 URL、存储联调仍依赖 `SUPABASE_SERVICE_ROLE_KEY`
3. `DEV_ADMIN_BYPASS_TOKEN` 不能替代真实 Supabase 登录态，当前无法仅凭伪造 localStorage session 进入登录后页面
4. Vite dev server 在短时重复拉起时出现过一次 `esbuild write EPIPE`，重启后恢复，暂未复现为构建问题

## 建议的下一步
1. 优先补齐 `SUPABASE_SERVICE_ROLE_KEY`，完成真实数据库 / 对象存储联调
2. 补充一组可用测试账号（普通用户 + 管理员），再执行登录后核心页面截图回归
3. 如短期仍无法补齐凭据，可转向清理根工作区历史单体文档与仓库说明
