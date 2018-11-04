import inspect
import os

from aiocqlengine.aiocassandra import aiosession
from cassandra import AlreadyExists
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection as cqlengine_connection
from cassandra.cqlengine import management
from cassandra.cqlengine.models import Model
from cassandra.query import dict_factory

from app import app
from models import db_schema

config = app.config


def get_models(app_module):
    """获取所有某个模块下所有的 cqlengine model
    """
    models = []
    for name, model in inspect.getmembers(app_module):
        # 判断是否
        cql_model_types = (Model, )
        is_model_class = (inspect.isclass(model)
                          and issubclass(model, cql_model_types)
                          and not model.__abstract__)

        if is_model_class:
            # 判断 model 是否有 keyspace
            if model.__keyspace__ is None \
                    or model.__keyspace__ == config.KEYSPACE:
                models.append(model)

    return models


class Singleton(type):
    """单例元类, 用于创建单例对象
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class DatabaseManagement(metaclass=Singleton):
    """数据库管理器类, 单例: 使用 DatabaseManagement() 得到的永远是一个对象
    """

    def __init__(self, timeout=10):
        self.timeout = timeout
        # 如果要修改数据库, 设置 allow management
        os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = 'true'
        self.all_models = get_models(db_schema)
        self._keyspace = None
        self.db_session = None
        self._is_connected = False

    @property
    def keyspace(self):
        if self._keyspace is None:
            self._keyspace = config.KEYSPACE
        return self._keyspace

    def connect(self):
        """连接数据库
        """
        if self._is_connected:
            return

        auth = PlainTextAuthProvider(
            username=config.CASSANDRA_USER, password=config.CASSANDRA_PASSWORD)
        cluster = Cluster(config.CASSANDRA_NODES, auth_provider=auth)
        self.db_session = cluster.connect()
        self.db_session.set_keyspace(self.keyspace)
        self.db_session.row_factory = dict_factory
        self.db_session.default_timeout = self.timeout

        cqlengine_connection.set_session(self.db_session)

        aiosession(self.db_session)

        self._is_connected = True

    def disconnect(self):
        """断开连接
        """
        if not self._is_connected:
            return
        self.db_session.cluster.shutdown()
        self.db_session = None
        self._is_connected = False

    def create_keyspace(self, use_network_topology_strategy=False):
        """
        创建 Cassandra 的 keyspace
        :param use_network_topology_strategy: 是否需要多机房复制策略，生产环境需要
        :return:
        """

        if use_network_topology_strategy:
            # 多机房的复制策略, 用于生产环境
            create_keyspace_cql = (
                'CREATE KEYSPACE %s WITH replication = '
                "{'class' : 'NetworkTopologyStrategy', 'dc1' : 3} "
                'AND durable_writes = true;' % self.keyspace)
        else:
            # 单机房的复制策略, 用于开发和测试环境
            create_keyspace_cql = (
                'CREATE KEYSPACE %s WITH replication = '
                "{'class': 'SimpleStrategy', 'replication_factor': '1'} "
                'AND durable_writes = true;' % self.keyspace)

        auth = PlainTextAuthProvider(
            username=config.CASSANDRA_USER, password=config.CASSANDRA_PASSWORD)
        cluster = Cluster(config.CASSANDRA_NODES, auth_provider=auth)
        db_session = cluster.connect()
        try:
            db_session.execute(create_keyspace_cql)
        except AlreadyExists:
            return False
        return True

    def sync_db(self):
        """同步数据库, 默认不使用多机房策略
        use_network_topology_strategy: 是否需要多机房复制策略，生产环境需要
        """
        self.create_keyspace(
            use_network_topology_strategy=config.USE_NETWORK_TOPOLOGY_STRATEGY)

        if not self._is_connected:
            self.connect()

        for model in self.all_models:
            management.sync_table(model)

    def drop_db(self):
        """删除数据表, 单元测试时使用
        """
        if not self._is_connected:
            self.connect()

        management.drop_keyspace(self.keyspace)

        # 清除数据表后断开连接
        self.disconnect()
