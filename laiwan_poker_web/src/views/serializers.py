from marshmallow import fields, validates, Schema, ValidationError


# Fixme: 删除 example
class ExampleSerializer(Schema):
    """用于反序列化请求的数据
    """
    example_field = fields.Str(required=True)

    @validates('example_field')
    def validate_example_field(self, value):
        """验证具体的字段
        """
        if value != 'example':
            raise ValidationError('Only accept "example".')
