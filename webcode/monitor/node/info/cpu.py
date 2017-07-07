# encoding:utf-8
import os
from info_util import append
import psutil

cpu = psutil.cpu_times()

path = '../../data'

cpu_csv=os.path.join(path,'cpu.csv')
append(cpu.__dict__, cpu_csv)