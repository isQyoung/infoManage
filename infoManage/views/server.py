from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from infoManage.untils.forms import ServerModelForm, ChangePasswordFrom, RegisterFrom
from django.core.paginator import Paginator
from infoManage.models import ServerInfo, Environment
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from infoManage.untils.auth import login_check


def create_server():
    """创建删除测试服务器"""
    for i in range(31):
        server = {
            "hostname": "测试服务器{}".format(i),
            "ipaddress": "172.16.1.{}".format(i),
            "platform": "Linux",
            "protocols": "rdp",
            "port": "3389",
            "note": "测试备注{}".format(i)
        }
        ServerInfo.objects.create(**server)
        # ServerInfo.objects.filter(hostname="测试服务器{}".format(i)).delete()


@login_check
def server_list(request, env_name):
    """服务器列表"""
    # create_server()
    # 使用默认环境或获取当前环境
    current_env = "所有环境"
    data = {}
    if env_name != "all":
        current_env = get_object_or_404(Environment, pk=env_name)
        data = {"environment__area": env_name}
    search_data = request.GET.get('search', "")
    if search_data:
        data["hostname__contains"] = search_data
    form = ServerModelForm()
    # 修改密码的form
    cp_form = ChangePasswordFrom()
    # 注册的form
    register_admin = RegisterFrom()
    env_list = Environment.objects.all().order_by("create_time")
    data_list = ServerInfo.objects.filter(**data).order_by("hostname")
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    keys = ServerInfo._meta.fields
    keys_list = [keys[i].verbose_name for i in range(len(keys))]
    # keys_list = [keys[i].name for i in range(len(keys))]
    context = {
        "title": f"{current_env} 服务器列表",
        "env_list": env_list,
        'env_name': env_name,
        "current_env": current_env,
        "search_data": search_data,
        "key_list": keys_list,
        "data_list": data_list,
        "page_obj": page_obj,
        "form": form,
        "cp_form": cp_form,
        "server": "active",
        "search_example": "搜 主机名",
        "register": register_admin,
    }
    return render(request, 'infoManage/server.html', context)


@login_check
@csrf_exempt
def server_add(request):
    """添加服务器(ajax请求)"""
    form = ServerModelForm(data=request.POST)
    # print(request.POST)
    # print(form)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@login_check
def server_detail(request):
    """获取服务器详情"""
    hostname = request.GET.get("hostname")
    row_dict = ServerInfo.objects.filter(hostname=hostname).values("hostname", "ipaddress", "platform", "protocols",
                                                                   "port",
                                                                   "note", "credentials", "environment").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {"status": True, 'data': row_dict}
    return JsonResponse(result)


@login_check
@csrf_exempt
def server_edit(request):
    """账号编辑"""
    hostname = request.GET.get("hostname")
    row_object = ServerInfo.objects.filter(hostname=hostname).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在"})
    form = ServerModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


@login_check
def server_delete(request):
    """服务器删除"""
    hostname = request.GET.get('hostname')
    if not ServerInfo.objects.filter(hostname=hostname).exists():
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    ServerInfo.objects.filter(hostname=hostname).delete()
    return JsonResponse({"status": True, 'msg': "删除成功"})


@login_check
@csrf_exempt
def upload_ajax_excel(request):
    """ajax上传excel，读取服务器数据写入数据库"""
    if request.method == 'POST':
        file_object = request.FILES.get('files')
        df = pd.read_excel(file_object, keep_default_na=False)
        # print(df)
        for i in df.index.values:
            df_dict = df.loc[
                i, ["hostname", "ipaddress", "platform", "protocols", "port", "credentials_id", "environment_id",
                    "note"]].to_dict()
            if df_dict["hostname"].startswith("#"):
                continue
            if not df_dict["credentials_id"]:
                del df_dict["credentials_id"]
            if not df_dict["environment_id"]:
                del df_dict["environment_id"]
            # print(df_dict)
            if ServerInfo.objects.filter(hostname=df_dict["hostname"]):
                continue
            ServerInfo.objects.create(**df_dict)
        return redirect("infoManage:server_list", env_name="all")
    return JsonResponse({'status': False, 'error': 'excel异常'})
