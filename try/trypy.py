# encoding:utf-8

from math import *

def distance(jd1,wd1,jd2,wd2):
    jd1=radians(jd1)
    wd1=radians(wd1)
    jd2=radians(jd2)
    wd2=radians(wd2)
    
    a= wd1-wd2
    b=jd1-jd2
    s= 2 * asin(sqrt( sin(a/2)**2 + cos(wd1)*cos(wd2)* sin(b/2)**2))
    s = s* 6367000
    return s
    
    #2 * Math.Asin(Math.Sqrt(Math.Pow(Math.Sin(a/2),2) +   
        #Math.Cos(radLat1)*Math.Cos(radLat2)*Math.Pow(Math.Sin(b/2),2)));      
    #hsinX=sin(jd1-jd2)*0.5
    #hsinY=sin(wd1-wd2)*0.5
    #h=hsinY**2 + cos(wd1)+cos(wd2)*hsinX**2
    #return 2*atan2(sqrt(h),sqrt(1-h))*pi/180*6367000

jd1=104.166178
jd2=104.166078
wd1=30.702633
wd2=30.702633

print(distance(jd1, wd1, jd2, wd2))
