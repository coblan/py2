# -*- encoding:utf-8 -*-

import sys, socket  
# 获取域名的IP地址  
domains="""
www.hanabimedia.net,
www.icequeenmedia.com,
www.applabsinc.net,
www.imagineappsltd.com,
www.toyboxmediainc.com,
www.toymakermedia.com,
www.bigbearentertainment.net,
www.moremysteries.com,
www.timeoutapps.net,
www.levelupapps.net,
www.tobiapps.com,
www.bluepillmedia.com,
www.iceageapps.com,
www.mega8studios.com,
www.oneothergame.com,
www.ticktockapps.com,
www.sniperstudio.com,
www.turbofireapps.com,
www.wallpapershdinc.com,
www.bluepillinc.com,
www.fitnessappsinc.com,
www.thewildlabs.com,
www.lazypugstudios.com,
www.bigfurrygames.com,
www.instaappsinc.com,
www.lockscreensHD.com,
www.workoutinc.net,
www.tofumediainc.com,
"""
out=[]
for d in domains.split(','):
    b=d.strip('\n')
    result = socket.getaddrinfo(b, None) 
    out.append([result[0][4][0],b])

for d in sorted(out):
    print(d) 