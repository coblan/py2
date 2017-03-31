from __future__ import division
from fp_growth import find_frequent_itemsets
from getRelatedRule import getRelatedRules
import getRelatedRule

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],]
    return simpDat

data2=[[1,3,4],
       [2,3,5],
       [1,2,3,5],
       [2,5]]




freq=[]
supportData={}

for itemset,conf in find_frequent_itemsets(loadSimpDat(),4, include_support=True):
    freq.append(frozenset(itemset))
    supportData[frozenset(itemset)]=conf*1.0

freq = sorted(freq,key=lambda x:len(x))


L=[]
crt = 0
for item in freq:
    if len(item) > crt:
        crt=len(item)
        tmp=[]
        L.append(tmp)
    tmp.append(item)

    
        
for k in freq:
    print(k,'conf:',supportData[k])
    
print('-'*30)

for k in L:
    print(k)

print('-'*30)


rules = getRelatedRules(L, supportData,minConf=0.5)



