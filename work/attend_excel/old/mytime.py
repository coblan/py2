# -*- encoding:utf8 -*-

class Time(object):
    '时间运算，转换。'
    def __init__(self,hour,minute=0):
        self.hour=hour
        self.minute =minute
    
    @staticmethod
    def strptime(str_):
        if not str_:
            return ''
        tm = Time(0)
        ls= str_.split(":")
        if ls:
            tm.hour = int(ls[0])
            tm.minute = int(ls[1]) 
        return tm
    
    def __sub__(self,other):
        tm1 = self.hour*60 + self.minute
        tm2 = other.hour*60 +other.minute
        span = tm1 -tm2
        if span <0:
            span = 0
        hour = span/60
        minute = span%60
        return Time(hour,minute)
    
    def __cmp__(self,other):
        if self.hour == other.hour:
            if self.minute<other.minute:
                return -1
            elif self.minute == other.minute:
                return 0
            elif self.minute>other.minute:
                return 1
        elif self.hour>other.hour:
            return 1
        elif self.hour < other.hour:
            return -1
    
    def __mul__(self,number):
        hour = self.hour*number
        minute = self.minute*number
        total = hour*60 +minute
        hour = total/60
        minute = total%60
        return Time(hour,minute)
    
    def __str__(self):
        return '%s:%02d:00'%(self.hour,self.minute)
    
    def __add__(self,other):
        hour = self.hour+other.hour
        minute = self.minute+other.minute
        hour = hour + minute/60
        minute = minute%60
        return Time(hour,minute)
    
    #def to_stdtime(self):
        #hour =self.hour%24
        #return time(hour,self.minute)