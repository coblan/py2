# encoding:utf-8
import os
from info_util import append
import psutil
import re
#path = '../../data'
def record(path):
    disk_part_list = psutil.disk_partitions()
    for part in disk_part_list:
        usag=psutil.disk_usage(part.mountpoint)
        name = re.sub('\W','_',part.device)
        fl_name =os.path.join(path,'disk_usage_%s.csv'%name)
        append(usag.__dict__,fl_name)

if __name__=='__main__':
    record('jj')