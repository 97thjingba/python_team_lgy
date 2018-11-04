import importlib
import time

import pytest
from sanic.server import HttpProtocol

from cassandra.cluster import NoHostAvailable

from models.management import DatabaseManagement

db_management = DatabaseManagement(timeout=30)


@pytest.yield_fixture
def app():
    """创建 sanic app, 进入时同步数据表, 退出时删除测试数据
    """
    from app.server import app as sanic_app

    # 使用 pycharm 的 pytest 模块时, 默认使用 local_settings
    if 'CASSANDRA_NODES' not in sanic_app.config:
        config_object = importlib.import_module('configs.local_settings')
        sanic_app.config.from_object(config_object)

    # 防止运行 CI 时连接失败, 等待 Cassandra 启动重新同步一次
    try:
        db_management.sync_db()
    except NoHostAvailable:
        time.sleep(20)
        db_management.sync_db()

    yield sanic_app
    db_management.drop_db()


@pytest.fixture
def client(loop, app, test_client):
    """创建 http client
    """
    return loop.run_until_complete(test_client(app, protocol=HttpProtocol))
