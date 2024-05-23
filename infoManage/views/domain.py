from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from infoManage.untils.forms import DomainModelForm, ChangePasswordFrom, RegisterFrom
from django.core.paginator import Paginator
from infoManage.models import DomainName, Environment
from django.views.decorators.csrf import csrf_exempt
from infoManage.untils.auth import login_check
import pandas as pd


def create_domain():
    """创建删除域名"""
    for i in range(31):
        server = {
            "domain_name": "test{}.cnwansun.com".format(i),
            "listen_port": "100{}".format(i),
            "server_ipaddress": "172.16.1.{}".format(i),
            "server_name": "测试服务{}".format(i),
            "server_use": "测试用途{}".format(i),
            "note": "测试备注{}".format(i)
        }
        DomainName.objects.create(**server)
        DomainName.objects.filter(domain_name="测试服务器{}".format(i)).delete()


@login_check
def domain_list(request, env_name):
    """域名列表"""
    # create_domain()
    # 使用默认环境或获取当前环境
    current_env = "所有环境"
    data = {}
    if env_name != "all":
        current_env = get_object_or_404(Environment, pk=env_name)
        data = {"environment__area": env_name}
    search_data = request.GET.get('search', "")
    if search_data:
        data["server_name__contains"] = search_data
    form = DomainModelForm()
    # 修改密码的form
    cp_form = ChangePasswordFrom()
    # 注册的form
    register_admin = RegisterFrom()
    env_list = Environment.objects.all().order_by("create_time")
    data_list = DomainName.objects.filter(**data).order_by("domain_name")
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    keys = DomainName._meta.fields
    keys_list = [keys[i].verbose_name for i in range(len(keys))]
    # keys_list = [keys[i].name for i in range(len(keys))]
    context = {
        "title": f"{current_env} 域名列表",
        "env_list": env_list,
        'env_name': env_name,
        "current_env": current_env,
        "search_data": search_data,
        "key_list": keys_list,
        "data_list": data_list,
        "page_obj": page_obj,
        "form": form,
        "cp_form": cp_form,
        "domain": "active",
        "search_example": "搜 服务名",
        "register": register_admin,
    }
    return render(request, 'infoManage/domain.html', context)


@login_check
@csrf_exempt
def domain_add(request):
    """添加域名(ajax请求)"""
    form = DomainModelForm(data=request.POST)
    # (request.POST)
    # print(form)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@login_check
def domain_detail(request):
    """获取域名详情"""
    server_name = request.GET.get("server_name")
    row_dict = DomainName.objects.filter(server_name=server_name).values("protocols", "domain_name", "listen_port",
                                                                         "server_ipaddress", "server_name",
                                                                         "server_use", "environment",
                                                                         "note").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {"status": True, 'data': row_dict}
    return JsonResponse(result)


@login_check
@csrf_exempt
def domain_edit(request):
    """域名编辑"""
    server_name = request.GET.get("server_name")
    row_object = DomainName.objects.filter(server_name=server_name).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在"})
    form = DomainModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


@login_check
def domain_delete(request):
    """域名删除"""
    server_name = request.GET.get('server_name')
    if not DomainName.objects.filter(server_name=server_name).exists():
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    DomainName.objects.filter(server_name=server_name).delete()
    return JsonResponse({"status": True, 'msg': "删除成功"})


@login_check
@csrf_exempt
def upload_ajax_excel(request):
    """ajax上传excel，读取域名数据写入数据库"""
    if request.method == 'POST':
        file_object = request.FILES.get('files')
        df = pd.read_excel(file_object, keep_default_na=False)
        # print(df)
        for i in df.index.values:
            df_dict = df.loc[
                i, ["protocols", "domain_name", "listen_port", "server_ipaddress", "server_name", "server_use",
                    "environment_id", "note"]].to_dict()
            if df_dict["protocols"].startswith("#"):
                continue
            if not df_dict["environment_id"]:
                del df_dict["environment_id"]
            # print(df_dict)
            if DomainName.objects.filter(protocols=df_dict["protocols"], domain_name=df_dict["domain_name"],
                                         listen_port=df_dict["listen_port"]):
                continue
            DomainName.objects.create(**df_dict)
        return redirect("infoManage:domain_list", env_name="all")
    return JsonResponse({'status': False, 'error': 'excel异常'})
