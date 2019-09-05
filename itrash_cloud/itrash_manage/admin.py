from django.contrib import admin
from .models import *


class picinfoadmin(admin.ModelAdmin):
    list_display=("PicID","predict","real","audit","time")
    empty_value_display = '无'


class sysinfoadmin(admin.ModelAdmin):
    list_display=("kname","kvalue")
    empty_value_display = '无'


class harmtrashadm(admin.ModelAdmin):
    list_display=("name",)
    empty_value_display = '无'

class cycletrashadm(admin.ModelAdmin):
    list_display=("name",)
    empty_value_display = '无'

class drytrashadm(admin.ModelAdmin):
    list_display=("name",)
    empty_value_display = '无'

class wettrashadm(admin.ModelAdmin):
    list_display=("name",)
    empty_value_display = '无'


# Register your models here.
admin.site.register(PicInfo, picinfoadmin)
admin.site.register(SysInfo, sysinfoadmin)
admin.site.register(HarmTrash,harmtrashadm)
admin.site.register(CycleTrash,cycletrashadm)
admin.site.register(DryTrash,drytrashadm)
admin.site.register(WetTrash,wettrashadm)

admin.site.site_header ="iTrash数据修改系统"
admin.site.site_title="iTrash"