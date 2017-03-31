# encoding:utf-8

import os
import re
import sys
import requests
import time
import json


sys.path.append(r'd:\coblan\py2')

root =  r'D:\work\vellum'

# root = r'D:\work\vellum\vellumStarter'
# url_temp = 'https://firebasestorage.googleapis.com/v0/b/vellum-3f635.appspot.com/o/vellumStarter%2F{num}.jpg?alt=media'

# root = r'D:\work\vellum\limitedEdition2'
# url_temp = 'https://firebasestorage.googleapis.com/v0/b/vellum-3f635.appspot.com/o/limitedEdition2%2F{num}.jpg?alt=media'

# root = r'D:\work\vellum\earthGoogle'
# url_temp = 'https://firebasestorage.googleapis.com/v0/b/vellum-3f635.appspot.com/o/earthGoogle%2F{num}.jpg?alt=media'

# root = r'D:\work\vellum\Synapse'
# url_temp='https://firebasestorage.googleapis.com/v0/b/vellum-3f635.appspot.com/o/Synapse%2F{num}.jpg?alt=media'

# root = r'D:\work\vellum\Recrystallized'
# url_temp = 'https://firebasestorage.googleapis.com/v0/b/vellum-3f635.appspot.com/o/Recrystallized%2F{num}.jpg?alt=media'

def norm_json_str(orginalJsonStr):
    addedSingleQuoteJsonStr = re.sub(r"(,?)(\w+?)\s*?:", r"\1'\2':", orginalJsonStr)
    doubleQuotedJsonStr = addedSingleQuoteJsonStr.replace("'", "\"")
    #remove comma before end of list
    removedLastCommaInList = re.sub(r",[\s|\n]*?]", "]", addedSingleQuoteJsonStr)
    removedLastCommaInList = re.sub(r",[\s|\n]*?}", "}", removedLastCommaInList)
    return removedLastCommaInList


has_fetched=['vellumStarter','limitedEdition2','earthGoogle','Synapse','Recrystallized']

rt = requests.get('https://firebasestorage.googleapis.com/v0/b/vellum-3f635.appspot.com/o/packs.json?alt=media&token=89a0ffdd-0a75-4032-bd5e-dd70c57dff4a')
json_str=norm_json_str(rt.text)
cat = json.loads(json_str)

folders =[]
for pack in cat.get('packs'):
    folder = pack.get('folder')
    folders.append(folder)

folders=filter(lambda x: x not in has_fetched,folders)

for folder in folders:
    url_temp='https://firebasestorage.googleapis.com/v0/b/vellum-3f635.appspot.com/o/{folder}%2F{num}.jpg?alt=media'
    print('---------')
    print(folder)
    try:
        os.makedirs(os.path.join(root,folder))
    except:
        pass
    errors=[]
    for num in range(200):
        url=url_temp.format(folder=folder,num=num)
        rt = requests.get(url)
        time.sleep(1)
        
        if len(errors)>10:
            break
        if rt.status_code !=200:
            errors.append(num)
            continue
        
        if rt.headers.get('Content-Type')=='image/jpeg':
            with open(os.path.join(root,folder,'%s.jpeg'%num),'wb') as f:
                f.write(rt.content)
                print('[ok] get %s'%num)
    
# print('errors:--------------')
# print(errors)
# for url in ls[length:]:
    # if url != '':
        # rt = requests.get(url)
        
        # c = re.search('([^/]+)$',url)
        # name = c.group(1)
        # path = os.path.join(root,name)
        # print(url)
        # with open(path, 'wb') as f:
            # f.write(rt.content)

