# -*- encoding:utf8 -*-
#
# 调用Leave.gen_leavetb() 会在当前目录生成sqlite3格式的 tmpfiles/leave.db 文件，
#
from tms import TmsData,EmployModel
from orm import Model,Field
import sqlite3
from datetime import date,datetime

class LeaveModel(Model):
    '暂存假期数据表'
    empid = Field()
    name = Field()
    startjob = Field()
    startmokie = Field()
    total_year = Field()
    mk_year = Field()
    legal_al=Field()
    comp_al=Field()
    available_al=Field()

LeaveModel.connection(sqlite3.connect("tmpfiles/leave.db"))
LeaveModel.create()

class Leave(object):
    """
    年假规则：
    ===================
    可用年假(available_al)= min(20, 法定年假+公司年假)
    法定年假(legal_al) = 根据工作年限(total_year)进行判断
                         1. 工作年限 <1 ,       0 天
                         2. 1<= 工作年限 <10  , 7 天
                         3. 10<=工作年限 <20  , 10 天
                         4. 工作年限>=20 ,      15 天
    公司年假(comp_al) = 摩奇工作年限
    """
    def gen_leavetb(self):
        '生成假期表'
        for p in TmsData.employee():
            assert isinstance(p,EmployModel)
            
            try:
                startjob = datetime.strptime(p.startjob,'%Y/%m/%d').date()
                total_year = getyearspan(date.today(),startjob)
            except ValueError:
                total_year = 0
            try:
                startmokie = datetime.strptime(p.startmokie,"%Y/%m/%d").date()
                mk_year = getyearspan(date.today(),startmokie)   
            except ValueError:
                mk_year = 0
            legal_al = self.get_legal_al(total_year)
            available_al = min(20,legal_al+mk_year)
            LeaveModel(
                empid = p.empid,
                name = p.name,
                startjob = p.startjob,
                startmokie = p.startmokie,
                total_year = total_year,
                mk_year = mk_year ,  
                legal_al = legal_al,
                comp_al = mk_year,
                available_al = available_al,
            ).save()
        LeaveModel.commit()
    
    def get_legal_al(self,total_year):
        '计算法定年假'
        if total_year<1:
            return 0
        elif 1<= total_year <10:
            return 7
        elif 10<=total_year <20:
            return 10
        else:
            return 15
        
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
    Leave(). gen_leavetb()
    