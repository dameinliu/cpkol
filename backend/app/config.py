import os
import boto3
import json
from urllib.parse import quote_plus

def get_secret_from_secrets_manager(secret_name, region_name):
    """从 AWS Secrets Manager 获取密码"""
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        return secret
    except Exception as e:
        print(f"⚠️  无法从 Secrets Manager 获取密码: {e}")
        return None

def get_rds_password():
    """获取 RDS 密码，支持多种来源"""
    # 1. 直接从环境变量获取
    password = os.environ.get('RDS_PASSWORD')
    if password:
        print("✅ 使用环境变量中的 RDS_PASSWORD")
        return password
    
    # 2. 从 AWS Secrets Manager 获取
    secret_name = os.environ.get('RDS_SECRET_NAME')
    if secret_name:
        region = os.environ.get('AWS_REGION', 'us-east-1')
        print(f"🔑 尝试从 Secrets Manager 获取密码: {secret_name}")
        
        secret = get_secret_from_secrets_manager(secret_name, region)
        if secret:
            # Secrets Manager 中可能有多种格式
            if 'password' in secret:
                print("✅ 从 Secrets Manager 获取密码成功")
                return secret['password']
            elif 'RDS_PASSWORD' in secret:
                print("✅ 从 Secrets Manager 获取密码成功")
                return secret['RDS_PASSWORD']
            else:
                print("⚠️  Secrets Manager 中未找到 password 字段")
    
    # 3. 检查是否有 RDS 实例的自动生成密码
    rds_instance_id = os.environ.get('RDS_INSTANCE_ID')
    if rds_instance_id:
        auto_secret_name = f"rds-db-credentials/{rds_instance_id}"
        region = os.environ.get('AWS_REGION', 'us-east-1')
        print(f"🔑 尝试获取 RDS 自动生成的密码: {auto_secret_name}")
        
        secret = get_secret_from_secrets_manager(auto_secret_name, region)
        if secret and 'password' in secret:
            print("✅ 获取 RDS 自动密码成功")
            return secret['password']
    
    print("❌ 未找到 RDS 密码")
    return None

def get_database_uri():
    """根据配置动态生成数据库连接字符串，优先使用 IAM 认证"""
    
    # 优先尝试 IAM 认证（生产环境推荐）
    if os.environ.get('USE_IAM_AUTH') == 'true':
        host = os.environ.get('RDS_HOST')
        port = os.environ.get('RDS_PORT', '5432')
        database = os.environ.get('RDS_DATABASE')
        username = os.environ.get('RDS_USERNAME')
        region = os.environ.get('AWS_REGION', 'us-east-1')
        
        if all([host, database, username]):
            try:
                print(f"尝试 IAM 认证连接到 RDS: {host}:{port}/{database}")
                
                # 生成 IAM 认证令牌
                rds_client = boto3.client('rds', region_name=region)
                token = rds_client.generate_db_auth_token(
                    DBHostname=host,
                    Port=int(port),
                    DBUsername=username
                )
                
                # URL 编码令牌中的特殊字符
                encoded_token = quote_plus(token)
                
                iam_uri = f"postgresql://{username}:{encoded_token}@{host}:{port}/{database}?sslmode=require"
                print("✅ IAM 认证令牌生成成功")
                return iam_uri
                
            except Exception as e:
                print(f"❌ IAM 认证失败: {e}")
                print("尝试回退到密码认证...")
                
                # IAM 认证失败时的回退方案：使用密码认证
                password = get_rds_password()
                if password:
                    fallback_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode=require"
                    print("✅ 使用密码认证作为回退方案")
                    return fallback_uri
                else:
                    print("⚠️  密码认证也不可用，继续尝试其他方案...")
        else:
            print(f"❌ RDS IAM 配置不完整: host={host}, database={database}, username={username}")
    
    # 第二优先级：使用预配置的 DATABASE_URL
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
    if database_url:
        print("✅ 使用预配置的 DATABASE_URL")
        return database_url
    
    # 第三优先级：本地开发数据库
    local_db = os.environ.get('DATABASE_URL_LOCAL')
    if local_db:
        print("✅ 使用本地开发数据库")
        return local_db
    
    # 最后回退：默认本地 PostgreSQL 配置
    print("⚠️  使用默认本地 PostgreSQL 配置")
    return 'postgresql://postgres:123456@localhost:5432/influencers'

class Config:
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG') == '1'
    TESTING = os.environ.get('FLASK_TESTING') == '1'

class DevelopmentConfig(Config):
    DEBUG = True