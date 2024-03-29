# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-08-27 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='picinfo',
            fields=[
                ('PicID', models.AutoField(primary_key=True, serialize=False, verbose_name='图像编号')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='接收时间')),
                ('machine', models.CharField(blank=True, max_length=20, null=True, verbose_name='机号')),
                ('image', models.ImageField(blank=True, null=True, upload_to='trashimg', verbose_name='图像')),
                ('thumb', models.ImageField(blank=True, null=True, upload_to='thumb_trashimg', verbose_name='缩略图')),
                ('predict', models.CharField(blank=True, max_length=20, null=True, verbose_name='预测结果')),
                ('real', models.CharField(blank=True, max_length=20, null=True, verbose_name='实际结果')),
                ('audit', models.BooleanField(default=False, verbose_name='已审核')),
                ('barcode', models.CharField(blank=True, max_length=50, null=True, verbose_name='条码结果')),
            ],
            options={
                'verbose_name': '回传相片信息',
                'verbose_name_plural': '回传相片信息',
            },
        ),
    ]
