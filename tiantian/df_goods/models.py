# coding=utf-8
from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20, default='水果')
    gpic = models.ImageField(upload_to='df_goods')  # 注意配置MEDIA_ROOT ,INSTALL PILLOW PACKAGE
    gprice = models.DecimalField(max_digits=5, decimal_places=2,default=88)
    gunit = models.CharField(max_length=10, default='500g')
    gclick = models.IntegerField(default=0)
    gintroduction = models.CharField(max_length=200, default='这是水果')
    gstock = models.IntegerField(default=999)
    gcontent = HTMLField(default='<h1>这是描述得水果</h1>')  # 注意导入HTMLFiled 以及installed app 进行相关配置
    isDelete = models.BooleanField(default=False)
    type = models.ForeignKey(TypeInfo, default=2)

    def __str__(self):
        return self.gtitle.encode('utf-8')
