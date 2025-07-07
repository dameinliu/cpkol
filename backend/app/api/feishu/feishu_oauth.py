from flask import Blueprint, redirect, request, jsonify
import os
from app.utils.feishu_client import FeishuClient

feishu_oauth_bp = Blueprint('feishu_oauth', __name__)

@feishu_oauth_bp.route('/api/feishu/oauth/login')
def feishu_oauth_login():
    app_id = os.getenv("FEISHU_APP_ID")
    redirect_uri = os.getenv("FEISHU_REDIRECT_URI")
    state = "random_state"  # 可自定义防CSRF
    url = (
        f"https://open.feishu.cn/open-apis/authen/v1/index"
        f"?app_id={app_id}&redirect_uri={redirect_uri}&state={state}"
    )
    print(os.getenv("FEISHU_APP_ID"))
    print(os.getenv("FEISHU_REDIRECT_URI"))
    return redirect(url)

@feishu_oauth_bp.route('/api/feishu/oauth/callback')
def feishu_oauth_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if not code:
        return "缺少code", 400
    client = FeishuClient()
    token_info = client.get_user_access_token(code)
    # 这里可以处理用户信息，如自动注册/登录/绑定
    return jsonify(token_info) 