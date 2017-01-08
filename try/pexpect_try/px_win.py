from pexpect.popen_spawn import PopenSpawn
import sys
#from subprocess import Popen
#import time

child = PopenSpawn('ssh coblan@enjoyst.com')
child.logfile = sys.stdout

child.expect("coblan@enjoyst.com's password:")
child.sendline('he7125158')
child.sendline('ls')
child.expect(pexpect.EOF, timeout=None)