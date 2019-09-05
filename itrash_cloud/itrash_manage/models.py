from django.db import models
from django.db.models.fields.files import ImageFieldFile
from itrash_cloud.settings import MEDIA_ROOT
from .utils import make_thumb_fixed
from PIL import Image
import os

# Create your models here.
class HarmTrash(models.Model):
    name=models.CharField(max_length=100,primary_key=True,verbose_name="垃圾名")
    class Meta:
        verbose_name = '有害垃圾'
        verbose_name_plural = '有害垃圾'
class CycleTrash(models.Model):
    name=models.CharField(max_length=100,primary_key=True,verbose_name="垃圾名")
    class Meta:
        verbose_name = '可回收垃圾'
        verbose_name_plural = '可回收垃圾'
class WetTrash(models.Model):
    name=models.CharField(max_length=100,primary_key=True,verbose_name="垃圾名")
    class Meta:
        verbose_name = '湿垃圾'
        verbose_name_plural = '湿垃圾'
class DryTrash(models.Model):
    name=models.CharField(max_length=100,primary_key=True,verbose_name="垃圾名")
    class Meta:
        verbose_name = '干垃圾'
        verbose_name_plural = '干垃圾'


class SysInfo(models.Model):
    kname=models.CharField(max_length=20,primary_key=True,verbose_name="键名")
    kvalue=models.CharField(max_length=50,verbose_name="值")

    class Meta:
        verbose_name = '系统信息'
        verbose_name_plural = '系统信息'

    def __str__(self):
        return str(self.kname)


class PicInfo(models.Model):
    PicID=models.AutoField(primary_key=True, verbose_name='图像编号')
    time=models.DateTimeField(verbose_name="接收时间",auto_now_add=True)
    machine = models.CharField(max_length=20, blank=True, null=True, verbose_name="机号")
    image=models.ImageField(upload_to="trashimg", blank=True, null=True,verbose_name="图像")
    thumb = models.ImageField(verbose_name='缩略图', upload_to='thumb_trashimg', blank=True, null=True)  # 缩略图
    predict=models.CharField(max_length=20, blank=True, null=True,verbose_name='预测结果')
    real=models.CharField(max_length=20, blank=True, null=True,verbose_name='实际结果')
    audit=models.BooleanField(default=False, verbose_name='已审核')
    barcode=models.CharField(max_length=50, blank=True, null=True,verbose_name='条码结果')

    class Meta:
        verbose_name = '回传相片信息'
        verbose_name_plural = '回传相片信息'

    def save(self):
        super(PicInfo, self).save()
        if self.audit==False and self.image:
            img_name = self.image.name.split('/')[-1]
            thumb_pixbuf = make_thumb_fixed(self.image.path)
            rel_thumb_path = 'thumb_trashimg/'+ img_name
            thumb_path=os.path.join(MEDIA_ROOT,"thumb_trashimg",img_name)
            with open(thumb_path,"wb") as f:
                thumb_pixbuf.save(f)
            self.thumb = ImageFieldFile(self, self.thumb, rel_thumb_path)
            super(PicInfo, self).save()

    def save_nothumb(self):
        super(PicInfo, self).save()

    def __str__(self):
        return str(self.predict)
