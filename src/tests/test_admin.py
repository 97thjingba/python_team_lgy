class TestAdmin:
    async def test_list_admin(self, client):
        response = await client.get('/admin/example')
        assert response.status == 200
