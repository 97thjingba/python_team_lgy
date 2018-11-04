# sanic_template

sanic 应用模板, 如果发现有需要优化的地方请提 pr 或 issue

ps: example 仅供参考, 使用时请把所有标记出 Fixme 的地方进行相应删改

## api 开发流程

### 1. 添加测试
1. 根据设计好的 api 添加相应测试, 测试中验证返回数据是否符合 api 期望

### 2. 添加 api
1. 在 `models.db_scheme` 中添加需要的 Model
2. 在 `views.serializers` 中添加用于验证 api 数据数据的 serializer
3. 在 `views.views` 中添加 api 处理视图类
4. 在 `views.routers` 中添加 url 路由

### 3. 添加文档
1. 文档中需要详细描述 api 的 `url path`, `url params`, `header`, `body`

### 4. 测试
1. 完善 `.drone.yml`
2. 本地使用时, 添加本地配置 `configs/local_settings.py`, 运行 `python manage.py test --config=local_settings` 进行测试
3. 本地同步数据库: `python manage.py sync_db --config=local_settings`
4. 本地启动服务器: `python manage.py runserver --config=local_settings`

### 5. 部署
1. 申请 sentry dsn, 配置到 `configs/__init__.py` 中
后续部署流程等待 k8s 使用流程确定好后完善
