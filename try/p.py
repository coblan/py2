
from subprocess import Popen,PIPE
import time


p=Popen('cmd /c start python',shell=True ,stdout=PIPE,stdin=PIPE )
# p.communicate('where python')
# time.sleep(3)
# p.communicate('where python')
# p.communicate('print("hello")')
# time.sleep(3)
print(p.communicate())
p.communicate('print("hello")')
print(p.communicate())
