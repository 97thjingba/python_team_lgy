import logging

from raven.handlers.logging import SentryHandler

import raven
import raven_aiohttp

from models.management import DatabaseManagement

logger = logging.getLogger('sanic')


def setup_db_session(app, loop):
    """make cassandra session async
    """
    db_management = DatabaseManagement()
    db_management.connect()
    logger.info('Cassandra session prepared')


def setup_sentry_client(app, loop):
    """设置 sentry client, 用于发送错误信息
    如果在 DEBUG 状态下, 不使用 sentry
    """
    if not app.config.DEBUG:
        app.sentry = raven.Client(
            dsn=app.config.SENTRY_DSN,
            transport=raven_aiohttp.AioHttpTransport,
            enable_breadcrumbs=False,
        )
        handler = SentryHandler(
            client=app.sentry,
            level=app.config.get('SENTRY_LEVEL', logging.ERROR))
        logging.getLogger('asyncio').addHandler(handler)

        logger.info('Sentry client prepared')


async def teardown_connection(app, loop):
    """断开连接
    """
    db_management = DatabaseManagement()
    db_management.disconnect()
    logger.info('Cassandra session has shutdown')
