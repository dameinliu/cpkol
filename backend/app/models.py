from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import json

class Influencer(db.Model):
    __tablename__ = 'influencer'

    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(128), unique=True, nullable=False)
    sec_uid = db.Column(db.String(256), nullable=True)
    follower_count = db.Column(db.Integer, default=0)
    video_count = db.Column(db.Integer, default=0)
    total_play_count = db.Column(db.Integer, default=0)
    total_comment_count = db.Column(db.Integer, default=0)
    total_digg_count = db.Column(db.Integer, default=0)
    # 存储视频列表，使用JSON字符串
    videos = db.Column(db.Text, default='[]')
    updated_date = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=True, default=db.func.now())
    content_type = db.Column(db.String(64), nullable=True, default='normal')

    def to_dict(self):
        return {
            'handle': self.handle,
            'sec_uid': self.sec_uid,
            'follower_count': self.follower_count,
            'video_count': self.video_count,
            'total_play_count': self.total_play_count,
            'total_comment_count': self.total_comment_count,
            'total_digg_count': self.total_digg_count,
            'videos': json.loads(self.videos) if self.videos else []
        }

    def __repr__(self):
        return f'<Influencer {self.handle}>'