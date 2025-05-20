from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

# 加载.env配置
load_dotenv()

influencer_bp = Blueprint('influencer', __name__)

@influencer_bp.route('/api/influencers/search', methods=['GET'])
def search_influencers():
    keyword = request.args.get('keyword', '')
    min_fans = request.args.get('min_fans', 0)
    # 其他筛选参数可根据需求添加

    url = "https://tiktok-api23.p.rapidapi.com/api/user/info"
    querystring = {"uniqueId": keyword}
    headers = {
        "X-RapidAPI-Key": os.getenv("TIKTOK_API_KEY"),
        "X-RapidAPI-Host": os.getenv("TIKTOK_API_HOST")
    }
    response = requests.get(url, headers=headers, params=querystring)
    try:
        data = response.json()
    except Exception:
        return jsonify({"error": "API响应解析失败"}), 500
    # 这里可以根据min_fans等参数做进一步筛选
    return jsonify({"followerCount": data["userInfo"]["stats"]["followerCount"]})
