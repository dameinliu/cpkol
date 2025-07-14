import os
import boto3
import json
from urllib.parse import quote_plus

print("🚀 [Config] Loading database configuration...")

def get_secret_from_secrets_manager(secret_name, region_name):
    """从 AWS Secrets Manager 获取密码"""
    print(f"  [Secrets Manager] Attempting to fetch secret: '{secret_name}' in region '{region_name}'")
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        print(f"  [Secrets Manager] ✅ Successfully fetched secret '{secret_name}'")
        return secret
    except Exception as e:
        print(f"  [Secrets Manager] ⚠️  Could not fetch secret '{secret_name}'. Error: {e}")
        return None

def get_rds_password():
    """获取 RDS 密码，支持多种来源"""
    print("  [Password] Searching for RDS password...")
    
    # 1. 直接从环境变量获取
    password = os.environ.get('RDS_PASSWORD')
    if password:
        print("  [Password] ✅ Found 'RDS_PASSWORD' in environment variables.")
        return password
    
    # 2. 从 AWS Secrets Manager 获取
    secret_name = os.environ.get('RDS_SECRET_NAME')
    if secret_name:
        region = os.environ.get('AWS_REGION', 'us-east-1')
        print(f"  [Password] Found 'RDS_SECRET_NAME' ('{secret_name}'), trying Secrets Manager...")
        
        secret = get_secret_from_secrets_manager(secret_name, region)
        if secret:
            if 'password' in secret:
                print("  [Password] ✅ Found 'password' key in the secret.")
                return secret['password']
            elif 'RDS_PASSWORD' in secret:
                print("  [Password] ✅ Found 'RDS_PASSWORD' key in the secret.")
                return secret['RDS_PASSWORD']
            else:
                print("  [Password] ⚠️  Secret found, but it does not contain a 'password' or 'RDS_PASSWORD' key.")
    
    print("  [Password] ❌ No RDS password found from any source.")
    return None

def get_database_uri():
    """根据配置动态生成数据库连接字符串，优先使用 IAM 认证"""
    print("  [DB URI] Starting database URI generation...")
    
    # 优先尝试 IAM 认证（生产环境推荐）
    use_iam_auth = os.environ.get('USE_IAM_AUTH', 'false').lower() == 'true'
    print(f"  [DB URI] USE_IAM_AUTH is set to: {use_iam_auth}")
    if use_iam_auth:
        print("  [DB URI] -> Attempting IAM Authentication.")
        host = os.environ.get('RDS_HOST')
        port = os.environ.get('RDS_PORT', '5432')
        database = os.environ.get('RDS_DATABASE')
        username = os.environ.get('RDS_USERNAME')
        region = os.environ.get('AWS_REGION', 'us-east-1')
        
        if all([host, database, username, region]):
            print("  [DB URI] All required RDS variables for IAM are present.")
            try:
                print("  [DB URI] Generating IAM auth token...")
                rds_client = boto3.client('rds', region_name=region)
                token = rds_client.generate_db_auth_token(DBHostname=host, Port=int(port), DBUsername=username)
                encoded_token = quote_plus(token)
                iam_uri = f"postgresql://{username}:{encoded_token}@{host}:{port}/{database}?sslmode=require"
                print("  [DB URI] ✅ Successfully generated IAM database URI.")
                return iam_uri
            except Exception as e:
                print(f"  [DB URI] ⚠️  IAM auth token generation failed: {e}")
                print("  [DB URI] Falling back to password authentication...")
                password = get_rds_password()
                if password:
                    fallback_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode=require"
                    print("  [DB URI] ✅ Generated URI using fallback password.")
                    return fallback_uri
                else:
                    print("  [DB URI] ❌ Fallback password not available.")
        else:
            print(f"  [DB URI] ❌ Incomplete RDS configuration for IAM auth. Missing some of: RDS_HOST, RDS_DATABASE, RDS_USERNAME, AWS_REGION")

    # 第二优先级：使用预配置的 DATABASE_URL
    print("  [DB URI] -> Checking for 'DATABASE_URL'...")
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')
    if database_url:
        print("  [DB URI] ✅ Found and using 'DATABASE_URL'.")
        return database_url
    
    # 第三优先级：本地开发数据库
    print("  [DB URI] -> Checking for 'DATABASE_URL_LOCAL'...")
    local_db = os.environ.get('DATABASE_URL_LOCAL')
    if local_db:
        print("  [DB URI] ✅ Found and using 'DATABASE_URL_LOCAL'.")
        return local_db
    
    # 最后回退
    print("  [DB URI] ⚠️  All methods failed. Using default hardcoded local database URI as a last resort.")
    return 'postgresql://postgres:123456@localhost:5432/influencers'

class Config:
    print("[Config] Setting Flask config properties...")
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    print(f"[Config] Final SQLALCHEMY_DATABASE_URI is set: {'URI is present' if SQLALCHEMY_DATABASE_URI else 'URI is missing or None'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG') == '1'
    TESTING = os.environ.get('FLASK_TESTING') == '1'

class DevelopmentConfig(Config):
    DEBUG = True