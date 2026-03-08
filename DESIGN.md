# 心植 HeartPlant - 设计文档（历史归档）

> 归档说明（2026-03-09）：本文主要描述的是拆分前/迁移早期的单体产品设计与页面结构，保留用于产品背景、视觉语言、交互意图追溯。
>
> 当前项目已切换为三端分离工作区，请勿再把根目录当作单体项目直接开发或部署：
> - 用户前端：`./heart-plant`
> - 管理后台：`./heart-plant-admin`
> - 后端 API：`./heart-plant-api`
>
> 当前执行入口请优先查看：`README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md`、`VERIFICATION_RECORD.md`。

## 文档用途
- 用于追溯产品原始设计理念、视觉系统与信息架构
- 可作为三端拆分后做 UI / 文案一致性校验时的历史参考
- 不再作为当前代码目录结构、部署方式或开发入口说明

## 当前映射关系
- 用户端页面与交互实现：`heart-plant/src/`
- 管理后台页面与运营流程：`heart-plant-admin/src/`
- 后端接口与数据流：`heart-plant-api/supabase/functions/server/`

## 📱 项目概述

**心植 (HeartPlant)** 是一款基于情感驱动的 IoT 社交小程序，通过智能植物养护设备将人与人之间的情感联系可视化。用户可以通过共同照顾一株植物来维系和深化不同类型的关系（亲情、爱情、友情）或进行个人成长（悦己）。

### 核心理念

- 🌱 **情感具象化**：将抽象的情感关系转化为可见的植物生长
- 💚 **异步陪伴**：通过 IoT 设备实现远程实时互动
- 📖 **记忆沉淀**：通过日记和心情记录建立共同回忆
- 🎨 **氛围感知**：UI 随情感模式动态变化

---

## 🎨 设计系统

### 情感主题系统

应用支持四种情感模式，每种模式拥有独立的视觉语言：

#### 1. 亲情模式 (Kinship)
```
主色调: #FF8C42 (温暖橙)
渐变: from-orange-400 to-amber-500
情感关键词: 温暖、稳定、包容
视觉元素: 暖色光晕、柔和圆角
```

#### 2. 爱情模式 (Romance)
```
主色调: #FF6B9D (浪漫粉)
渐变: from-pink-400 to-rose-500
情感关键词: 浪漫、甜蜜、心动
视觉元素: 飘落的心形、渐变光影
```

#### 3. 友情模式 (Friendship)
```
主色调: #4ECDC4 (活力青)
渐变: from-teal-400 to-cyan-500
情感关键词: 轻松、活力、信任
视觉元素: 跳跃动画、明快色块
```

#### 4. 悦己模式 (Solo)
```
主色调: #556270 (沉静灰蓝)
渐变: from-slate-400 to-gray-600
情感关键词: 独立、专注、成长
视觉元素: 简约线条、专注氛围
```

### 字体系统

```css
/* 主标题 */
font-family: system-ui, -apple-system
font-weight: 900 (Black)
font-size: 24-32px
letter-spacing: -0.02em

/* 次级标题 */
font-weight: 700 (Bold)
font-size: 16-20px

/* 标签和元数据 */
font-weight: 700 (Bold)
font-size: 10-12px
text-transform: uppercase
letter-spacing: 0.1em

/* 正文 */
font-weight: 400 (Regular)
font-size: 14px
line-height: 1.6
```

### 圆角系统

```css
/* 卡片 */
border-radius: 32px (2rem)

/* 按钮 */
border-radius: 24px (1.5rem) - 全圆形

/* 输入框 */
border-radius: 24px (1.5rem)

/* 小元素 */
border-radius: 16px (1rem)
```

### 阴影层级

```css
/* 浮起 */
shadow-sm: 0 1px 2px rgba(0,0,0,0.05)

/* 卡片 */
shadow: 0 4px 16px rgba(0,0,0,0.08)

/* 强调 */
shadow-lg: 0 10px 40px rgba(0,0,0,0.12)

/* 顶层 */
shadow-2xl: 0 20px 60px rgba(0,0,0,0.15)
```

---

## 📐 页面架构

### 信息架构

