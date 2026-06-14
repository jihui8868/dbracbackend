# Swagger UI 登录与认证指南

## 概述

FastAPI 应用已配置支持 OAuth2 标准认证方案，允许在 Swagger UI 中直接登录并在测试其他 API 时保持登录状态。

## 如何在 Swagger UI 中登录

### 1. 启动应用
```bash
uv run uvicorn app.main:app --reload
```

### 2. 打开 Swagger UI
访问：`http://localhost:8000/docs`

### 3. 在 Swagger UI 中登录

#### 步骤 A: 注册新用户（如果还没有账户）
1. 找到 `POST /auth/register` 端点
2. 点击 "Try it out" 按钮
3. 填入以下信息：
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123"
}
```
4. 点击 "Execute" 完成注册

#### 步骤 B: 登录获取 Token
1. 找到 `POST /auth/login` 端点（登录是一个特殊的认证端点）
2. 在 Swagger UI 右上角找到 🔓 **"Authorize"** 按钮（或锁形图标）
3. 点击 "Authorize" 按钮
4. 在弹出的对话框中输入：
   - **username**: testuser
   - **password**: testpass123
5. 点击 "Authorize" 按钮
6. 点击 "Close" 关闭对话框

### 4. 验证登录状态
登录成功后，你会看到：
- 🔒 锁形图标变成 **已锁定**（表示已认证）
- 右上角显示用户已登录

### 5. 测试受保护的 API

现在所有需要认证的端点都会自动在请求头中包含 JWT token：

#### 测试获取当前用户信息
1. 找到 `GET /auth/me` 端点
2. 点击 "Try it out"
3. 点击 "Execute"
4. 应该看到你的用户信息

#### 测试创建对话
1. 找到 `POST /chat/sessions` 端点
2. 点击 "Try it out"
3. 点击 "Execute"
4. 应该成功创建对话

#### 测试列表对话
1. 找到 `GET /chat/sessions` 端点
2. 点击 "Try it out"
3. 点击 "Execute"
4. 应该看到你创建的所有对话

#### 测试发送消息
1. 找到 `POST /chat/{conversation_id}/message` 端点
2. 点击 "Try it out"
3. 填入对话 ID（从列表对话端点获取）
4. 填入消息请求体：
```json
{
  "message": "Hello, how are you?"
}
```
5. 点击 "Execute"
6. 应该看到流式的 SSE 响应

## 自动令牌管理

### 令牌自动包含
登录后，所有带有安全标记的端点会自动在以下地方包含令牌：
- **Authorization 请求头**: `Authorization: Bearer <token>`

### 令牌过期处理
- 令牌默认有效期：**60 分钟**（可在 `.env` 中配置 `ACCESS_TOKEN_EXPIRE_MINUTES`）
- 令牌过期后，重新点击 "Authorize" 登录

### 手动登出
要清除 Swagger UI 中的认证：
1. 点击右上角的 "Authorize" 按钮
2. 点击 "Logout"
3. 确认

## 常见问题

### Q: 为什么看不到 Authorize 按钮？
A: 确保应用已正确启动，并且 `app/main.py` 中包含了 OAuth2 配置。

### Q: 登录后其他 API 仍显示 401 Unauthorized
A: 
- 检查令牌是否过期
- 尝试重新登录
- 检查 `.env` 中的 `SECRET_KEY` 是否正确

### Q: 如何在 curl 中使用令牌？
A: 从 Swagger UI 登录后，复制返回的 `access_token`，然后：
```bash
TOKEN="your-access-token-here"
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Q: 如何在代码中使用？
A: 使用从登录端点获得的 token：
```python
import requests

# 登录
response = requests.post(
    "http://localhost:8000/auth/login",
    data={"username": "testuser", "password": "testpass123"}
)
token = response.json()["access_token"]

# 使用 token 调用受保护的 API
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/auth/me",
    headers=headers
)
print(response.json())
```

## API 端点安全性总结

| 端点 | 需要认证 | 说明 |
|------|---------|------|
| POST /auth/register | ❌ | 注册新用户 |
| POST /auth/login | ❌ | 登录获取 token |
| GET /auth/me | ✅ | 获取当前用户（需要登录） |
| GET /chat/sessions | ✅ | 列表对话（需要登录） |
| POST /chat/sessions | ✅ | 创建对话（需要登录） |
| POST /chat/{id}/message | ✅ | 发送消息（需要登录） |
| GET /health | ❌ | 健康检查 |

## 技术细节

### 使用的认证方案
- **类型**: OAuth2 with Password flow (Resource Owner Password Credentials)
- **Token 类型**: JWT (JSON Web Token)
- **算法**: HS256
- **存储位置**: Request Header (`Authorization: Bearer <token>`)

### Swagger UI 集成
- 自动生成 "Authorize" 按钮
- 令牌自动注入到所有需要认证的请求
- 支持令牌刷新（过期时重新登录）

## 下一步

1. 启动应用：`uv run uvicorn app.main:app --reload`
2. 打开 Swagger UI：`http://localhost:8000/docs`
3. 点击 Authorize 登录
4. 测试 API 端点
5. 查看完整 API 文档：`http://localhost:8000/redoc`

---

**提示**: ReDoc（`/redoc`）也支持 OAuth2 认证，提供更好的文档展示。
