
from fabric.api import local, settings,lcd,env,cd,get,put,prefix
from fabric.api import run

import wingdbstub


print('into herer')

env.hosts = ['coblan@enjoyst.com']
env.passwords={'coblan@enjoyst.com:22':'he7125158'}
env.always_use_pty =False

#env.key_filename =r'D:\home\.ssh\id_rsa'

def first():
    with lcd(r'D:\coblan\web\first'):
        with prefix(r'D:\ve\first\Scripts\activate.bat'):
            local('python manage.py collectstatic --noinput')
            #local('pip list')
            local('git add .')
            local('git commit -m "auto commit"')
            local('git push')
    with cd('/pypro/first/first'):
        run('git pull')
        with cd('../run'):
            run('touch first.reload')
    
env.prompts={"https://git.oschina.net': ": 'coblan@163.com',}

def push():
    # warn_only=True,prompts={"https://git.oschina.net':": 'coblan@163.com\n'}
    with settings():
        with lcd(r'D:\coblan\web\first'):
            print('[start] ========push first')
            _auto_push()
            print('[success] push first')
        
        with lcd(r'D:\coblan\py2'):
            print('[start]========= push py2')
            _auto_push()
            print('[success] push py2')
        
        with lcd(r'D:\coblan\webcode'):
            print('[start]======= push webcode')
            _auto_push()
            print('[success] push webcode')
        
        with lcd(r'D:\coblan\web\insight'):
            print('[start]======= push insight')
            _auto_push() 
            print('[success] push insight')

def _auto_push():
    rt = local('git status',capture=True)
    if not rt.stdout.endswith('nothing to commit, working directory clean'):
        local('git add .',capture=True)
        local('git commit -m "auto commit"',capture=True)
    local('git push')

def pull():
    ls=[r'/cygdrive/d/coblan/web/first',
        r'/cygdrive/d/coblan/py2',
        r'/cygdrive/d/coblan/webcode',
        r'/cygdrive/d/coblan/web/insight']
    for path in ls:
        with lcd(path):
            print('==='+path)
            local('git pull')

    
