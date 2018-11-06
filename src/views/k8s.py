from sanic import response


async def healthz(request):
    """
    k8s healtz 检测
    """
    return response.text('ok')


async def rediness(request):
    """
    k8s readiness 检测
    """
    return response.text('ok')
