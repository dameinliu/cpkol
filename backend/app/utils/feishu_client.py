import os
import requests
from dotenv import load_dotenv

load_dotenv()

FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
FEISHU_REDIRECT_URI = os.getenv("FEISHU_REDIRECT_URI")

class FeishuClient:
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or FEISHU_APP_ID
        self.app_secret = app_secret or FEISHU_APP_SECRET
        self.tenant_access_token = None

    def get_tenant_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        self.tenant_access_token = resp.json().get("tenant_access_token")
        return self.tenant_access_token

    def get_user_access_token(self, code):
        """
        通过用户授权code换取user_access_token
        文档：https://open.feishu.cn/document/server-docs/authen-v1/access_token/create
        """
        url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
        headers = {"Content-Type": "application/json"}
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()

    # def get_bitable_records(self, app_token, table_id):
    #     if not self.tenant_access_token:
    #         self.get_tenant_access_token()
    #     url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
    #     headers = {
    #         "Authorization": f"Bearer {self.tenant_access_token}",
    #         "Content-Type": "application/json"
    #     }
    #     resp = requests.post(url, headers=headers, json={})
    #     resp.raise_for_status()
    #     return resp.json() 