```
HeartPlant App
│
├─ 🏠 Home (首页)
│  ├─ 植物列表卡片
│  ├─ 健康状态概览
│  └─ 快速操作入口
│
├─ 💬 Interaction (互动页)
│  ├─ 沉浸式植物视图
│  ├─ IoT 传感器仪表盘
│  ├─ 远程养护控制
│  ├─ 记录心情 → /mood/:plantId
│  ├─ 合写日记 → /journal/:plantId
│  └─ 成长时间轴
│
├─ ✨ Moments (瞬间页)
│  ├─ 照片墙瀑布流
│  ├─ 心情记录展示
│  └─ 日记精选内容
│
├─ 👤 Profile (我的)
│  ├─ 个人资料
│  ├─ 我的植物
│  ├─ 主题切换
│  └─ 设置项
│
├─ 🌱 Plant Adoption (认领页)
│  ├─ 植物档案展示
│  ├─ 认领流程
│  └─ 情感模式选择
│
├─ 😊 Mood Record (心情记录)
│  ├─ 情感状态选择 (6种)
│  ├─ 内容输入 (500字)
│  ├─ 活动标签 (6种)
│  └─ 照片上传
│
└─ 📝 Journal Write (合写日记)
   ├─ 标题输入
   ├─ 写作风格选择
   ├─ 多段落接力创作
   └─ 灵感提示
```

---

## 🔄 用户流程

### 1. 首次使用流程

```
启动应用 
  → 包容性入门
    → 选择使用模式（社交 / 悦己）
      → 浏览植物档案
        → 选择心仪植物
          → 确认认领
            → [社交模式] 邀请结缘对象
            → [悦己模式] 设置个人目标
              → 进入主界面
```

### 2. 日常互动流程

```
打开应用
  → 查看植物健康状态
    → 选择操作：
      ├─ 远程浇水 → 动画反馈 → 时间轴记录
      ├─ 远程施肥 → 动画反馈 → 时间轴记录
      ├─ 记录心情 → 填写表单 → 发布 → 回到互动页
      └─ 合写日记 → 接力创作 → 发布 → 回到互动页
```

### 3. 心情记录流程

```
点击"记录心情"
  → 导航到 /mood/:plantId
    → 选择当前心情 (6种状态)
      → 输入文字内容 (500字以内)
        → [可选] 添加活动标签
          → [可选] 上传照片
            → 点击"保存记录"
              → API 提交
                → Toast 确认
                  → 返回互动页
```

### 4. 合写日记流程

```
点击"合写日记"
  → 导航到 /journal/:plantId
    → 输入标题
      → 选择写作风格 (随笔/诗意/日记)
        → [可选] 查看灵感提示
          → 编写第一段内容
            → 点击"添加段落"
              → [多人模式] 自动切换到下一位作者
                → 继续添加段落...
                  → 点击"发布日记"
                    → API 提交
                      → Toast 确认
                        → 返回互动页
```

---

## 🧩 核心功能模块

### 1. 情感主题引擎

**技术实现**: React Context API

```typescript
interface EmotionalTheme {
  type: 'kinship' | 'romance' | 'friendship' | 'solo';
  primary: string;
  gradient: string;
  bg: string;
}

// 全局状态管理
const ThemeContext = React.createContext<ThemeContextValue>();

// 自动切换逻辑
useEffect(() => {
  if (currentPlant.type !== theme) {
    setTheme(currentPlant.type);
  }
}, [currentPlant]);
```

**功能特性**:
- 根据植物类型自动切换主题
- 平滑过渡动画（0.3s ease-in-out）
- 颜色变量注入到所有组件
- 持久化到本地存储

### 2. IoT 传感器仪表盘

**数据来源**: 模拟数据 + 未来接入真实硬件

```typescript
interface SensorData {
  temperature: number;    // 温度 (°C)
  humidity: number;       // 湿度 (%)
  light: number;          // 光照强度 (lux)
  soilMoisture: number;   // 土壤湿度 (%)
  lastUpdate: string;     // 最后更新时间
}
```

**可视化组件**:
- 实时数据卡片（温度、湿度）
- Recharts 迷你折线图
- 状态标签（NORMAL / THIRSTY / WARNING）
- 自动刷新机制

### 3. 远程养护控制

**交互设计**:
```
点击浇水按钮
  → 按钮缩放动画 (scale: 0.9)
  → 水滴图标跳动 (bounce)
  → 蓝色波纹扩散动画
  → Toast 提示 "爱心水滴已送达 💧"
  → 2秒后恢复正常状态
  → 时间轴添加操作记录
```

**未来扩展**: 
- 实际调用 IoT API
- 操作日志持久化
- 多人操作冲突处理
- 操作权限管理

### 4. 心情记录系统

**数据模型**:
```typescript
interface MoodRecord {
  id: string;
  plantId: string;
  userId: string;
  mood: 'happy' | 'calm' | 'sad' | 'love' | 'excited' | 'peaceful';
  content: string;        // 500字以内
  tags: string[];         // 活动标签
  photos?: string[];      // 照片URL数组
  timestamp: string;
}
```

**UI 组件**:
- 6种情感图标选择器（网格布局）
- 多行文本输入框（500字限制）
- 活动标签多选按钮（6种预设）
- 照片上传占位符（未来实现）
- 固定底部提交按钮

