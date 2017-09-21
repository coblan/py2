# encoding:utf-8

with open(r"C:\Users\heyulin\Desktop\pts.txt") as f:
    ss = f.read()
    ls = ss.split('\n')
    ls=[x.split(':') for x in ls]
    
    with open(r"C:\Users\heyulin\Desktop\pts_pswd.txt") as f2:
        zz = f2.read()
        pswd=zz.split('\n')
        pswd=[x.split(':') for x in pswd if x]
        pswd_dc=dict(pswd)
    
    yy=[[x[0],x[1],pswd_dc[x[0]] ] for x in ls if len(
        x)==2]
    print(yy)
    outstr_ls=[]
    outstr="username,email,password\n"
    for row in yy:
        outstr_ls.append(','.join(row))
    outstr +='\n'.join(outstr_ls)
    with open(r"C:\Users\heyulin\Desktop\pts_pswd.csv",'wb') as f3:
        f3.write(outstr)