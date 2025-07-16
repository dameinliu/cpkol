# app模块初始化
from flask import Flask
from flask_cors import CORS
from .config import config
import os
from .extentions import db, migrate

def create_app(config_name='default'):
    from dotenv import load_dotenv
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    # 注册蓝图
    from .api.kol import kol_bp
    from .api.video import video_bp
    from .api.feishu.feishu import feishu_bp
    from .api.feishu.feishu_oauth import feishu_oauth_bp
    app.register_blueprint(kol_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(feishu_bp)
    app.register_blueprint(feishu_oauth_bp)

    # 注册自定义 CLI 命令
    from .cli import reset_db
    app.cli.add_command(reset_db)

    # 健康检查
    @app.route('/health')
    def health():
        return {"status": "ok"}, 200

    from sqlalchemy import text
    @app.route('/ping-db')
    def ping_db():
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ok", "message": "Database connection successful"}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500

    return app

