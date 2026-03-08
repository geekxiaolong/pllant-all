# 三端分离验证记录

更新时间：2026-03-09 03:24 (Asia/Shanghai)

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

### 9. 为剩余历史目录补齐 README 级归档说明
本轮继续沿着“目录层级也要明确归档身份”的思路，新增以下目录说明：
- `.vscode/README.md`
- `workflows/README.md`
- `utils/README.md`
- `utils/supabase/README.md`
- `supabase/functions/README.md`

处理方式：
- 在目录级 README 中统一标注 `Archived root workspace`
- 明确这些目录仅保留拆分前根工作区的本地配置、历史工作流或 Supabase/工具残留
- 统一指回 `README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md`，并提示当前应进入三端子仓库开发

验证方式：
- 执行 `grep -R -n "Archived root workspace" .vscode/README.md workflows/README.md utils/README.md utils/supabase/README.md supabase/functions/README.md`
- 确认 5 份新 README 均命中归档标识
- 执行 `find .vscode workflows utils supabase/functions -maxdepth 2 -name 'README.md' | sort`，确认目录级说明文件均已落盘

结论：
- 根工作区剩余缺少目录级提示的历史目录已进一步补齐归档说明
- 进入编辑器配置、历史工作流、旧 Supabase/工具目录时，能更早看到“这里不是当前开发入口”的提示

### 13. 根工作区归档审计脚本落地
本轮将“继续清理根工作区残余历史单体文件（优先根目录残余清单、空目录说明与未归档仓库说明）”进一步固化为可重复执行的脚本校验，新增：
- `scripts/README.md`
- `scripts/root_archive_audit.py`

处理方式：
- 用脚本统一检查根工作区顶层残余资产是否仍被 `ROOT_ARCHIVE_MANIFEST.md` 覆盖
- 自动扫描历史目录是否存在缺 `README.md` 的情况
- 自动扫描是否存在未说明空目录
- 将顶层资产白名单固定为当前归档根目录应保留的集合，后续若新增残余文件可第一时间被审计发现

验证方式：
- 执行 `python3 scripts/root_archive_audit.py`
- 输出结果：
  - `missing README dirs: 0`
  - `empty dirs: 0`
  - `manifest missing entries: 0`
  - `unexpected top-level entries: 0`
  - `RESULT: PASS`

结论：
- 根工作区“残余清单 + 目录说明 + 空目录”已具备脚本级回归能力
- 后续 cron 可以直接复跑该脚本，快速发现新的根层归档遗漏，而不再完全依赖人工巡检

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


### 10. 为剩余未覆盖的历史源码目录补齐 README 级归档说明
本轮继续沿着“目录层级先提示归档身份”的思路，补齐此前仍缺少 `README.md` 的历史目录：
- `supabase/functions/server/README.md`
- `guidelines/README.md`
- `src/app/context/README.md`
- `src/app/utils/README.md`
- `src/app/components/README.md`
- `src/app/components/ui/README.md`
- `src/app/components/figma/README.md`
- `src/app/pages/README.md`

处理方式：
- 在每个目录级 README 中统一标注 `Archived root workspace`
- 明确这些目录仅保留拆分前单体的历史 server / guideline / context / utils / components / pages 结构
- 统一指回根目录 `README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md` 与三端子仓库

验证方式：
- 运行目录扫描脚本，确认根工作区（排除 `.git`、三端子仓库、`node_modules`）**不再存在缺少 `README.md` 的目录**
- 使用 `grep -nE "Archived root workspace|历史归档"` 校验上述 8 份 README 均命中归档标识

结论：
- 根工作区历史源码/配置目录已全部补齐目录级归档说明
- 进入任一残留目录时，均能在目录层直接看到“这里不是当前开发入口”的提示，进一步压缩误把根目录旧单体结构当成现行代码库的空间

### 11. 新增根工作区残余清单总览
本轮继续沿着 execution-state 中“优先清理根目录残余清单、空目录说明与未归档仓库说明”的备选路径推进，新增：
- `ROOT_ARCHIVE_MANIFEST.md`

处理方式：
- 汇总根工作区中“仍需维护的导航/状态文件”与“仅作历史参考的归档文件”
- 明确哪些根目录文件还可作为当前入口，哪些只能作为历史材料或归档守卫
- 在 `README.md` 与 `START_HERE.md` 中补充对该清单的链接，形成主导航闭环

