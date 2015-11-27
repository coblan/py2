# -*- encoding:utf8 -*-
"""
作用
=================================
计算当前年假的算法

"""
from datetime import date,datetime



class LeaveCompute(object):
    """
    年假规则：
    ===================
    可用年假(available_al)= min(20, 法定年假+公司年假)
    法定年假(legal_al) = 根据工作年限(total_year)进行判断
                         1. 工作年限 <1 ,       0 天
                         2. 1<= 工作年限 <10  , 7 天
                         3. 10<=工作年限 <20  , 10 天
                         4. 工作年限>=20 ,      15 天
    公司年假(mokie_al) = 摩奇工作年限
    
    调用函数获取年假
    ==========================================
    get_available_al()    获取当前规定可用年假，返回Int
    get_legal_al()        获取当前法定可用年假，返回Int
    get_mokieyear()       获取当前摩奇工作年限，返回Int
    get_totalyear()       获取当前总的工作年限，返回Int

    """
    def __init__(self,startjob,startmokie):
        """
        startjob:   开始工作的日期，格式："2010/11/09" 字符串
        startmokie: 开始在摩奇上班的日期 ，格式："2010/11/09" 字符串
        """
        self.startjob = startjob
        self.startmokie = startmokie
        
    def get_totalyear(self):
        """
        返回总的工作年限，int
        """
        startjob = datetime.strptime(self.startjob,"%Y/%m/%d")
        return getyearspan(date.today(),startjob)
    
    def get_mokieyear(self):
        startmokie = datetime.strptime(self.startmokie,"%Y/%m/%d")
        return getyearspan(date.today(),startmokie)
    
    def get_legal_al(self):
        """
         计算法定年假
        """
        totalyear = self.get_totalyear()
        if totalyear<1:
            return 0
        elif 1<= totalyear <10:
            return 7
        elif 10<=totalyear <20:
            return 10
        else:
            return 15    
    def get_mokie_al(self):
        return self.get_mokieyear()
    
    def get_available_al(self):
        return min(20,self.get_legal_al()+self.get_mokie_al())
   
def getyearspan(date1,date2):
    "date1 later than date2"
    year = date1.year-date2.year
    if date1.month >date2.month:
        return year
    elif date1.day > date2.day:
        return year
    else:
        return year -1
  
if __name__ == '__main__':
    obj = LeaveCompute(startjob="2004/8/15", startmokie="2005/9/16")
    print(obj.get_available_al())
    print(obj.get_mokieyear())
    print(obj.get_mokie_al())
    print(obj.get_totalyear())
    print(obj.get_legal_al())