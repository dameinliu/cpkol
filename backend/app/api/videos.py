from flask import Blueprint, request, jsonify
from tikapi import ValidationException, ResponseException
from app.utils.tikapi_client import api  # 引入独立的 TikAPI 客户端
import os
from app.models import Video, db

videos_bp = Blueprint('videos', __name__)

@videos_bp.route('/api/videos', methods=['GET'])
def get_videos_by_country():
    try:
        # 从请求参数中获取国家代码，默认为美国 ('us')
        country_code = request.args.get('country', 'TH').strip()
        print(f"收到请求，国家代码: {country_code}")

        # 使用 TikAPI 的 explore 方法获取指定国家的热门视频
        response = api.public.explore(
            session_id=0,  # TikAPI 的 session_id 参数，通常为 '0'
            country=country_code
        )
        print(f"TikAPI 响应状态码: {response.status_code}")
        print(f"TikAPI 响应内容: {response.text}")

        # 检查响应状态码
        if response.status_code != 200:
            return jsonify({"error": f"TikAPI请求失败，状态码: {response.status_code}"}), response.status_code

        # 解析响应数据
        data = response.json()
        videos = data.get('itemList', [])
        for video in videos:
            video_id = video.get('id')
            if not Video.query.filter_by(id=video_id).first():
                db.session.add(Video(
                    id=video_id,
                    desc=video.get('desc'),
                    author_id=video.get('authorId'),
                    country=country_code,
                    play_count=video.get('stats', {}).get('playCount', 0),
                    digg_count=video.get('stats', {}).get('diggCount', 0),
                    comment_count=video.get('stats', {}).get('commentCount', 0),
                    share_count=video.get('stats', {}).get('shareCount', 0),
                    create_time=video.get('createTime')
                ))
        db.session.commit()
        videos = Video.query.order_by(Video.create_time.desc()).limit(30).all()
        return jsonify([video.to_dict() for video in videos])
    except ValidationException as e:
        print(f"参数校验失败: {str(e)}")
        return jsonify({"error": f"参数校验失败: {str(e)}"}), 400
    except ResponseException as e:
        print(f"TikAPI响应异常: {str(e)}, 状态码: {e.response.status_code}")
        return jsonify({"error": f"TikAPI响应异常: {str(e)}"}), 502
    except Exception as e:
        print(f"API响应解析失败: {str(e)}")
        return jsonify({"error": f"API响应解析失败: {str(e)}"}), 500