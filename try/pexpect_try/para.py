import paramiko
import time
s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect(hostname='api.uacar.cn', username='root', password='Zhaozijian@123')
stdin, stdout, stderr = s.exec_command('ls -al')
#sin, sout, serr = stdin.readlines(), stdout.readlines(), stderr.readlines()
sout=stdout.readlines()
for line in sout:
    print(line)

stdin, stdout, stderr = s.exec_command( 'mysqldump -u root -p 123456789 xiche>xiche_{stamp}.sql'.format(stamp= int(time.time())) )
stdin.write('123456789')
stdin.flush()
sout=stdout.readlines()
for line in sout:
    print(line)

