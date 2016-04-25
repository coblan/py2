# -*- encoding:utf-8 -*-
import time
from xml.sax import ContentHandler,parseString
import re
class MyXml(ContentHandler):
    def __init__(self):
        self.currentTag = ''
        self.toUserName = ''
    def startElement(self, tag, attributes):
        self.currentTag = tag
    
    def endElement(self, tag):
        self.currentTag = ''   
    
    def characters(self, content):
        if self.currentTag == 'original':
            self.original=content

import xml.etree.cElementTree as ET

    
import requests

#url='http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=techyyy.com'
#rt=requests.get(url)
#ss=rt.text
#ss=ss.replace('gb2312', 'utf-8')

#handel=MyXml()

#parseString(ss,handel)
#print handel.original

def check(name):
    url='http://panda.www.net.cn/cgi-bin/check.cgi?area_domain='+name
    #url = 'http://alidns.aliyuncs.com/?Action=DescribeDomainWhoisInfo&DomainName='+name
    rt=requests.get(url)
    ss=rt.text
    ss=ss.replace('gb2312', 'utf-8')
    handel=MyXml()
    
    parseString(ss,handel)
    if handel.original.startswith('210') :
        print(name)
        
def letter():
    #ls='abcdefghijklmnopkrstuvwxyz'
    #for i in ls:
        #for j in ls:
            #for k in ls:
                #yield i+j+k
    #for i in ls:
        #yield i+i
    #with open('english.txt') as f:
        #en=f.read()
        #en_list=en.split('\n')
        #for i in en_list:
            #yield i
    with open(ur'D:\360安全浏览器下载\english-words-master\words.txt') as f:
        en=f.read()
        en_list=en.split('\n')
        for i in en_list:
            if re.match('^[A-Za-z]+$',i):
                yield i
    
def main():
    pre=''
    cnt=0
    for after in letter():
        #if after<'lw':
            #continue
        #if after>'tie':
            #break
        if len(after)!=4:
            continue
        #if after[0]<'p':
            #continue
        time.sleep(1)
        name=after+pre+'.com'
        check(name)
        cnt+=1
        if cnt%10==2:
            print('----------'+str(cnt)+name)
            

if __name__=='__main__':
    main()