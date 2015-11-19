# -*- encoding:utf8 -*-

# 模拟TMS数据
# 直接运行该文件，会运行geninfo()函数，其目的是从record,report提取雇员的信息，如雇员号，考勤号等，将模型EmployModel。最后保存为sqlite3文件
# 该文件被别的模块调用时，主要调用TmsData.empoyee()生成器，其目的是罗列出雇员信息。
# EmployModel 当前雇员模型


import openpyxl,pickle
from attend_reader import Raw_Record
from orm import Model,Field
import sqlite3


class EmployModel(Model):
    "雇员的信息，当前信息来源于从excel提取出的固定信息"
    empid = Field()
    kao_number = Field()
    name = Field()
    pname =Field()
    status = Field()
    work_type = Field()
    work_shift = Field()
    expect_days = Field()
    startjob = Field()
    startmokie = Field()
    
EmployModel.connection(sqlite3.connect("tmpfiles/employee"))
class TmsData(object):
    @staticmethod
    def employee():
        "罗列出雇员"
        for p in EmployModel.select():
            if p.empid =='AE1774':
                p.kao_number = 1157
                p.save()
            elif p.empid == 'AE1776':
                p.kao_number= 1158 
                p.save()
            yield p  
        EmployModel.commit()

def geninfo():
    "直接运行该函数，将解析xlsx与xls文件，将生成一个列表，并保存到硬盘，目的是将empID同kao_number对应起来。"

    from attend_reader import Reader
    
    conn = sqlite3.connect(':memory:')
    Reader.read03(conn, r"D:\work\attendance\attendance record.xls")
    cursor = conn.cursor()
    Raw_Record.connection(conn)
    
    '从excel提取员工信息，保存为pickle格式，作为测试用'

    
    EmployModel.create()
    
    wb = openpyxl.load_workbook(r"D:\work\attendance\MK_HR_Attendance Report_Cecilia_201510.xlsx")
    ws = wb['report']
    out =[]
    head=True
    for i in ws.rows:
        if head:
            head =False
            continue
        ls = [j.value for j in i]
        kao_number='000'
        #for i in  cursor.execute("SELECT * FROM raw_record WHERE name='%s'"%ls[1]):
        for i in Raw_Record.select("WHERE name='%s'"%ls[1]):
            kao_number = i.kao_number
            break
        EmployModel(empid=ls[0],kao_number=kao_number,name=ls[1],pname=ls[2],status=ls[3],work_type=ls[4],work_shift=ls[5],expect_days=ls[6]).save()
        #ls.append(kao_number)
        
        #out.append(ls)
    EmployModel.commit()
    
    wb2 = openpyxl.load_workbook(r"D:\work\attendance\MK_HR_Leave Record2015_TEST.xlsx")
    ws2 = wb2["Annual Leave"]
    for i in ws2.rows:
        ls = [j.value for j in i]
        empid = ls[0]
        for i in EmployModel.select("WHERE empid='%s'"%empid):
            try:
                i.startjob = ls[5].strftime("%Y/%m/%d")
            except:
                i.startjob=""
            try:
                i.startmokie = ls[6].strftime("%Y/%m/%d")
            except:
                i.startmokie =""
            i.save()
            
    EmployModel.commit()
            
if __name__ =='__main__':
    geninfo()