# 🌱 心植项目 - 视频流快速开始指南

> **归档说明（2026-03-09）**：本文档基于拆分前工作区结构整理，现仅作为流媒体方案历史参考。
> 当前三端分离后的开发入口请查看 `README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md`。


## 🎯 目标

让你的 RTSP 摄像头流能在浏览器中播放。

## 📊 方案对比

我们提供了两种方案：

| | 方案 A：自建服务（推荐） | 方案 B：使用 MediaMTX |
|---|---|---|
| **优点** | • 可定制化<br>• 与项目集成<br>• 易于调试 | • 成熟稳定<br>• 功能完整<br>• 生产就绪 |
| **缺点** | • 需要维护 | • 配置稍复杂 |
| **适用场景** | 开发/原型/学习 | 生产环境 |

---

## 🚀 方案 A：自建流媒体服务（5分钟）

### 第 1 步：安装依赖

#### 安装 Deno

```bash
# macOS/Linux
curl -fsSL https://deno.land/install.sh | sh

# Windows (PowerShell)
irm https://deno.land/install.ps1 | iex
```

#### 安装 FFmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# 下载: https://www.gyan.dev/ffmpeg/builds/
# 解压并添加到 PATH
```

**验证安装**:
```bash
deno --version
ffmpeg -version
```

### 第 2 步：配置流源

编辑 `/stream-server/ffmpeg-websocket-server.ts` 的第 17 行：

```typescript
const CONFIG = {
  port: 8889,
  rtspSources: {
    'heartplant': {
      url: 'rtsp://admin:reolink123@192.168.92.202:554',  // ⬅️ 修改为你的摄像头地址
      name: '心植默认流',
    },
    // 可以添加更多摄像头
  },
  // ...
};
```

### 第 3 步：启动服务器

```bash
cd stream-server

# Linux/macOS
chmod +x start.sh
./start.sh

# Windows
start.bat

# 或直接运行
deno run --allow-net --allow-read --allow-env --allow-run ffmpeg-websocket-server.ts
```

**成功标志**:
```
🌱 心植流媒体转换服务器 (FFmpeg + WebSocket)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 监听端口: 8889
📹 输出格式: mjpeg
🎥 可用流:
   • heartplant: 心植默认流
```

### 第 4 步：测试

在应用中：
1. 访问互动页面
2. 点击"🔧 视频流调试工具"
3. 点击"测试服务器连接"
4. 点击"启动播放器"

应该能看到实时视频！🎉

---

## 🏢 方案 B：使用 MediaMTX（生产环境）

### 第 1 步：下载 MediaMTX

访问: https://github.com/bluenviron/mediamtx/releases

下载对应版本：
- Windows: `mediamtx_vX.X.X_windows_amd64.zip`
- macOS: `mediamtx_vX.X.X_darwin_amd64.tar.gz`
- Linux: `mediamtx_vX.X.X_linux_amd64.tar.gz`

### 第 2 步：配置

解压后，在同目录创建 `mediamtx.yml`:

```yaml
# WebRTC 配置
webRTC: yes
webRTCAddress: :8889
webRTCAllowOrigin: '*'

# ICE 服务器
webRTCICEServers2:
  - urls: ['stun:stun.l.google.com:19302']

# 流路径
paths:
  heartplant:
    source: rtsp://admin:reolink123@192.168.92.202:554
    sourceOnDemand: yes
```

### 第 3 步：启动

```bash
# Windows
./mediamtx.exe

# macOS/Linux
./mediamtx
```

### 第 4 步：更新前端配置

在前端使用 WebRTC 模式：

```typescript
// 在 Interaction 页面或测试页面
<WebRTCPlayer 
  streamUrl="http://localhost:8889/heartplant/whep"  // ⬅️ WHEP 端点
  rtspUrl="rtsp://admin:reolink123@192.168.92.202:554"
/>
```

---

## 🔧 故障排除

### 问题 1: "Failed to fetch" / 无法连接

**检查**:
```bash
# 服务器是否运行？
curl http://localhost:8889/health  # 方案 A
curl http://localhost:8889/       # 方案 B

