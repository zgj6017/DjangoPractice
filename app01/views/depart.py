from app01 import models
from app01.utils.pagination import Pagination
from django.shortcuts import render, redirect

def depart_list(request):
    """部门列表"""

    queryset = models.Department.objects.all()

    page_obj=Pagination(request,queryset,page_size=3)
    context = {
        "queryset":page_obj.page_queryset,
        "page_string":page_obj.html()
    }

    return render(request,"depart_list.html",context)

def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request,'depart_add.html')

    # 获取用户POST提交过来的数据
    title = request.POST.get('title')

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表
    return redirect('/depart/list/')

def depart_delete(request):
    """删除部门"""

    nid=request.GET.get('nid')

    models.Department.objects.filter(id=nid).delete()

    return redirect('/depart/list/')

def depart_edit(request,nid):
    """编辑部门"""
    if request.method == "GET":
        row_object=models.Department.objects.filter(id=nid).first()

        return render(request,'depart_edit.html',{"row_object":row_object})

    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')