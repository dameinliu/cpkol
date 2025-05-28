from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from app.api.influencers import influencer_bp
from app.models import db
from app.cli import  reset_db #重置数据库
from flask_cors import CORS
import os
import sys

try:
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "DATABASE_URL",
        'postgresql://postgres:123456@localhost:5432/influencers'                                                   
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(influencer_bp)
    app.cli.add_command(reset_db)

    @app.route('/health')
    def health():
        return {"status": "ok"}, 200

    from sqlalchemy import text

    @app.route('/ping-db')
    def ping_db():
        try:
            # 执行一条最简单的 SQL 查询
            db.session.execute(text("SELECT 1"))
            return {"status": "ok", "message": "Database connection successful"}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500


    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(debug=True, host="0.0.0.0", port=port)
except Exception as e:
    print("Flask app failed to start:", e, file=sys.stderr)
    raise