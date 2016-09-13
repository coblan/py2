# encoding=utf8
'''
Created on 2016-08-18

@author: jingyang <jingyang@nexa-corp.com>

Usage:
    fab staging deploy
    fab prod deploy
'''
from fabric.api import local
from fabric.context_managers import lcd, cd,prefix
from fabric.operations import put, run
from fabric.state import env


PROJECT_NAME = "wallpaperv3"
PROJECT_DIR = "/data/project/wallpaperv3/"  # project dir on server


def staging():
    env.user = "develop"
    env.hosts = ["216.12.198.100"]
    env.key_filename =r'D:\home\myopenssh'
    env.active='source /data/project/wallpaperv3/env/bin/activate'


def prod():
    env.user = "develop"
    env.hosts = ["173.193.163.144"]
    env.key_filename =r'D:\home\myopenssh'
    env.active='source /data/project/wallpaperv3/venv/bin/activate'    


tags="""TV Shows
Patterns
Sports
Space
Soccer
Pink
Quotes
Singers
Nature
Movies
Motivational
Monogram
Love
Landscapes
Illustrations
Girls
Games
Funny
Food
Flowers
Fashion
Dogs
Cute
Colors
Celebrities
Cats
Cartoons
Cars
Calendars
Brands
Black and White
Basketball
Art
Anime
Animals
Actresses
Actors"""
tags=[tag for tag in tags.split('\n') if tag!='']
tags=','.join(tags)
bundle_id='com.ticktockapps.iphone7-wallhd-10000'
size='1080x1920'

def add_bundle():
    with cd(PROJECT_DIR):
        with cd('src'):
            with prefix(env.active):
                run('python manage.py image_add_bundle_id "{tags}" {bundle_id} "{size}"'.format(tags=tags,bundle_id=bundle_id,size=size))

def test():
    with prefix(env.active):
        run('pip freeze')