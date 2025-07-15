from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name','password','age','account','create_time','gender','depart']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control',"placeholder":field.label}

class PrettyModelForm(forms.ModelForm):

    # 验证方式1
    mobile=forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'\d{11}+$','手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields=['mobile','price','level','status']
        # fields='__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control',"placeholder":field.label}

    # 验证格式2:
    # def clean_mobile(self):
    #     txt_mobile=self.cleaned_data['mobile']
    #     if len(txt_mobile)!=11:
    #         raise ValidationError('格式错误')
    #
    #     return txt_mobile

    def clean_mobile(self):
        txt_mobile=self.cleaned_data['mobile']
        exists=models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if  exists:
            raise ValidationError('手机号已存在')

        return txt_mobile

class PrettyEditModelForm(forms.ModelForm):

    # 不能修改手机号
    # mobile=forms.CharField(disabled=True,label="手机号")
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'\d{11}+$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields=['mobile','price','level','status']
        # fields='__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control',"placeholder":field.label}

    def clean_mobile(self):
        txt_mobile=self.cleaned_data['mobile']
        exists=models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')
        return txt_mobile

