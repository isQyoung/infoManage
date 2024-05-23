from django.shortcuts import render
from infoManage.models import Environment, AccountPassword, ServerInfo, DomainName
from infoManage.untils.forms import ChangePasswordFrom, RegisterFrom
from infoManage.untils.auth import login_check


@login_check
def home_page(request):
    # 修改密码的form
    cp_form = ChangePasswordFrom()
    # 注册的form
    register_admin = RegisterFrom()
    env_queryset = Environment.objects.all().values('area', 'area_name')
    account_count, server_count, domain_count = {}, {}, {}
    for i in env_queryset:
        account_count['key'], server_count['key'], domain_count['key'] = i['area_name'], i['area_name'], i['area_name']
        account_count[i['area_name']] = AccountPassword.objects.filter(environment=i['area']).count()
        server_count[i['area_name']] = ServerInfo.objects.filter(environment=i['area']).count()
        domain_count[i['area_name']] = DomainName.objects.filter(environment=i['area']).count()
    context = {
        "title": "主页",
        "env_name": "all",
        "cp_form": cp_form,
        "register": register_admin,
        "account_count": account_count,
        "server_count": server_count,
        "domain_count": domain_count
    }
    return render(request, 'infoManage/home.html', context)
