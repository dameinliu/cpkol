from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

# 加载.env配置
load_dotenv()

influencer_bp = Blueprint('influencer', __name__)

@influencer_bp.route('/api/influencers/search', methods=['GET'])
def search_influencers():
    handle = request.args.get('handle', '')
    # 其他筛选参数可根据需求添加

    url = "https://tiktok-api23.p.rapidapi.com/api/user/info"
    querystring = {"uniqueId": handle}
    headers = {
        "X-RapidAPI-Key": os.getenv("TIKTOK_API_KEY"),
        "X-RapidAPI-Host": os.getenv("TIKTOK_API_HOST")
    }
    response = requests.get(url, headers=headers, params=querystring)
    try:
        data = response.json()
    except Exception:
        return jsonify({"error": "API响应解析失败"}), 500
    # 直接返回完整的userInfo数据
    user_info = data.get("userInfo", {})
    sec_uid = user_info.get("user", {}).get("secUid", None)

    print(sec_uid)
    # 新增：用secUid获取视频统计
    video_stats = {}
    if sec_uid:
        videos_url = "https://tiktok-api23.p.rapidapi.com/api/user/posts"
        videos_query = {"secUid": sec_uid, "count": 30}
        videos_resp = requests.get(videos_url, headers=headers, params=videos_query)
        
        try:
            videos_data = videos_resp.json()
            total_play_count = 0
            total_digg_count = 0
            total_comment_count = 0
            videos = videos_data.get("data", {}).get("itemList", [])

            print(videos_data)
            
            for video in videos:
                total_play_count += video.get("stats", {}).get("playCount", 0)
                total_comment_count += video.get("stats", {}).get("commentCount", 0)
                total_digg_count += video.get("stats", {}).get("diggCount", 0)
            video_stats = {
                "total_play_count": total_play_count,
                "total_comment_count": total_comment_count,
                "total_digg_count": total_digg_count,
                "video_count": len(videos),
                "videos": videos
            }
        except Exception:
            video_stats = {"error": "Videos API响应解析失败"}

    print(video_stats)

    return jsonify({
        "userInfo": user_info,
        "secUid": sec_uid,
        "videoStats": video_stats
    })
