# -*-encoding:utf-8 -*-

import sync_code

dc={
    'dirs':[[ur'D:\try\中文测试',ur'D:\try\test'],],
    'include_file':lambda src,dst: not src.endswith('.pyc')
    }

sync_code.sync(dc)