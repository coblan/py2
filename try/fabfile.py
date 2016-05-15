# -*- encoding:utf-8 -*-

from fabric.api import local, settings,lcd,env,cd,get,put
from fabric.api import run
import wingdbstub

env.hosts = ['coblan@enjoyst.com']
env.passwords={'coblan@enjoyst.com:22':'he7125158'}

prompts={"Username for 'https://git.oschina.net':": 'coblan@163.com','Password':'he7125158','show me':'wowo\n'}

def prepare_deploy():
    #local("dir")
    with settings(warn_only=True,prompts=prompts):
        tt()
        with lcd(r'D:\coblan\webcode'):
            local('git add .',capture=True)
            #rt2=local('git commit -m "test fabric"')
            rt2= local('git push',capture=True)
    print(rt2.stdout)
    print(rt.stderr )


def host_type():
    with cd('/pypro/first/'):
        run('uname -s')
        run('ls')
        get(remote_path='/pypro/first/first/',local_path='D:/try/aliyun/first/%(dirname)s',use_sudo=True)



def put_python():
    put('mytar.py','mytar.py')
    run('python mytar.py /pypro/first/first/')
    get(remote_path='your.tar.gz',local_path='D:/try/aliyun/')

def tt():
    aa=raw_input('show me')
    print('hello %s'%aa)
    
def hello():
    print("Hello world!")

def dj():
    with lcd(r'D:\coblan\web\first'):
        local(r'D:\ve\first\Scripts\activate.bat')
        local(r'python manage.py runserver')
    
        