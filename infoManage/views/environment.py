import pandas as pd
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from infoManage.untils.forms import EnvModelForm, ChangePasswordFrom, RegisterFrom
from infoManage.models import Environment
from infoManage.untils.auth import login_check


@login_check
def environment_list(request):
    """环境列表"""
    data = {}
    search_data = request.GET.get('search', "")
    if search_data:
        data["area_name__contains"] = search_data
    form = EnvModelForm
    # 修改密码的form
    cp_form = ChangePasswordFrom()
    # 注册的form
    register_admin = RegisterFrom()
    env_list = Environment.objects.all()
    # print(list(env_list))
    # print(env_list.values())
    data_list = Environment.objects.filter(**data).order_by("create_time")
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    keys = Environment._meta.fields
    keys_list = [keys[i].verbose_name for i in range(len(keys))]
    context = {
        "title": "区域列表",
        "env_list": env_list,
        'env_name': "all",
        "search_data": search_data,
        "key_list": keys_list,
        "data_list": data_list,
        "page_obj": page_obj,
        "form": form,
        "cp_form": cp_form,
        "area": "active",
        "search_example": "搜 区域",
        "register": register_admin,
    }
    return render(request, 'infoManage/environment.html', context)


@login_check
@csrf_exempt
def environment_add(request):
    """添加区域 (ajax请求)"""
    form = EnvModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@login_check
def environment_detail(request):
    """获取区域详情"""
    area = request.GET.get("area")
    # print(area)
    row_dict = Environment.objects.filter(area=area).values("area", "area_name", "note").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {"status": True, 'data': row_dict}
    return JsonResponse(result)


@login_check
@csrf_exempt
def environment_edit(request):
    """区域编辑"""
    area = request.GET.get("area")
    row_object = Environment.objects.filter(area=area).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在"})
    form = EnvModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


@login_check
@csrf_exempt
def environment_delete(request):
    """区域删除"""
    area = request.GET.get('area')
    if not Environment.objects.filter(area=area).exists():
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    Environment.objects.filter(area=area).delete()
    return JsonResponse({"status": True, 'msg': "删除成功"})


@login_check
@csrf_exempt
def upload_ajax_excel(request):
    """ajax上传excel，读取数据写入数据库"""
    if request.method == 'POST':
        file_object = request.FILES.get('files')
        df = pd.read_excel(file_object, keep_default_na=False)
        # print(df)
        for i in df.index.values:
            df_dict = df.loc[i, ["area", "area_name", "note"]].to_dict()
            if df_dict["area"].startswith("#"):
                continue
            if Environment.objects.filter(area=df_dict["area"]):
                continue
            Environment.objects.create(**df_dict)
        return redirect("infoManage:environment_list")
    return JsonResponse({'status': False, 'error': 'excel异常'})
