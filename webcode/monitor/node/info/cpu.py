# encoding:utf-8

import logging
log=logging.getLogger('core')

import psutil

mem = psutil.virtual_memory()

print(mem)