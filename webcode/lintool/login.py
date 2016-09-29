# -*- encoding:utf8 -*-
"""
当前login模块的使用
==============================
1.在主url中设置登陆的url, example:
  url(r'^accounts/login/$','lintool.login.login')
  # 因为@login_required默认跳到r'^accounts/login/$'
  
2.在使用views中引入装饰器
  from django.contrib.auth.decorators import login_required
  
3.在views函数上带上装饰器
@login_required
def qiangda(request):
    return render(request,'nianhui/qiang_da.html')

自定义login后台
=================================
原理：现实一个auth后台，django在使用auth.authenticate()认证时，会依次调用 AUTHENTICATION_BACKENDS列表中的
BACKENDS,只要有一个BACKENDS返回了user，用户就能登陆。BACKENDS可以接受各种关键字参数

步骤
-------------------
1.setting.py 里面设置变量
AUTHENTICATION_BACKENDS= ['django.contrib.auth.backends.ModelBackend',
                          'lintool.weixin.auth.MyBackend']
                          
2.
#  实现后台
必须实现authenticate,get_user两个函数，
authenticate必须返回一个user对象(User数据库对象)

from django.contrib.auth.models import User
from lintool.struct import get_or_none

class MyBackend(object):
    def authenticate(self, token):
        if token == '778899':
            user = get_or_none(User,username='coblan')
            return user
        else:
            return None
    def get_user(self, user_id):
       try:
         return User.objects.get(pk=user_id)
       except User.DoesNotExist:
           return None

# 另外一种 authenticate，顺道，在User数据库中创建用户
def authenticate(self, token):   
    login_valid = (settings.ADMIN_LOGIN == username)
    pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
    if login_valid and pwd_valid:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Create a new user. Note that we can set password
            # to anything, because it won't be checked; the password
            # from settings.py will.
            user = User(username=username, password='get from settings.py')
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user
    return None

3. 认证函数
通过不同的关键字参数，来获取user，只要有一个获取到了，就用auth.login()登陆

def do_login(name,password,request):
    user= auth.authenticate(username=name,password=password)
    if user and user.is_active:  
        auth.login(request, user)
        return {'status':'success'}
    user = auth.authenticate(token=name)
    if user:
        auth.login(request, user)
        return {'status':'success'}
    else:
        return {'status':'fail','msg':'user or password not match'} 
"""

from django.shortcuts import render
import json
from django.contrib import auth 
from django.contrib.auth.models import User
from struct import jsonpost,require_request
from django.core.urlresolvers import reverse
from functools import partial
import re

json_proc= partial(jsonpost,scope=globals())
def login(request):
    if request.method=='GET':
        next_url=request.GET.get('next')
        if not next_url:
            next_url='/'
        if request.user.is_authenticated():
            is_login='true'
        else:
            is_login='false'
        dc={
            'next':next_url,
            'is_login':is_login,
            'registe':reverse('registe')
        }
        return render(request,'lintool/login.html',context=dc)
        
    elif request.method=='POST':
        return json_proc(request)

def regist_user(request):
    if request.method=='GET':
        dc={
            'login_url':reverse('login')
        }
        return render(request,'lintool/regist.html',context=dc)
    elif request.method=='POST':
        return json_proc(request)    

@require_request
def logout(request):
    auth.logout(request)
    return {'status':'success'}

@require_request
def do_login(name,password,request):
    if re.search('@',name):
        try:
            user = User.objects.get(email=name)
            name = user.username
        except User.DoesNotExist:
            return {'status':'fail','msg':'email not exist'}
    user= auth.authenticate(username=name,password=password)
    if user and user.is_active:  
        auth.login(request, user)
        return {'status':'success'}
    user = auth.authenticate(token=name)
    if user and user.is_active:
        auth.login(request, user)
        return {'status':'success'}
    else:
        return {'status':'fail','msg':'user or password not match'}  

def registe(username,password):
    try:
        User.objects.get(username=username)
        return {'status':'fail','msg':'username has exist'}
    except User.DoesNotExist:
        user=User.objects.create_user(username=username,password=password)
        user.is_active=True
        user.save()
        return {'status':'success'}