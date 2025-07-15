from app01 import models
from app01.utils.pagination import Pagination
from django.shortcuts import render, redirect
from app01.utils.form import PrettyModelForm,PrettyEditModelForm

def pretty_list(request):
    """靓号列表"""
    # 搜索处理
    data_dict = {}
    search_data = request.GET.get('q', "").strip()
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 获取所有符合条件的数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

    # 使用分页组件
    page_obj = Pagination(request, queryset, page_size=10)

    context = {
        "queryset": page_obj.page_queryset,  # 分页后的数据
        "search_data": search_data,
        "page_string": page_obj.html(),  # 分页HTML
    }

    return render(request, 'pretty_list.html', context)

def pretty_add(request):
    """添加靓号"""
    if request.method == "GET":
        form=PrettyModelForm()
        return render(request,'pretty_add.html',{"form":form})

    form=PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request,'pretty_add.html',{"form":form})

def pretty_edit(request,nid):
    """编辑靓号"""

    row_object=models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form=PrettyEditModelForm(instance=row_object)
        return render(request,'pretty_edit.html',{"form":form})

    form=PrettyEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request,'pretty_edit.html',{"form":form})

def pretty_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')