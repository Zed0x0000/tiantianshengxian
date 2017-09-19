# coding=utf-8
from django.db import models


class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    ouser = models.ForeignKey('df_user.UserInfo')
    odate = models.DateTimeField(auto_now=True)
    ostatus = models.IntegerField(default=0)  # 0为未支付, 1为支付,2为已发货,3.以收获,4.订单完成
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=150, )


class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()


