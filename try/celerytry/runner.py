from tasks import add
import time
rt=add.delay(4, 4)
while not rt.ready():
    time.sleep(1)

print( rt.get() )
print(rt.traceback)
print(rt.id)
    