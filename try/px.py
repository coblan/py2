from pexpect.popen_spawn import PopenSpawn
import sys
#from subprocess import Popen
#import time

child = PopenSpawn(r'cmd D:\ve\first\Scripts\activate.bat')
child.logfile = sys.stdout
# child.logfile = sys.stdout
# for line in child.readlines():
    # print(line.decode('gbk'))
# child.send('git pull')
# for line in child.readlines():
    # print(line.decode('gbk'))

#ls=[r'D:',
    #r'cd D:\coblan\web\first',
    #r'D:\ve\first\Scripts\activate.bat',
    #r'python manage.py runserver']

#for cmd in ls:
    #child.sendline(cmd)
    #child.expect('>')

#child.sendline(u'python fabfile.py')
import os
os.chdir(r'D:\coblan\py2\heTools')
child.sendline('cd D:\coblan\py2\heTools')
child.sendline('fab push')
child.expect("Username for 'https://git.oschina.net':")
child.sendline('coblan@163.com')

#child.expect('>')
#child.sendline(r'cd D:\coblan\web\first')
#child.expect('>')
#child.sendline('python manage.py runserver')

#while True:
    #child.expect('.+',timeout=-1)
    #print(child.before)
#child.wait()

#child.kill()
#child.sendline('D:')
#child.expect('\r\n')
#child.sendline(r'cd D:\coblan\web\first')
#child.expect('\r\n')
#child.sendline(r'D:\ve\first\Scripts\activate.bat')
#child.expect('\r\n')
#child.sendline(r'python manage.py runserver')

#Popen('cmd /k start python manage.py runserver')
#while True:
    #time.sleep(10)
#p.wait()
#while True:
    #child.expect('\r\n')

    
# child.expect('git')
# child.expect('>')
# child.expect('>')
# child.sendline('dir')
# child.expect('>')
