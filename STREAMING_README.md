# 🌱 心植 (HeartPlant) WebRTC 实时流播放

> **归档说明（2026-03-09）**：本文档基于拆分前根目录/旧单体结构编写，仅作为流媒体联调历史参考。
> 当前三端分离后的实际开发入口请优先查看 `README.md`、`START_HERE.md`、`THREE-APP-DEPLOYMENT.md`，并进入 `heart-plant/`、`heart-plant-admin/`、`heart-plant-api/` 对应子仓库执行。


这个功能实现了在互动页使用 WebRTC 技术实时播放 RTSP 摄像头流。

## 📋 功能概述

- ✅ WebRTC 低延迟实时流播放
- ✅ RTSP 到 WebRTC 自动转换
- ✅ 自动重连机制
- ✅ 优雅的连接状态显示
- ✅ 错误处理和故障提示

## 🚀 快速开始

### 方式 1: 使用自动化脚本（推荐）

#### Linux / macOS

```bash
# 运行自动配置脚本
chmod +x mediamtx-quickstart.sh
./mediamtx-quickstart.sh

# 脚本会自动:
# 1. 下载 mediamtx
# 2. 创建配置文件
# 3. 配置摄像头信息
# 4. 生成启动脚本
```

#### Windows

```cmd
# 双击运行
mediamtx-quickstart.bat

# 或在命令行中运行
mediamtx-quickstart.bat
```

### 方式 2: 使用 Docker（最简单）

```bash
# 创建配置文件（使用上面脚本生成的配置）
# 或手动创建 mediamtx.yml

# 运行 Docker 容器
docker run --rm -it \
  -p 8889:8889 \
  -p 8888:8888 \
  -p 8554:8554 \
  -v $(pwd)/mediamtx/mediamtx.yml:/mediamtx.yml \
  bluenviron/mediamtx:latest
```

### 方式 3: 手动配置

详细步骤请参考 [WEBRTC_SETUP.md](./WEBRTC_SETUP.md)

## 🎯 验证配置

### 1. 启动 mediamtx

```bash
cd mediamtx
./start.sh  # Linux/macOS
# 或
start.bat   # Windows
```

你应该看到类似输出：

```
2026/03/03 10:00:00 INF MediaMTX v1.8.1
2026/03/03 10:00:00 INF [path heartplant] source ready
2026/03/03 10:00:00 INF [WebRTC] listener opened on :8889
```

### 2. 访问 Web UI

打开浏览器访问：http://localhost:8888

你应该能看到 `heartplant` 流的状态。

### 3. 测试应用

1. 启动 HeartPlant 前端应用
2. 登录并进入**互动页**
3. 点击**摄像头图标**按钮（Camera 图标）
4. 应该能看到实时视频流播放

## 📁 项目文件结构

```
your-project/
├── src/
│   └── app/
│       ├── components/
│       │   └── WebRTCPlayer.tsx         # WebRTC 播放器组件
│       └── pages/
│           └── Interaction.tsx           # 互动页（使用播放器）
├── mediamtx/                             # mediamtx 安装目录
│   ├── mediamtx                          # 可执行文件
│   ├── mediamtx.yml                      # 配置文件
│   └── start.sh / start.bat              # 启动脚本
├── WEBRTC_SETUP.md                       # 详细配置文档
├── STREAMING_README.md                   # 本文件
├── mediamtx-quickstart.sh                # Linux/macOS 快速配置脚本
└── mediamtx-quickstart.bat               # Windows 快速配置脚本
```

## ⚙️ 配置说明

### 修改摄像头地址

编辑 `mediamtx/mediamtx.yml`：

```yaml
paths:
  heartplant:
    source: rtsp://USERNAME:PASSWORD@CAMERA_IP:554
```

### 修改前端配置

编辑 `/src/app/pages/Interaction.tsx`：

```tsx
<WebRTCPlayer 
  streamUrl="http://YOUR_MEDIAMTX_IP:8889/heartplant/whep"
  rtspUrl="rtsp://username:password@CAMERA_IP:554"
/>
```

### 添加多个摄像头

在 `mediamtx.yml` 中：

