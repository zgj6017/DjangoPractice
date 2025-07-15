from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from app01 import models
from app01.utils.pagination import Pagination
def admin_list(request):
    """管理员列表"""

    # 检测用户是否已登录,已登录,继续向下走。未登录，跳转回登录页面
    # 用户发来请求，获取cookie随机字符串，拿到随机字符串来看看session中有没有。
    info=request.session.get('info')
    if not info:
        return redirect('/login/')

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "").strip()
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    page_obj = Pagination(request, queryset, page_size=2)

    context = {
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
        "search_data": search_data,
    }

    return render(request,"admin_list.html",context)

from django import forms
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5

class AdminModelForm(BootstrapModelForm):

    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )
    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd=self.cleaned_data["password"]
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

class AdminResetModelForm(BootstrapModelForm):

    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )
    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd=self.cleaned_data["password"]
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists=models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


def admin_add(request):
    """添加管理员"""

    if request.method == "GET":
        form = AdminModelForm()
        return render(request,"change.html",{"form":form})

    form=AdminModelForm(data= request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request,"change.html",{"form":form})

def admin_edit(request,nid):
    """编辑管理员"""
    row_object=models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request,'error.html')

    if request.method == "GET":
        form=AdminEditModelForm(instance=row_object)
        return render(request,"change.html",{"form":form})

    form=AdminEditModelForm(instance=row_object,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request,"change.html",{"form":form})

def admin_delete(request,nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")

def admin_reset(request,nid):
    """重置密码"""
    row_object=models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request,'error.html')

    if request.method == "GET":
        form=AdminResetModelForm()
        return render(request,"change.html",{"form":form})

    form=AdminResetModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request,"change.html",{"form":form})
