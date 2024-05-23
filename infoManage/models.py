from django.db import models
from .untils.hash import pbkdf2
from .untils.aes_cbc import encrypt, check_text


class AdminUser(models.Model):
    """登录系统的账号密码"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=128)
    name = models.CharField(verbose_name="名称", max_length=32, blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """重新配置password字段，使用md5或者pbkdf2加密算法保存"""
        self.password = pbkdf2(self.password)
        super(AdminUser, self).save(*args, **kwargs)


class Environment(models.Model):
    """管理的环境区域"""
    area = models.CharField(verbose_name="区域代号", max_length=32, primary_key=True)
    area_name = models.CharField(verbose_name="区域名称", max_length=32)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, editable=False, blank=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, editable=False, blank=True)
    note = models.CharField(verbose_name="备注", max_length=128, blank=True, null=True)

    def __str__(self):
        return self.area_name


class AccountPassword(models.Model):
    """账号密码表"""
    name = models.CharField(verbose_name="名称", max_length=32, primary_key=True)
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=128)
    environment = models.ForeignKey("Environment", verbose_name="所属环境", on_delete=models.SET_NULL, blank=True,
                                    null=True, default="default")
    note = models.CharField(verbose_name="备注", max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not check_text(self.password):
            """重新配置password字段，使用aes加密算法保存"""
            self.password = encrypt(self.password)
        super(AccountPassword, self).save(*args, **kwargs)


class ServerInfo(models.Model):
    """主机信息表"""
    hostname = models.CharField(verbose_name="主机名", max_length=32, primary_key=True)
    ipaddress = models.GenericIPAddressField(verbose_name="IP地址")
    platform_choices = (
        ("Linux", "Linux"),
        ("Windows", "Windows"),
        ("MacOS", "MacOS"),
        ("Unix", "Unix"),
        ("Other", "Other"),
    )
    platform = models.CharField(verbose_name="平台", max_length=32, choices=platform_choices, default="Linux")
    protocol_choices = (
        ("ssh", "ssh"),
        ("rdp", "rdp"),
        ("telnet", "telnet"),
        ("vnc", "vnc"),
    )
    protocols = models.CharField(verbose_name="协议", max_length=32, choices=protocol_choices, default="ssh")
    port = models.PositiveIntegerField(verbose_name="端口")
    credentials = models.ForeignKey("AccountPassword", verbose_name="账户凭证", on_delete=models.SET_NULL, blank=True,
                                    null=True)
    environment = models.ForeignKey("Environment", verbose_name="所属环境", on_delete=models.SET_NULL, blank=True,
                                    null=True, default="default")
    note = models.CharField(verbose_name="备注", max_length=128, blank=True, null=True)


class DomainName(models.Model):
    """域名信息表"""
    protocol_choices = (
        ("http", "http"),
        ("https", "https"),
        ("ws", "ws"),
        ("wss", "wss"),
    )
    protocols = models.CharField(verbose_name="协议", max_length=32, choices=protocol_choices, default="http")
    domain_name = models.CharField(verbose_name="公开域名", max_length=128)
    listen_port = models.PositiveIntegerField(verbose_name="监听端口")
    server_ipaddress = models.CharField(verbose_name="主机ip", max_length=128)
    server_name = models.CharField(verbose_name="服务名称", max_length=128, blank=True, null=True)
    server_use = models.CharField(verbose_name="用途", max_length=128, blank=True, null=True)
    environment = models.ForeignKey("Environment", verbose_name="所属环境", on_delete=models.SET_NULL, blank=True,
                                    null=True, default="default")
    note = models.CharField(verbose_name="备注", max_length=128, blank=True, null=True)

# class File(models.Model):
#     """文件信息"""
#     file = models.FileField(upload_to=user_directory_path, null=True)
#     upload_method = models.CharField(max_length=20, verbose_name="上传方法")
