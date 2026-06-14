# Swagger UI 认证 - 快速参考

## 🚀 30秒快速开始

### 1. 启动服务器
```bash
uv run uvicorn app.main:app --reload
```

### 2. 打开 Swagger UI
浏览器访问: **http://localhost:8000/docs**

### 3. 流程

```
┌─────────────────────────────────────────────────────┐
│ 1. 点击右上角 "Authorize" 按钮 (🔓)                 │
├─────────────────────────────────────────────────────┤
│ 2. 弹窗出现，输入:                                  │
│    • username: testuser                             │
│    • password: testpass123                          │
├─────────────────────────────────────────────────────┤
│ 3. 点击 "Authorize" 按钮                           │
├─────────────────────────────────────────────────────┤
│ 4. 看到成功消息，点击 "Close"                      │
├─────────────────────────────────────────────────────┤
│ 5. 现在可以测试所有 API（自动带 token）             │
└─────────────────────────────────────────────────────┘
```

## 🔓 登录状态指示

| 图标 | 状态 | 说明 |
|------|------|------|
| 🔓 | 未登录 | 点击可登录 |
| 🔒 | 已登录 | 已通过认证，所有请求自动携带 token |

## 📋 常用测试流程

### 完整测试流程
```
1. [可选] 先 POST /auth/register 注册新账户
   ↓
2. 点击 Authorize 登录（使用已有账户）
   ↓
3. 测试 GET /auth/me (获取当前用户信息)
   ↓
4. 测试 POST /chat/sessions (创建对话)
   ↓
5. 测试 GET /chat/sessions (列表对话)
   ↓
6. 测试 POST /chat/{id}/message (发送消息)
```

## 🔑 JWT Token 信息

- **获取方式**: 点击 Authorize 登录
- **存储位置**: 浏览器本地（Swagger UI 管理）
- **过期时间**: 60 分钟（可配置）
- **格式**: `Authorization: Bearer eyJhbGc...`

## ❌ 常见问题速解

| 问题 | 解决方案 |
|------|--------|
| 看不到 Authorize 按钮 | 刷新页面，确保应用已启动 |
| 登录后仍显示 401 | 重新登录，或检查 token 是否过期 |
| Authorize 按钮不响应 | 检查浏览器控制台是否有错误 |
| 需要使用新账户 | 先点击 "Logout"，再登录新账户 |

## 🧪 示例 API 调用

### 注册（不需要 Authorize）
```
POST /auth/register
Body: {
  "username": "newuser",
  "email": "user@example.com",
  "password": "pass123"
}
```

### 登录（不需要 Authorize）
```
POST /auth/login
Body: username=testuser&password=testpass123
Response: { "access_token": "...", "token_type": "bearer" }
```

### 获取用户信息（需要 Authorize ✅）
```
GET /auth/me
Response: {
  "id": "uuid",
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2026-06-14T..."
}
```

### 创建对话（需要 Authorize ✅）
```
POST /chat/sessions
Response: {
  "id": "conv-uuid",
  "created_at": "2026-06-14T..."
}
```

### 列表对话（需要 Authorize ✅）
```
GET /chat/sessions
Response: [
  {
    "id": "conv-uuid",
    "title": null,
    "created_at": "2026-06-14T..."
  }
]
```

### 发送消息（需要 Authorize ✅）
```
POST /chat/{conversation_id}/message
Body: {
  "message": "Hello!"
}
Response: [Server-Sent Events 流式响应]
```

## 🎯 提示

1. **自动 Token 注入**: 登录后，Swagger UI 自动在所有请求的 Authorization 头中添加 token

2. **Token 有效期**: 默认 60 分钟，过期需重新登录

3. **浏览器存储**: Token 存储在浏览器，刷新页面后仍然有效

4. **多账户切换**: 点击 Logout，然后用不同账户重新 Authorize

5. **curl 测试**: 从 Swagger UI 登录后，复制 token 用于 curl 命令：
```bash
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/auth/me
```

---

**快速链接**:
- 📖 详细指南: [SWAGGER_LOGIN_GUIDE.md](SWAGGER_LOGIN_GUIDE.md)
- 🔐 安全配置: `app/router/auth.py`
- ⚙️ 环境配置: `.env`
