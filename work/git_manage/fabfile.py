# encoding=utf8
'''
Created on 2016-08-18

@author: jingyang <jingyang@nexa-corp.com>

Usage:
    fab staging add_bundle
    fab staging download
'''
from fabric.api import local
from fabric.context_managers import lcd, cd,prefix
from fabric.operations import put, run, get
from fabric.state import env
import re,os


#import sys
#sys.path.append('D:\coblan\py2')
#import wingdbstub



PROJECT_NAME = "wallpaperv3"
PROJECT_DIR = "/data/project/wallpaperv3/"  # project dir on server

reposits=[
    {'path':r'D:\coblan\web\insight','with_helpers':True,'src':'git@github.com:coblan/insight.git'},
    {'path':r'D:\coblan\web\first','with_helpers':True},
    {'path':r'D:\work\insight01','with_helpers':True},
    #{'path':r'D:\work\wx_case01','with_helpers':True},
    {'path':r'D:\coblan\webcode','with_helpers':False},
    {'path':r'D:\coblan\py2','with_helpers':False},
    {'path':r'D:\coblan\py3','with_helpers':False},
    # {'path':r'D:\coblan\py3','with_helpers':False},
    {'path':r'D:\coblan\web\yunwei','with_helpers':False},
    #{'path':r'D:\work\xiche','with_helpers':True}
    {'path':r'D:\work\mywallpaper','with_helpers':False},
    
    # {'path':r'D:\work\liucheng','with_helpers':True},
    {'path':r'D:\work\uihome','with_helpers':True},
    {'path':r'D:\work\liantang','with_helpers':True},
    {'path':r'D:\work\zhaoxiang','with_helpers':True},
    {'path':r'D:\work\xuncha','with_helpers':True},
]

def insight():
    env['target']=[{'path':r'D:\coblan\web\insight','with_helpers':True,'src':'git@github.com:coblan/insight.git'}]

def xiche():
    env['target']=[{'path':r'D:\work\xiche','with_helpers':True}]

def sim():
    env['target']=[{'path':r'D:\try\geodjango','with_helpers':False,'src':'git@github.com:coblan/geodjango.git'}]


def pull():
    if env.get('target'):
        for repo in env.get('target'):
            pull_item(repo)
    else:
        for repo in reposits:
            pull_item(repo)
            
def pull_item(item):
    print('')
    print('start pull %s'%item.get('path'))
    print('='*20)
    
    if not os.path.exists(item.get('path')):
        clone_item(item)
    else:
        with lcd(item.get('path')):
            if item.get('src'):
                local('git remote set-url origin %(src)s'%item)
            local('git pull')
            
            print('[submodule update]')
            print('-'*20)
            local('git submodule update --merge')            
            # if item.get('with_helpers'):
                # print('[helpers]')
                # print('-'*20)
                # with lcd('src/helpers'):
                    # local('git checkout master')
                # local('git submodule update --merge')
                # with lcd('src/helpers'):
                    # local('git pull')

def clone_item(item):
    path = item.get('path')
    par = os.path.dirname(path)
    if not os.path.exists(par):
        os.makedirs(par)
    with lcd(par):
        local('git clone %(src)s'%item)
        
    with lcd(path):
        print('[submodule update]')
        print('-'*20)       
        local('git submodule init')
        local('git submodule update --merge')

"""
helpers起作用的是pull，不是update，不管是否更新 submodule的指针，在下次fab pull时，都会使helpers指向最新。所以没有必要，在push时，让所有库的helpers指针指向最新。
"""

def push():
    if env.get('target'):
        for repo in env.get('target'):
            push_item(repo)  
    else:
        for repo in reposits:
            push_item(repo)

def push_item(item):
    print('')
    print('[push] %s'%item.get('path'))
    print('='*20)
    if not os.path.exists(item.get('path')):
        print('%(path)s not exist. Quit push!'%item)
        return
    
    with lcd(item.get('path')):
        status = local('git status',capture=True)
        print(status)
        if re.search('nothing to commit',status,re.S):
            return
        else:
            if item.get('with_helpers'):
                print('[helpers]')
                print('-'*20)
                with lcd('src/helpers'):
                    status=local('git status',capture=True)
                    if re.search('nothing to commit',status):
                        pass
                    else:
                        local('git checkout master') # may not need
                        local('git add .')
                        local('git commit -m "auto commit"')
                        local('git push')
            print('[do push]')
            print('-'*20)
            local('git add .')
            local('git commit -m "auto commit"')
            local('git push')
  
    


# def staging():
    # env.user = "develop"
    # env.hosts = ["216.12.198.100"]
    # env.key_filename =r'D:\home\myopenssh'
    # env.active='source /data/project/wallpaperv3/env/bin/activate'


# def prod():
    # env.user = "develop"
    # env.hosts = ["173.193.163.144"]
    # env.key_filename =r'D:\home\myopenssh'
    # env.active='source /data/project/wallpaperv3/venv/bin/activate'    




# def add_bundle():
    # with lcd(PROJECT_DIR):
        # with cd('src'):
            # with prefix(env.active):
                # run('python manage.py image_add_bundle_id "{tags}" {bundle_id} "{size}"'.format(tags=tags,bundle_id=bundle_id,size=size))

# def test():
    # with prefix(env.active):
        # run('pip freeze')


# def download():
    # with cd('/data/project/wallpaperv3/data'):
        # run('mv user_image ready_download')
        # run('mkdir user_image')
        # run('chmod -R 777 user_image')
        # run('tar -zcvf user_uploaded.tar.gz ready_download')
        # # run('zip -r user_uploaded.zip ready_download')
        
        # get(remote_path='user_uploaded.tar.gz',local_path='D:/')
        # run('rm user_uploaded.tar.gz')
        # run('rm -R ready_download')


