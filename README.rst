=====
信息管理系统infoManage
=====

Detailed documentation is in the "docs" directory.

打包
-----------
::

  cd django-infoManage
  python setup.py sdist
  # 预期会在dist里生成django-infoManage-0.1.tar.gz

安装
----
::

  pip install django-infoManage-0.1.tar.gz

快速开始
-----------

1. Add "infoManage" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "infoManage",
    ]

2. Include the info URLconf in your project urls.py like this::

    path("info/", include("infoManage.urls")),

3. Run ``python manage.py migrate`` to create the infoManage models.

4. Run ``python manage.py loaddata init_data.json`` to init database

5. Run ``python manage.py runserver`` to Start the development server

6. visit http://127.0.0.1:8000/admin/ to create a infoManage (you'll need the Admin app enabled).

7. Visit http://127.0.0.1:8000/info/ to participate in the infoManage.

8. 自己注册账号密码登录即可

# docker 打包
------
::

    python setup.py sdist
    docker build -f Dockerfile.base -t python:3.8.17-base .
    docker build -f Dockerfile -t infomanage:1.0 .
    docker run --name infomanage -p 8080:8080 -d infomanage:1.0
