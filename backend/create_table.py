# 创建表
from main import app
from app.models import db

with app.app_context():
    db.create_all()
    print("All tables created!")