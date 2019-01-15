"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from cmdb import views

urlpatterns = [
    url('admin/', admin.site.urls),
    # 路由首页
    url(r'^index/$', views.index),
    # 路由对来源的搜索
    url(r'^index/source=(.+)/$', views.search_by_source),
    # 路由对任意字符的搜索
    url(r'^index/text=(.+)/$', views.search_by_text),
    # 路由对关键字的搜索
    url(r'^index/detail=(\d+)/$', views.show_detail),
]
