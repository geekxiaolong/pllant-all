# MediaMTX 设置指南 - 心植项目

> **归档说明（2026-03-09）**：本文档属于拆分前根工作区的流媒体部署资料，仅保留为历史参考。
> 继续开发/部署请先查看 `THREE-APP-DEPLOYMENT.md`，并在三端子仓库中执行当前流程。


## 快速开始

MediaMTX 是一个轻量级的流媒体服务器，可以将 RTSP 流转换为 WebRTC，使其能在浏览器中播放。

## 步骤 1: 下载 MediaMTX

访问 [GitHub Releases](https://github.com/bluenviron/mediamtx/releases)

下载适合你系统的版本：
- **Windows**: `mediamtx_vX.X.X_windows_amd64.zip`
- **macOS (Intel)**: `mediamtx_vX.X.X_darwin_amd64.tar.gz`
- **macOS (Apple Silicon)**: `mediamtx_vX.X.X_darwin_arm64.tar.gz`
- **Linux**: `mediamtx_vX.X.X_linux_amd64.tar.gz`

## 步骤 2: 解压并配置

### Windows
```cmd
# 解压 zip 文件到你想要的目录
# 例如: C:\mediamtx\
```

### macOS/Linux
```bash
# 解压 tar.gz 文件
tar -xzf mediamtx_vX.X.X_*.tar.gz

# 移动到系统目录（可选）
sudo mv mediamtx /usr/local/bin/
```

## 步骤 3: 配置文件

在 mediamtx 所在目录创建或编辑 `mediamtx.yml` 文件：

```yaml
###############################################
# MediaMTX 配置文件 - 心植项目
###############################################

# 日志级别
logLevel: info
logDestinations: [stdout]

# API 服务器（可选，用于监控）
api: yes
apiAddress: :9997

###############################################
# WebRTC 配置（必需）
###############################################
webRTC: yes
webRTCAddress: :8889

# 允许所有来源的 CORS 请求
webRTCAllowOrigin: '*'

# ICE 服务器配置
webRTCICEServers2:
  - urls: ['stun:stun.l.google.com:19302']

###############################################
# RTSP 服务器配置
###############################################
rtspAddress: :8554
rtsp: yes

###############################################
# 流路径配置
###############################################
paths:
  # 心植项目默认流
  heartplant:
    # RTSP 源地址（替换为你的摄像头地址）
    source: rtsp://admin:reolink123@192.168.92.202:554
    
    # 按需启动（有人观看时才连接源）
    sourceOnDemand: yes
    
    # 源协议
    sourceProtocol: automatic
    
    # 当流准备好时运行的命令（可选）
    runOnReady: echo "Heart Plant stream is ready"
    
    # 当流断开时运行的命令（可选）
    runOnNotReady: echo "Heart Plant stream disconnected"
  
  # 你可以添加更多流路径
  # plant2:
  #   source: rtsp://username:password@camera-ip:554/stream
  #   sourceOnDemand: yes
```

## 步骤 4: 启动服务器

### Windows
```cmd
# 在 mediamtx 目录下打开命令提示符
mediamtx.exe

# 或者双击 mediamtx.exe 文件
```

### macOS/Linux
```bash
# 方法 1: 如果在当前目录
./mediamtx

# 方法 2: 如果已安装到系统目录
mediamtx

# 方法 3: 后台运行
nohup ./mediamtx > mediamtx.log 2>&1 &
```

## 步骤 5: 验证运行

成功启动后，你应该看到：

```
2024/03/03 10:00:00 INF [RTSP] listener opened on :8554
2024/03/03 10:00:00 INF [WebRTC] listener opened on :8889
2024/03/03 10:00:00 INF [API] listener opened on :9997
```

## 步骤 6: 测试连接

### 方法 1: 使用心植测试工具
1. 在应用中访问 `/stream-test` 页面
2. 点击"测试服务器连接"
3. 查看测试结果

### 方法 2: 浏览器测试
访问：
- API: `http://localhost:9997/v3/config/global/get`
- WebRTC: `http://localhost:8889/heartplant` (应显示流信息)

### 方法 3: VLC 测试 RTSP 源
使用 VLC 媒体播放器打开网络流：
```
rtsp://admin:reolink123@192.168.92.202:554
```

## 常见问题

### 问题 1: "Failed to fetch" 或无法连接

**可能原因：**
- MediaMTX 未运行
- 防火墙阻止端口 8889
- IP 地址不正确

**解决方案：**
```bash
# 检查 MediaMTX 是否运行
ps aux | grep mediamtx  # Linux/macOS
tasklist | findstr mediamtx  # Windows

# 检查端口是否被占用
netstat -ano | findstr 8889  # Windows
lsof -i :8889  # Linux/macOS

# 测试端口是否可访问
curl http://localhost:8889/
```

### 问题 2: CORS 错误

确保 `mediamtx.yml` 中设置了：
```yaml
webRTCAllowOrigin: '*'
```

### 问题 3: RTSP 源无法连接

**检查清单：**
- [ ] 摄像头在线且可访问
- [ ] RTSP URL 正确（包括用户名、密码、端口）
- [ ] 网络连接正常
- [ ] 防火墙未阻止 RTSP 端口（通常是 554）

**测试命令：**
```bash
# 使用 ffmpeg 测试
ffmpeg -rtsp_transport tcp -i rtsp://admin:reolink123@192.168.92.202:554 -frames:v 1 test.jpg

# 使用 ffprobe 检查流信息
ffprobe -rtsp_transport tcp rtsp://admin:reolink123@192.168.92.202:554
```

### 问题 4: 在 Windows 上启动失败

1. 确保已安装 [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. 以管理员身份运行
3. 检查杀毒软件是否阻止

### 问题 5: 视频延迟高

在 `mediamtx.yml` 中调整：
```yaml
paths:
  heartplant:
    source: rtsp://admin:reolink123@192.168.92.202:554
    sourceOnDemand: yes
    # 添加这些选项
    readBufferCount: 2
```

## 高级配置

### 多摄像头支持

```yaml
paths:
  plant1:
    source: rtsp://admin:password@192.168.1.100:554
  plant2:
    source: rtsp://admin:password@192.168.1.101:554
  plant3:
    source: rtsp://admin:password@192.168.1.102:554
```

### HTTPS 支持（生产环境推荐）

```yaml
webRTCServerKey: /path/to/server.key
webRTCServerCert: /path/to/server.crt
```

### 认证保护

```yaml
paths:
  heartplant:
    source: rtsp://admin:reolink123@192.168.92.202:554
    readUser: viewer
    readPass: secret123
```

## 性能优化

### 内存优化
```yaml
readBufferCount: 512
```

### CPU 优化
```yaml
# 减少编码开销
protocols: [webrtc]
```

## 开机自启动

### Windows (使用 NSSM)
```cmd
# 下载 NSSM: https://nssm.cc/download
nssm install mediamtx "C:\mediamtx\mediamtx.exe"
nssm start mediamtx
```

### Linux (systemd)
创建 `/etc/systemd/system/mediamtx.service`:
```ini
[Unit]
Description=MediaMTX RTSP/WebRTC Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/mediamtx
ExecStart=/path/to/mediamtx/mediamtx
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable mediamtx
sudo systemctl start mediamtx
sudo systemctl status mediamtx
```

### macOS (launchd)
创建 `~/Library/LaunchAgents/com.mediamtx.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mediamtx</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/mediamtx</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

加载服务：
```bash
launchctl load ~/Library/LaunchAgents/com.mediamtx.plist
```

## 监控和日志

### 查看实时日志
```bash
# Linux/macOS
tail -f /path/to/mediamtx.log

# 或直接运行查看输出
./mediamtx
```

### API 监控
访问 `http://localhost:9997/v3/paths/list` 查看所有流状态

### 健康检查
```bash
curl http://localhost:9997/v3/config/global/get
```

## 资源

- [官方文档](https://github.com/bluenviron/mediamtx)
- [配置参考](https://github.com/bluenviron/mediamtx/blob/main/mediamtx.yml)
- [问题反馈](https://github.com/bluenviron/mediamtx/issues)

## 需要帮助？

如果遇到问题：
1. 检查 MediaMTX 日志输出
2. 使用心植应用的测试工具诊断
3. 确认网络和防火墙配置
4. 测试 RTSP 源是否可用

祝你的植物茁壮成长！🌱
