from datetime import datetime

from cassandra.cqlengine import columns

from aiocqlengine.models import AioModel


class Example(AioModel):
    # Fixme: 删掉 example
    __table_name__ = 'example'

    id = columns.UUID(primary_key=True)
    created_at = columns.DateTime(default=datetime.utcnow)

    example_field = columns.Text()
