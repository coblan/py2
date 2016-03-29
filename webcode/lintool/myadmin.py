# -*- encoding:utf8 -*-
from django.shortcuts import render
import json
from django.db import connection
import sys  
import StringIO  
from django.contrib.auth.models import User
from django.http import HttpResponse  
from django.contrib import auth 

def admin(request):  
    # admin_user = request.session.get('admin_user')

    if request.method=='GET':
        cmd =request.GET.get('cmd')
        if cmd:
            result = manage_cmd(cmd)
            return HttpResponse(result)
        else:
            return render(request,'lintool/admin.html')
    elif request.method=='POST':
        dc= json.loads(request.body)
        cmd= dc.pop('cmd')
        if  cmd=='remote_cmd':   
            command=dc.get('value')
            #重定向标准输出重定向到内存的字符串缓冲(由StringIO模块提供)  
            #saveout = sys.stdout  
            #log_out = StringIO.StringIO()    
            #sys.stdout = log_out   
            ##利用django提供的命令行工具来执行“manage.py syncdb”  
            #from django.core.management import execute_from_command_line  
            #execute_from_command_line(["manage.py", command])  
            ##获得“manage.py syncdb”的执行输出结果，并展示在页面  
            #result = log_out.getvalue()  
            #sys.stdout = saveout
            result = manage_cmd(command)
            response_data={
                'status':'success',
                'stdout': result
            }
            
        elif cmd =='migrate_model':
            appid=dc.get('appid')
            name=dc.get('name')
            cursor = connection.cursor()
            cursor.execute("UPDATE django_migrations SET name = '%s' WHERE id = %s"%(name,appid))
            response_data={
                'status':'success',
            } 
        elif cmd =='get_migration_model':
            rows= my_custom_sql()
            for row in rows:
                row['applied']=row['applied'].strftime('%Y/%m/%d %H:%M:%S')  
            response_data={
                'status':'success',
                'rows':rows
            }
        elif cmd=='createsuperuser':
            user = User.objects.create_user(dc.get('name'),password=dc.get('pswd'))
            user.is_staff=1
            user.is_superuser=1
            user.save()
            
            response_data={
                'status':'success',
            }            
        elif cmd=='login':
            user= dc.get('user')
            if user.get('name')=='root' and user.get('pswd')=='676767':
                request.session['admin_user']=user.get('name')
                response_data={
                    'status':'success'
                }
            else:
                response_data={'status':'error'}
        elif cmd=='logout':
            request.session.pop('admin_user')
            response_data={'status':'success'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")  

def manage_cmd(command):
    #重定向标准输出重定向到内存的字符串缓冲(由StringIO模块提供)  
    saveout = sys.stdout  
    log_out = StringIO.StringIO()    
    sys.stdout = log_out   
    #利用django提供的命令行工具来执行“manage.py syncdb”  
    from django.core.management import execute_from_command_line  
    execute_from_command_line(["manage.py", command])  
    #获得“manage.py syncdb”的执行输出结果，并展示在页面  
    result = log_out.getvalue()  
    sys.stdout = saveout  
    result = result.replace("\n","<br/>"),
    return result

def my_custom_sql():
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM django_migrations")
    rows = dictfetchall(cursor)
    return rows

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


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
            'is_login':is_login
        }
        return render(request,'lintool/login.html',context=dc)
    elif request.method=='POST':
        dc= json.loads(request.body)
        cmd=dc.get('cmd')
        if cmd=='logout':
            auth.logout(request)
            response_data={
                'status':'success'
                }
        else:
            username=dc.get('name','')  
            password=dc.get('password','')  
            user= auth.authenticate(username=username,password=password)
            if user and user.is_active:  
                auth.login(request, user)
                response_data={
                    'status':'success'
                }
                 
            else:
                response_data={
                    'status':'error',
                }
        return HttpResponse(json.dumps(response_data), content_type="application/json") 
        