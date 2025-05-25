from flask import Blueprint, request, jsonify
import os
import json
from dotenv import load_dotenv
from tikapi import TikAPI, ValidationException, ResponseException
from app.models import db, Influencer

# 加载.env配置
load_dotenv()
influencer_bp = Blueprint('influencer', __name__)
api = TikAPI(os.getenv("TIKAPI_API_KEY"))

@influencer_bp.route('/api/influencers/search', methods=['GET'])
def search_influencers():
    handle = request.args.get('handle', '').strip()
    print(f"收到前端请求 handle: {handle}")
    if not handle:
        return jsonify({"error": "handle参数不能为空"}), 400

    influencer = Influencer.query.filter_by(handle=handle).first()
    if influencer:
        print(f"数据库已存在 influencer: {influencer.to_dict().get('follower_count')}")
        return jsonify(influencer.to_dict())

    try:
        # 获取用户基本信息
        response = api.public.check(username=handle)
        data = response.json()
        # print("TikAPI check 返回:", data)
        user_info = data.get('userInfo', {})
        sec_uid = user_info.get("user", {}).get("secUid", None)
        # print("user_info:", user_info)
        # print("sec_uid:", sec_uid)

        if not user_info or not sec_uid:
            # print("未找到 userInfo 或 secUid，返回 404")
            return jsonify({"error": "未找到该用户"}), 404

        # 获取视频列表及统计
        video_data = api.public.posts(sec_uid).json()
        # print("TikAPI posts 返回:", video_data)
        videos = video_data.get("itemList", [])
        # print(f"获取到 {len(videos)} 个视频")

        total_play_count = sum(video.get("stats", {}).get("playCount", 0) for video in videos)
        total_comment_count = sum(video.get("stats", {}).get("commentCount", 0) for video in videos)
        total_digg_count = sum(video.get("stats", {}).get("diggCount", 0) for video in videos)
        video_count = len(videos)
        # print(f"统计: play={total_play_count}, comment={total_comment_count}, digg={total_digg_count}, count={video_count}")

        # print("TikAPI返回：", video_data)

        # 存储到数据库
        influencer_obj = Influencer(
            handle=handle,
            sec_uid=sec_uid,
            follower_count=user_info.get("stats", {}).get("followerCount", 0),
            video_count=video_count,
            total_play_count=total_play_count,
            total_comment_count=total_comment_count,
            total_digg_count=total_digg_count,
            videos=json.dumps(videos)
        )
        db.session.add(influencer_obj)
        db.session.commit()

        print("数据库存储成功，返回数据：", influencer_obj.to_dict().get('follower_count'))
        return jsonify(influencer_obj.to_dict())

    except ValidationException as e:
        return jsonify({"error": f"参数校验失败: {str(e)}"}), 400
    except ResponseException as e:
        return jsonify({"error": f"TikAPI响应异常: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"API响应解析失败: {str(e)}"}), 500
