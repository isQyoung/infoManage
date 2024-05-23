## 信息管理系统infoManage  


###打包
```
# 预期会在dist里生成django-infoManage-0.1.tar.gz
cd django-infoManage
python setup.py sdist 
```
### 安装
`pip install django-infoManage-0.1.tar.gz`

### 快速开始


1. 添加 "infoManage" 到你的 INSTALLED_APPS 设置中如下所示：
```
INSTALLED_APPS = [
    ...,
    "infoManage",
]
```
2. 包含 info 配置到你的项目的 urls.py 如下所示:  
`path("info/", include("infoManage.urls")),`

3. 创建infomanage的models  
`python manage.py migrate`

4. 导入基础数据到数据库  
`python manage.py loaddata init_data.json`

5. 开始启动服务  
`python manage.py runserver`

6. 访问创建管理员账户  
`http://127.0.0.1:8000/admin/`

7. 访问infomanage页面  
`http://127.0.0.1:8000/info/`

8. 自己注册账号密码登录即可

#### docker 打包
```
python setup.py sdist
docker build -f Dockerfile.base -t python:3.8.17-base .
docker build -f Dockerfile -t infomanage:1.0 .
docker run --name infomanage -p 8000:8080 -d infomanage:1.0
```

