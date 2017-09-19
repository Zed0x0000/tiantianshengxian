# coding=utf-8
from django.test import TestCase


# class A(object):
#     def __init__(self, **kwargs):
#         for key, value in kwargs.items():
#             # print key
#             setattr(self, key, value)
#
#     def showName(self):
#         print self.name
#
# a = A(name='chi', gender='boy')
# # print a.name
# a.showName()

a = '登录'
print a
if a != '1登录':
    print '登录'
b = ['张', '池']
print b
print str(b)
for i in str(b).decode('string_escape'):
    print i
print str(b).decode('string_escape')