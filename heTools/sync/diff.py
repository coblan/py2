from __future__ import print_function
from difflib import ndiff,HtmlDiff

with open('local_try.py') as f:
    aa = f.readlines()

with open('loop_test.py') as f:
    bb = f.readlines()
a=['abcd','bcde']
b=['abcd','bffe']
# for i in ndiff(aa,bb):
    # print(i,end='')

print( HtmlDiff().make_file(aa,bb) )
def get_table():
    
    return HtmlDiff().make_file(aa,bb)