### 5. 合写日记系统

**协作机制**:
```typescript
interface JournalEntry {
  id: string;
  plantId: string;
  title: string;
  style: 'casual' | 'poetic' | 'diary';
  entries: Array<{
    id: string;
    author: string;
    content: string;
    timestamp: string;
  }>;
  createdAt: string;
}
```

**接力创作流程**:
1. 用户A写第一段 → 点击"添加段落"
2. 系统自动切换到用户B
3. 用户B写第二段 → 点击"添加段落"
4. 循环往复...
5. 任一用户点击"发布日记"完成创作

**特色功能**:
- 5条灵感提示语（可点击插入）
- 3种写作风格选择（影响UI风格）
- 作者头像接力显示
- 实时段落预览
- 删除段落功能

### 6. 成长时间轴

**事件类型**:
```typescript
type TimelineEvent = 
  | { type: 'watering'; author: string; }
  | { type: 'fertilizing'; author: string; }
  | { type: 'mood'; mood: string; preview: string; }
  | { type: 'journal'; title: string; authors: string[]; }
  | { type: 'photo'; caption: string; }
  | { type: 'system'; message: string; };
```

**交互逻辑**:
- 默认显示最近 2 条
- 点击"展开"显示全部
- 点击"收起"折叠回 2 条
- 图标旋转动画（180度）
- 列表项布局动画（Motion layout）

---

## 🛠 技术架构

### 前端技术栈

```
React 18               → 核心框架
TypeScript             → 类型安全
React Router v7        → 客户端路由
Tailwind CSS v4        → 样式系统
Motion (Framer Motion) → 动画库
Recharts               → 数据可视化
Lucide React           → 图标库
Sonner                 → Toast 通知
```

### 后端架构

```
Supabase Edge Functions (Deno)
  ↓
Hono Web Framework
  ↓
Three-Tier Architecture:
  - Frontend (React)
  - Server (Hono)
  - Database (PostgreSQL + KV Store)
```

### API 端点设计

```typescript
// 心情记录
POST   /make-server-4b732228/mood
GET    /make-server-4b732228/mood/:plantId
DELETE /make-server-4b732228/mood/:id

// 合写日记
POST   /make-server-4b732228/journal
GET    /make-server-4b732228/journal/:plantId
GET    /make-server-4b732228/journal/:id

// 植物管理
GET    /make-server-4b732228/plants
POST   /make-server-4b732228/plants/adopt
PATCH  /make-server-4b732228/plants/:id

// IoT 控制（未来）
POST   /make-server-4b732228/iot/water
POST   /make-server-4b732228/iot/fertilize
GET    /make-server-4b732228/iot/sensor-data/:plantId
```

### 数据存储策略

**KV Store 使用场景**:
```typescript
// 用户-植物关系
kv.set(`user:${userId}:plants`, plantIds);

// 植物元数据
kv.set(`plant:${plantId}:metadata`, plantData);

// 心情记录（轻量）
kv.set(`mood:${moodId}`, moodRecord);

// 日记条目
kv.set(`journal:${journalId}`, journalData);

// 时间轴缓存
kv.set(`timeline:${plantId}`, events);
```

**未来扩展**: 
- 照片存储使用 Supabase Storage
- 实时数据使用 Supabase Realtime
- 用户认证使用 Supabase Auth

---

## 🎯 关键设计决策

### 1. 为什么选择页面导航而非弹框？

**原因**:
- 小程序用户习惯页面跳转交互
- 表单内容较多，需要完整屏幕空间
- 避免弹框层级管理复杂性
- 更好的键盘输入体验
- 清晰的返回逻辑

**实现**:
- 使用 React Router 实现页面级路由
- 传递 `plantId` 参数到子页面
- 提交成功后使用 `navigate(-1)` 返回
- 保留时间轴的展开/收起功能

### 2. 情感主题自动切换

**设计思路**:
- 当用户切换植物时，主题自动跟随植物类型变化
- 避免用户手动切换主题的认知负担
- 强化"不同植物代表不同关系"的心智模型

**实现细节**:
```typescript
useEffect(() => {
  if (currentPlant.type !== theme) {
    setTheme(currentPlant.type as EmotionalTheme);
  }
}, [currentPlant, theme, setTheme]);
```

### 3. 悦己模式的差异化设计

**与社交模式的区别**:

| 特性 | 社交模式 | 悦己模式 |
|------|---------|---------|
| 颜色 | 暖色调 | 冷灰调 |
| 互动 | 多人协作 | 个人专注 |
| 文案 | "记录心情" | "成长记录" |
| 文案 | "合写日记" | "生长曲线" |
| 氛围 | Live / 热烈 | Focus / 沉静 |

