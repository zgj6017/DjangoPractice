import random
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.pagination import Pagination

class OrderModelForm(BootstrapModelForm):
    class Meta:
        model=models.Order
        exclude=["oid","admin"] # 排除oid和admin

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为必填字段添加HTML属性
        for field in self.fields.values():
            if field.required:
                field.widget.attrs['required'] = 'required'

def order_list(request):
    """订单列表"""
    queryset=models.Order.objects.all().order_by('-id')
    page_obj=Pagination(request,queryset,page_size=10)
    form=OrderModelForm()
    context={
        "queryset":queryset,
        "page_object":page_obj,
        "form":form,
        "page_string": page_obj.html()
    }

    return render(request,'order_list.html',context)

@csrf_exempt
def order_add(request):
    """新建订单(Ajax请求)"""
    form=OrderModelForm(data= request.POST)
    if form.is_valid():
        # 额外增加一些不是用户输入的值(自己计算出来)
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(1000,9999))
        # 固定设置管理员ID,去哪里获取?
        form.instance.admin_id=request.session["info"]["id"]

        form.save()
        return JsonResponse({'status':True})

    return JsonResponse({'status':False,'error':form.errors})

def order_delete(request):
    """删除订单"""
    uid=request.GET.get("uid")
    exists=models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status':False,'error':"数据不存在,删除失败"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status':True})

def order_detail(request):
    """根据ID获取订单详细"""
    # 方式1
    """
    uid=request.GET.get("uid")
    row_object=models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'error': "数据不存在"})

    # 从数据库中获取一个对象 row_object
    result={
        "status":True,
        "data":row_object.title,
        "price":row_object.price,
        "status": row_object.status,
    }
    return JsonResponse(result)
    """

    # 方式2
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title","price","status").first()
    if not row_dict:
        return JsonResponse({'status': False, 'error': "数据不存在"})

    # 从数据库中获取一个对象 row_object
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get("uid")
    row_object=models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status":False,"tips":"数据不存在"})

    form=OrderModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})
