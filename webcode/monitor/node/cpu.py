# encoding:utf-8
import os
from ..csv_util import append
import logging
log=logging.getLogger('core')

import psutil

mem = psutil.virtual_memory()

path = '../../data'

cpu_csv=os.path.join(path,'cpu/cpu.csv')
append(mem.__dict__, cpu_csv)