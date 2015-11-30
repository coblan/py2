# -*- encoding:utf8 -*-

class Time(object):
    """
    由于python标准库的datetime.time运算不方面，所以这里简单的实现了time的计算功能。
    
    两个方式生成Time对象
    ========================
    1.构造函数： obj=Time(8,45)
    2.字符串 : obj= Time.strptime("8:45")
    
    操作
    ========================
    实现了 + ,- ,* ,排序比较 ，str()
    
    注意
    =======================
    1.当Time相减时，如果为负数，则自动清空为Time(0)
    2.str(Time(0))返回的是空字符串，而不是"0:00"
    
    """
    def __init__(self,hour,minute=0):
        self.hour=hour
        self.minute =minute
    
    @staticmethod
    def strptime(str_):
        if not str_:
            return Time(0)
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
        if self.hour==0 and self.minute == 0:
            return ""
        else:
            return '%s:%02d'%(self.hour,self.minute)
    
    def __add__(self,other):
        hour = self.hour+other.hour
        minute = self.minute+other.minute
        hour = hour + minute/60
        minute = minute%60
        return Time(hour,minute)
    
    def __eq__(self,other):
        assert isinstance(other,Time)
        return self.hour == other.hour and self.minute == other.minute
    
    def __repr__(self):
        return "<myTime(%s,%s)>"%(self.hour,self.minute)



    
    