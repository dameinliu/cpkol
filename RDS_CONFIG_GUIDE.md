# 🔐 RDS 配置指南

由于当前 AWS 用户权限限制，请按照以下步骤手动获取 RDS 配置信息：

## 📋 1. 获取 RDS 基本信息

### 在 AWS 控制台中：
1. 登录 [AWS 控制台](https://console.aws.amazon.com)
2. 进入 **RDS 服务**
3. 在左侧菜单点击 **数据库**
4. 找到您的 PostgreSQL 实例，点击实例名称

### 记录以下信息：
```bash
# 从 "连接和安全性" 标签页获取：
RDS_HOST=您的端点地址.rds.amazonaws.com
RDS_PORT=5432  # 通常是 5432
RDS_DATABASE=您的数据库名

# 从 "配置" 标签页获取：
RDS_USERNAME=您的主用户名  # 通常是 postgres 或其他用户名
```

## 🔑 2. 密码配置选项

### 选项 A: 使用您设置的密码
如果您创建 RDS 时设置了密码：
```bash
RDS_PASSWORD=您创建时设置的密码
```

### 选项 B: 使用 AWS Secrets Manager
如果您的密码存储在 Secrets Manager 中：

1. 进入 **AWS Secrets Manager** 控制台
2. 查找名称包含 "rds"、"database" 的密码
3. 记录 Secret 名称：
```bash
RDS_SECRET_NAME=您的Secret名称
```

### 选项 C: 重置密码
如果忘记了密码，可以在 RDS 控制台重置：

1. 选择您的 RDS 实例
2. 点击 **修改**
3. 在 **新主用户密码** 中输入新密码
4. 应用更改

## 🔧 3. GitHub Secrets 配置

将以下变量添加到 GitHub 仓库的 Secrets 中：

### 基础配置：
```
AWS_REGION=ap-southeast-1
AWS_ACCESS_KEY_ID=您的Key
AWS_SECRET_ACCESS_KEY=您的Secret

RDS_HOST=您的RDS端点
RDS_PORT=5432
RDS_DATABASE=您的数据库名
RDS_USERNAME=您的用户名
```

### 密码配置（三选一）：
```
# 选项 A：直接密码
RDS_PASSWORD=您的密码

# 选项 B：Secrets Manager
RDS_SECRET_NAME=您的Secret名称

# 选项 C：完整连接字符串
DATABASE_URL=postgresql://用户名:密码@主机:5432/数据库名
```

## ⚙️ 4. IAM 认证配置（可选但推荐）

如果您想使用 IAM 认证：

### 4.1 启用 RDS IAM 认证
1. 在 RDS 控制台选择您的实例
2. 点击 **修改**
3. 找到 **数据库认证选项**
4. 勾选 **启用 IAM 数据库认证**
5. 应用更改

### 4.2 创建 IAM 数据库用户
连接到您的数据库，执行：
```sql
CREATE USER iam_user;
GRANT rds_iam TO iam_user;
GRANT ALL PRIVILEGES ON DATABASE your_database TO iam_user;
```

### 4.3 更新 GitHub Secrets
```
USE_IAM_AUTH=true
RDS_USERNAME=iam_user
```

## ✅ 5. 验证配置

部署完成后，检查以下端点：
- 后端健康检查：`http://您的EC2地址:5000/health`
- 数据库连接测试：`http://您的EC2地址:5000/ping-db`

## 🚨 6. 常见问题

### 问题：连接被拒绝
**解决方案：**
1. 检查 RDS 安全组是否允许 EC2 访问
2. 确保 RDS 不是私有子网（除非 EC2 也在同一私有子网）

### 问题：认证失败
**解决方案：**
1. 验证用户名和密码是否正确
2. 如果使用 IAM 认证，确保已创建 IAM 用户并授权

### 问题：权限错误
**解决方案：**
1. 确保数据库用户有足够的权限
2. 检查数据库名称是否正确

## 📞 需要帮助？

如果遇到问题，请提供：
1. 错误日志（从 `docker logs cp-backend` 获取）
2. 您的 RDS 配置信息（隐藏敏感信息）
3. 具体的错误信息 