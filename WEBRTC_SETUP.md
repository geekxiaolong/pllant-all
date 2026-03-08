# WebRTC RTSP 流播放设置指南

> **归档说明（2026-03-09）**：本文档保留的是拆分前工作区的 WebRTC / MediaMTX 联调笔记，不再代表当前三端分离后的主入口。
> 若要继续开发，请先阅读根目录 `README.md`、`START_HERE.md` 与 `THREE-APP-DEPLOYMENT.md`，再进入对应子仓库处理实际代码与部署。


本项目使用 WebRTC 技术在互动页播放 RTSP 摄像头流。为了使浏览器能够播放 RTSP 流，需要配置 **mediamtx** 媒体服务器作为中间转换层。

## 架构说明

```
RTSP 摄像头 → mediamtx 服务器 → WebRTC → 浏览器
(192.168.92.202:554)  (转换层)      (WHEP协议)  (前端)
```

## 安装 mediamtx

### 方式 1: 下载预编译版本（推荐）

1. 访问 [mediamtx GitHub Releases](https://github.com/bluenviron/mediamtx/releases)
2. 下载适合你系统的版本：
   - Windows: `mediamtx_v1.x.x_windows_amd64.zip`
   - Linux: `mediamtx_v1.x.x_linux_amd64.tar.gz`
   - macOS: `mediamtx_v1.x.x_darwin_amd64.tar.gz`

3. 解压到任意目录

### 方式 2: 使用 Docker

```bash
docker run --rm -it \
  -e MTX_PROTOCOLS=tcp \
  -p 8889:8889 \
  -p 8554:8554 \
  -p 1935:1935 \
  -p 8888:8888 \
  bluenviron/mediamtx:latest
```

## 配置 mediamtx

### 1. 创建配置文件

在 mediamtx 目录下创建 `mediamtx.yml` 文件：

```yaml
# mediamtx.yml

# API 和 WebRTC 端口配置
api: yes
apiAddress: :9997

# WebRTC 配置
webrtc: yes
webrtcAddress: :8889
webrtcServerKey: server.key
webrtcServerCert: server.crt
webrtcAllowOrigin: '*'

# 路径配置
paths:
  # HeartPlant 摄像头流
  heartplant:
    # RTSP 源地址（你的 Reolink 摄像头）
    source: rtsp://admin:reolink123@192.168.92.202:554
    
    # 自动重连
    sourceOnDemand: yes
    sourceOnDemandStartTimeout: 10s
    sourceOnDemandCloseAfter: 10s
    
    # 转码设置（可选，降低延迟）
    runOnReady: ffmpeg -i rtsp://localhost:$RTSP_PORT/$MTX_PATH -c copy -f null -
    runOnReadyRestart: yes
```

### 2. 生成 SSL 证书（用于 WebRTC）

WebRTC 在生产环境中需要 HTTPS，但在本地开发可以使用自签名证书：

```bash
# 生成自签名证书
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes -subj "/CN=localhost"
```

或者，在本地开发时可以在配置中禁用 SSL（仅用于测试）：

```yaml
webrtc: yes
webrtcAddress: :8889
webrtcICEServers: []
```

### 3. 启动 mediamtx

```bash
# Windows
.\mediamtx.exe

# Linux/macOS
./mediamtx
```

启动后你应该看到类似输出：

```
2026/03/03 10:00:00 INF MediaMTX v1.x.x
2026/03/03 10:00:00 INF [path heartplant] source ready
2026/03/03 10:00:00 INF [WebRTC] listener opened on :8889
```

## 验证配置

### 1. 检查流是否可用

在浏览器访问 mediamtx 的 Web UI：

```
http://localhost:8888
```

你应该能看到 `heartplant` 流的状态。

### 2. 测试 WHEP 端点

```bash
curl http://localhost:8889/heartplant/whep
```

应该返回 405 错误（因为需要 POST 请求），这表示端点正常工作。

### 3. 在应用中测试

1. 启动 HeartPlant 应用
2. 登录并进入互动页
3. 点击摄像头图标按钮
4. 应该能看到实时视频流

## 配置说明

### 修改前端配置

如果你的 mediamtx 服务器运行在不同的地址或端口，需要修改前端配置：

在 `/src/app/pages/Interaction.tsx` 中找到：

```tsx
<WebRTCPlayer 
  streamUrl="http://192.168.92.202:8889/heartplant/whep"
  rtspUrl="rtsp://admin:reolink123@192.168.92.202:554"
/>
```

修改为你的配置：

```tsx
<WebRTCPlayer 
  streamUrl="http://YOUR_SERVER_IP:8889/YOUR_PATH/whep"
  rtspUrl="rtsp://username:password@YOUR_CAMERA_IP:554"
/>
```

### 添加多个摄像头

在 `mediamtx.yml` 中添加更多路径：

```yaml
paths:
  heartplant:
    source: rtsp://admin:reolink123@192.168.92.202:554
  
  plant2:
    source: rtsp://admin:password@192.168.92.203:554
  
  plant3:
    source: rtsp://admin:password@192.168.92.204:554
```

然后在前端根据植物 ID 动态切换流：

```tsx
<WebRTCPlayer 
  streamUrl={`http://192.168.92.202:8889/${currentPlant.cameraId}/whep`}
/>
```

## 性能优化

### 1. 降低延迟

在 `mediamtx.yml` 中添加：

```yaml
paths:
  heartplant:
    source: rtsp://admin:reolink123@192.168.92.202:554
    sourceProtocol: tcp  # 使用 TCP 而非 UDP
    readTimeout: 10s
    writeTimeout: 10s
```

### 2. 转码设置

如果摄像头输出的码率太高，可以使用 FFmpeg 转码：

```yaml
paths:
  heartplant:
    source: rtsp://admin:reolink123@192.168.92.202:554
    runOnReady: >
      ffmpeg -i rtsp://localhost:$RTSP_PORT/$MTX_PATH
      -c:v libx264 -preset ultrafast -tune zerolatency
      -b:v 1000k -maxrate 1000k -bufsize 2000k
      -c:a aac -b:a 128k
      -f rtsp rtsp://localhost:$RTSP_PORT/${MTX_PATH}_transcoded
    runOnReadyRestart: yes
```

### 3. 网络优化

- 确保摄像头和服务器在同一局域网
- 使用有线连接而非 Wi-Fi
- 配置防火墙允许 WebRTC 端口（默认 8889）

## 故障排查

### 问题 1: 连接失败

**症状**: WebRTC 播放器显示 "Stream Connection Failed"

**解决方案**:
1. 检查 mediamtx 是否正常运行
2. 验证 RTSP 源地址是否正确
3. 检查防火墙设置
4. 查看 mediamtx 日志：`./mediamtx 2>&1 | tee mediamtx.log`

### 问题 2: 视频卡顿

**症状**: 视频播放不流畅，频繁缓冲

**解决方案**:
1. 降低摄像头输出码率
2. 使用转码功能降低带宽占用
3. 检查网络连接质量
4. 增加 `readTimeout` 和 `writeTimeout` 值

### 问题 3: 浏览器不支持

**症状**: 某些浏览器无法播放

**解决方案**:
- 使用现代浏览器（Chrome 94+, Firefox 92+, Safari 15.4+）
- 确保浏览器启用了 WebRTC
- 在 HTTPS 环境下部署（生产环境）

### 问题 4: 跨域问题

**症状**: CORS 错误

**解决方案**:
在 `mediamtx.yml` 中设置：

```yaml
webrtcAllowOrigin: '*'  # 开发环境
# 或
webrtcAllowOrigin: 'https://yourdomain.com'  # 生产环境
```

## 生产环境部署

### 使用 Systemd（Linux）

创建服务文件 `/etc/systemd/system/mediamtx.service`:

```ini
[Unit]
Description=MediaMTX RTSP/WebRTC Server
After=network.target

[Service]
Type=simple
User=mediamtx
WorkingDirectory=/opt/mediamtx
ExecStart=/opt/mediamtx/mediamtx /opt/mediamtx/mediamtx.yml
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable mediamtx
sudo systemctl start mediamtx
```

### 使用 Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mediamtx:
    image: bluenviron/mediamtx:latest
    container_name: heartplant-mediamtx
    restart: unless-stopped
    ports:
      - "8889:8889"  # WebRTC
      - "8554:8554"  # RTSP
      - "8888:8888"  # Web UI
    volumes:
      - ./mediamtx.yml:/mediamtx.yml
    environment:
      - MTX_PROTOCOLS=tcp
```

启动：

```bash
docker-compose up -d
```

## 安全建议

1. **使用 HTTPS**: 生产环境必须使用 HTTPS 和有效的 SSL 证书
2. **限制访问**: 使用防火墙限制 mediamtx 端口的访问
3. **认证**: 在 mediamtx 配置中启用认证

```yaml
paths:
  heartplant:
    source: rtsp://admin:reolink123@192.168.92.202:554
    publishUser: admin
    publishPass: secretpassword
    readUser: viewer
    readPass: viewerpassword
```

4. **定期更新**: 保持 mediamtx 更新到最新版本

## 参考资源

- [mediamtx 官方文档](https://github.com/bluenviron/mediamtx)
- [WebRTC 标准](https://webrtc.org/)
- [WHEP 协议规范](https://datatracker.ietf.org/doc/draft-ietf-wish-whep/)
- [Reolink API 文档](https://support.reolink.com/hc/en-us/articles/360007010473-CGI-Commands)

## 联系支持

如果遇到问题，请检查：
1. mediamtx 日志文件
2. 浏览器开发者工具控制台
3. 网络连接状态

项目地址：https://github.com/bluenviron/mediamtx
