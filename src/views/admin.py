from models.db_schema import Example
from views.serializers import ExampleSerializer
from views.utils import AdminListView


class ListExampleView(AdminListView):

    serializer_class = ExampleSerializer

    async def get_all_objects(self):
        return await Example.filter().only(['id', 'created_at']).async_all()

    def search(self, results):
        return results
