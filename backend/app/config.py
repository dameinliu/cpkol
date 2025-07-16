import logging
import os
import json
from urllib.parse import quote_plus

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] [%(name)s] %(message)s')
logger = logging.getLogger(__name__)

def get_rds_password():
    """从 AWS Secrets Manager 获取 RDS 密码。"""
    secret_name = os.environ.get("DB_SECRET_NAME")
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    if not secret_name:
        logger.warning("DB_SECRET_NAME not set. Cannot fetch password from Secrets Manager.")
        return None

    logger.info(f"Attempting to fetch secret '{secret_name}' from region '{region_name}'...")

    # session = boto3.session.Session()
    client = boto3.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except NoCredentialsError:
        logger.error("AWS credentials not found. Cannot connect to Secrets Manager.")
        return None
    except ClientError as e:
        logger.error(f"Error fetching secret from Secrets Manager: {e}")
        return None
        
    secret = get_secret_value_response.get('SecretString')
    if secret:
        try:
            secret_dict = json.loads(secret)
            password = secret_dict.get('password')
            if password:
                logger.info("✅ Successfully fetched and parsed password from secret.")
                return password
            else:
                logger.error("'password' key not found in the secret string.")
        except json.JSONDecodeError:
            logger.error("Failed to parse secret string as JSON.")
    else:
        logger.error("SecretString is empty in the response from Secrets Manager.")
    
    return None

def _get_iam_uri():
    """生成基于 IAM 认证的数据库 URI。"""
    logger.info("-> Attempting IAM Authentication.")
    host = os.environ.get('RDS_HOST')
    port = os.environ.get('RDS_PORT', '5432')
    database = os.environ.get('RDS_DATABASE')
    username = os.environ.get('RDS_USERNAME')
    region = os.environ.get('AWS_REGION', 'us-east-1')

    if not all([host, database, username, region]):
        logger.error("❌ Incomplete RDS configuration for IAM auth. Missing one of: RDS_HOST, RDS_DATABASE, RDS_USERNAME, AWS_REGION")
        return None

    logger.info("All required RDS variables for IAM are present.")
    try:
        logger.info("Generating IAM auth token...")
        rds_client = boto3.client('rds', region_name=region)
        token = rds_client.generate_db_auth_token(DBHostname=host, Port=int(port), DBUsername=username)
        encoded_token = quote_plus(token)
        iam_uri = f"postgresql://{username}:{encoded_token}@{host}:{port}/{database}?sslmode=require"
        logger.info("✅ Successfully generated IAM database URI.")
        return iam_uri
    except NoCredentialsError:
        logger.error("AWS credentials not found. Cannot generate IAM auth token.")
        return None
    except Exception as e:
        logger.error(f"⚠️ IAM auth token generation failed: {e}")
        return None

def _get_password_uri():
    """生成基于密码认证的数据库 URI。"""
    logger.info("-> Attempting Password Authentication using Secrets Manager.")
    host = os.environ.get('RDS_HOST')
    port = os.environ.get('RDS_PORT', '5432')
    database = os.environ.get('RDS_DATABASE')
    username = os.environ.get('RDS_USERNAME')
    
    if not all([host, database, username]):
        logger.error("❌ Incomplete RDS configuration for password auth. Missing one of: RDS_HOST, RDS_DATABASE, RDS_USERNAME")
        return None

    password = get_rds_password()
    if not password:
        logger.error("❌ Failed to retrieve password from Secrets Manager.")
        return None
    
    encoded_password = quote_plus(password)
    password_uri = f"postgresql://{username}:{encoded_password}@{host}:{port}/{database}"
    logger.info("✅ Successfully built database URI using password from Secrets Manager.")
    return password_uri

def get_database_uri():
    """
    根据环境变量动态生成数据库连接字符串。
    优先级顺序:
    1. DATABASE_URL 环境变量
    2. IAM 认证 (如果 USE_IAM_AUTH=true)
    3. 密码认证 (从 Secrets Manager 获取)
    """
    logger.info("Starting database URI generation...")

    # 1. 最高优先级：直接提供 URI
    if 'DATABASE_URL' in os.environ:
        uri = os.environ.get('DATABASE_URL')
        logger.info(f"✅ Using provided DATABASE_URL: {uri}")
        return uri

    # 2. 决定认证策略
    use_iam_auth = os.environ.get('USE_IAM_AUTH', 'false').lower() == 'true'
    logger.info(f"USE_IAM_AUTH is set to: {use_iam_auth}")

    if use_iam_auth:
        return _get_iam_uri()
    else:
        return _get_password_uri()


class Config:
    """基本配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key')
    
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_database_uri()

    # 日志配置
    LOG_GROUP_NAME = os.environ.get('LOG_GROUP_NAME')
    LOG_STREAM_NAME = os.environ.get('LOG_STREAM_NAME')

# 开发环境配置
class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    # 只用DATABASE_URL，不使用get_database_uri()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///dev.db"
    if not SQLALCHEMY_DATABASE_URI:
        logger.info(f"DevelopmentConfig is defaulting to local sqlite DB: {SQLALCHEMY_DATABASE_URI}")


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 从基类继承 URI
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
    # 在生产环境中，URI 必须被成功配置
    if not SQLALCHEMY_DATABASE_URI:
        logger.critical("❌❌❌ DATABASE URI NOT CONFIGURED IN PRODUCTION! SHUTTING DOWN. ❌❌❌")
        raise ValueError("SQLALCHEMY_DATABASE_URI must be set in production environment.")


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///:memory:')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}