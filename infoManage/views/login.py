from infoManage.untils.check_code import check_code
from io import BytesIO
from infoManage.untils.forms import LoginForm, RegisterFrom, ChangePasswordFrom
from infoManage.models import AdminUser
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from infoManage.untils.auth import login_check


def index(request):
    """默认跳转登录"""
    if request.method == "GET":
        return redirect("infoManage:login")


def login(request):
    """用户登录"""
    register_admin = RegisterFrom()
    if request.method == "GET":
        if request.session.get('info'):
            return redirect("infoManage:environment_list")
        form = LoginForm()
        return render(request, 'infoManage/login.html', {"form": form, 'register': register_admin})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 去数据库校验账号密码
        user_input_code = form.cleaned_data.pop('code')
        image_show_code = request.session.get('image_code', "")
        # print(form.cleaned_data)
        if image_show_code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'infoManage/login.html', {"form": form, 'register': register_admin})
        admin_project = AdminUser.objects.filter(**form.cleaned_data).first()
        # print(admin_project)
        if not admin_project:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'infoManage/login.html', {"form": form, 'register': register_admin})
        # 用户名密码正确 网站生成随机字符串 存到用户cookie中，写入session中
        request.session["info"] = {'id': admin_project.id, 'name': admin_project.name,
                                   'username': admin_project.username}
        request.session.set_expiry(60 * 60 * 24 * 7)
        # session_id = request.session.session_key
        # print(session_id)
        return redirect("infoManage:home_page")
    return render(request, 'infoManage/login.html', {"form": form, 'register': register_admin})


def logout(request):
    """用户注销"""
    request.session.flush()
    return redirect("infoManage:login")


def image_code(request):
    """生成图片验证码"""
    # 调用pillow函数 生产图片
    img, code_string = check_code()
    # 写入到自己的session中,60秒过期
    request.session['image_code'] = code_string
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


@login_check
@csrf_exempt
def register(request):
    """创建用户"""
    register_data = {}
    form = RegisterFrom(data=request.POST)
    field_names = list(form.fields.keys())
    if form.is_valid():
        # print(form.cleaned_data)
        confirm_password = form.cleaned_data.pop('confirm_password')
        password = form.cleaned_data['register_password']
        if confirm_password != password:
            form.add_error("confirm_password", "密码不一致")
            return JsonResponse({'status': False, 'error': form.errors})
        register_data['name'] = form.cleaned_data['register_name']
        register_data['username'] = form.cleaned_data['register_username']
        register_data['password'] = form.cleaned_data['register_password']
        AdminUser.objects.create(**register_data)
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, "field_names": field_names, 'error': form.errors})


@login_check
@csrf_exempt
def change_password(request):
    """用户修改密码"""
    change_data = {}
    form = ChangePasswordFrom(data=request.POST)
    field_names = list(form.fields.keys())
    # print(field_names)
    # print(form.errors)
    # print(form.is_valid())
    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.pop('current_username')
        # print(username)
        password_queryset = AdminUser.objects.filter(username=username).values('password')
        password_dict = password_queryset.first()
        current_password = form.cleaned_data.pop('current_password')
        old_password = password_dict['password']
        # print(current_password, old_password)
        if current_password != old_password:
            form.add_error("current_password", "当前密码不正确")
            return JsonResponse({'status': False, 'error': form.errors})
        new_password = form.cleaned_data['new_password']
        confirm_password = form.cleaned_data.pop('confirm_password')
        if confirm_password != new_password:
            form.add_error("confirm_password", "密码不一致")
            return JsonResponse({'status': False, 'error': form.errors})
        change_data['username'] = username
        change_data['password'] = form.cleaned_data['new_password']
        AdminUser.objects.filter(username=username).update(**change_data)
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, "field_names": field_names, 'error': form.errors})
