from app01 import models
from app01.utils.pagination import Pagination
from datetime import datetime, date
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from app01.utils.form import UserModelForm,PrettyModelForm,PrettyEditModelForm


def user_list(request):
    """用户管理"""
    # 获取所有用户数据
    queryset = models.UserInfo.objects.all()

    # 使用分页组件
    page_obj = Pagination(request, queryset, page_size=2)  # 每页显示2条

    context = {
        "queryset": page_obj.page_queryset,  # 分页后的数据
        "page_string": page_obj.html()  # 分页HTML
    }

    return render(request, 'user_list.html', context)

def user_add(request):
    """添加用户(原始方法)"""

    # 准备上下文数据
    context = {
        'gender_choices': models.UserInfo.gender_choices,
        'department_choices': models.Department.objects.all(),
        'form_data': {}  # 用于保存已填写的数据
    }

    if request.method == "GET":
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    form_data = {
        'user': request.POST.get('user', '').strip(),
        'pwd': request.POST.get('pwd', '').strip(),
        'age': request.POST.get('age', '').strip(),
        'account': request.POST.get('account', '').strip(),
        'ctime': request.POST.get('ctime', '').strip(),
        'gender': request.POST.get('gender', '').strip(),
        'department': request.POST.get('department', '').strip()
    }
    context['form_data'] = form_data

    # === 服务器端验证 ===
    errors = []

    # 1. 验证必填字段
    required_fields = ['user', 'pwd', 'age', 'account', 'ctime', 'gender', 'department']
    for field in required_fields:
        if not form_data[field]:
            errors.append(
                f"{dict(zip(required_fields, ['姓名', '密码', '年龄', '账户余额', '入职时间', '性别', '部门']))[field]}不能为空")

    # 2. 验证年龄
    try:
        age = int(form_data['age'])
        if age < 18 or age > 60:
            errors.append("年龄必须在18-60岁之间")
    except ValueError:
        errors.append("年龄必须是有效数字")

    # 3. 验证账户余额
    try:
        account = float(form_data['account'])
        if account < 0:
            errors.append("账户余额不能为负数")
    except ValueError:
        errors.append("账户余额必须是有效数字")

    # 4. 验证入职日期
    if form_data['ctime']:
        try:
            hire_date = datetime.strptime(form_data['ctime'], '%Y-%m-%d').date()
            if hire_date > date.today():
                errors.append("入职日期不能晚于今天")
        except ValueError:
            errors.append("入职日期格式无效，请使用YYYY-MM-DD格式")

    # 5. 验证部门是否存在
    if form_data['department'] and not models.Department.objects.filter(id=form_data['department']).exists():
        errors.append("选择的部门不存在")

    # 如果有错误，返回表单并显示错误
    if errors:
        context['errors'] = errors
        return render(request, 'user_add.html', context)

    # === 所有验证通过，保存数据 ===
    try:
        models.UserInfo.objects.create(
            name=form_data['user'],
            password=form_data['pwd'],
            age=age,
            account=account,
            create_time=hire_date,  # 使用转换后的日期对象
            gender=form_data['gender'],
            depart_id=form_data['department']
        )
        messages.success(request, '用户添加成功！')
        return redirect('/user/list/')
    except Exception as e:
        errors.append(f"保存数据时出错: {str(e)}")
        context['errors'] = errors
        return render(request, 'user_add.html', context)


def user_model_form_add(request):
    """添加用户(ModelForm)"""

    name=forms.CharField(min_length=2,max_length=20,label="用户名")

    if request.method == "GET":
        form=UserModelForm()
        return render(request,'user_model_form_add.html',{"form":form})

    # 用户POST提交数据,数据校验
    form= UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request,'user_model_form_add.html',{"form":form})

def user_edit(request,nid):
    """编辑用户"""
    # 根据ID去数据库获取要编辑的那一行数据(对象)
    row_object=models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form=UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{"form":form})


    form=UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request,'user_edit.html',{"form":form})

def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')