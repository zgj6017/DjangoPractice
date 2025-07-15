from django.utils.safestring import mark_safe
from django.http import QueryDict


class Pagination:
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        分页组件

        :param request: 请求对象
        :param queryset: 查询集数据
        :param page_size: 每页显示条数
        :param page_param: URL中页码的参数名
        :param plus: 显示当前页前后几页
        """
        # 深拷贝GET参数并移除page参数
        self.query_dict = QueryDict(request.GET.urlencode(), mutable=True)
        if page_param in self.query_dict:
            self.query_dict.pop(page_param)

        self.page_param = page_param
        self.page_size = page_size
        self.plus = plus

        # 处理页码
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
            if page < 1:
                page = 1
        else:
            page = 1
        self.page = page

        # 分页数据
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]

        # 计算总页数
        total_count = queryset.count()
        total_pages, div = divmod(total_count, page_size)
        if div:
            total_pages += 1
        self.total_pages = total_pages

    def html(self):
        # 生成带参数的URL
        def make_url(page):
            query = self.query_dict.copy()
            query[self.page_param] = page
            return '?' + query.urlencode()

        # 计算页码范围
        if self.total_pages <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_pages
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_pages:
                    start_page = self.total_pages - 2 * self.plus
                    end_page = self.total_pages
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []

        # 首页
        if self.page > 1:
            page_str_list.append(f'<li class="page-item"><a class="page-link" href="{make_url(1)}">首页</a></li>')
        else:
            page_str_list.append('<li class="page-item disabled"><a class="page-link" href="#">首页</a></li>')

        # 上一页
        if self.page > 1:
            page_str_list.append(
                f'<li class="page-item"><a class="page-link" href="{make_url(self.page - 1)}">上一页</a></li>')
        else:
            page_str_list.append('<li class="page-item disabled"><a class="page-link" href="#">上一页</a></li>')

        # 页码
        for i in range(start_page, end_page + 1):
            if i > self.total_pages:
                continue
            if i == self.page:
                page_str_list.append(
                    f'<li class="page-item active"><a class="page-link" href="{make_url(i)}">{i}</a></li>')
            else:
                page_str_list.append(f'<li class="page-item"><a class="page-link" href="{make_url(i)}">{i}</a></li>')

        # 下一页
        if self.page < self.total_pages:
            page_str_list.append(
                f'<li class="page-item"><a class="page-link" href="{make_url(self.page + 1)}">下一页</a></li>')
        else:
            page_str_list.append('<li class="page-item disabled"><a class="page-link" href="#">下一页</a></li>')

        # 尾页
        if self.page < self.total_pages:
            page_str_list.append(
                f'<li class="page-item"><a class="page-link" href="{make_url(self.total_pages)}">尾页</a></li>')
        else:
            page_str_list.append('<li class="page-item disabled"><a class="page-link" href="#">尾页</a></li>')

        # 添加页数信息
        page_str_list.append(
            f'<li class="page-item disabled"><span class="page-link">共 {self.total_pages} 页</span></li>')

        # 跳转表单
        jump_html = """
        <li class="page-item">
            <form class="page-form" method="get">
                <div class="input-group">
                    <input type="text" class="form-control page-input" 
                           name="page" placeholder="页码" aria-label="页码">
                    {}
                    <button class="btn btn-outline-secondary" type="submit">跳转</button>
                </div>
            </form>
        </li>
        """.format("".join(
            [f'<input type="hidden" name="{k}" value="{v}">'
             for k, v in self.query_dict.items()]
        ))
        page_str_list.append(jump_html)

        return mark_safe("".join(page_str_list))