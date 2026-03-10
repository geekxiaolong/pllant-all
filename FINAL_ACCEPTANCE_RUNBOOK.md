# HeartPlant 最终联调验收单

更新时间：2026-03-10 11:00 (Asia/Shanghai)

这份文档只回答三件事：
1. 三个子仓库现在分别到什么完成度
2. 真机/真实环境下还剩哪一组最小人工 E2E 要验
3. 什么情况下可以判定 phase-1 可交付

---

## 1. 当前多仓库完成状态

### 用户前端 `heart-plant/`
- 最近提交：`2734629 feat: improve public profiles and follow state sync`
- 当前判断：**可进入真实账号联调**
- 已稳定的主链路：
  - 登录 / 注册
  - 受保护接口统一鉴权头
  - moments / following / public profile 关注态同步
  - 个人资料编辑与头像上传回退
  - 植物详情时间线请求恢复
  - `npm run build` 已通过

### 管理后台 `heart-plant-admin/`
- 最近提交：`a6dae58 feat: harden admin plant and diary workflows`
- 当前判断：**可进入真实管理员账号联调**
- 已稳定的主链路：
  - 管理员登录判定与请求头统一
  - 植物库新增 / 编辑 / 删除后的自动刷新
  - 日记详情 / 精选 / 删除与错误处理
  - Dashboard / 认领视图 / 时间线 payload 兼容
  - `npm run build` 已通过

### 后端 API `heart-plant-api/`
- 最近提交：`bd3e1e6 docs: add backend release and auth validation notes`
- 当前判断：**代码与接口已接近发布，仍需最后一轮真实凭据验证**
- 已闭环的接口能力：
  - `/profile` 读写
  - follow / unfollow / is-following / following
  - public profile / user moments 查询
  - admin library 写路径与删除
  - journal feature / delete / detail alias
  - upload-url / image-url helper
  - `deno task check` 已通过

---

## 2. 当前真正剩余的阻塞

1. **缺 `SUPABASE_SERVICE_ROLE_KEY`**
   - 影响：真实写库、存储上传、签名 URL、部分管理写操作无法完成最终验收
2. **缺真实测试账号 / 有效 Supabase 登录态**
   - 影响：用户端与后台登录后页面无法做真实人工回归
3. **根仓库未配置 `origin`**
   - 影响：根目录文档可本地提交，但当前不能直接 push

结论：
- 现在不是“代码还没做完”，而是“最后一轮真实环境验收条件还没补齐”。

---

## 3. 最小人工 E2E 验证集

目标：只跑最小集合，但能覆盖 user / admin / backend 三端交付风险。

### A. 用户侧（普通测试账号）

#### U1. 登录与会话恢复
- 用现有账号登录成功并进入首页
- 刷新页面后仍保持登录
- 打开 Network，确认受保护请求带用户 JWT，而不是 anon key 冒充 bearer

#### U2. 资料编辑
- 进入 `Profile`
- 修改 `name / bio / location`
- 保存后当前页立即回显
- 上传一张头像，确认新头像可展示

#### U3. 社交链路
- 进入 `Moments`
- 对 1 个用户执行关注，再取消关注
- 进入 `Following`，确认状态同步
- 点击头像进入 `/u/:userId`
- 确认查看自己主页时不显示关注按钮

#### U4. 植物详情
- 打开任一植物详情
- 确认时间线正常返回，无 401 / 404 / 路径字面量错误

> 用户侧最小通过标准：U1~U4 全过，且无白屏、无致命控制台错误。

### B. 管理侧（管理员账号）

#### A1. 管理员登录与权限
- 用真实管理员账号登录 `/admin/login`
- 能进入 `/admin`
- 用非管理员账号验证一次拦截逻辑（如条件允许）

#### A2. 植物库写操作
- 新增 1 个植物（直接填写图片 URL）
- 编辑该植物的名称或文案
- 删除该植物，或确认后端明确返回当前不支持提示
- 每次动作后列表都能自动刷新

#### A3. 日记后台操作
- 打开日记列表
- 进入 1 条日记详情
- 执行一次精选切换
- 执行一次删除，或确认后端明确返回当前不支持提示
- 返回列表后状态刷新正确

#### A4. Dashboard / 认领 / 时间线
- Dashboard 统计卡片正常显示
- 已认领植物列表正常
- 认领管理页正常
- 切换某 plantId 的时间线时页面无报错

> 管理侧最小通过标准：A1~A4 全过，且所有写操作要么成功，要么返回与当前后端能力一致的明确结果，不能是假成功。

### C. 后端侧（真实环境配置）

#### B1. 基础健康检查
- `GET /health`
- `GET /library`

#### B2. 普通用户 JWT 验证
- `GET /profile`
- `PUT /profile`
- `GET /moments/user/:userId`
- 完整跑一次 follow -> is-following -> unfollow -> following

#### B3. 管理员 JWT 验证
- `POST /library`
- `DELETE /library/:id`
- `POST /journal-feature/:id`
- `DELETE /journal/:id`
- `GET /plants?admin_view=true`
- `DELETE /admin/plants/:id`

#### B4. 存储链路
- `POST /upload-url`
- 用返回的 signed URL 上传 1 个文件
- `GET /image-url/:path` 校验最终可访问

> 后端侧最小通过标准：B1~B4 全过；若失败，必须能明确归因到 env/config，而不是接口契约漂移。

---

## 4. 推荐执行顺序（最省时间）

1. 先补齐环境：`SUPABASE_SERVICE_ROLE_KEY` + 普通测试账号 + 管理员账号
2. 先跑后端 B1~B4
   - 因为 user/admin 的大部分“看起来像前端问题”的故障，本质都会先暴露在这里
3. 再跑用户侧 U1~U4
4. 最后跑管理侧 A1~A4
5. 若三段都通过，记录截图/视频/接口响应即可给出 phase-1 验收通过结论

---

## 5. 一票否决项

出现以下任一情况，不应判定为已验收通过：
- 登录成功但刷新后会话丢失
- 前端受保护请求未携带真实用户 JWT
- 管理写操作出现“前端提示成功、后端实际未落库”
- upload-url / signed upload / image-url 任一环节失效
- 关注、资料、植物、日记任一主流程出现 401/403/404 契约错位
- 页面白屏或控制台出现可复现致命错误

---

## 6. phase-1 验收通过定义

满足以下条件即可判定 phase-1 可交付：
- 用户侧 U1~U4 通过
- 管理侧 A1~A4 通过
- 后端侧 B1~B4 通过
- 已知阻塞项中的前两项（service role / 测试账号）已解除
- 根仓库是否有 `origin` 不影响“本地验收通过”，只影响根目录文档 push

---

## 7. 立即下一步

**先不要再扩功能。**
直接去补三样东西，然后按本文顺序做最后一轮真实联调：
- `SUPABASE_SERVICE_ROLE_KEY`
- 普通测试账号
- 管理员测试账号

拿到这三样后，优先执行：**后端 B1~B4 → 用户 U1~U4 → 管理 A1~A4**。
