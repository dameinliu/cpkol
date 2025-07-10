import pytest
from app import create_app
from app.models import db, Influencer
from datetime import datetime

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    with app.app_context():
        db.create_all()
        # 可选：插入一个 Influencer 测试数据
        influencer = Influencer(
            handle='test_handle',
            sec_uid='test_sec_uid',
            follower_count=123,
            video_count=2,
            total_play_count=1000,
            total_comment_count=10,
            total_digg_count=20,
            videos='[]',
            updated_date=datetime(2024, 7, 9, 0, 0, 0)
        )
        db.session.add(influencer)
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_search_influencers_success(client):
    # 测试正常传参
    response = client.get('/kol/search', query_string={'keyword': 'test_handle'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert any(item['handle'] == 'test_handle' for item in data['items'])

def test_search_influencers_empty_keyword(client):
    # 测试 keyword 为空
    response = client.get('/kol/search', query_string={'keyword': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_search_influencers_not_found(client):
    # 测试数据库无此 handle
    response = client.get('/kol/search', query_string={'keyword': 'not_exist_handle'})
    assert response.status_code == 200
    data = response.get_json()
    # items 应该为空，errors 可能有内容
    assert isinstance(data['items'], list)