验证方式：
- 读取 `ROOT_ARCHIVE_MANIFEST.md`，确认已覆盖根目录有效入口、历史文档、历史脚本、历史目录与当前阻塞说明
- 读取 `README.md` 与 `START_HERE.md`，确认两处主导航均已出现 `ROOT_ARCHIVE_MANIFEST.md`
- 执行目录扫描脚本，确认根工作区（排除 `.git`、三端子仓库、`node_modules`）仍不存在缺少 `README.md` 的目录

结论：
- 根工作区现在除了“主入口文档 + 执行状态 + 验证记录”外，又补齐了一份面向维护者的残余资产总清单
- 后续无论是回溯历史资料，还是继续清理根目录残留文件，都有统一索引可循，进一步降低误把根目录当成现行单体仓库的概率

### 12. 补齐根工作区残余清单的遗漏文件项
本轮继续沿着“如仍缺少凭据，则继续清理根工作区其余历史单体残留文件”的备选路径推进，对 `ROOT_ARCHIVE_MANIFEST.md` 做了一次基于实盘文件列表的补漏修订。

补齐内容：
- 在“仍应保留并持续维护的根目录文件”中补充 `package-lock.json`，明确它当前只是根工作区最小归档锁文件，不再承载旧单体依赖树
- 在“历史文档”中补充 `ATTRIBUTIONS.md`
- 在“历史脚本 / 历史入口守卫”中补充 `mediamtx-config.yml`、`mediamtx-config-fixed.yml`、`mediamtx-minimal.yml`

验证方式：
- 运行 `find . -maxdepth 2` 顶层文件扫描，核对根目录当前真实文件集合
- 重新读取 `ROOT_ARCHIVE_MANIFEST.md`，确认上述遗漏项已落盘
- 运行目录扫描脚本，确认根工作区（排除 `.git`、三端子仓库、`node_modules`）仍不存在缺少 `README.md` 的目录
- 运行空目录扫描脚本，确认当前根工作区不存在未说明的空目录残留

结论：
- 根工作区残余资产总清单已从“主导航索引”进一步提升为“与当前落盘文件基本一致的归档盘点”
- 后续若继续收口根目录残留文件，可直接以该清单作为基线，减少遗漏与重复清理

### 14. 根工作区归档标识抽检脚本补强
本轮继续沿着 `execution-state.json -> nextSteps` 的 fallback 路线，补强 `scripts/root_archive_audit.py`，将原先仅检查“文件/目录是否存在”的审计提升为“内容级归档标识抽检”。

新增校验项：
- 历史文档、历史脚本、历史配置、目录级 `README.md` 必须命中至少一个归档标识（如 `归档说明（2026-03-09）`、`Archived root workspace`、`Archived root script` 等）
- 上述历史文件必须继续命中至少一个三端导航标识（如 `README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md`、子仓库路径）
- 维持原有的顶层残余资产清单、目录 `README.md` 覆盖、空目录与异常顶层项检查

实际回归：
1. 首次执行 `python3 scripts/root_archive_audit.py`
   - 新规则立即发现 6 处历史文件未被当前 marker 词典覆盖：
     - `ATTRIBUTIONS.md`
     - `THREE-APP-SPLIT-STATUS.md`
     - `docker-compose.yml`
     - `mediamtx-config.yml`
     - `mediamtx-config-fixed.yml`
     - `mediamtx-minimal.yml`
   - 输出 `RESULT: FAIL`
2. 根据真实落盘内容补全脚本中的 archive marker 词典（覆盖 `Historical archive notice`、`归档状态说明`、`Archived root docker compose`、`Archived root MediaMTX config` 等已有归档写法）
3. 二次执行 `python3 scripts/root_archive_audit.py`
   - `archive marker gaps: 0`
   - `navigation marker gaps: 0`
   - `RESULT: PASS`

结论：
- 根工作区归档巡检已从“结构层存在性检查”提升到“内容层标识一致性检查”
- 之后若有人把历史文件改回无归档提示、或删掉三端导航入口，cron 可直接在脚本层发现，而不再依赖人工抽样

### 15. 根工作区 manifest 分类段落一致性校验补强
本轮继续沿着 `execution-state.json -> nextSteps` 的 fallback 路线，补强 `scripts/root_archive_audit.py`，让它不仅检查 `ROOT_ARCHIVE_MANIFEST.md` 是否“提到过”顶层资产，还校验这些资产是否落在正确的分类段落中。

