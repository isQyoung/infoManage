#!/bin/bash

cd ${APP_NAME} || exit
#sed "/^SECRET_KEY/c\SECRET_KEY = \'$SECRET_KEY\'" ${APP_NAME}/${APP_NAME}/settings.py
# sed -i "s/myDjangoAppSecretKey/${SECRET_KEY}/" ${APP_NAME}/settings.py
# sed -i "s/DJANGOAPP/${APP_NAME}/g" uwsgi.ini

# 生成admin密码哈希
ADMIN_PASS_HASH=$(python manage.py shell -c "from infoManage.untils.hash import pbkdf2;print(pbkdf2('admin'));")
find /usr/local/lib/ -name init_data.json -exec sed -i "s/use_password_hash_instead_me/${ADMIN_PASS_HASH}/g" {} \;

# 生成初始数据库
python manage.py makemigrations
python manage.py migrate
# 导入初始数据
function init_data() {
  python manage.py loaddata init_data.json
}

python manage.py shell -c 'from infoManage.models import Environment;exit(0) if Environment.objects.filter(area="default").exists() else exit(1)' || init_data

uwsgi --ini uwsgi.ini