```yaml
paths:
  heartplant:
    source: rtsp://admin:password@192.168.92.202:554
  
  plant2:
    source: rtsp://admin:password@192.168.92.203:554
  
  plant3:
    source: rtsp://admin:password@192.168.92.204:554
```

## 🐛 故障排查

### 问题：无法连接到摄像头

**检查项**:
- ✅ 摄像头 IP、用户名、密码是否正确
- ✅ 摄像头是否在同一网络
- ✅ RTSP 端口是否正确（默认 554）
- ✅ 防火墙是否阻止连接

**测试命令**:
```bash
# 使用 VLC 或 ffplay 测试 RTSP 流
ffplay rtsp://admin:reolink123@192.168.92.202:554
```

### 问题：WebRTC 连接失败

**检查项**:
- ✅ mediamtx 是否正常运行
- ✅ 端口 8889 是否被占用
- ✅ 浏览器是否支持 WebRTC
- ✅ CORS 配置是否正确

**查看日志**:
```bash
# 查看 mediamtx 日志
cd mediamtx
./mediamtx mediamtx.yml 2>&1 | tee mediamtx.log
```

### 问题：视频卡顿或延迟高

**优化建议**:
1. 确保使用有线网络连接
2. 降低摄像头输出码率
3. 使用 TCP 而非 UDP 传输
4. 启用转码功能（参考 WEBRTC_SETUP.md）

### 问题：浏览器显示连接错误

**解决方案**:
1. 检查浏览器控制台错误信息
2. 确认 mediamtx 的 `webrtcAllowOrigin` 设置
3. 尝试在 HTTPS 环境下使用（生产环境）

## 📊 性能参数

| 指标 | 值 |
|------|-----|
| 延迟 | < 1 秒 |
| 带宽 | 1-5 Mbps（取决于摄像头设置） |
| CPU 使用 | 低（无转码时） |
| 支持浏览器 | Chrome 94+, Firefox 92+, Safari 15.4+ |

## 🔐 安全建议

### 生产环境必做：

1. **使用 HTTPS**
   ```yaml
   webrtcAddress: :8889
   webrtcServerKey: /path/to/server.key
   webrtcServerCert: /path/to/server.crt
   ```

2. **限制访问来源**
   ```yaml
   webrtcAllowOrigin: 'https://yourdomain.com'
   ```

3. **启用认证**
   ```yaml
   paths:
     heartplant:
       readUser: viewer
       readPass: secure_password
   ```

4. **使用防火墙**
   ```bash
   # 只允许特定 IP 访问
   sudo ufw allow from 192.168.1.0/24 to any port 8889
   ```

## 📚 相关文档

- [详细配置指南](./WEBRTC_SETUP.md)
- [mediamtx 官方文档](https://github.com/bluenviron/mediamtx)
- [WebRTC 标准](https://webrtc.org/)
- [Reolink API](https://support.reolink.com/hc/en-us/articles/360007010473)

## 🎨 使用示例

### 基本使用

```tsx
import { WebRTCPlayer } from '../components/WebRTCPlayer';

function MyComponent() {
  return (
    <WebRTCPlayer 
      streamUrl="http://192.168.92.202:8889/heartplant/whep"
      rtspUrl="rtsp://admin:reolink123@192.168.92.202:554"
    />
  );
}
```

### 带错误处理

```tsx
<WebRTCPlayer 
  streamUrl="http://192.168.92.202:8889/heartplant/whep"
  rtspUrl="rtsp://admin:reolink123@192.168.92.202:554"
  onError={(error) => {
    console.error('Stream error:', error);
    toast.error('摄像头连接失败');
  }}
/>
```

### 动态切换流

```tsx
const [currentStream, setCurrentStream] = useState('heartplant');

<WebRTCPlayer 
  streamUrl={`http://192.168.92.202:8889/${currentStream}/whep`}
  rtspUrl={`rtsp://admin:reolink123@192.168.92.202:554`}
/>
```

## 🤝 贡献

如果你发现任何问题或有改进建议，欢迎提交 Issue 或 Pull Request。

## 📄 许可

本项目基于 MIT 许可证开源。

---

**开发团队**: 心植 (HeartPlant) IoT 社交项目组  
**最后更新**: 2026年3月3日
