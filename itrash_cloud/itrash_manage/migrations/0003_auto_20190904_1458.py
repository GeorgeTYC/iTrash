# Generated by Django 2.2.4 on 2019-09-04 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itrash_manage', '0002_sysinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysinfo',
            name='kvalue',
            field=models.CharField(max_length=50, verbose_name='值'),
        ),
    ]