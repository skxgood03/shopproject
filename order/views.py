from django.shortcuts import render
from django.http import *
# Create your views here.
from django.views import View

import jsonpickle

from cart.cartmanager import getCartManger


class ToOrderViews(View):
    def get(self,request):
        #获取请求参数
        cartitems = request.GET.get('cartitems','')
        #判断用户是否登录
        if not request.session.get('user'):
            return render(request,'login.html',{'cartitems':cartitems,'redirect':'order'})

        return HttpResponseRedirect('/order/order.html?cartitems='+cartitems)





class OrderListViews(View):
    def get(self,request):
        #获取请求参数
        cartitems=request.GET.get('cartitems','')
        print(cartitems)
        #将json格式字符串转换成python对象(字典{goodsid:1...})列表
        cartitemList = jsonpickle.loads('['+cartitems +']')
        #将python对象列表转换成CarItem对象列表
        # 列表推导式 循环cartitemList 如果有 item,使用getCartManger(request)的get_cartitems方法
        cartitemObjList = [getCartManger(request).get_cartitems(**item) for item in cartitemList if item ]
        #获取用户默认的收获地址
        address= request.session.get('user').address_set.get(isdefault = True)
        #获取支付总金额
        totalPrice = 0
        for cm in cartitemObjList:
            totalPrice+=cm.getTotalPrice()

        return render(request,'order.html',{'cartitemObjList':cartitemObjList,'address':address,'totalPrice':totalPrice})