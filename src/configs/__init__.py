"""
基础配置信息
通过 configs/__init__.py 将这个模块设置为默认的 config
"""
DEBUG = True

# sanic server config
HOST = '0.0.0.0'
PORT = 8000
WORKERS = 1

# cassandra config
CASSANDRA_NODES = ['test_server']
CASSANDRA_USER = 'cassandra'
CASSANDRA_PASSWORD = 'cassandra'
# Fixme: 设置合适的 keyspace 名称
KEYSPACE = 'example'
# 是否需要多机房复制策略, 如果 cassandra 节点放在不同的数据中心需要设置为 True
USE_NETWORK_TOPOLOGY_STRATEGY = False

# sentry, Fixme: 设置合适的 sentry dsn
SENTRY_DSN = ''
