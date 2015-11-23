# -*- encoding:utf8 -*-
import xlrd,sqlite3,re
from openpyxl import Workbook
from mytime import Time,MyTimeField
from datetime import datetime,date,timedelta
from orm.model import Model
from orm.fields import CharField,DateField,DateField
import kaoqin

# TMS模拟数据
from tms import TmsData

def pre_process(path):
    kaolist = read_raw_03(path)
    kaolist = div_time_col(kaolist)
    RecordModel.initFromList(kaolist)
    return RecordModel.get_days()

def process(daysettings,path):
    RecordModel.setdaystn(daysettings)     
    RecordModel.main_process()
    RecordModel.overtime_bonus()
    RecordModel.gen07(path)
    
def read_raw_03(path):
    rawdata = xlrd.open_workbook(path,encoding_override='gbk')
    table = rawdata.sheets()[0]
    nrows = table.nrows
    kaolist = []
    for i in range(1, nrows):
        kaolist.append(table.row_values(i))
    return kaolist

def div_time_col(kaolist):
    """分割时间字符串栏
    kaolist = [ [kao_number,name,department,date,timestr],]
    """
    for row in kaolist:
        start,end=find_min_max(row[4])
        row[4]=start
        row.append(end)
    return kaolist
    
def find_min_max(timestr):
    "分解时间字符串，并且返回最小，最大时间"
    timestr = timestr.strip()
    if timestr:
        ls = timestr.split(u' ')
        if ls:
            ls = [Time.strptime(str_) for str_ in ls]
            ls.sort()
            return ls[0],ls[-1]
    
    return '',''
    
    
class RecordModel(Model): 
    """
    整理后的考勤记录数据表。
    
    函数：setdaystn() 设置日期，哪些是工作日，哪些不工作，以及工作日的作息时间等。
    格式如下:

    {
    "workday": [
        "2015/09/01", 
        "2015/09/02", 
        ...
    ], 
    "restday": [
        "2015/09/05", 
        "2015/09/06", 
        ...
    ], 
    "special": [], 
    "time": {
        "special": [
            "10:00", 
            "17:30"
        ]
    }
}
    其中：
    workday 按照个人workshift计算上班下班时间
    restday 不计算个人迟到早退
    special  按照time中设置的时间计算上下班
    中午午饭:12:30-1:30不计算在工作时长中。
    """
    
    kao_number=CharField(default='')
    name = CharField(default='')
    department = CharField(default='')
    date = DateField(default='')
    workshift = CharField(default='')
    workstart = MyTimeField(default=Time(0))
    workleave = MyTimeField(default=Time(0))
    note = CharField(default='')
    sub_sequence = CharField(default='')
    late_team = MyTimeField(default=Time(0))
    workspan = MyTimeField(default=Time(0))
    late_person=MyTimeField(default=Time(0))
    overtime =MyTimeField(default=Time(0))
    early_leave = MyTimeField(default=Time(0))
    
   #保存的工作日字典
    daystn={}
    
    @classmethod
    def initFromList(cls,ls):
        "ls = [ [kao_number,name,department,date,workstart,workleave],]"
        conn = sqlite3.connect(':memory:')
        RecordModel.connection(conn)
        RecordModel.create()  
        for row in ls:
            dc ={"kao_number":row[0],
                "name":row[1],
                "department":row[2],
                "date":row[3],
                "workstart":row[4],
                "workleave":row[5],
                }   
            p = RecordModel(**dc)
            p.save()
        RecordModel.commit() 
        
    @classmethod
    def setdaystn(cls,daysettings):
        cls.daystn = daysettings
        
    @classmethod
    def get_days(cls):
        days = []
        for p in RecordModel.select():
            days.append(p.date)
        days =list(set(days))
        days.sort()
        return days    
     
    @classmethod
    def main_process(cls):
        "行之间不相互影响的处理，放在这里进行"
        for p in RecordModel.select():
            # 必须先添加workshift，因为后面属性计算会用到
            p.workshift = TmsData.kao2workshift(p.kao_number)

            p.note = kaoqin.get_note(p.date, p.daystn, p.workstart, p.workleave)
            p.sub_sequence = kaoqin.get_sub_sequence(p.date,p.daystn,p.workstart,p.workleave)

            p.late_team = kaoqin.get_late_team(p.date,p.daystn,p.workstart)
            p.workspan= kaoqin.get_workspan(workstart,workleave) 
            p.late_person = kaoqin.get_late_person(p.date,p.workstart)
            p.overtime= kaoqin.get_over_time(p.date,p.workleave)
            p.early_leave = kaoqin.get_early_leave(p.date,p.daystn,p.workstart)
            
            p.save()
       
        RecordModel.commit()  
    
    @classmethod
    def overtime_bonus(cls):
        "行之间会相互影响，所以单独提出来"
        overtimelist = []
        for p in RecordModel.select():
            assert isinstance(p,RecordModel)
            overtime = p.overtime 
            if overtime!=Time(0) and p.note !="restday":
                overtimelist.append(p)
        
        for p in overtimelist:
            date = p.date 
            if date.weekday()!=4:
                lastday = date + timedelta(days=1)
                laststr = lastday.strftime("%Y/%m/%d")
                for i in RecordModel.select("WHERE date='%s' AND kao_number='%s'"%(laststr,p.kao_number)):
                    i.late_team= i.get_late_team(tic=Time(10))
                    i.late_person = i.get_late_person(tic=Time(10))
                    i.sub_sequence = i.get_sub_sequence(Time(10))
                    i.save()
                    break    
        RecordModel.commit()  
        
    @classmethod
    def gen07(cls, path):
        wb = Workbook()
        ws = wb.active 
        ws.title='record'
        ws.append([u"考勤号码",u"姓名",u"部门",u"日期",u'workshift',u"上班时间",u"下班时间",u'Note',u'sub-sequence',u'迟到时长-团队',u'工作时长',u'迟到时长-个人出勤率',u'加班时长',u'早退'])
        
        for row in RecordModel.select("ORDER BY kao_number ,date"):
            
            assert isinstance(row,RecordModel)

            # 整理格式准备写入excel2007
            outrow=[row.kao_number,row.name,row.department,row.date.strftime("%Y/%m/%d"),row.workshift,row.workstart,row.workleave,row.note,row.sub_sequence,row.late_team,row.workspan,row.late_person,row.overtime,row.early_leave]
            outrow = [ str(x) for x in outrow]
            ws.append(outrow)  
        
        wb.save(path)

 

        

if __name__ == '__main__':
    outlist = read_raw_03(r"D:\work\attendance\attendance record.xls")
    for i in outlist:
        print(i)