# -*- encoding:utf-8 -*-

"""
未完成
"""
import random
def random_number():
    rand=random.randint(10000,99999)%10000
    return rand


def guss(rand,cnt):
    print('inter number')
    num=raw_input()
    mt=matched(rand,num)
    cnt+=1
    if mt<4:
        print '*'*mt
        return guss(rand,cnt)
    else:
        print '*'*4
        print 'you got it ,%s'%cnt

def matched(rand,num):
    if rand==num:
        return 4
    else:
        return 0

if __name__=='__main__':
    rand=random_number()
    cnt=0
    guss(rand,cnt)