新增校验项：
- 为 `ROOT_ARCHIVE_MANIFEST.md` 建立显式 section -> expected entries 基线，覆盖：
  - `## 一、当前仍应保留并持续维护的根目录文件`
  - `### 2.1 历史文档`
  - `### 2.2 历史脚本 / 历史入口守卫`
  - `### 2.3 历史目录（目录内已有 README 归档说明）`
- 审计脚本现会解析各段中的列表项，检查：
  - 应在该段中的条目是否缺失
  - 不应落在该段中的条目是否被误归类
- 对最后一个清单段落的截取逻辑做了收紧，避免把后续“维护约定”中的反引号示例误识别为目录清单项

实际回归：
1. 首次执行 `python3 scripts/root_archive_audit.py`
   - 发现新规则有效抓到一个真实解析问题：
     - `### 2.3 历史目录（目录内已有 README 归档说明） :: unexpected entry execution-state.json`
   - 根因不是 manifest 分类错误，而是解析范围过宽，把第六节维护约定中的 `` `execution-state.json` `` 误识别成 2.3 清单项
   - 输出 `RESULT: FAIL`
2. 调整脚本：
   - 将 section 解析改为逐行提取真正的列表项
   - 将最后一段的截取终点改为“下一个 Markdown heading”，避免把后续正文混入当前清单段
3. 二次执行 `python3 scripts/root_archive_audit.py`
   - `manifest section issues: 0`
   - `RESULT: PASS`

结论：
- 根工作区归档巡检现已覆盖“是否列入 manifest”与“是否列入正确段落”两层一致性约束
- 后续即便 `ROOT_ARCHIVE_MANIFEST.md` 中出现分类漂移、段落误归类或列表解析回归，也能被脚本直接发现

### 16. manifest 保留/归档分类与 audit targets 交叉覆盖校验
本轮继续沿着 `execution-state.json -> nextSteps` 的 fallback 路线，进一步补强 `scripts/root_archive_audit.py`，让它检查 `ROOT_ARCHIVE_MANIFEST.md` 的“保留/归档分类”是否真的覆盖到了脚本当前正在抽检的 archive targets 基线，而不是只看 section 文本本身是否齐全。

新增校验项：
- 建立 manifest 分类条目 -> 实际 audit targets 的显式映射：
  - 历史文档、历史脚本 / 守卫文件采用一对一映射
  - 历史目录条目采用一对多映射，覆盖目录级 `README.md`（如 `src/README.md`、`src/app/README.md`、`src/imports/README.md`、`src/styles/README.md`）
- 审计脚本现会额外检查：
  - manifest archive 分类基线是否存在未映射项
  - `ARCHIVE_TARGETS` 中是否存在未被 manifest 分类覆盖的审计目标
  - 保留基线与 archive audit target 是否发生错误重叠
  - manifest 分类映射出的目标文件是否真实存在于磁盘

实际回归：
1. 首次执行 `python3 scripts/root_archive_audit.py`
   - 新规则发现 5 处真实覆盖缺口：
     - `THREE-APP-SPLIT-STATUS.md`
     - `scripts/README.md`
     - `src/app/README.md`
     - `src/imports/README.md`
     - `src/styles/README.md`
   - 其中前两项暴露的是“audit targets 基线比 manifest archive 分类更宽”，后三项暴露的是 `src/` 分类仅覆盖了顶层 `src/README.md`，尚未把已存在的子目录归档 README 一并纳入映射
   - 输出 `RESULT: FAIL`
2. 调整脚本：
   - 将 `THREE-APP-SPLIT-STATUS.md` 从 archive marker audit targets 中移除，保持其作为“保留但历史摘要文件”的单独角色，不再强制要求落入 archive 分类映射
   - 将 `scripts/README.md` 从 archive marker audit targets 中移除，避免把活动脚本目录中的目录说明误判为 archive 分类项
   - 将 `src/` 的 manifest 分类映射扩展为同时覆盖 `src/README.md`、`src/app/README.md`、`src/imports/README.md`、`src/styles/README.md`
3. 二次执行 `python3 scripts/root_archive_audit.py`
   - `manifest classification issues: 0`
   - 其余检查项保持为 0
   - `RESULT: PASS`

结论：
- 根工作区归档巡检现已从“文件存在 / 标识存在 / section 正确”进一步提升到“manifest 分类是否真正覆盖 audit 基线”这一层
- 后续若新增 archive targets 但忘记接入 manifest 分类映射，脚本会直接报错，减少根工作区归档基线持续漂移的风险
