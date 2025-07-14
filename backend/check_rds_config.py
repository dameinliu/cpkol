#!/usr/bin/env python3
"""
RDS 配置检查工具
帮助查找和配置 RDS 数据库密码
"""

import os
import boto3
import json
from datetime import datetime

def check_rds_instances():
    """检查用户的 RDS 实例"""
    print("🔍 正在检查您的 RDS 实例...")
    
    try:
        region = os.environ.get('AWS_REGION', 'us-east-1')
        rds_client = boto3.client('rds', region_name=region)
        
        response = rds_client.describe_db_instances()
        instances = response['DBInstances']
        
        if not instances:
            print("❌ 未找到 RDS 实例")
            return []
        
        print(f"✅ 找到 {len(instances)} 个 RDS 实例:")
        
        for i, instance in enumerate(instances, 1):
            print(f"\n📊 实例 {i}:")
            print(f"   ID: {instance['DBInstanceIdentifier']}")
            print(f"   引擎: {instance['Engine']}")
            print(f"   状态: {instance['DBInstanceStatus']}")
            print(f"   主用户名: {instance['MasterUsername']}")
            print(f"   端点: {instance.get('Endpoint', {}).get('Address', 'N/A')}")
            print(f"   端口: {instance.get('Endpoint', {}).get('Port', 'N/A')}")
            print(f"   数据库名: {instance.get('DBName', 'N/A')}")
            
            # 检查是否启用了 IAM 认证
            iam_enabled = instance.get('IAMDatabaseAuthenticationEnabled', False)
            print(f"   IAM 认证: {'✅ 已启用' if iam_enabled else '❌ 未启用'}")
            
        return instances
        
    except Exception as e:
        print(f"❌ 检查 RDS 实例失败: {e}")
        return []

def check_secrets_manager():
    """检查 Secrets Manager 中的 RDS 相关密码"""
    print("\n🔍 正在检查 Secrets Manager 中的 RDS 密码...")
    
    try:
        region = os.environ.get('AWS_REGION', 'us-east-1')
        secrets_client = boto3.client('secretsmanager', region_name=region)
        
        response = secrets_client.list_secrets()
        secrets = response['SecretList']
        
        rds_secrets = []
        for secret in secrets:
            name = secret['Name']
            if any(keyword in name.lower() for keyword in ['rds', 'database', 'db', 'postgres', 'mysql']):
                rds_secrets.append(secret)
        
        if not rds_secrets:
            print("❌ 未找到 RDS 相关的 Secrets")
            return []
        
        print(f"✅ 找到 {len(rds_secrets)} 个 RDS 相关的 Secrets:")
        
        for i, secret in enumerate(rds_secrets, 1):
            print(f"\n🔑 Secret {i}:")
            print(f"   名称: {secret['Name']}")
            print(f"   描述: {secret.get('Description', 'N/A')}")
            
            # 尝试获取 Secret 内容
            try:
                secret_response = secrets_client.get_secret_value(SecretId=secret['Name'])
                secret_data = json.loads(secret_response['SecretString'])
                
                print(f"   包含的键:")
                for key in secret_data.keys():
                    if 'password' in key.lower():
                        print(f"     - {key} ✅")
                    else:
                        print(f"     - {key}")
                        
            except Exception as e:
                print(f"   ⚠️  无法读取内容: {e}")
        
        return rds_secrets
        
    except Exception as e:
        print(f"❌ 检查 Secrets Manager 失败: {e}")
        return []

def generate_config_suggestions(instances, secrets):
    """生成配置建议"""
    print("\n💡 配置建议:")
    
    if not instances:
        print("❌ 请先创建 RDS 实例")
        return
    
    # 选择第一个实例作为示例
    instance = instances[0]
    instance_id = instance['DBInstanceIdentifier']
    endpoint = instance.get('Endpoint', {}).get('Address', '')
    port = instance.get('Endpoint', {}).get('Port', 5432)
    db_name = instance.get('DBName', 'postgres')
    master_username = instance['MasterUsername']
    iam_enabled = instance.get('IAMDatabaseAuthenticationEnabled', False)
    
    print(f"\n🎯 基于实例 '{instance_id}' 的配置:")
    
    # GitHub Secrets 配置
    print(f"\n📝 GitHub Secrets 配置:")
    print(f"   RDS_HOST={endpoint}")
    print(f"   RDS_PORT={port}")
    print(f"   RDS_DATABASE={db_name}")
    print(f"   RDS_USERNAME={master_username}")
    
    if iam_enabled:
        print(f"   USE_IAM_AUTH=true")
        print(f"   # IAM 认证已启用 ✅")
    else:
        print(f"   USE_IAM_AUTH=false")
        print(f"   # ⚠️  建议启用 IAM 认证以提高安全性")
    
    # 密码配置选项
    print(f"\n🔐 密码配置选项:")
    
    if secrets:
        print(f"   选项1: 使用 Secrets Manager")
        print(f"   RDS_SECRET_NAME={secrets[0]['Name']}")
        print(f"   # 推荐：安全性最高 ✅")
    
    print(f"\n   选项2: 使用环境变量")
    print(f"   RDS_PASSWORD=您的数据库密码")
    print(f"   # 注意：密码会在环境变量中明文存储")
    
    print(f"\n   选项3: 使用 RDS 自动密码")
    print(f"   RDS_INSTANCE_ID={instance_id}")
    print(f"   # 如果使用了 RDS 自动生成的密码")
    
    # 完整连接字符串
    print(f"\n🔗 完整数据库连接字符串示例:")
    print(f"   DATABASE_URL=postgresql://{master_username}:密码@{endpoint}:{port}/{db_name}")

def main():
    """主函数"""
    print("🚀 RDS 配置检查工具\n")
    
    # 检查 AWS 凭证
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if not credentials:
            print("❌ 未找到 AWS 凭证，请配置 AWS CLI 或设置环境变量")
            return
        print("✅ AWS 凭证验证成功")
    except Exception as e:
        print(f"❌ AWS 凭证验证失败: {e}")
        return
    
    # 检查 RDS 实例
    instances = check_rds_instances()
    
    # 检查 Secrets Manager
    secrets = check_secrets_manager()
    
    # 生成配置建议
    generate_config_suggestions(instances, secrets)
    
    print(f"\n📋 接下来的步骤:")
    print(f"1. 在 GitHub 仓库的 Settings → Secrets and variables → Actions 中设置上述变量")
    print(f"2. 如果使用 IAM 认证，确保 EC2 实例有访问 RDS 的 IAM 角色")
    print(f"3. 如果使用 Secrets Manager，确保有访问 Secrets 的权限")
    print(f"4. 重新部署应用")

if __name__ == "__main__":
    # 加载环境变量
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    main() 