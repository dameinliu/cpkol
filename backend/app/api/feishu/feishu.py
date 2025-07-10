from flask import Blueprint, request, jsonify
from app.utils.feishu_client import FeishuClient
from app.models import db
import json

feishu_bp = Blueprint('feishu', __name__)

@feishu_bp.route('/api/feishu/download', methods=['POST'])
def download_feishu_table():
    """
    请求体参数：{
        "app_token": "飞书多维表app_token",
        "table_id": "飞书多维表table_id"
    }
    """
    data = request.get_json()
    app_token = data.get('app_token')
    table_id = data.get('table_id')
    if not app_token or not table_id:
        return jsonify({"error": "缺少app_token或table_id"}), 400

    client = FeishuClient()
    try:
        records_json = client.get_bitable_records(app_token, table_id)
        # 这里只打印数据，后续可扩展为写入数据库
        print("飞书表格数据：", json.dumps(records_json, ensure_ascii=False, indent=2))
        return jsonify({"msg": "数据获取成功", "data": records_json}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 