import requests
import urlparse
import json
import re

# def batch_get_tags(ids):
    # ids=[str(x) for x in ids]
    # imgs=[]
    # url=urlparse.urljoin('http://d2-wallpaperv3.ticktockapps.com','images/tags?images=%s'%','.join(ids))
    # # url='http://d2-wallpaperv3.ticktockapps.com/images/tags?images=%s'%','.join(ids)
    # resp=requests.get(url)
    # imgs=json.loads(resp.content)
    # # imgs=json.loads(url)
    # # for img_id in ids:
        # # url = 'http://d2-wallpaperv3.ticktockapps.com/images/{img_id}/tags'.format(img_id=img_id)
        # # resp = requests.get(url)
        # # tags= json.loads(resp.content)
        # # imgs.append({'id':img_id,'tags':tags})
    # return imgs


# print( batch_get_tags(['1255867']) )
def get_img_info(imgid):
    url = 'http://d2-wallpaperv3.ticktockapps.com/images/%(imgid)s/info'%({'imgid':imgid})
    rt = requests.get(url)
    rt_json = json.loads(rt.content)
    return rt_json.get('url')

with open('two_month.txt') as f:
    out =[]
    cnt=0
    for line in f.readlines():
        line_str = line.replace(',','')
        line_str = line_str.strip()
        pair = re.split('\W',line_str)
        
        imgid=pair[0]
        url = get_img_info(imgid)
        print('%(imgid)s  -> %(url)s'%{'imgid':pair[0],'url':url})
        out.append({'imgid':pair[0],'url':url,'count':pair[1]})
        # cnt +=1
        # if cnt >5:
            # break
    
    with open('two_month.json','w') as f:
        json.dump(out,f)
        
        
    # string = f.read()
    # line = string.split('\n')
# get_img_info('1255867')