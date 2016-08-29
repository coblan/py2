from __future__ import print_function
from difflib import ndiff

with open('local_try.py') as f:
    aa = f.readlines()

with open('loop_test.py') as f:
    bb = f.readlines()
a=['abcd','bcde']
b=['abcd','bffe']
for i in ndiff(aa,bb):
    print(i,end='')