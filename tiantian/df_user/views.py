# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from hashlib import sha1
from models import UserInfo, DeliveryInfo
import user_decorator
from df_goods.models import GoodsInfo
from django.db import transaction
from df_order.models import OrderInfo
from django.core.paginator import Paginator


def register(request):
    return render(request, 'df_user/register.html',{'title': '注册'})


def register_handle(request):
    # 接收数据
    post = request.POST
    user_name = post.get('user_name')
    pwd = post.get('pwd')
    cpwd= post.get('cpwd')
    email = post.get('email')

    # 判断密码是否一致
    if pwd != cpwd:
        return redirect('/user/register/')
    print ('-------------------------------------')
    # 密码加密
    s1 = sha1()
    s1.update(pwd)
    pwd3 = s1.hexdigest()

    # 用户数据存储
    userinfo = UserInfo()
    userinfo.user_name = user_name
    userinfo.user_password = pwd3
    userinfo.user_email = email
    userinfo.save()
    return redirect('/user/login/')


def register_exist(request):
    user_name = request.GET.get('user_name')
    count = UserInfo.objects.filter(user_name=user_name).count()
    return JsonResponse({'count': count})


def login(request):
    user_name = request.COOKIES.get('user_name', '')
    context = {'title': '登陆', 'name_error': 0, 'pwd_error': 0, 'username': user_name}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 获取登陆帐号跟密码
    input_name = request.POST.get('username')
    input_password = request.POST.get('pwd')
    is_remember = request.POST.get('isremember', 0)

    userinfo_list = UserInfo.objects.filter(user_name=input_name)
    print (userinfo_list)

    # 如果存在账户的条件
    if len(userinfo_list) == 1:
        s1 = sha1()
        s1.update(input_password)

        # 帐号密码都正确，返回到用户中心页面
        if s1.hexdigest() == userinfo_list[0].user_password:
            url = request.COOKIES.get('url')
            red = redirect(url)
            # 是否记住用户名
            if is_remember == 0:
                red.set_cookie('user_name', '',max_age=-1)
            else:
                red.set_cookie('user_name', input_name)
            # 设置session状态保持
            request.session['user_id'] = userinfo_list[0].id
            request.session['user_name'] = input_name
            return red
        else:
            context = {'title': '登陆', 'name_error': 0, 'pwd_error': 1, 'username': input_name, 'pwd': input_password}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '登陆', 'name_error': 1, 'pwd_error': 0, 'username': input_name, 'pwd': input_password}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


@user_decorator.login
def user_center_info(request):
    user_id = request.session['user_id']
    user_name = request.session['user_name']
    user_email = UserInfo.objects.get(pk=user_id).user_email
    # 获取cookie中最近浏览得几个商品id
    goods_browsed = request.COOKIES.get('goods_browsed', '[]')
    goods_browsed = eval(goods_browsed)
    goodsinfo_browsed= []
    for g_id in goods_browsed:
        goodsinfo_browsed.append(GoodsInfo.objects.get(pk=g_id))

    context = {'title': '用户中心',
               'page_name': 1,
               'user_name': user_name,
               'user_email': user_email,
               'goodsinfo_browsed': goodsinfo_browsed,
               }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def user_center_order(request, page_index):
    uid = request.session['user_id']
    # 获取所有订单对象
    orderinfo_list = OrderInfo.objects.filter(ouser_id=uid).order_by('-odate')
    # 分页对象
    paginator = Paginator(orderinfo_list, 2)
    if page_index == '':
        page_index = 1
    page = paginator.page(page_index)

    context = {
        'title': '订单中心', 'page_name': 1,
        # 'orderinfo_list': orderinfo_list,
        'page': page,
    }
    return render(request, 'df_user/user_center_order.html', context)


@transaction.atomic()
@user_decorator.login
def user_center_site(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(pk=user_id)
    # 如果是post方式,那么来储存地址信息
    current_deliveryinfo=user.deliveryinfo_set.filter(current_delivery=True)[0]
    print user
    print current_deliveryinfo
    if request.method == 'POST':
        tran_id = transaction.savepoint()
        try:
            post = request.POST
            deliveryinfo = DeliveryInfo()
            deliveryinfo.consignee = post.get('consignee')
            deliveryinfo.address = post.get('address')
            deliveryinfo.postcode = post.get('postcode')
            deliveryinfo.phone = post.get('phone')
            deliveryinfo.current_delivery = True
            deliveryinfo.user = user
            deliveryinfo.save()
            # 保存这个为当前收获地址,得吧上一个进行改为false
            current_deliveryinfo.current_delivery = False
            current_deliveryinfo.save()  # current_deliveryinfo[0]此处有坑,查询及不会缓存,每次都会产生新得对象

        except Exception as result:
            transaction.savepoint_rollback(tran_id)

        else:
            transaction.savepoint_commit(tran_id)

    # user_deliveryinfo_list = DeliveryInfo.objects.filter(user_id=user_id)
    user_deliveryinfo_list = user.deliveryinfo_set.filter(current_delivery=False)
    current_deliveryinfo = user.deliveryinfo_set.filter(current_delivery=True)[0]
    # print current_deliveryinfo.consignee
    # print type(current_deliveryinfo.consignee)
    # test_str1 = '你好'  # 输出为str byte
    # test_str2 = '%s你好' % current_deliveryinfo.consignee.encode('utf-8')  # 输出为str byte
    # test_str3 = '%s' % current_deliveryinfo.consignee  #输出为unicode
    # print ("_________________----------")
    # print type(test_str1)
    # print type(test_str2)
    # print type(test_str3)

    context = {'title': '收获地址',
               'page_name': 1,
               # 'consignee': consignee,
               # 'address': address,
               # 'postcode': postcode,
               # 'phone': phone,
               'user_deliveryinfo_list': user_deliveryinfo_list,
               'current_deliveryinfo': current_deliveryinfo,
               'user': user,

               }

    return render(request, 'df_user/user_center_site.html',context)






