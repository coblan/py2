import json
import re

with open('two_month.json') as f:
    js = json.load(f)
    for img in js:
        if img.get('url'):
            mt = re.search('(.*)(\.\w+$)',img.get('url'))
            img['thumb'] = mt.group(1)+'-305x543'+mt.group(2)
    
    with open('two_month_normed.json','w') as f2:
        json.dump(js,f2)