# coding=utf-8
from django.shortcuts import render, redirect
from df_user.models import DeliveryInfo, UserInfo
from df_cart.models import CartInfo
from models import *
from df_user import user_decorator
from django.db import transaction
from datetime import datetime
# from django.utils import timezone
from decimal import Decimal

@user_decorator.login
def order(request):
    uid = request.session.get('user_id', '')
    # 获取地址
    deliveryinfo = DeliveryInfo.objects.get(user_id=uid, current_delivery=True)
    address = deliveryinfo.address.encode('utf-8')
    consignee = deliveryinfo.consignee.encode('utf-8')
    phone = deliveryinfo.phone.encode('utf-8')
    delivery_str = '%s   &nbsp;&nbsp;(%s &nbsp;收)  &nbsp; %s' % (address, consignee, phone)

    # 获取购物车
    carts_id = request.GET.getlist('cart_id')
    cartinfo_list = CartInfo.objects.filter(pk__in=carts_id)

    context = {
        'title': '提交订单',
        'page_name': 1,
        'delivery_str': delivery_str,
        'cartinfo_list': cartinfo_list,
        'freight': 10,
        'carts_id': carts_id,
    }
    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    # 接收所有购车id
    carts_id = eval(request.POST.get('carts_id', '[]'))
    try:
        # 创建订单对象
        orderinfo = OrderInfo()
        now = datetime.now()
        print now
        uid = request.session.get('user_id')
        orderinfo.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        orderinfo.ouser_id = uid
        orderinfo.odate = now
        orderinfo.ostatus = 0
        orderinfo.ototal = Decimal(request.POST['total'])
        orderinfo.oaddress = request.POST['address']
        orderinfo.save()

        for cart_id in carts_id:
            # 创建订单详情对象
            order_detail = OrderDetailInfo()
            cartinfo = CartInfo.objects.get(pk=cart_id)
            order_detail.order = orderinfo
            # 判断库存是否足够
            goods = cartinfo.goods
            if cartinfo.count <= goods.gstock:
                goods.gstock -= cartinfo.count
                goods.save()
                # 完善订单详情对象
                order_detail.goods_id = goods.id
                order_detail.price = goods.gprice
                order_detail.count = cartinfo.count
                order_detail.save()
                # 删除购物车条目对象
                cartinfo.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')

        transaction.savepoint_commit(tran_id)
    except Exception as result:
        print(result)
        transaction.savepoint_rollback(tran_id)
    return redirect('/user/order/')









