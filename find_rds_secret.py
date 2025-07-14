#!/usr/bin/env python3
"""
帮助找到 RDS 自动生成的 Secret 名称
"""

import boto3
import json

def guess_rds_secret_names():
    """根据常见命名模式猜测 RDS Secret 名称"""
    
    print("🔍 RDS 自动生成的 Secret 常见命名模式：")
    print()
    
    # 常见的命名模式
    patterns = [
        "rds-db-credentials/auto-generated-secret",
        "rds-db-credentials/{instance-id}",
        "rds!db-{random-string}",
        "prod/rds/credentials",
        "dev/rds/credentials",
        "staging/rds/credentials",
        "{app-name}/rds/password"
    ]
    
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. {pattern}")
    
    print()
    print("💡 最常见的是: rds-db-credentials/{您的RDS实例ID}")

def try_common_secret_names(rds_instances):
    """尝试常见的 Secret 名称"""
    print("\n🔑 尝试获取 RDS Secret...")
    
    if not rds_instances:
        print("❌ 请先提供 RDS 实例 ID")
        return
    
    secrets_client = boto3.client('secretsmanager', region_name='ap-southeast-1')
    
    # 生成可能的 Secret 名称
    possible_names = []
    for instance_id in rds_instances:
        possible_names.extend([
            f"rds-db-credentials/{instance_id}",
            f"rds!db-{instance_id}",
            f"prod/rds/{instance_id}",
            f"dev/rds/{instance_id}",
            f"cpkol/rds/{instance_id}",
            f"{instance_id}/credentials"
        ])
    
    # 添加通用名称
    possible_names.extend([
        "rds-db-credentials/auto-generated",
        "prod/rds/credentials",
        "dev/rds/credentials",
        "staging/rds/credentials",
        "cpkol/rds/password",
        "database/credentials"
    ])
    
    successful_secrets = []
    
    for secret_name in possible_names:
        try:
            print(f"尝试: {secret_name}")
            response = secrets_client.get_secret_value(SecretId=secret_name)
            secret_data = json.loads(response['SecretString'])
            
            print(f"✅ 找到 Secret: {secret_name}")
            print(f"   包含的键: {list(secret_data.keys())}")
            
            # 检查是否包含密码
            if 'password' in secret_data:
                print(f"   ✅ 包含密码字段")
            
            successful_secrets.append({
                'name': secret_name,
                'data': secret_data
            })
            
        except secrets_client.exceptions.ResourceNotFoundException:
            print(f"   ❌ 不存在")
        except Exception as e:
            print(f"   ⚠️  无法访问: {e}")
    
    return successful_secrets

def main():
    print("🚀 RDS Secret 查找工具\n")
    
    # 显示命名模式
    guess_rds_secret_names()
    
    print("\n" + "="*50)
    print("📋 手动查找步骤：")
    print("1. 登录 AWS 控制台")
    print("2. 进入 AWS Secrets Manager")
    print("3. 在搜索框中输入 'rds' 或您的实例ID")
    print("4. 查找包含数据库凭证的 Secret")
    print("5. 记录 Secret 的完整名称")
    
    print("\n" + "="*50)
    print("🔧 GitHub Secrets 配置：")
    print("找到 Secret 后，在 GitHub 中设置：")
    print("RDS_SECRET_NAME=您找到的Secret完整名称")
    print("USE_IAM_AUTH=true")
    
    print("\n" + "="*50)
    print("🎯 如果您知道 RDS 实例 ID，我可以尝试猜测 Secret 名称")
    
    # 获取用户输入的实例 ID
    instance_ids = []
    print("\n请输入您的 RDS 实例 ID（多个用逗号分隔，直接回车跳过）:")
    user_input = input().strip()
    
    if user_input:
        instance_ids = [id.strip() for id in user_input.split(',') if id.strip()]
        secrets = try_common_secret_names(instance_ids)
        
        if secrets:
            print(f"\n🎉 找到 {len(secrets)} 个可用的 Secret:")
            for secret in secrets:
                print(f"✅ Secret 名称: {secret['name']}")
                print(f"   配置: RDS_SECRET_NAME={secret['name']}")
        else:
            print("\n❌ 未找到匹配的 Secret")
            print("请手动在 AWS 控制台中查找")

if __name__ == "__main__":
    main() 