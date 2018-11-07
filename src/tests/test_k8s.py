class TestK8s:
    async def test_healthz(self, client):
        """
        k8s healthz 检测
        """
        response = await client.get('/healthz')
        assert response.status == 200
        text = await response.text()
        assert text == 'ok'

    async def test_readiness(self, client):
        """
        k8s readiness 检测
        """
        response = await client.get('/readiness')
        assert response.status == 200
        text = await response.text()
        assert text == 'ok'
