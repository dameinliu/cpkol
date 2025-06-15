from flask import Blueprint, request, jsonify
import json
from tikapi import ValidationException, ResponseException
from app.models import db, Influencer
from app.utils.tikapi_client import api  # 引入独立的 TikAPI 客户端

influencer_bp = Blueprint('influencer', __name__)

@influencer_bp.route('/api/influencers/search', methods=['GET'])
def search_influencers():
    handles = request.args.get('handles', '').strip()
    if not handles:
        return jsonify({"error": "handles参数不能为空"}), 400

    handle_list = [h.strip() for h in handles.split(',') if h.strip()]
    if not handle_list:
        return jsonify({"error": "请至少输入一个用户名"}), 400

    results = []
    errors = []

    for handle in handle_list:
        influencer = Influencer.query.filter_by(handle=handle).first()
        if influencer:
            results.append(influencer.to_dict())
            continue

        try:
            response = api.public.check(username=handle)
            data = response.json()
            user_info = data.get('userInfo', {})
            sec_uid = user_info.get("user", {}).get("secUid", None)

            if not user_info or not sec_uid:
                errors.append({"handle": handle, "error": "未找到该用户"})
                continue

            video_data = api.public.posts(sec_uid).json()
            videos = video_data.get("itemList", [])

            total_play_count = sum(video.get("stats", {}).get("playCount", 0) for video in videos)
            total_comment_count = sum(video.get("stats", {}).get("commentCount", 0) for video in videos)
            total_digg_count = sum(video.get("stats", {}).get("diggCount", 0) for video in videos)
            video_count = len(videos)

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
            results.append(influencer_obj.to_dict())
        except ValidationException as e:
            errors.append({"handle": handle, "error": f"参数校验失败: {str(e)}"})
        except ResponseException as e:
            errors.append({"handle": handle, "error": f"TikAPI响应异常: {str(e)}"})
        except Exception as e:
            errors.append({"handle": handle, "error": f"API响应解析失败: {str(e)}"})

    return jsonify({"results": results, "errors": errors})

@influencer_bp.route('/api/influencers', methods=['GET'])
def list_influencers():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        pagination = Influencer.query.order_by(Influencer.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        items = [i.to_dict() for i in pagination.items]
        return jsonify({
            'items': items,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
