from django.urls import path
from infoManage.views import login,home, account, server, domain, environment

app_name = 'infoManage'
urlpatterns = [
    # 登录
    path('', login.index, name='index'),
    path('login/', login.login, name='login'),
    path('logout/', login.logout, name='logout'),
    path('image_code/', login.image_code, name='image_code'),
    # 注册
    path('register/', login.register, name='register'),
    # 修改密码
    path('change_password/', login.change_password, name='change_password'),
    # 主页
    path('home/', home.home_page, name='home_page'),
    # 区域列表
    path('env/list/', environment.environment_list, name='environment_list'),
    path('env/add/', environment.environment_add, name='environment_add'),
    path('env/detail/', environment.environment_detail, name='environment_detail'),
    path('env/edit/', environment.environment_edit, name='environment_edit'),
    path('env/delete/', environment.environment_delete, name='environment_delete'),
    # 区域模板上传
    path('env/upload/', environment.upload_ajax_excel, name='environment_upload'),
    # 账号密码列表
    path('<env_name>/account/', account.account_list, name='account_list'),
    path('account/add/', account.account_add, name='account_add'),
    path('account/detail/', account.account_detail, name='account_detail'),
    path('account/edit/', account.account_edit, name='account_edit'),
    path('account/delete/', account.account_delete, name='account_delete'),
    path('account/get_password/', account.get_password, name='account_get_password'),
    # 账号模板上传
    path('account/upload/', account.upload_ajax_excel, name='account_upload'),
    # 服务器列表
    path('<env_name>/server/', server.server_list, name='server_list'),
    path('server/add/', server.server_add, name='server_add'),
    path('server/detail/', server.server_detail, name='server_detail'),
    path('server/edit/', server.server_edit, name='server_edit'),
    path('server/delete/', server.server_delete, name='server_delete'),
    # 服务器模板上传
    path('server/upload/', server.upload_ajax_excel, name='server_upload'),
    # 域名列表
    path('<env_name>/domain/', domain.domain_list, name='domain_list'),
    path('domain/add/', domain.domain_add, name='domain_add'),
    path('domain/detail/', domain.domain_detail, name='domain_detail'),
    path('domain/edit/', domain.domain_edit, name='domain_edit'),
    path('domain/delete/', domain.domain_delete, name='domain_delete'),
    # 域名模板上传
    path('domain/upload/', domain.upload_ajax_excel, name='domain_upload'),
]
