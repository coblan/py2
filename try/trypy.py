# encoding:utf-8

#from subprocess import Popen,PIPE

##p = Popen(u'dir',stdout=PIPE,shell=True)
##stdoutdata, stderrdata = p.communicate()
##print(stdoutdata.decode('gbk'))
###for data in stdoutdata:
    ###print(data)
###print(p.communicate())
##print('over')
#import os
#print(os.getcwd())
#p =Popen('fab tt',stdout=PIPE,stdin=PIPE)
## while p.poll():
#stdoutdata, stderrdata = p.communicate()
#print(stdoutdata)

import time

def say(tm=time.time()):
    print(tm)

def say2(tm= lambda:time.time()):
    print(tm())
    
def test():
    while True:
        time.sleep(1)
        say()
        say2()

if __name__=='__main__':
    test()
        

