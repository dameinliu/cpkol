from flask import request, jsonify
import json
from datetime import datetime
from tikapi import ValidationException, ResponseException
from . import kol_bp
from app.models import db, Influencer
from app.utils.tikapi_client import api  # 引入独立的 TikAPI 客户端

@kol_bp.route('/search', methods=['GET'])
def search_influencers():
    handles = request.args.get('keywords', '').strip()
    handle_list = [h.strip() for h in handles.split(',') if h.strip()]
    # print(handle_list)
    if not handle_list:
        return jsonify({"error": "handle parameter cannot be empty"}), 400
    

    items = []
    errors = []

    for handle in handle_list:
        influencer = Influencer.query.filter_by(handle=handle).first()

        if influencer:
            items.append(influencer.to_dict())
            continue

        response = api.public.check(username=handle)
        data = response.json()
        user_info = data.get('userInfo', {})
        sec_uid = user_info.get("user", {}).get("secUid", None)

        if not user_info or not sec_uid:
            errors.append({"handle": handle, "error": "Can't find the user"})
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
            videos=json.dumps(videos),
            updated_date=datetime.now()
        )

        db.session.add(influencer_obj)
        db.session.commit()
        items.append(influencer_obj.to_dict())

    return jsonify({"items": items, "errors": errors})

@kol_bp.route('/list', methods=['GET'])
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

@kol_bp.route('/update', methods=['POST'])
def update_influencer():
    data = request.json

    influencer = Influencer.query.filter_by(handle=data['handle']).first()

    if influencer:
        influencer.content_type = ','.join(data['content_type'])
        influencer.note = data['note']
        influencer.updated_date = datetime.now()
        db.session.commit()
        return jsonify({'message': 'Influencer updated successfully'})
    else:
        return jsonify({'message': 'Influencer not found'}), 404

    