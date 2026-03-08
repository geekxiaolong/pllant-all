# ⚡ 快速部署指南

> **归档说明（2026-03-09）**：本文档描述的是拆分前根目录的一体化快速部署路径，已不再是当前标准流程。
> 现阶段请优先按三端分离方式部署：用户前端 `heart-plant/`、管理后台 `heart-plant-admin/`、后端 API `heart-plant-api/`；详见 `THREE-APP-DEPLOYMENT.md`。


5 分钟内完成"心植 (HeartPlant)"项目部署！

---

## 🚀 方案选择

### 方案 A: 一键自动部署（推荐）

**适用于：** 有自己服务器的开发者

```bash
# 1. 配置服务器信息（修改为你的实际信息）
export DEPLOY_HOST="123.456.789.0"      # 服务器 IP
export DEPLOY_USER="root"                # SSH 用户名
export DEPLOY_DIR="/var/www/heartplant"  # 部署目录

# 2. 赋予执行权限
chmod +x deploy.sh deploy-supabase.sh

# 3. 一键部署前端
./deploy.sh

# 4. 一键部署后端
./deploy-supabase.sh
```

完成！访问 `http://你的服务器IP` 即可。

---

### 方案 B: Vercel 部署（最简单）

**适用于：** 想要快速上线的开发者

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 登录
vercel login

# 3. 部署
vercel --prod
```

完成！Vercel 会给你一个域名。

---

### 方案 C: Netlify 拖拽部署（无需命令行）

**适用于：** 不熟悉命令行的开发者

```bash
# 1. 构建项目
pnpm install
pnpm build

# 2. 访问 https://app.netlify.com/drop
# 3. 拖拽 dist 文件夹到页面
```

完成！Netlify 会给你一个域名。

---

### 方案 D: Docker 部署

**适用于：** 熟悉容器化的开发者

```bash
# 1. 构建并启动
docker-compose up -d

# 2. 访问 http://localhost
```

---

## 🔧 后端配置（所有方案必做）

### 1. 更新 Supabase 配置

编辑 `/utils/supabase/info.tsx`:

```typescript
export const projectId = 'YOUR_PROJECT_ID';      // ← 改这里
export const publicAnonKey = 'YOUR_ANON_KEY';    // ← 改这里
```

### 2. 部署 Edge Functions

```bash
# 方式 1: 使用脚本
./deploy-supabase.sh

# 方式 2: 手动部署
supabase login
supabase link --project-ref YOUR_PROJECT_ID
supabase functions deploy make-server-4b732228 --no-verify-jwt
```

---

## ✅ 部署检查清单

部署完成后，请确认：

- [ ] 前端可以正常访问
- [ ] 可以登录/注册用户
- [ ] 管理员账号（776427024@qq.com）可以访问后台
- [ ] 植物数据可以正常显示
- [ ] API 请求没有 CORS 错误

---

## 🆘 常见问题

### ❓ 白屏/404 错误

**原因：** 路由配置问题

**解决：** 确保 Nginx 配置了 SPA 重写：

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

### ❓ API 请求失败

**原因：** Supabase 配置错误

**解决：**
1. 检查 `/utils/supabase/info.tsx` 配置
2. 确认 Edge Functions 已部署
3. 查看浏览器控制台错误信息

### ❓ 401 认证错误

**原因：** JWT Token 问题

**解决：**
1. 清除浏览器缓存
2. 重新登录
3. 检查后端日志：`supabase functions logs make-server-4b732228`

### ❓ 部署脚本失败

**原因：** SSH 权限或路径问题

**解决：**
```bash
# 测试 SSH 连接
ssh root@your-server-ip "echo 'Connection OK'"

# 检查服务器磁盘空间
ssh root@your-server-ip "df -h"

# 手动创建部署目录
ssh root@your-server-ip "mkdir -p /var/www/heartplant"
```

---

## 🔄 更新部署

已经部署过了？更新很简单：

```bash
# 拉取最新代码
git pull origin main

# 重新部署（会自动覆盖）
./deploy.sh
```

---

## 📞 需要帮助？

1. 查看完整文档：[DEPLOYMENT.md](./DEPLOYMENT.md)
2. 检查部署日志：
   ```bash
   # 前端日志
   tail -f /var/log/nginx/heartplant-error.log
   
   # 后端日志
   supabase functions logs make-server-4b732228 --tail
   ```

---

## 🎯 生产环境优化（可选）

部署成功后，建议进行以下优化：

### 1. 配置 SSL 证书

```bash
# 安装 Certbot
apt install certbot python3-certbot-nginx -y

# 自动配置 SSL
certbot --nginx -d your-domain.com
```

### 2. 配置 CDN

- 推荐使用 Cloudflare（免费）
- 或者使用 阿里云 CDN / 腾讯云 CDN

### 3. 启用 Gzip/Brotli 压缩

Nginx 配置文件中已包含，确保已启用。

### 4. 配置监控

```bash
# 安装 PM2（可选）
npm install -g pm2

# 监控 Nginx
pm2 start nginx
```

---

**祝部署顺利！🌱**

有问题随时问！
