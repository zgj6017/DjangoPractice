from django.http import JsonResponse
from django.shortcuts import render

def chart_list(request):
    """数据统计表"""
    return render(request ,'chart_list.html')

def chart_bar(request):
    """构造柱状图的数据"""
    legend=["销量","业绩"]

    series_list= [
        {
            "name": "销量",
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '业绩',
            "type": 'bar',
            "data": [50, 230, 46, 80, 40, 27]
        }
    ]

    x_axis=['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'   ]
    result={
        "status": True,
        "data": {
            "series_list": series_list,
            "x_axis": x_axis,
            "legend": legend,
        }
    }
    return JsonResponse(result)

def chart_pie(request):
    """构造饼状图的数据"""

    db_data_list= [
        {"value": 1048, "name": '搜索引擎'},
        {"value": 735, "name": '直接访问'},
        {"value": 580, "name": '邮件营销'},
        {"value": 484, "name": '联盟广告'},
        {"value": 300, "name": '视频广告'}
    ]

    result={
        "status": True,
        "data": db_data_list,
    }
    return JsonResponse(result)