from django import forms

class BootStrap:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环ModelForm中的所有字符串,给每个字段的插件设置
        for name,field in self.fields.items():
            # 字段中有属性，保留原来的属性，没有属性，才能加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs={
                    "class":"form-control",
                    "placeholder":field.label
                }

class BootstrapModelForm(BootStrap,forms.ModelForm):
    pass

class BootstrapForm(BootStrap,forms.Form):
    pass