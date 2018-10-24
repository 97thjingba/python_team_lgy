# app_qrcode
App介绍，下载。使用二维码扫码后下载

## 开始开发

### 启动 docker

```
$ cd docker
$ docker-compose up -d
```

### 进入 docker
```
$ docker-compose exec app_qrcode bash
```

### 跑Web
```
$ python manage.py runserver 
```
然后就可以访问 <http://localhost:8000/download> 

或者<http://0.0.0.0:8000/download>

## 数据库

### 本地创建 couchdb 的管理员
有两种方式：

1.  curl -s -X PUT <http://couchdb:5984/_node/nonode@nohost/_config/admins/develop> -d '"devpwd"'
2.  使用管理界面： http://<docker machine ip>:5984/_utils/#addAdmin/nonode@nohost

### 在 服务器 环境创建 couchdb 管理员

需要手动创建 secret 后(见/k8s-ansible/k8s/couchdb/couchdb_secret.sh)，再使用 helm 部署 couchdb

## 使用文档

----------------

----------------

## 上传 App 文件

### 使用方法：

使用 qrcode_cli 脚本

``` sh
$ python qrcode.py --help
Usage: qrcode.py [OPTIONS]

  publish app

Options:
  -p, --path PATH  file path
  -l, --log TEXT   change log

```

相关参数详解:

-   `-p` , app路径
-   `-l` , 自定义发布时的 change log

### 例子：

``` sh
python qrcode.py -p ~/Download/doudizhu.apk -l 增加头像修改功能
```

返回值：

```json
{
    "ok":true,
    "message":"",
    "result":{
        "short_link": "https://api-staging.shafayouxi.org/e92e7"
    }
}
```

----------------

## 下载 App 文件

### API 方式下载

GET {{shafayouxi}}/v1/download/{{name}}-{{version}}.{{ext}}

|Key    |Value |
|---    |---   |
|name   |app名称|
|version|app版本|
|ext    |apk或ipa| 

注：ipa文件只可以通过苹果设备进行下载，apk文件除苹果设备均可下载（通过浏览器User-Agent进行判断）

### 浏览器下载

浏览器可以直接打开上传返回的短链接进行下载（同样区分User-Agent）
