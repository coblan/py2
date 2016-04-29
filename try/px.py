from pexpect.popen_spawn import PopenSpawn
import sys

child = PopenSpawn(u'cmd')
child.logfile = sys.stdout
# child.logfile = sys.stdout
# for line in child.readlines():
    # print(line.decode('gbk'))
# child.send('git pull')
# for line in child.readlines():
    # print(line.decode('gbk'))
    
child.expect('>')
child.sendline('D:')
child.expect('>')
child.sendline(r'cd D:\work\production_tracking\src')
child.expect('>')
child.sendline(r'D:\ve\pts\Scripts\activate.bat')
child.expect('>')
child.sendline(r'python manage.py runserver')
child.expect_loop(searcher, timeout=-1, searchwindowsize=-1)
# child.expect('git')
# child.expect('>')
# child.expect('>')
# child.sendline('dir')
# child.expect('>')
