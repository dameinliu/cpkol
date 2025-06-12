import os
import pytest
from app.utils.feishu_client import FeishuClient

@pytest.mark.skipif(
    not (os.getenv('FEISHU_APP_ID') and os.getenv('FEISHU_APP_SECRET')),
    reason='需要配置FEISHU_APP_ID和FEISHU_APP_SECRET环境变量'
)

# 测试获取tenant_access_token
def test_get_tenant_access_token():
    client = FeishuClient()
    token = client.get_tenant_access_token()
    assert isinstance(token, str) and len(token) > 10