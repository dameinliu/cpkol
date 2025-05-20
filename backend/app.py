from flask import Flask
from app.api.influencers import influencer_bp

app = Flask(__name__)
app.register_blueprint(influencer_bp)

if __name__ == '__main__':
    app.run(debug=True) 