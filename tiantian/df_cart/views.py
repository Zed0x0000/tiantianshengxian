# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from models import CartInfo
from df_user import user_decorator

@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    cartinfo_list = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'page_name': 1,
        'cartinfo_list': cartinfo_list,
    }
    return render(request, 'df_cart/cart.html', context)

@user_decorator.login
def add_to_cart(request, gid, count):
    uid = request.session.get('user_id')
    # 判断是否有这条记录
    cartinfo_list = CartInfo.objects.filter(user_id=uid, goods_id=int(gid))
    if len(cartinfo_list) >= 1:
        cartinfo = cartinfo_list[0]
        cartinfo.count = cartinfo.count + int(count)
    else:
        cartinfo = CartInfo()
        cartinfo.user_id = uid
        cartinfo.goods_id = int(gid)
        cartinfo.count = int(count)
    cartinfo.save()
    # 如果是ajax
    if request.is_ajax():
        cart_count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'cart_count': cart_count})
    else:
        return redirect('/cart/')
@user_decorator.login
def edit_cart(request, cid, count):
    try:
        cartinfo = CartInfo.objects.get(id=cid)
        count1 = cartinfo.count
        cartinfo.count = int(count)
        cartinfo.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)

@user_decorator.login
def delete_cart(request, cid):
    try:
        cartinfo = CartInfo.objects.get(id=cid)
        cartinfo.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)

