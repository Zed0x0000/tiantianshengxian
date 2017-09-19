# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import TypeInfo, GoodsInfo
from django.core.paginator import Paginator
from df_cart.models import CartInfo
from haystack.views import SearchView


def index(request):
    # 获取数据每个分类中最热得最新得四条即可
    typeinfo_list = TypeInfo.objects.all()[0:3]
    hot_goodsinfo = []
    new_goodsinfo = []
    for typeinfo in typeinfo_list:
        hot_goodsinfo.append(typeinfo.goodsinfo_set.order_by('-gclick')[0:4])
        new_goodsinfo.append(typeinfo.goodsinfo_set.order_by('id')[0:4])
    context = {
        'title': '主页', 'guest_cart': 1,
        'hot_goodsinfo': hot_goodsinfo,
        'new_goodsinfo': new_goodsinfo,
        'cart_count': cart_count(request),
    }
    return render(request, 'df_goods/index.html', context)


def detail(request, gid):
    goodsinfo = GoodsInfo.objects.get(pk=gid)  # 如果确定一个最好用get来提升性能
    goodsinfo.gclick = goodsinfo.gclick + 1
    goodsinfo.save()
    typeinfo = goodsinfo.type  # 此处注意不是 typeinfo 另外可以在模板中直接来提取,不需要在这传递
    # typeinfo = TypeInfo.objects.filter(id=goodsinfo.type_id)[0]
    new = typeinfo.goodsinfo_set.order_by('id')[0:2]

    context ={
        'title': '商品详情',
        'guest_cart': 1,
        'typeinfo': typeinfo,
        'goodsinfo': goodsinfo,
        'new': new,
        'cart_count': cart_count(request),

    }
    red = render(request, 'df_goods/detail.html', context)

    # 将最近浏览得商品放进cookie中
    goods_browsed = request.COOKIES.get('goods_browsed', '[]')
    goods_browsed = eval(goods_browsed)

    # if goods_browsed:  # 如果有这个cookie, 继续判断
    if int(gid) in goods_browsed:
        goods_browsed.remove(int(gid))
    goods_browsed.insert(0, int(gid))
    if len(goods_browsed) >5:
        goods_browsed.pop()

    red.set_cookie('goods_browsed', goods_browsed)
    print goods_browsed
    return red


def cart_count(request):
    uid = request.session.get('user_id', '')
    if uid:
        return CartInfo.objects.filter(user_id=uid).count()
    else:
        return 0


def list_info(request, tid, sort, page_num):
    typeinfo = TypeInfo.objects.filter(pk=tid)[0]
    new = GoodsInfo.objects.filter(type_id=tid).order_by('id')[0:2]
    # sort=1 默认最新排序
    if sort == '1':
        goodsinfo_list = GoodsInfo.objects.filter(type_id=tid).order_by('id')
    # sort=2 价格排序
    if sort == '2':
        goodsinfo_list = GoodsInfo.objects.filter(type_id=tid).order_by('gprice')
    # sort=3 人气排序
    if sort == '3':
        goodsinfo_list = GoodsInfo.objects.filter(type_id=tid).order_by('-gclick')

    # 分页处理
    paginator = Paginator(goodsinfo_list, 10)
    page = paginator.page(page_num)  # 注意此处可以转成int(page_num)



    context ={
        'title': '商品列表',
        'guest_cart': 1,
        'typeinfo': typeinfo,
        'sort': int(sort),
        'new': new,
        'goodsinfo_list': goodsinfo_list,
        'page': page,
        'cart_count': cart_count(request),

    }
    return render(request, 'df_goods/list.html',context)


class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '搜索'
        context['guest_cart'] = 1
        context['cart_count'] = cart_count(self.request)
        return context
