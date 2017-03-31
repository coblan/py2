from __future__ import division
from fp_growth import find_frequent_itemsets


def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

freq=[]

for itemset in find_frequent_itemsets(loadSimpDat(),3):
    freq.append(sorted(itemset))

print('-'*30)

def get_co(single_item):
    has_item_set = filter(lambda x:single_item in x,freq)
    all_ele=frozenset(reduce(lambda x,y:x+y,has_item_set))
    sup_item=len(has_item_set)/len(freq)
    
    for sub_set in get_sub_set(single_item,all_ele):
        print(sub_set)
        

def get_sub_set(ele,all_ele):
    for sub_set in power_set(all_ele):
        if ele in sub_set:
            yield sub_set

def get_sup(sub_set,comp_set_list):
    count=0
    for com_set in comp_set_list:
        if sub_set.issubset(com_set):
            count+=1
    return count

        
get_co('x')

