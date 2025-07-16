import pytest
import os

def pytest_configure(config):
    """
    在 pytest 启动时、在导入任何测试文件之前设置环境变量。
    这是解决在导入时检查配置问题的标准方法。
    """
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    # 也可以显式设置其他测试所需的环境变量
    os.environ['USE_IAM_AUTH'] = 'False'

@pytest.fixture(scope='function')
def app():
    """
    为每个测试函数创建一个新的、干净的 Flask app 实例。
    """
    from app import create_app, db  # <-- **关键改动：将导入移到函数内部**

    # 使用 'testing' 配置，这将激活 TestingConfig
    app = create_app('testing')

    # app_context 确保了应用相关的操作（如数据库访问）有正确的上下文
    with app.app_context():
        # 创建所有数据库表
        db.create_all()
        # 'yield' 将 app 对象提供给测试函数
        yield app
        # 测试结束后，清理会话并删除所有表，确保测试隔离
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """
    提供一个用于向应用发送请求的测试客户端。
    依赖于 app fixture。
    """
    # client fixture 不需要导入 app，它接收已经创建好的 app 实例
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """
    提供一个用于测试 Flask CLI 命令的运行器。
    """
    return app.test_cli_runner() 