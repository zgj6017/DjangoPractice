import json
from django.shortcuts import render
from django import forms
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.pagination import Pagination
from app01.models import Task

class TaskModelForm(BootstrapModelForm):
    class Meta:
        model=models.Task
        fields="__all__"
        widgets={
            "detail":forms.TextInput,
            # "detail": forms.Textarea
        }


def task_list(request):
    """任务列表"""
    # 获取所有任务并按ID降序排列
    queryset = Task.objects.all().order_by('-id')

    # 初始化分页组件
    pagination = Pagination(
        request=request,
        queryset=queryset,
        page_size=10,  # 每页显示10条
        page_param="page",  # URL中页码的参数名
        plus=5  # 显示当前页前后5页
    )

    # 获取分页后的数据
    page_queryset = pagination.page_queryset

    # 初始化表单
    form = TaskModelForm()

    context = {
        'queryset': page_queryset,  # 使用分页后的数据
        'form': form,
        'pagination_html': pagination.html(),  # 分页HTML
    }

    return render(request, "task_list.html", context)

@csrf_exempt
def task_add(request):

    # 用户发过来的数据进行校验(ModelForm进行校验)
    form=TaskModelForm(data= request.POST)
    if form.is_valid():
        form.save()
        data_dict={"status":True}
        return HttpResponse(json.dumps(data_dict))

    data_dict={"status":False,'error':form.errors}
    return HttpResponse(json.dumps(data_dict,ensure_ascii=False))

