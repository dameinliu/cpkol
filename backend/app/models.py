from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(128), unique=True, nullable=False)
    sec_uid = db.Column(db.String(128))
    nickname = db.Column(db.String(128))
    follower_count = db.Column(db.Integer)
    heart_count = db.Column(db.Integer)
    video_count = db.Column(db.Integer)
    # ... 其他字段

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 视频ID
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'))
    desc = db.Column(db.Text)
    play_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    digg_count = db.Column(db.Integer)
    share_count = db.Column(db.Integer)
    # ... 其他字段
