"""
sanic server
"""

from app import app
from app import listeners
from views.routers import api_blueprint, admin_blueprint, k8s_blueprint

app.listener('before_server_start')(listeners.setup_db_session)
app.listener('before_server_start')(listeners.setup_sentry_client)
app.listener('after_server_stop')(listeners.teardown_connection)

app.blueprint(api_blueprint)
app.blueprint(admin_blueprint)
app.blueprint(k8s_blueprint)


def run_server():
    """启动服务器
    根据启动参数加载配置, 如果没有相应的配置文件直接抛出错误
    """
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        workers=app.config.WORKERS,
        debug=app.config.DEBUG)
