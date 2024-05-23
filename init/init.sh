#!/bin/bash

# 创建django项目
django-admin startproject $APP_NAME

# 修改django的settings.py 配置
#sed "/^SECRET_KEY/c\SECRET_KEY = \'$key\'" ${APP_NAME}/${APP_NAME}/settings.py
#sed "/^ALLOWED_HOSTS/c\ALLOWED_HOSTS = ['*']" ${APP_NAME}/${APP_NAME}/settings.py
#sed "/^DEBUG/c\DEBUG = False" ${APP_NAME}/${APP_NAME}/settings.py
#sed '/django.contrib.staticfiles/a \    '\''infoManage'\'',' ${APP_NAME}/${APP_NAME}/settings.py

# 修改django的urls.py 配置
#sed 's/import path/import path, include/' ${APP_NAME}/${APP_NAME}/urls.py
#sed '/path(/a \    \'path\(\'\',include\(\'infoManage.urls\'\)\), ${APP_NAME}/${APP_NAME}/urls.py

# 覆盖原有配置
mv -f my_settings.py ${APP_NAME}/${APP_NAME}/settings.py
mv -f my_urls.py ${APP_NAME}/${APP_NAME}/urls.py
mv -f uwsgi.ini  ${APP_NAME}/
rm container_init.py  django-infoManage-0.1.tar.gz
