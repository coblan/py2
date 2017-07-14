from __future__ import unicode_literals
import os
import re
import csv


def convert(data):
    ls=[]
    start=0
    for item in re.finditer(r'".*?"',data):
        ls.append(data[start:item.start()].replace(',',';'))
        ls.append(item.group().replace('"',''))
        start=item.end()
    out_str = ''.join(ls)
    out_str=out_str.replace('\n',r'\n')
    return out_str

def main():
    for item in os.listdir('.'):
        mt = re.match(r'^(.*).csv$',item)
        if mt:
            if not mt.group(1).endswith('_norm'):
                data_ls=[]
                with open(item,'rb') as f:
                    spamreader = csv.reader(f)
                    for row in spamreader:
                        ls=[x.decode('gbk') for x in row]
                        row_str=';'.join(ls).rstrip(' ')
                        row_str = row_str.replace('\n',r'\n')
                        data_ls.append(row_str) 
                data_str='\n'.join(data_ls)
                # data_str=data_str.replace('\n',r'\n')
                file_name=mt.group(1)+'_norm.csv'
                with open(file_name,'wb') as out_file:
                    out_file.write(data_str.encode('utf-8'))                
                
                # with open(item,'rb') as f:
                    # data=f.read()
                    # data=data.decode('gbk')
                    # data=convert(data)
                    # file_name=mt.group(1)+'_norm.csv'
                    # with open(file_name,'wb') as out_file:
                        # out_file.write(data.encode('utf-8'))
                    
                    

if __name__=='__main__':
    # ss='sgdsg"sdg,sdg",sdg"jj"'
    # print(convert(ss))
    main()