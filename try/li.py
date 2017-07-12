with open(r'd:/try/jj/OOG104_Resource.csv','rb') as f:
    aa= f.read()
    uuaa=aa.decode('gbk')
    print(aa.decode('gbk'))
    with open(r'd:/try/jj/OOG104_Resource_utf_8.csv','wb') as f2:
        f2.write(uuaa.encode('utf-8'))