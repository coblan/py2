from pexpect.popen_spawn import PopenSpawn
import sys


child = PopenSpawn(u'ssh coblan@115.29.99.226')
child.logfile = sys.stdout
while True:
    i=child.expect(['password:', 'continue connecting (yes/no)?'])
    if i == 0 :
        ssh.sendline('he7125158')
        break
    elif i == 1:
        ssh.sendline('yes\n')
        ssh.expect('password: ')
        ssh.sendline('he7125158') 
        break
child.expect('\r\n')
child.sendline('ls')