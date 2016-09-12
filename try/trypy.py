# encoding:utf-8

from subprocess import Popen,PIPE

p = Popen(u'dir',stdout=PIPE,shell=True)
stdoutdata, stderrdata = p.communicate()
print(stdoutdata.decode('gbk'))
#for data in stdoutdata:
    #print(data)
#print(p.communicate())
print('over')