**目的**: 满足独居用户、个人成长用户的需求

### 4. 时间轴的渐进式披露

**信息架构**:
```
默认状态: 显示 2 条最新事件
  ↓ 点击"展开"
完全展开: 显示所有历史事件
  ↓ 点击"收起"
返回默认状态
```

**设计理由**:
- 避免首屏信息过载
- 快速查看最新动态
- 按需加载完整历史

---

## 📊 性能优化策略

### 1. 图片优化
```typescript
// 使用 Unsplash API 的优化参数
const imageUrl = `${baseUrl}?q=80&w=1080&auto=format`;

// 懒加载
<img loading="lazy" src={imageUrl} />

// 占位符
<ImageWithFallback src={imageUrl} fallback={placeholder} />
```

### 2. 动画性能
```css
/* 使用 GPU 加速属性 */
transform: translateX() translateY() scale() rotate();
opacity: 0.5;

/* 避免触发重排的属性 */
❌ width, height, left, top
✅ transform, opacity
```

### 3. 代码分割
```typescript
// 路由级别的代码分割
const MoodRecordPage = lazy(() => import('./pages/MoodRecordPage'));
const JournalWritePage = lazy(() => import('./pages/JournalWritePage'));
```

### 4. 状态管理优化
```typescript
// 使用 Context 避免 prop drilling
// 使用 memo 避免不必要的重渲染
const MemoizedComponent = React.memo(Component);
```

---

## 🔮 未来规划

### Phase 1: MVP (已完成)
- [x] 四种情感主题系统
- [x] 植物认领流程
- [x] IoT 仪表盘（模拟数据）
- [x] 心情记录功能
- [x] 合写日记功能
- [x] 成长时间轴

### Phase 2: 硬件集成
- [ ] 接入真实 IoT 传感器
- [ ] WebSocket 实时数据同步
- [ ] 远程控制命令下发
- [ ] 设备状态监控

### Phase 3: 社交增强
- [ ] 用户注册/登录系统
- [ ] 好友系统与邀请机制
- [ ] 评论与互动功能
- [ ] 通知推送（浇水提醒）

### Phase 4: 内容扩展
- [ ] 照片上传与相册
- [ ] 视频日记功能
- [ ] 语音备忘录
- [ ] 植物成长动画

### Phase 5: 智能化
- [ ] AI 养护建议
- [ ] 情感分析（NLP）
- [ ] 个性化推荐
- [ ] 自动生成成长报告

---

## 🎨 设计资源

### 配色参考
- **亲情**: Sunset Orange (#FF8C42)
- **爱情**: Bubblegum Pink (#FF6B9D)
- **友情**: Turquoise (#4ECDC4)
- **悦己**: Slate Gray (#556270)

### 字体推荐
- **西文**: SF Pro (Apple) / Inter / Manrope
- **中文**: PingFang SC / Source Han Sans / HarmonyOS Sans

### 图标库
- Lucide React (主要使用)
- Heroicons (备选)

### 插画风格
- 3D Isometric Plant Illustrations
- Soft Gradient Backgrounds
- Hand-drawn Botanical Elements

---

## 📝 开发规范

### 命名约定
```typescript
// 组件: PascalCase
export function MoodRecordPage() {}

// 工具函数: camelCase
export function formatTimestamp() {}

// 常量: UPPER_SNAKE_CASE
const API_BASE_URL = '...';

// CSS类名: kebab-case
<div className="mood-selector" />
```

### 文件结构
```
/src
  /app
    /components       # 可复用组件
    /pages           # 页面级组件
    /context         # React Context
    /hooks           # 自定义 Hooks
    /utils           # 工具函数
    /styles          # 全局样式
  /supabase
    /functions
      /server        # 后端代码
```

### Git 提交规范
```
feat: 新增心情记录页面路由
fix: 修复时间轴展开动画卡顿
style: 调整悦己模式配色
refactor: 重构主题切换逻辑
docs: 更新设计文档
```

---

## 🤝 贡献指南

### 设计贡献
1. 遵循四种情感主题的视觉语言
2. 保持 32px 圆角和柔和阴影的统一性
3. 动画时长控制在 200-400ms
4. 优先考虑无障碍设计（对比度、触摸区域）

### 代码贡献
1. 使用 TypeScript 并提供完整类型定义
2. 遵循 React Hooks 最佳实践
3. 组件必须响应式适配移动端
4. 提交前运行 `npm run lint`

---

## 📄 许可证

MIT License - 自由使用和修改

---

## 联系方式

- **项目名称**: 心植 HeartPlant
- **设计版本**: v1.0.0
- **最后更新**: 2026-03-02

---

**设计理念**: 让情感像植物一样生长，让陪伴像阳光一样温暖。🌱💚
