import pandas as pd
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from infoManage.untils.forms import UserModelForm, ChangePasswordFrom, RegisterFrom
from infoManage.models import AccountPassword, Environment
from infoManage.untils.auth import login_check
from infoManage.untils.aes_cbc import decrypt


def create_account():
    """创建删除测试账号"""
    for i in range(31):
        account = {
            "name": "测试账号{}".format(i),
            "username": "test{}".format(i),
            "password": "password{}".format(i),
            "note": "测试备注{}".format(i)
        }
        AccountPassword.objects.create(**account)
        # AccountPassword.objects.filter(username="test{}".format(i)).delete()


@login_check
def account_list(request, env_name):
    """环境用户列表"""
    # create_account()
    # 使用默认环境或获取当前环境
    current_env = "所有环境"
    data = {}
    if env_name != "all":
        current_env = get_object_or_404(Environment, pk=env_name)
        data = {"environment__area": env_name}
    search_data = request.GET.get('search', "")
    if search_data:
        data["username__contains"] = search_data
    form = UserModelForm()
    # 修改密码的form
    cp_form = ChangePasswordFrom()
    # 注册的form
    register_admin = RegisterFrom()
    env_list = Environment.objects.all().order_by("create_time")
    # print(list(env_list))
    # print(env_list.values())
    data_list = AccountPassword.objects.filter(**data).order_by("name")
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    keys = AccountPassword._meta.fields
    keys_list = [keys[i].verbose_name for i in range(len(keys))]
    context = {
        "title": f"{current_env} 账号列表",
        "env_list": env_list,
        'env_name': env_name,
        "current_env": current_env,
        "search_data": search_data,
        "key_list": keys_list,
        "data_list": data_list,
        "page_obj": page_obj,
        "form": form,
        "cp_form": cp_form,
        "account": "active",
        "search_example": "搜 用户名",
        "register": register_admin,
    }
    return render(request, 'infoManage/account.html', context)


@login_check
@csrf_exempt
def account_add(request):
    """添加用户 (ajax请求)"""
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@login_check
def account_detail(request):
    """获取账号详情"""
    account_name = request.GET.get("name")
    row_dict = AccountPassword.objects.filter(name=account_name).values("name", "username", "password", "environment",
                                                                        "note").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {"status": True, 'data': row_dict}
    # print(row_dict)
    return JsonResponse(result)


@login_check
@csrf_exempt
def account_edit(request):
    """账号编辑"""
    account_name = request.GET.get("name")
    row_object = AccountPassword.objects.filter(name=account_name).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在"})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


@login_check
@csrf_exempt
def account_delete(request):
    """账号删除"""
    account_name = request.GET.get('name')
    if not AccountPassword.objects.filter(name=account_name).exists():
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    AccountPassword.objects.filter(name=account_name).delete()
    return JsonResponse({"status": True, 'msg': "删除成功"})


@login_check
@csrf_exempt
def get_password(request):
    """获取明文密码 (ajax请求)"""
    data = request.POST['encryption_password']
    # print(data)
    plaintext = decrypt(data)
    if plaintext:
        return JsonResponse({'status': True, 'message': '解密成功', 'plaintext': plaintext})
    return JsonResponse({'status': False, 'message': '解密失败'})


@login_check
@csrf_exempt
def upload_ajax_excel(request):
    """ajax上传excel，读取数据写入数据库"""
    if request.method == 'POST':
        file_object = request.FILES.get('files')
        df = pd.read_excel(file_object, keep_default_na=False)
        # print(df)
        for i in df.index.values:
            df_dict = df.loc[i, ["name", "username", "password", "note", "environment_id"]].to_dict()
            if df_dict["name"].startswith("#"):
                continue
            if not df_dict["environment_id"]:
                del df_dict["environment_id"]
            if AccountPassword.objects.filter(name=df_dict["name"]):
                continue
            AccountPassword.objects.create(**df_dict)
        return redirect("infoManage:account_list", env_name="all")
    return JsonResponse({'status': False, 'error': 'excel异常'})
