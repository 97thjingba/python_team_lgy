class TestExample:
    # Fixme: 更换命名

    example_url = '/v1/example'

    async def test_example_api(self, client):
        # Fixme: 添加测试, 更改方法命名

        request_body = {'example_field': 'example'}
        response = await client.post(self.example_url, json=request_body)

        assert response.status == 200
        json_result = await response.json()
        print(json_result)
        assert json_result['ok'] is True
