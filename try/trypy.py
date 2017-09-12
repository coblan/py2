# encoding:utf-8
import requests
rt = requests.get("https://ssl.gstatic.com/accounts/static/_/js/k=gaia.gaiafe_glif.zh_CN.ihEUHp_x7EQ.O/m=P9M9H/am=ggAQAgAAgApUEEQIJqAikGE/rt=j/d=0/rs=ABkqax3TM5r73XoVSSe5GPeSZc5Nf_6LyA")
# rt = requests.get('https://www.google.com')
print(rt.content)