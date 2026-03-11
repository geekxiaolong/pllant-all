# NEXT_ACTION.md

更新时间：2026-03-10 14:03 (Asia/Shanghai)

## 下一步唯一动作

> **继续真实验收，不再扩功能，不再重复讨论凭据是否缺失。**

---

## 执行顺序（严格按此顺序）

### 1. 后端真实验证
优先验证：
- `GET /health`
- `GET /library`
- `GET /profile`
- `PUT /profile`
- `GET /moments/user/:userId`
- `POST /follow`
- `GET /is-following/:userId`
- `DELETE /follow/:userId`
- `GET /following`
- `POST /upload-url`
- `GET /image-url/:path`
- `POST /journal-feature/:id`
- `DELETE /journal/:id`
- `GET /plants?admin_view=true`
- `DELETE /admin/plants/:id`

### 2. 用户侧真实验证
优先验证：
- 登录成功
- 刷新后会话恢复
- `Profile` 资料读取 / 保存 / 头像展示
- 公开用户页（含 0 内容用户）
- follow / unfollow
- following 列表同步
- 植物详情时间线

### 3. 管理侧真实验证
优先验证：
- 管理员登录
- 植物库新增 / 编辑 / 删除
- 上传图片链路
- 日记列表 / 详情 / 精选 / 删除
- 已认领植物
- 时间线
- Dashboard 关键加载

---

## 执行规则

- 不要再把 `SUPABASE_SERVICE_ROLE_KEY` 当阻塞
- 不要再把测试账号当阻塞
- 若当前环境无法做完整浏览器交互，就做“最强可行验证”，并明确区分：
  - 已验证
  - 未完全验证
  - 真正阻塞
- 只有在**真实验收也无法继续**时，才允许向用户汇报阻塞

---

## 完成定义

满足以下条件，才可把 phase-1 判定为“验收通过”：
- 后端关键链路完成真实验证
- 用户侧关键链路完成真实验证
- 管理侧关键链路完成真实验证
- 关键失败项能明确归因，不存在“前端显示成功但后端未落库”的假成功

---

## 如果下一轮又断片

先读：
1. `CURRENT_STATE.md`
2. `NEXT_ACTION.md`
3. `MANUAL_VERIFICATION_PACKAGE.md`

然后直接继续执行，不要重新开题。