#-*- encoding:utf8 -*-
from subprocess import Popen
import os
def open_with_os(path):
    Popen( ('cmd /C start "title" "%s"'%os.path.normpath(path)),shell=True)  # 添加shell=True才不会 闪现黑框

