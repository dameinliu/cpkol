import os
import boto3
from urllib.parse import quote_plus

def get_database_uri():
    """根据配置动态生成数据库连接字符串"""
    # 如果使用 IAM 认证
    if os.environ.get('USE_IAM_AUTH') == 'true':
        host = os.environ.get('RDS_HOST')
        port = os.environ.get('RDS_PORT', '5432')
        database = os.environ.get('RDS_DATABASE')
        username = os.environ.get('RDS_USERNAME')
        region = os.environ.get('AWS_REGION', 'us-east-1')
        
        if not all([host, database, username]):
            raise ValueError("Missing required RDS configuration for IAM auth")
        
        # 生成 IAM 认证令牌
        rds_client = boto3.client('rds', region_name=region)
        token = rds_client.generate_db_auth_token(
            DBHostname=host,
            Port=int(port),
            DBUsername=username
        )
        
        # URL 编码令牌中的特殊字符
        encoded_token = quote_plus(token)
        
        return f"postgresql://{username}:{encoded_token}@{host}:{port}/{database}?sslmode=require"
    
    # 传统方式（从环境变量或 Secrets Manager）
    return os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI')

class Config:
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG') == '1'
    TESTING = os.environ.get('FLASK_TESTING') == '1'

class DevelopmentConfig(Config):
    DEBUG = True