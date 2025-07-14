#!/usr/bin/env python3
"""
帮助找到 RDS 自动生成的 Secret 名称
"""

import boto3
import json

def main():
    print("🚀 RDS Secret 查找工具\n")
    
    print("🔍 RDS 自动生成的 Secret 常见命名模式：")
    print("1. rds-db-credentials/{您的RDS实例ID}")
    print("2. rds!db-{随机字符串}")
    print("3. prod/rds/credentials")
    print("4. dev/rds/credentials")
    print("5. {应用名}/rds/password")
    
    print("\n" + "="*50)
    print("📋 手动查找步骤（推荐）：")
    print("1. 登录 AWS 控制台")
    print("2. 进入 AWS Secrets Manager (ap-southeast-1 区域)")
    print("3. 在搜索框中输入 'rds'")
    print("4. 查找包含数据库凭证的 Secret")
    print("5. 点击 Secret 名称查看详情")
    print("6. 记录 Secret 的完整名称")
    
    print("\n" + "="*50)
    print("🔧 GitHub Secrets 配置：")
    print("找到 Secret 后，设置以下 GitHub Secrets：")
    print()
    print("RDS_SECRET_NAME=您找到的Secret完整名称")
    print("USE_IAM_AUTH=true")
    print("AWS_REGION=ap-southeast-1")
    
    print("\n" + "="*50)
    print("💡 提示：")
    print("- Secret 名称通常包含您的 RDS 实例 ID")
    print("- 如果找到多个相关 Secret，选择最新创建的")
    print("- Secret 内容应包含 username, password, host 等字段")

if __name__ == "__main__":
    main() 