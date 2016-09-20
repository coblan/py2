# import logging  
# FORMAT = "%(message)s"

# logging.basicConfig(format=FORMAT)

# logging.info('hello')
# print('over')

import os
os.chdir(r'd:/')
for i in os.listdir(r'd:/KK22.lnk'):
    print(i.decode('gbk'))