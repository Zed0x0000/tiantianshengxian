# coding=utf-8
from django.db import models

# class UserInfoManager(models.Manager):
#     def create_user(self):
#         user = self.create(user_name='zhangchi', user_password=123456, user_email='787')
#         return user


class UserInfo(models.Model):
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=40)
    user_email = models.CharField(max_length=20)

    def __str__(self):
        return self.user_name.encode('utf-8')


# 收件人模型类
class DeliveryInfo(models.Model):
    consignee = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    postcode = models.CharField(max_length=6)
    phone = models.CharField(max_length=11)
    current_delivery = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.consignee.encode('utf-8')
