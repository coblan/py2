
from fabric.api import local, settings,lcd,env,cd,get,put
from fabric.api import run

env.hosts = ['coblan@enjoyst.com']
env.passwords={'coblan@enjoyst.com:22':'he7125158'}

def first():
    with lcd(r'D:\coblan\web\first'):
        local(r'D:\ve\first\Scripts\activate.bat')
        local('git add .')
        local('git commit -m "auto commit"')
        local('git push')
    with cd('/pypro/first/first'):
        run('git pull')
        with cd('../run'):
            run('touch first.reload')
    
import wingdbstub

def push():
    with settings(warn_only=True):
        with lcd(r'D:\coblan\web\first'):
            _auto_push()
        
        with lcd(r'D:\coblan\py2'):
            _auto_push()
        
        with lcd(r'D:\coblan\webcode'):
            _auto_push()

def _auto_push():
    rt = local('git status',capture=True)
    if not rt.stdout.endswith('nothing to commit, working directory clean'):
        local('git add .')
        local('git commit -m "auto commit"')
    rt=local('git push',capture=True)  
    print(rt)
