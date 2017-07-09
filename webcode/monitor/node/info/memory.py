# encoding:utf-8
import os
from info_util import append

import psutil



#path = '../../data'

def record(path):
    mem = psutil.virtual_memory()
    csv_path=os.path.join(path,'memory.csv')
    append(mem.__dict__, csv_path)    
