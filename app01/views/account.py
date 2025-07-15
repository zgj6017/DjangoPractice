from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django import forms
from app01 import models
from app01.utils.bootstrap import BootstrapForm
from app01.utils.encrypt import md5
from app01.utils.check_code import check_code

class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required = True,
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True,
    )
    def clean_password(self):
        password = self.cleaned_data["password"]
        return md5(password)

def login(request):
    """登录"""

    if request.method == "GET":
        form = LoginForm()
        return render(request,'login.html',{'form':form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code=form.cleaned_data.pop('code')
        code=request.session.get('image_code',"")
        if code.upper() != user_input_code.upper():
            form.add_error("code","验证码错误")
            return render(request,'login.html',{'form':form})

        admin_object=models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password","用户名或密码错误")
            return render(request,'login.html',{'form':form})


        # 用户名和密码正确
        # return HttpResponse("提交成功")
        # 网站生成随机字符串;写到用户浏览器的cookie中;在写入到session中;
        request.session['info'] = {'id':admin_object.id,'username':admin_object.username}
        # session可以保存1天
        request.session.set_expiry(60*60*24)
        return redirect('/admin/list/')
    return render(request,'login.html',{'form':form})

def image_code(request):
    """生成验证码图片"""
    # 调用pillow函数，生成图片
    img,code_string=check_code()

    # 写入到自己的session中(以便于获取验证码再进行校验)
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream=BytesIO()
    img.save(stream,'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    """注销"""

    request.session.clear()
    return redirect('/login/')