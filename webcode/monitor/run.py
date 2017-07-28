

import requests
import fl_tar
import shutil
from node.info import cpu
from node.info import memory
from node.info import disk

name='node1'

path='data'
cpu.record(path)
memory.record(path)
disk.record(path)

fl_tar.tgz('data')
files = {'file': open('data.tar.gz', 'rb')}

rt = requests.post('http://localhost:8000/upload?node=%s'%name,files=files)
shutil.rmtree('data')
print(rt.content)
