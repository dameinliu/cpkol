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
        influencer1 = Influencer(
            handle='test_handle1',
            sec_uid='test_sec_uid1',
            follower_count=123,
            video_count=2,
            total_play_count=1000,
            total_comment_count=10,
            total_digg_count=20,
            videos='[]',
            updated_date=datetime(2024, 7, 9, 0, 0, 0)
        )
        influencer2 = Influencer(
            handle='test_handle2',
            sec_uid='test_sec_uid2',
            follower_count=123,
            video_count=2,
            total_play_count=1000,
            total_comment_count=10,
            total_digg_count=20,
            videos='[]',
            updated_date=datetime(2024, 7, 9, 0, 0, 0)
        )
        db.session.add(influencer)
        db.session.add(influencer1)
        db.session.add(influencer2)
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_search_influencers_single(client):
    response = client.get('/kol/search', query_string=[('keywords', 'test_handle')])
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert isinstance(data['items'], list)

def test_search_influencers_multiple(client):
    handles = ['test_handle1', 'test_handle2']
    response = client.get('/kol/search', query_string=[('keywords', h) for h in handles])
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert isinstance(data['items'], list)
    assert 'errors' in data
    assert isinstance(data['errors'], list)
    # 可选：检查 items/ errors 数量与输入 handle 数量关系

def test_search_influencers_empty(client):
    response = client.get('/kol/search', query_string=[])
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_search_influencers_invalid(client):
    response = client.get('/kol/search', query_string=[('keywords', ', , ,')])
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
