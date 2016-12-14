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


# tags="""TV Shows
# Patterns
# Sports
# Space
# Cars
# Calendars
# Brands
# Black and White
# Basketball
# Art
# Anime
# Animals
# Actresses
# Actors"""
tags="""Cartoon
Actresses
Actors
Monogram
Colorful
Anime
Cats
Singers
Flowers
Funny
Fashion
Animals
Cute
Girls
Love
Pattern
Dogs
Quotes
Pink
Blue
Purple
Winter
Summer
Spring
Autumn
Marvel
Galaxy
Food
Illustrations
Motivational
Movies
TV Shows
Landscape"""

# bundle_id='com.ticktockapps.iphone7-wallhd-10000'
# bundle_id='com.wallpapershdinc.pinkwallpapers-wallhd'
bundle_id='com.ticktockapps.android_girlywallpapers'

tags=[tag for tag in tags.split('\n') if tag!='']
tags=','.join(tags)

# size='1080x1920'
size='1080x1920,2048x2048'

def add_bundle():
    with cd(PROJECT_DIR):
        with cd('src'):
            with prefix(env.active):
                run('python manage.py image_add_bundle_id "{tags}" {bundle_id} "{size}"'.format(tags=tags,bundle_id=bundle_id,size=size))

def test():
    with prefix(env.active):
        run('pip freeze')


def download():
    with cd('/data/project/wallpaperv3/data'):
        run('mv user_image ready_download')
        run('mkdir user_image')
        run('chmod -R 777 user_image')
        run('tar -zcvf user_uploaded.tar.gz ready_download')
        # run('zip -r user_uploaded.zip ready_download')
        
        get(remote_path='user_uploaded.tar.gz',local_path='D:/')
        run('rm user_uploaded.tar.gz')
        run('rm -R ready_download')
        