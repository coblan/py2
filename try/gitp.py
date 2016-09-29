from subprocess import Popen,PIPE
import os
os.chdir(r'D:\coblan\web\first')
p = Popen('git status',shell=True,stdout=PIPE)

while p.
info,err = p.communicate()
print(info.decode('gbk'))