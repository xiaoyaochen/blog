from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
import re
from django.http import JsonResponse
from django.contrib import auth

def login(request):
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        input_valid_codes = request.POST.get("valid_code")

        #检验认证码
        keep_valid_codes = request.session.get("keep_valid_codes")
        '''
        1、拿到cookie中sessionid对应的随机字符串
        2、在django-session表中过滤记录
        '''
        login_response = {"user":None,"error_msg":""}
        if keep_valid_codes.upper()==input_valid_codes.upper():
            user = auth.authenticate(username=user,password=pwd)
            if user:
                auth.login(request,user)
                login_response['user'] = user.username
            else:
                login_response['error_msg'] = "用户名或密码错误"
        else:
            login_response['error_msg'] = "验证码错误"
        import json
        return HttpResponse(json.dumps(login_response))
    else:
        return render(request, "login.html")

#获取验证码
def get_valid_img(request):
    from myblog.utils import valid_code
    data = valid_code.get_valid_value(request)
    return HttpResponse(data)

def index(request):
    print("===",request.user)
    article_list = Article.objects.all().order_by("-create_time")
    return render(request,"index.html",{"article_list":article_list})

from django import forms
from django.forms import widgets
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError
#按from表单构建forms组件
class Regform(forms.Form):
    user = forms.CharField(min_length=4,max_length=8,widget=widgets.TextInput(attrs={"class":"form-control"}),
                           error_messages={"min_length":"输入过短，至少输入4个字符",
                                           "max_length":"输入过长，至多输入8个字符",
                                           "required":"必填"}
                           )
    pwd = forms.CharField(min_length=5,widget=widgets.PasswordInput(attrs={"class":"form-control"}),
                          error_messages={"min_length":"输入过短，至少输入5个字符","required":"必填"})
    repeat_pwd = forms.CharField(min_length=5,
                                 widget=widgets.PasswordInput(attrs={"class":"form-control"}),
                                 error_messages={"min_length":"输入过短，至少输入5个字符","required":"必填"})
    email = forms.EmailField(min_length=5,
                             widget=widgets.EmailInput(attrs={"class":"form-control"}),
                             error_messages={"min_length":"s输入过短，至少输入5个字符","required":"必填"})

    #勾子函数
    def clean_user(self):
        val=self.cleaned_data.get("user")
        if not val.isdigit():
            return val
        else:
            raise ValidationError("用户名不能纯数字！")

    def clean_pwd(self):
        val = self.cleaned_data.get("pwd")

        if not val.isdigit():
            return val
        else:
            raise ValidationError("密码不能纯数字！")

#注册
def register(request):
    if request.is_ajax():
        print("request.POST",request.POST)
        print("request.FILES",request.FILES)
        form_obj = Regform(request.POST)
        reg_response = {"user":None,"error_mes":None}

        if form_obj.is_valid():
            user = form_obj.cleaned_data.get("user")
            pwd = form_obj.cleaned_data.get("pwd")
            email = form_obj.cleaned_data.get("email")
            avatar_img = form_obj.cleaned_data.get("avatar_img")
            blog = Blog.objects.create(title=user+'的博客',site="/blog/"+user,theme="未设置...")
            if avatar_img:
                print("avatar_img....",avatar_img)
                user = UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar_img,blog=blog)
            else:
                user = UserInfo.objects.create_user(username=user,password=pwd,email=email,blog=blog)


            reg_response["user"] = user.username
        else:
            reg_response["error_mes"] = form_obj.errors
        return JsonResponse(reg_response)
    else:
        form_obj=Regform()
        return render(request,'reg.html',{"form_obj":form_obj})

#注销
def log_out(request):
    auth.logout(request)
    return  redirect("/login")



#个人站点设计
def home_site(request,username,**kwargs):
    print("kwargs",kwargs)
    print(username)
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("<h3>404<h3>")
    #当前访问站点对象
    blog = user.blog
    #当前访问长点的所有文章
    if not kwargs:
        article_list = Article.objects.filter(user=user)
    else:
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition=="cate":
            article_list=Article.objects.filter(user=user).filter(homeCategory__title=param)
        elif condition=="tag":
            if param:
                article_list=Article.objects.filter(user=user).filter(tags__title=param).order_by('-create_time')
            else:
                article_list = Article.objects.filter(user=user).order_by("-up_count")
        else:
            year,month = param.split("-")
            article_list = Article.objects.filter(user=user).filter(create_time__year=year,create_time__month=month)
    return render(request,"blog/home_site.html",locals())


