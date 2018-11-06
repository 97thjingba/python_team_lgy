"""
路由 http 请求
"""
from sanic.blueprints import Blueprint

from views import views, admin, k8s

###############################
# api
###############################
api_blueprint = Blueprint('example', version='1')

api_blueprint.add_route(
    views.ExampleView.as_view(), '/example', methods=['POST'])

###############################
# Admin 接口
###############################
admin_blueprint = Blueprint('admin')

admin_blueprint.add_route(
    admin.ListExampleView.as_view(), '/admin/example', methods=['GET'])

###############################
# k8s 检查
###############################
k8s_blueprint = Blueprint('k8s')

k8s_blueprint.add_route(k8s.healthz, '/healthz', methods=['GET'])
k8s_blueprint.add_route(k8s.rediness, '/readiness', methods=['GET'])
