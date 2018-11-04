import uuid

from models.db_schema import Example
from views.utils import CreateView, ok_response
from views.serializers import ExampleSerializer


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
