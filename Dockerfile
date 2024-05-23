FROM registry.cn-shenzhen.aliyuncs.com/qiuyangfeng/qiuyangfeng:python-3.8.17-base
# FROM python:3.8.17-base
MAINTAINER 695702782@qq.com
COPY dist/django-infoManage-0.1.tar.gz /root/
COPY init/ /root/
WORKDIR /root
ENV APP_NAME='djangoApp'
ENV SECRET_KEY='WdTvDU3NEHkWBeXdgANyqueDn2r8@VV!D&vjBtYvmVCLTR-y#mJhT4yLF#33g&VyL&'
RUN python container_init.py && pip install django-infoManage-0.1.tar.gz && ./init.sh
EXPOSE 8080
CMD ["/root/docker-entrypoint.sh"]