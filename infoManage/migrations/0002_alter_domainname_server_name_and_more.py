# Generated by Django 4.2.2 on 2023-08-15 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infoManage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainname',
            name='server_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='服务名称'),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='server_use',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='用途'),
        ),
    ]