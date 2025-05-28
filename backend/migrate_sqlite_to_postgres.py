import os
import json
from flask import Flask
from app.models import db, Influencer

# 1. 连接 SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(BASE_DIR, 'instance', 'influencers.db')
sqlite_app = Flask(__name__)
sqlite_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{SQLITE_PATH}'
sqlite_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(sqlite_app)

with sqlite_app.app_context():
    influencers = Influencer.query.all()
    data = []
    for i in influencers:
        data.append({
            'handle': i.handle,
            'sec_uid': i.sec_uid,
            'follower_count': i.follower_count,
            'video_count': i.video_count,
            'total_play_count': i.total_play_count,
            'total_comment_count': i.total_comment_count,
            'total_digg_count': i.total_digg_count,
            'videos': i.videos  # 保持为字符串
        })

# 2. 连接 PostgreSQL
pg_app = Flask(__name__)
pg_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:123456@localhost:5432/influencers'
)
pg_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(pg_app)

with pg_app.app_context():
    db.create_all()  # 确保表结构已创建
    for d in data:
        # 检查是否已存在，避免重复导入
        if not Influencer.query.filter_by(handle=d['handle']).first():
            influencer = Influencer(**d)
            db.session.add(influencer)
    db.session.commit()
    print(f"迁移完成，共迁移 {len(data)} 条记录。")