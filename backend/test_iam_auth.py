#!/usr/bin/env python3
"""
测试脚本：验证 RDS IAM 认证配置
可以在部署前本地测试或在容器中调试使用
"""

import os
import boto3
from urllib.parse import quote_plus

def test_iam_auth():
    """测试 IAM 认证配置"""
    print("🔍 正在测试 RDS IAM 认证配置...")
    
    # 检查必要的环境变量
    required_vars = ['RDS_HOST', 'RDS_DATABASE', 'RDS_USERNAME', 'AWS_REGION']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        return False
    
    host = os.environ.get('RDS_HOST')
    port = os.environ.get('RDS_PORT', '5432')
    database = os.environ.get('RDS_DATABASE')
    username = os.environ.get('RDS_USERNAME')
    region = os.environ.get('AWS_REGION')
    
    print(f"📝 配置信息:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Database: {database}")
    print(f"   Username: {username}")
    print(f"   Region: {region}")
    
    try:
        # 测试 AWS 凭证
        print("\n🔑 测试 AWS 凭证...")
        rds_client = boto3.client('rds', region_name=region)
        
        # 生成 IAM 认证令牌
        print("🔄 生成 IAM 认证令牌...")
        token = rds_client.generate_db_auth_token(
            DBHostname=host,
            Port=int(port),
            DBUsername=username
        )
        
        print("✅ IAM 认证令牌生成成功!")
        print(f"   令牌长度: {len(token)} 字符")
        print(f"   令牌前缀: {token[:50]}...")
        
        # URL 编码
        encoded_token = quote_plus(token)
        connection_string = f"postgresql://{username}:{encoded_token}@{host}:{port}/{database}?sslmode=require"
        
        print("✅ 数据库连接字符串构建成功!")
        print(f"   连接字符串长度: {len(connection_string)} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ IAM 认证测试失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        return False

def test_aws_credentials():
    """测试 AWS 凭证配置"""
    print("\n🔍 测试 AWS 凭证配置...")
    
    # 检查环境变量
    aws_vars = {
        'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
        'AWS_REGION': os.environ.get('AWS_REGION'),
        'AWS_DEFAULT_REGION': os.environ.get('AWS_DEFAULT_REGION')
    }
    
    for var, value in aws_vars.items():
        if value:
            print(f"✅ {var}: {'*' * min(len(value), 20)}...")
        else:
            print(f"❌ {var}: 未设置")
    
    try:
        # 测试 boto3 会话
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials:
            print("✅ boto3 会话创建成功")
            print(f"   Access Key: {credentials.access_key[:10]}...")
            print(f"   Secret Key: {'*' * 20}")
        else:
            print("❌ 无法获取 AWS 凭证")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ AWS 凭证测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始 RDS IAM 认证测试\n")
    
    # 加载环境变量（如果有 .env 文件）
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ 已加载 .env 文件")
    except ImportError:
        print("⚠️  python-dotenv 未安装，跳过 .env 文件加载")
    
    # 运行测试
    aws_test = test_aws_credentials()
    iam_test = test_iam_auth()
    
    print(f"\n📊 测试结果:")
    print(f"   AWS 凭证: {'✅ 通过' if aws_test else '❌ 失败'}")
    print(f"   IAM 认证: {'✅ 通过' if iam_test else '❌ 失败'}")
    
    if aws_test and iam_test:
        print("\n🎉 所有测试通过！IAM 认证配置正确。")
        exit(0)
    else:
        print("\n⚠️  测试失败，请检查配置。")
        exit(1) 