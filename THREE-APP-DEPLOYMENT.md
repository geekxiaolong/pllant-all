# 三端分离部署说明

更新时间：2026-03-09 00:36 (Asia/Shanghai)

本文档针对三端拆分后的部署结构：

1. `heart-plant`：用户前端
2. `heart-plant-admin`：管理后台
3. `heart-plant-api`：后端 API（Supabase Edge Function / Deno）

> 说明：旧版 `DEPLOYMENT.md` 仍偏单体前端部署；本文件用于补充拆分后的独立部署方式。

---

## 1. 推荐部署拓扑

### 方案 A：双静态站点 + 一套 API（推荐）
- 用户端：`https://app.example.com`
- 管理后台：`https://admin.example.com`
- API：`https://api.example.com` 或 `https://<project>.supabase.co/functions/v1/make-server-4b732228`

优点：
- 用户端与后台彻底隔离
- 可分别发布、回滚、加缓存
- 更符合本次三端分离目标

### 方案 B：同域不同路径
- 用户端：`https://example.com/`
- 管理后台：`https://example.com/admin/`
- API：`https://example.com/api/`

注意：当前前端使用 **Hash Router**，静态资源部署更容易，但仍建议前后端使用独立域名或反向代理。

---

## 2. 本地开发端口

- 用户端：`3000`（若被占用，Vite 会自动尝试下一个端口）
- 管理后台：`3001`
- API：`8000`

常用启动命令：

```bash
# 用户端
cd heart-plant
npm install
npm run dev

# 管理后台
cd heart-plant-admin
npm install
npm run dev

# API
cd heart-plant-api
deno task serve
```

---

## 3. 前端部署

### 3.1 用户端 `heart-plant`

构建：

```bash
cd heart-plant
npm install
npm run build
```

产物目录：
- `heart-plant/dist`

部署要求：
- 托管静态文件即可
- 由于使用 Hash Router，一般不需要额外 SPA rewrite，但建议保留 `index.html` 兜底

### 3.2 管理后台 `heart-plant-admin`

构建：

```bash
cd heart-plant-admin
npm install
npm run build
```

产物目录：
- `heart-plant-admin/dist`

部署要求：
- 独立静态站点部署
- 建议单独绑定后台域名，便于访问控制和日志隔离

---

## 4. API 部署

### 4.1 本地运行

```bash
cd heart-plant-api
deno task serve
```

默认监听：
- `http://localhost:8000/`

### 4.2 生产部署建议

当前后端代码位于：
- `heart-plant-api/supabase/functions/server/index.tsx`

建议两种生产方式：

#### 方式 1：作为 Supabase Edge Function 部署
适用于当前项目结构，兼容已有 Supabase 生态。

```bash
supabase login
supabase link --project-ref <YOUR_PROJECT_ID>
supabase functions deploy make-server-4b732228 --no-verify-jwt
```

#### 方式 2：自托管 Deno 服务
适用于后续想完全独立于 Supabase Functions 的场景。

要求：
- 自行提供 Deno runtime
- 自行配置反向代理、日志、进程守护
- 仍需访问 Supabase 数据库与存储

---

## 5. 关键环境变量

### 5.1 API 侧
必须具备：

```bash
SUPABASE_URL=https://<YOUR_PROJECT_ID>.supabase.co
SUPABASE_ANON_KEY=<YOUR_ANON_KEY>
SUPABASE_SERVICE_ROLE_KEY=<YOUR_SERVICE_ROLE_KEY>
```

说明：
- `SUPABASE_SERVICE_ROLE_KEY` 当前是后续真实写库/存储联调的关键依赖
- 缺失时，本地 mock 初始化写入 `kv_store_4b732228` 会触发 RLS

### 5.2 前端侧
拆分后前端不再建议继续依赖硬编码 Functions URL。

当前代码已经改为统一通过 API 工具封装调用：
- `apiUrl(...)`
- `buildApiHeaders(...)`

部署前需确认前端 API 目标地址与实际后端一致。

建议为前端提供统一配置来源，例如：

```bash
VITE_API_BASE_URL=https://api.example.com
# 或
VITE_API_BASE_URL=https://<YOUR_PROJECT_ID>.supabase.co/functions/v1/make-server-4b732228
```

> 若当前仓库尚未全面切到 `.env` 注入，可在上线前再统一收口；但部署时必须确保构建产物指向正确 API 地址。

---

## 6. Nginx 反向代理示例

### 6.1 用户端

```nginx
server {
    listen 80;
    server_name app.example.com;

    root /var/www/heart-plant;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 6.2 管理后台

```nginx
server {
    listen 80;
    server_name admin.example.com;

    root /var/www/heart-plant-admin;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 6.3 API 反向代理（自托管 Deno 时）

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 7. 上线前检查清单

### 用户端
- [ ] `npm run build` 通过
- [ ] 登录页可访问
- [ ] 首页/互动/广场/个人 路由可达
- [ ] API 地址指向生产环境

### 管理后台
- [ ] `npm run build` 通过
- [ ] 管理员登录页可访问
- [ ] `/admin` 主入口可达
- [ ] 植物库/日志/监控/时间线等页面 API 指向正确

### API
- [ ] `deno task serve` 或生产运行方式可启动
- [ ] `/health` 可访问
- [ ] `/admin/*` 路由可访问
- [ ] `SUPABASE_SERVICE_ROLE_KEY` 已配置
- [ ] 存储上传、签名 URL、写库链路已联调

---

## 8. 当前已知风险

1. 真实写库和对象存储联调尚依赖 `SUPABASE_SERVICE_ROLE_KEY`
2. 本轮完成了登录页与源码级 UI 一致性检查，但登录后深层业务页仍建议补充截图回归
3. 如继续保留 Vite dev 自动跳端口特性，联调脚本和人工回归时要注意端口漂移

---

## 9. 建议发布顺序

1. 先部署 API
2. 验证 `/health` 和 `/admin/*`
3. 部署管理后台并验证管理员登录
4. 部署用户端并验证登录/首页/互动/广场/个人
5. 最后做一次真实写库、上传、日志链路回归
