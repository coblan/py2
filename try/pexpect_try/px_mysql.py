import pexpect

import time
import sys
#child  = pexpect.spawn('ssh coblan@enjoyst.com')
#child.logfile = sys.stdout 
#child.expect("coblan@enjoyst.com's password:")
#child.sendline('he7125158')
#child.sendline('ls')
#child.expect(pexpect.EOF, timeout=None)

child = pexpect.spawn('mysqldump -u root -p xiche>xiche_{stamp}.sql'.format(stamp= int(time.time()))) 
child.logfile = sys.stdout
#child.expect(" Login password for 'root':")
#child.sendline('Zhaozijian@123')
child.expect('Enter password:')
child.sendline('123456789')
child.expect(pexpect.EOF)
child.close()


#print child.before

