import pytest
from app.models import db, Influencer

def test_search_influencers_single_found(client):
    """
    测试：使用单个关键词搜索，并成功找到一个 influencer。
    """
    # 准备数据：只为本次测试添加一个特定的 influencer
    with client.application.app_context():
        influencer = Influencer(handle='test_user_1', sec_uid='uid1')
        db.session.add(influencer)
        db.session.commit()

    # 执行请求
    response = client.get('/kol/search?keywords=test_user_1')

    # 验证结果
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1
    assert data['items'][0]['handle'] == 'test_user_1'
    assert len(data['errors']) == 0

def test_search_influencers_multiple_keywords_only_processes_first(client):
    """
    测试：提供多个 keywords 时，API 当前只处理第一个。
    这是一个有用的测试，可以记录下 API 的当前行为。
    """
    # 准备数据
    with client.application.app_context():
        db.session.add(Influencer(handle='user_a', sec_uid='uida'))
        db.session.add(Influencer(handle='user_b', sec_uid='uidb'))
        db.session.commit()

    # 执行请求
    response = client.get('/kol/search?keywords=user_a&keywords=user_b&keywords=user_c')

    # 验证 API 是否只处理了第一个关键词
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1  # <--- 验证只返回了1个
    assert data['items'][0]['handle'] == 'user_a'
    assert len(data['errors']) == 0 # <--- 验证没有错误返回

def test_search_influencers_no_keywords(client):
    """
    测试：请求中不提供 keywords 参数。
    """
    response = client.get('/kol/search')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    # 验证返回的是实际的错误信息
    assert 'handle parameter cannot be empty' in data['error']

def test_search_influencers_empty_keywords(client):
    """
    测试：提供的 keywords 参数为空字符串或只包含无效字符。
    """
    response = client.get('/kol/search?keywords=, ,')
    
    # 验证服务器返回了 400 Bad Request
    assert response.status_code == 400
