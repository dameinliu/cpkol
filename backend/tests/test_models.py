import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import db
from app.models import Influencer
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_influencer_create(app):
    with app.app_context():
        influencer = Influencer(handle='testuser', follower_count=123)
        db.session.add(influencer)
        db.session.commit()
        found = Influencer.query.filter_by(handle='testuser').first()
        assert found is not None
        assert found.follower_count == 123 