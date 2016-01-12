def tt():
    jk=12
    locals()['jk']=34
    return jk

print(tt())