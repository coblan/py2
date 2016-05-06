from pexpect.popen_spawn import PopenSpawn
from pexpect import EOF
import sys
try:
    child = PopenSpawn(u'cmd',cwd=r'D:\coblan\web\first')
    child.logfile = sys.stdout
    child.sendline('git push')
    child.expect(r"Username for 'https://git.oschina.net':")
    child.send('coblan@163.com')
    while True:
        i =child.expect([r'Username for .*\.net','Password for'])
        if i==0:
            child.sendline('coblan@163.com')
        elif i==1:
            child.sendline('he7125158')
except EOF :
    pass