# 端口是否被占用？
netstat -ano | findstr 8889  # Windows
lsof -i :8889                # Linux/macOS
```

**解决**: 
- 确保服务器正在运行
- 检查防火墙设置
- 尝试更换端口

### 问题 2: FFmpeg 未找到

**检查**:
```bash
which ffmpeg   # Linux/macOS
where ffmpeg   # Windows
```

**解决**: 重新安装 FFmpeg 并确保在 PATH 中

### 问题 3: RTSP 源无法连接

**测试摄像头**:
```bash
# 方法 1: FFmpeg 测试
ffmpeg -rtsp_transport tcp -i rtsp://admin:reolink123@192.168.92.202:554 -frames:v 1 test.jpg

# 方法 2: 使用 VLC 播放器
# 打开 VLC -> Media -> Open Network Stream
# 输入 RTSP URL
```

**检查清单**:
- [ ] 摄像头 IP 地址正确
- [ ] 用户名密码正确
- [ ] 端口正确（通常是 554）
- [ ] 网络连通（ping 摄像头 IP）
- [ ] 防火墙未阻止

### 问题 4: 视频延迟高

**优化方案 A**:

编辑 `ffmpeg-websocket-server.ts` 第 91 行：

```typescript
const ffmpegArgs = [
  '-rtsp_transport', 'tcp',
  '-fflags', 'nobuffer',       // ⬅️ 添加：禁用缓冲
  '-flags', 'low_delay',       // ⬅️ 添加：低延迟
  '-i', rtspUrl,
  '-f', 'mjpeg',
  '-q:v', '5',
  '-vf', 'scale=640:360',      // ⬅️ 降低分辨率
  '-r', '10',                  // ⬅️ 降低帧率
  'pipe:1'
];
```

### 问题 5: 黑屏但没有错误

**检查**:
1. 打开浏览器控制台（F12）
2. 查看 Console 标签的错误信息
3. 查看 Network 标签的网络请求

**常见原因**:
- RTSP 源返回黑帧
- 视频格式不兼容
- 浏览器权限问题

---

## 📋 配置参数说明

### 方案 A (WebSocket)

```typescript
// 视频质量
'-q:v', '3',  // 1=最高, 31=最低

// 分辨率
'-vf', 'scale=1280:720',  // 宽x高

// 帧率
'-r', '25',  // 每秒帧数

// 传输协议
'-rtsp_transport', 'tcp',  // 或 'udp'
```

**推荐配置**:

| 场景 | 质量 | 分辨率 | 帧率 | 延迟 | 带宽 |
|------|------|--------|------|------|------|
| 演示 | 5 | 640x360 | 15 | ~1s | ~2 Mbps |
| 正常 | 4 | 1280:720 | 25 | ~1.5s | ~5 Mbps |
| 高清 | 2 | 1920x1080 | 30 | ~2s | ~15 Mbps |

### 方案 B (MediaMTX)

```yaml
# 按需启动（节省资源）
sourceOnDemand: yes

# 读取超时
readTimeout: 10s

# 缓冲设置
readBufferCount: 512
```

---

## 🎓 工作原理

### 方案 A 流程
```
摄像头 (RTSP)
    ↓
FFmpeg (转 MJPEG)
    ↓
WebSocket (传输帧)
    ↓
浏览器 (显示)
```

### 方案 B 流程
```
摄像头 (RTSP)
    ↓
MediaMTX (转 WebRTC)
    ↓
WHEP 协议
    ↓
浏览器 (显示)
```

---

## ✅ 验证清单

部署前检查：

- [ ] FFmpeg/MediaMTX 已安装并可运行
- [ ] 服务器成功启动（查看日志）
- [ ] RTSP 源可访问（用 VLC 测试）
- [ ] 防火墙已配置（开放 8889 端口）
- [ ] 前端配置正确（URL 地址）
- [ ] 浏览器控制台无错误
- [ ] 测试页面可以连接
- [ ] 实际视频能播放

---

## 📚 更多资源

- **详细文档**: `/stream-server/README.md`
- **MediaMTX 设置**: `/mediamtx-setup.md`
- **测试工具**: 应用内 `/stream-test` 页面
- **视频组件**: `/src/app/components/WebRTCPlayer.tsx`

## 🆘 需要帮助？

1. 查看服务器日志
2. 使用测试工具诊断
3. 检查浏览器控制台
4. 参考故障排除部分

---

**祝你的植物健康成长！🌱📹**
