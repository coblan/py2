# encoding:utf-8
import os
from info_util import append

import psutil

mem = psutil.virtual_memory()

path = '../../data'

csv_path=os.path.join(path,'memory.csv')
append(mem.__dict__, csv_path)