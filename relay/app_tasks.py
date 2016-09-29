from tasks import add
import time
rt=add.delay(4,4)
print(rt.backend)
#while not rt.ready():
    #time.sleep(1)
print(rt.get())