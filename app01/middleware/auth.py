from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info in [ '/login/','/image/code/']:
            return
        # 排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL

        # 读取当前访问的用户的session信息，如果能读到，说明已登录过，可以继续向下走
        info_dict=request.session.get('info')
        if info_dict:
            return

        # 如果没有登录过，重新回到登录界面
        return redirect('/login/')




