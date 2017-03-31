# encoding:utf-8

"""
后件是运算的关键单元
"""

def getRelatedRules(L,supportData,minConf=0.7):
    """
    @L: 平凡集
    """
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet]
            if (i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
            
    return bigRuleList

def calcConf(freqSet,H,supportData,br1,minConf=0.7):
    prunedH=[]
    for conseq in H: # H 是前面出现过的 高conf 后件列表
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        if conf>=minConf:
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq) # 存放 conf高的 后件
    return prunedH

def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.7):
    m=len(H[0])
    if (len(freqSet)>(m+1)):
        Hmp1=aprioriGen(H,m+1)
        Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf)  # 返回 高conf 后件 列表
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)
            
def aprioriGen(LK,k):
    retList=[]
    lenLk=len(LK)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1=list(LK[i])[:k-2]
            L2=list(LK[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retList.append(LK[i]|LK[j])
    return retList
    