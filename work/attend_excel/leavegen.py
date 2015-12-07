# -*- encoding:utf8 -*-
#
# 调用Leave.gen_leavetb() 会在当前目录生成sqlite3格式的 tmpfiles/leave.db 文件，
#
from tms import TmsData,EmployModel
from orm.model import Model,CharField,IntField
import sqlite3
from datetime import date,datetime
from leave import LeaveCompute


def gen_leave_tb():
    """
    生成可用年假数据库
    """
    for p in TmsData.employee():
        assert isinstance(p,EmployModel)
        try:
            startjob = datetime.strptime(p.startjob,'%Y/%m/%d').date()
        except ValueError:
            startjob = date.today()
        try:
            startmokie = datetime.strptime(p.startmokie,"%Y/%m/%d").date()  
        except ValueError:
            startmokie = date.today()
        startjob = startjob.strftime("%Y/%m/%d")
        startmokie=startmokie.strftime("%Y/%m/%d")
        computer = LeaveCompute(startjob, startmokie)
        
        LeaveModel(
            empid = p.empid,
            name = p.name,
            startjob = startjob,
            startmokie = startmokie,
            total_year = computer.get_totalyear(),
            mk_year = computer.get_mokieyear() ,  
            legal_al = computer.get_legal_al(),
            comp_al = computer.get_mokie_al(),
            available_al = computer.get_available_al(),
        ).save()
    LeaveModel.commit()    
    
class LeaveModel(Model):
    '暂存假期数据表'
    empid = CharField(default='')
    name = CharField(default='')
    startjob = CharField(default='')
    startmokie = CharField(default='')
    total_year = IntField(default='')
    mk_year = IntField(default='')
    legal_al= IntField(default='')
    comp_al= IntField(default='')
    available_al= IntField(default='')

  
if __name__ == '__main__':
    LeaveModel.connection(sqlite3.connect("tmpfiles/leave.db"))
    LeaveModel.create()
    
    gen_leave_tb()
    