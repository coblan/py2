# -*- encoding:utf8 -*-
from __future__ import unicode_literals
entrys=[
    {'src':r"D:\try\中文测试",
     'dst':r"D:\try\test",
     'include_file':lambda src,dst: not src.endswith('pyc'),
     'include_dir':lambda dir: dir!='simPage'
     },
]


