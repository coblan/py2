# encoding:utf-8
import os
from info_util import append
import psutil

#path = '../../data'
def record(path):
    cpu = psutil.cpu_times()
    cpu_csv=os.path.join(path,'cpu.csv')
    append(cpu.__dict__, cpu_csv)