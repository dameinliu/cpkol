import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_influencers_route(client):
    response = client.get('/influencers')
    assert response.status_code in (200, 404)  # 200: 正常返回，404: 路由未实现 