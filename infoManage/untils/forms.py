from django import forms
from infoManage.models import AccountPassword, ServerInfo, DomainName, Environment
from infoManage.untils.hash import pbkdf2


class Bootstrap():
    # password = forms.CharField(min_length=6, label="密码")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.fields.items():
            if k == "create_time":
                v.widget.attrs = {"class": "form-control", "type": "text",
                                  "onclick": "WdatePicker({el:this,dateFmt:'yyyy-MM-dd'})", "placeholder": v.label}
                continue
            v.widget.attrs = {"class": "form-control", "placeholder": v.label}


class BootstrapModelForm(Bootstrap, forms.ModelForm):
    pass


class BootstrapForm(Bootstrap, forms.Form):
    pass


# modelform #

class EnvModelForm(BootstrapModelForm):
    """环境"""

    class Meta:
        model = Environment
        fields = "__all__"


class UserModelForm(BootstrapModelForm):
    """用户"""
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

    class Meta:
        model = AccountPassword
        fields = ["name", "username", "password", "environment", "note"]


class ServerModelForm(BootstrapModelForm):
    """服务器"""

    class Meta:
        model = ServerInfo
        fields = "__all__"


class DomainModelForm(BootstrapModelForm):
    """域名"""

    class Meta:
        model = DomainName
        fields = "__all__"


class LoginForm(BootstrapForm):
    """登录"""
    username = forms.CharField(label="用户名", widget=forms.TextInput, required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput, required=True)
    code = forms.CharField(label="验证码", widget=forms.TextInput, required=True)

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # return md5(pwd)
        return pbkdf2(pwd)


class RegisterFrom(BootstrapForm):
    """注册"""
    register_name = forms.CharField(label="昵称", widget=forms.TextInput, required=True)
    register_username = forms.CharField(label="登录账户", widget=forms.TextInput, required=True)
    register_password = forms.CharField(label="登录密码", widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label="重复密码", widget=forms.PasswordInput, required=True)


class ChangePasswordFrom(BootstrapForm):
    """修改密码"""
    current_username = forms.CharField(label="当前用户", widget=forms.TextInput, required=True)
    current_password = forms.CharField(label="当前密码", widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(label="新密码", widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label="重复新密码", widget=forms.PasswordInput, required=True)

    # 处理数据方式一
    def clean_current_password(self):
        """当前密码"""
        pwd = self.cleaned_data.get("current_password")
        # return md5(pwd)
        return pbkdf2(pwd)

    def clean_new_password(self):
        """新密码"""
        pwd = self.cleaned_data.get("new_password")
        # return md5(pwd)
        return pbkdf2(pwd)

    def clean_confirm_password(self):
        """重复新密码"""
        pwd = self.cleaned_data.get("confirm_password")
        # return md5(pwd)
        return pbkdf2(pwd)

    # 处理数据方式二 为空时候会导致报错
    # def clean(self):
    # cleaned_data = super().clean()
    # new_password = cleaned_data.get('new_password')
    # confirm_password = cleaned_data.get('confirm_password')
    # cleaned_data['new_password'] = pbkdf2(new_password)
    # cleaned_data['confirm_password'] = pbkdf2(confirm_password)
