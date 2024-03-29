# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-08-27 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itrash_manage', '0002_auto_20190827_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picinfo',
            name='audit',
            field=models.BooleanField(default=False, verbose_name='已审核'),
        ),
        migrations.AlterField(
            model_name='picinfo',
            name='machine',
            field=models.CharField(max_length=20, null=True, verbose_name='机号'),
        ),
        migrations.AlterField(
            model_name='picinfo',
            name='predict',
            field=models.CharField(max_length=20, null=True, verbose_name='预测结果'),
        ),
        migrations.AlterField(
            model_name='picinfo',
            name='real',
            field=models.CharField(max_length=20, null=True, verbose_name='实际结果'),
        ),
    ]
