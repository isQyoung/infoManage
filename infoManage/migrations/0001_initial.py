# Generated by Django 4.2.2 on 2023-08-15 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountPassword',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='名称')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('note', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='名称')),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('area', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='区域代号')),
                ('area_name', models.CharField(max_length=32, verbose_name='区域名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('note', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='ServerInfo',
            fields=[
                ('hostname', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='主机名')),
                ('ipaddress', models.GenericIPAddressField(verbose_name='IP地址')),
                ('platform', models.CharField(choices=[('Linux', 'Linux'), ('Windows', 'Windows'), ('MacOS', 'MacOS'), ('Unix', 'Unix'), ('Other', 'Other')], default='Linux', max_length=32, verbose_name='平台')),
                ('protocols', models.CharField(choices=[('ssh', 'ssh'), ('rdp', 'rdp'), ('telnet', 'telnet'), ('vnc', 'vnc')], default='ssh', max_length=32, verbose_name='协议')),
                ('port', models.PositiveIntegerField(verbose_name='端口')),
                ('note', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('credentials', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='infoManage.accountpassword', verbose_name='账户凭证')),
                ('environment', models.ForeignKey(blank=True, default='default', null=True, on_delete=django.db.models.deletion.SET_NULL, to='infoManage.environment', verbose_name='所属环境')),
            ],
        ),
        migrations.CreateModel(
            name='DomainName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocols', models.CharField(choices=[('http', 'http'), ('https', 'https'), ('ws', 'ws'), ('wss', 'wss')], default='http', max_length=32, verbose_name='协议')),
                ('domain_name', models.CharField(max_length=128, verbose_name='公开域名')),
                ('listen_port', models.PositiveIntegerField(verbose_name='监听端口')),
                ('server_ipaddress', models.CharField(max_length=128, verbose_name='主机ip')),
                ('server_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='服务名称')),
                ('server_use', models.CharField(blank=True, max_length=32, null=True, verbose_name='用途')),
                ('note', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
                ('environment', models.ForeignKey(blank=True, default='default', null=True, on_delete=django.db.models.deletion.SET_NULL, to='infoManage.environment', verbose_name='所属环境')),
            ],
        ),
        migrations.AddField(
            model_name='accountpassword',
            name='environment',
            field=models.ForeignKey(blank=True, default='default', null=True, on_delete=django.db.models.deletion.SET_NULL, to='infoManage.environment', verbose_name='所属环境'),
        ),
    ]
