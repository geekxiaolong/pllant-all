# WebRTC 视频流调试指南

> **归档说明（2026-03-09）**：本文档为旧单体阶段的 WebRTC 调试记录，现仅作历史排障参考。
> 当前代码开发请以三端分离仓库为准；工作区导航见 `README.md` / `START_HERE.md`。


## 🎯 问题分析

根据 MediaMTX 日志，我们看到：

```
✅ WebRTC 会话创建成功
✅ RTSP 源成功连接摄像头 (192.168.92.202:554)
✅ 检测到 2 个轨道 (H264 视频 + MPEG-4 音频)
✅ WebRTC 对等连接建立成功
❌ 8秒后连接关闭: "peer connection closed"
```

## 🔍 根本原因

**前端问题**：WebRTC 连接建立后，视频元素可能没有正确播放，导致浏览器认为连接无用并关闭。

可能的原因：
1. ❌ `video` 元素的 `autoPlay` 被浏览器阻止
2. ❌ 视频轨道接收后没有触发播放
3. ❌ 组件卸载或重新渲染导致连接中断

## ✅ 已修复的内容

### 1. **强制视频播放**
```typescript
pc.ontrack = (event) => {
  if (videoRef.current && event.streams[0]) {
    videoRef.current.srcObject = event.streams[0];
    
    // ✅ 显式调用 play() 并处理错误
    videoRef.current.play()
      .then(() => {
        setStatus('connected');
        onConnected?.();
      })
      .catch(err => {
        console.warn('Video play failed:', err);
        // 即使 autoplay 被阻止，仍标记为已连接
        setStatus('connected');
        onConnected?.();
      });
  }
};
```

### 2. **增强调试日志**
- ✅ 启用 `enableDebug={true}`
- ✅ 在浏览器控制台输出详细日志
- ✅ 在 UI 上显示实时调试信息

### 3. **连接状态监控**
- ✅ 监听 `onconnectionstatechange`
- ✅ 监听 `oniceconnectionstatechange`
- ✅ 所有状态变化都记录到日志

## 🧪 测试步骤

### 步骤 1：打开浏览器控制台
- 按 `F12` 打开开发者工具
- 切换到 `Console` 标签页

### 步骤 2：进入互动页面
1. 刷新页面
2. 进入 "互动" 页面
3. 点击摄像头图标 📷

### 步骤 3：观察日志
你应该看到类似的日志：
```
[HH:MM:SS] Connecting to: http://192.168.92.162:8889/heartplant/whep
[HH:MM:SS] RTCPeerConnection created
[HH:MM:SS] Transceivers added (video + audio)
[HH:MM:SS] SDP offer created and set
[HH:MM:SS] ICE gathering complete
[HH:MM:SS] Sending WHEP request to http://192.168.92.162:8889/heartplant/whep
[HH:MM:SS] WHEP response: 201
[HH:MM:SS] Remote SDP answer set, waiting for connection...
[HH:MM:SS] Connection state: connecting
[HH:MM:SS] ICE state: checking
[HH:MM:SS] Received track: video
[HH:MM:SS] Video playback started  ← 关键！
[HH:MM:SS] Connection state: connected
```

### 步骤 4：检查 MediaMTX 日志
```bash
# 在 MediaMTX 终端查看日志
# 你应该看到会话保持活动，而不是 8 秒后关闭
```

## 🚨 如果仍然失败

### 使用网络诊断工具
1. 点击互动页面底部的 **"网络诊断"** 按钮
2. 点击 **"开始诊断"**
3. 查看哪一步失败了

### 常见问题排查

#### 问题 1：浏览器阻止自动播放
**症状**：日志显示 "Play error: play() failed because..."

**解决方案**：
- 手动点击视频区域尝试播放
- 在浏览器设置中允许自动播放

#### 问题 2：防火墙阻止 WebRTC 端口
**症状**：日志停在 "ICE state: checking"

**解决方案**：
```bash
# 确保 UDP 端口开放
# macOS
sudo pfctl -d  # 临时关闭防火墙测试

# 或添加规则允许 8889 端口
```

#### 问题 3：摄像头断开
**症状**：MediaMTX 日志显示 "RTSP source: stopped: EOF"

**解决方案**：
- 检查摄像头电源和网络
- 尝试直接访问 RTSP 流：
  ```bash
  ffplay rtsp://admin:reolink123@192.168.92.202:554
  ```

## 📱 移动端测试

如果在移动设备上测试：
1. 确保设备和服务器在同一网络
2. 使用 HTTPS（WebRTC 在非本地网络需要 HTTPS）
3. 或使用 Chrome://flags 启用不安全源的 WebRTC

## 🎥 预期结果

**成功的表现**：
- ✅ 3-5 秒内看到视频画面
- ✅ 左上角显示绿色 "WebRTC • LIVE" 指示器
- ✅ MediaMTX 日志中会话保持活动
- ✅ Toast 提示 "视频流已连接"

**失败的表现**：
- ❌ 长时间显示 "Establishing WebRTC Connection..."
- ❌ 显示红色错误提示
- ❌ MediaMTX 日志中会话在 8 秒后关闭

## 📞 获取更多帮助

如果问题仍未解决：
1. 复制浏览器控制台的完整日志
2. 复制 MediaMTX 服务器日志
3. 截图错误信息
4. 描述具体的测试步骤

---

**最后更新**: 2026/03/03
**版本**: v2.0 (增强版)
