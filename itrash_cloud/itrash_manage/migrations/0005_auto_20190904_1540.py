# Generated by Django 2.2.4 on 2019-09-04 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itrash_manage', '0004_cycletrash_drytrash_harmtrash_wettrash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycletrash',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='垃圾名'),
        ),
        migrations.AlterField(
            model_name='drytrash',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='垃圾名'),
        ),
        migrations.AlterField(
            model_name='harmtrash',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='垃圾名'),
        ),
        migrations.AlterField(
            model_name='wettrash',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='垃圾名'),
        ),
    ]
