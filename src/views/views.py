import uuid
import sys

from sanic.response import html
from models.db_schema import Example
from views.utils import CreateView, ok_response
from views.serializers import ExampleSerializer
from sanic.views import HTTPMethodView
from jinja2 import Environment, PackageLoader, select_autoescape
enable_async = sys.version_info >= (3, 6)

env = Environment(
    loader=PackageLoader('views.routers', '../templates'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)


async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(**kwargs))


class HomePageView(HTTPMethodView):
    template_file = ''

    async def get(slef, request, **kwargs):
        return template(slef.template_file)


class ExampleView(CreateView):
    # Fixme: 删掉 example

    serializer_class = ExampleSerializer

    async def save(self):
        """保存数据"""
        await Example.async_create(
            id=uuid.uuid4(),
            example_field=self.validated_data['example_field'])

    def response(self):
        return ok_response({'example': self.validated_data['example_field']})
