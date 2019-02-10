"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path,include
from myblog import views
from django.views.static import serve
from blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^login/',views.login),
    re_path(r"^get_valid_img/",views.get_valid_img),
    re_path(r"^index/",views.index),
    re_path(r"^register/",views.register),
    re_path(r"^$",views.index),
    re_path(r"^logout/$",views.log_out),
    re_path(r"add/",views.submit),
    re_path(r"update_pwd/",views.update_pwd),
    re_path(r"sub_pwd/",views.sub_pwd),

    #myblog分发
    re_path(r"^blog/",include("myblog.urls")),

    #media配置
    re_path(r"^media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT}),

    #文本编辑器上传
    re_path(r"^upload_img/",views.upload_img)


]
