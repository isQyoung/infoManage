from django.contrib import admin
from .models import AccountPassword, ServerInfo, AdminUser, DomainName, Environment

admin.site.register(AccountPassword)
admin.site.register(ServerInfo)
admin.site.register(AdminUser)
admin.site.register(DomainName)
admin.site.register(Environment)