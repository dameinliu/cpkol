from flask import Flask
from app.api.influencers import influencer_bp
from app.models import db

app = Flask(__name__)
app.register_blueprint(influencer_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///influencers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
if __name__ == '__main__':
    app.run(debug=True) 