# -*- encoding:utf-8 -*-

from fabric.api import local, settings,lcd,env,cd,get,put,prefix
from fabric.api import run
from datetime import datetime
# import wingdbstub


# env.hosts = ['coblan@enjoyst.com']
# env.passwords={'coblan@enjoyst.com:22':'he7125158'}

prompts={"Username for 'https://git.oschina.net':": 'coblan@163.com','Password':'he7125158','show me':'wowo\n'}

def stm(syst):
    if syst=='pts':
        env.hosts=['develop@pts.stm.com']
        env.passwords={'develop@pts.stm.com:22':'kibi00'}
        
        env.pro_path='/var/project/production_tracking'
        env.pre='pts'
        env.db='db_pts'
        env.touch = '/var/run/uwsgi/production_tracking.reload'


def moki(syst):
    if syst=='pts':
        env.hosts=['develop@pts.mokitech.com']
        env.passwords={'develop@pts.mokitech.com:22':'kibi00'}
        
        env.pro_path='/var/project/production_tracking'
        env.pre='pts'
        env.db='db_pts'
        env.touch = '/var/run/uwsgi/production_tracking.reload'

  

def backup():
    now= datetime.now().strftime('%Y%m%d_%H%M')
    with settings(warn_only=True):
        run('mkdir backup')
    with cd('backup'):
        put('mytar.py','mytar.py')
        run('python mytar.py tar  {pro_path} {target}'.format(pro_path=env.pro_path,
                    target='{prefix}{time}'.format(prefix=env.pre,time=now)))
        
        run('mysqldump -u{db} -p{db} {db}>{db}_{now}.sql'.format(now=now,db=env.db))


def fast():
    with cd('backup'):
        put('mytar.py','mytar.py')
        run('python mytar.py untar {syst} {pro_path}'.format(syst=env.pre, pro_path=env.pro_path))  # syst的目的是在back目录中查找最新的，prefix为syst的tar.gz文件
        run('touch {touch}'.format(touch=env.touch))
        

# def fastdb():
    # with cd('backup'):
        # run('mysql  -uroot -proot {db} < {new_db}'.format(db=env.db,new_db=))

def deploy():
    with cd(env.pro_path):
        with cd('deploy'):
            run('. deploy.sh')
            
        # with cd('src'), prefix('. ../venv/bin/activate'):
                # run('python manage.py migrate')
                
        run('touch {touch}'.format(touch=env.touch))
            
        

# def prepare_deploy():
    # #local("dir")
    # with settings(warn_only=True,prompts=prompts):
        # tt()
        # with lcd(r'D:\coblan\webcode'):
            # local('git add .',capture=True)
            # #rt2=local('git commit -m "test fabric"')
            # rt2= local('git push',capture=True)
    # print(rt2.stdout)
    # print(rt.stderr )


# def host_type():
    # with cd('/pypro/first/'):
        # run('uname -s')
        # run('ls')
        # get(remote_path='/pypro/first/first/',local_path='D:/try/aliyun/first/%(dirname)s',use_sudo=True)



# def put_python():
    # put('mytar.py','mytar.py')
    # run('python mytar.py /pypro/first/first/')
    # get(remote_path='your.tar.gz',local_path='D:/try/aliyun/')


    
# def hello():
    # print("Hello world!")

# def dj():
    # with lcd(r'D:\coblan\web\first'):
        # local(r'D:\ve\first\Scripts\activate.bat')
        # local(r'python manage.py runserver')
    
        