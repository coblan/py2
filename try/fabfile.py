
from fabric.api import local, settings,lcd
import wingdbstub
def prepare_deploy():
    #local("dir")
    with settings(warn_only=True):
        lcd(r'D:\coblan\webcode')
        rt =local('git add .',capture=True)
        rt2=local('git commit -m "test fabric"')
    print(rt.stdout)
    print(rt.stderr )


def hello():
    print("Hello world!")