def article_detail(request,username,article_id):
    article_obj = Article.objects.filter(pk=article_id).first()
    comment_list = Comment.objects.filter(article_id=article_id)
    return render(request,"blog/article_detail.html",{"article_obj":article_obj,"username":username,"comment_list":comment_list})

import json
from django.db.models import F
from django.http import JsonResponse
from django.db import transaction

def up_down(request):
    print(request.POST)

    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))
    user_id = request.user.pk
    print(is_up)

    res = {"state":True,"err":""}
    try:
        #处理事务
        with transaction.atomic():
            obj=ArticleUpDown.objects.create(user_id=user_id,article_id=article_id,is_up=is_up)
            if is_up:
                Article.objects.filter(pk=article_id).update(up_count=F('up_count')+1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F('down_count')+1)
    except Exception as e:
        obj=ArticleUpDown.objects.filter(user_id=user_id,article_id=article_id).first()
        res["state"] = False
        res["err"] = obj.is_up
    return JsonResponse(res)

def comment(request):
    content=request.POST.get("content")
    article_id = request.POST.get("article_id")
    pid = request.POST.get("pid")
    user_id = request.user.pk
    res = {}
    with transaction.atomic():
        if pid:
            obj = Comment.objects.create(content=content,article_id=article_id,user_id=user_id,parent_conment_id=pid)
        else:
            obj = Comment.objects.create(content=content,article_id=article_id,user_id=user_id)
        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)
    res["create_time"] = obj.create_time.strftime("%Y-%m-%d %H:%M")
    res["content"] = obj.content
    return JsonResponse(res)


def backend(request):
    username = request.user
    article_list = Article.objects.filter(user=request.user)
    return render(request,"blog/backend.html",locals())

def add_article(request):
    username = request.user.username
    return render(request,"blog/add_article.html",locals())

def submit(request):
    try:
        title = request.POST.get("title")
        content = request.POST.get("content")
        des = content.split("\r\n")[0]+'...'
        cate = request.POST.get("cate")
        tg = request.POST.get("tag")
        username = request.user

        user = UserInfo.objects.filter(username=username).first()
        blog = Blog.objects.filter(userinfo=user).first()
        category = Category.objects.filter(title=cate,blog=blog).first()
        tag = Tag.objects.filter(title=tg,blog=blog).filter().first()

        if not category:
            category = Category.objects.create(title=cate,blog=blog)
            category.save()
        if not tag:
            tag = Tag(title=tg, blog=blog)
            tag.save()
        article = Article.objects.create(title=title,desc=des,homeCategory=category,user=user)
        article.save()

        articleDetail = ArticleDetail.objects.create(content=content,article=article)
        articleDetail.save()

        articleTag = ArticleTag.objects.create(article=article,tag=tag)
        articleTag.save()
        #article.save()

        return HttpResponse('<h3>提交成功<h3><li><a href="/blog/backend/add_article/">点击返回</a></li>')
    except:
        article.delete()
        return HttpResponse('<h3>提交失败<h3><li><a href="/blog/backend/add_article/">点击返回</a></li>')




def upload_img(request):
    print(request.FILES)
    obj = request.FILES.get("put_img")
    name = obj.name

    from blog import settings
    import os
    path = os.path.join(settings.MEDIA_ROOT,"add_article_img",name)

    f = open(path,"wb")

    for line in obj:
        f.write(line)
    f.close()
    res = {"url":"/media/add_article_img/"+name,
           "error":0
           }
    return HttpResponse(json.dumps(res))

def update_pwd(request):
    return render(request,"blog/update_pwd.html",locals())

def sub_pwd(request):
    username = request.user.username
    old_pwd = request.POST.get("old_pwd")
    new_pwd = request.POST.get("new_pwd")
    re_pwd = request.POST.get("re_pwd")
    user = UserInfo.objects.filter(username=username)
    user = auth.authenticate(username=username, password=old_pwd)
    if user is not None:
        if user.is_active:
            if new_pwd != re_pwd:
                return HttpResponse("</h3>密码前后输入有误</h3>")
            user.set_password(new_pwd)
            user.save()
            return HttpResponse('<h3>修改成功<h3><li><a href="/logout/">重新登陆</a></li>')
    else:
        return HttpResponse("</h3>旧密码密码有误</h3>")