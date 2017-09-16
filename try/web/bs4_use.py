from bs4 import BeautifulSoup
import base64

with open(r'D:\try\emoj\Full Emoji List, v5.0.html') as f:
    text=f.read()
    
    dc={}
    
    soup = BeautifulSoup(text,'html.parser')
    trlist=soup.select('tr')
    for tr in trlist:
        ls= tr.select('td.code')
        if ls:
            key=ls[0].text
            
            print(key)
            google=tr.select('td')[4]
            img = google.select('img')[0]
            # print(img.attrs['src'])
            
            dc[ls[0].text]=img.attrs['src']
            file_name=r'D:\try\emoj\images'+r'\%s'%key+'.png'
            src=img.attrs['src']
            dd=src[22:]
            dd=base64.b64decode(dd)
            with open(file_name,'wb') as f:
                f.write(dd)
     
    