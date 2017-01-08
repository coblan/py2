# -*- encoding:utf8 -*-
"""

1. 调用pre_process(path) path:考勤原始记录路径。返回需要设置日期作息时间的字典
2. 调用process(daysttings,path) ,daysttings是经过修改的日期作息时间字典，path是保存excel07文件路径

"""
import xlrd,sqlite3,re
from openpyxl import Workbook
from mytime import Time
from datetime import datetime,date,timedelta
from orm.model import Model
from orm.fields import CharField,DateField,DateField
from kaoqin import get_kaoqin_list,KaoRecord

# TMS模拟数据
from tms import TmsData

def pre_process(path):
    "预处理，传输path,"
    kaolist = get_kaoqin_list(path)
    RecordModel.initFromList(kaolist)
    return RecordModel.get_days()

def process(daysettings,path):
    RecordModel.setdaystn(daysettings)     
    RecordModel.main_process()
    RecordModel.gen07(path)


class MyTimeField(CharField):
    def todb(self, obj):
        if obj is None:
            return "NULL"
        assert isinstance(obj,Time)
        return "'%s'"%str(obj)
    def __set__(self, obj, val):
        if val is None or isinstance(val,Time):
            setattr(obj,"_field%s"%self.cnt,val)
        elif isinstance(val,(str,unicode)):
            setattr(obj,"_field%s"%self.cnt,Time.strptime(val))
        else:
            raise ValueError("MYTimeField set erro")


class RecordModel(Model): 
    """
    整理后的考勤记录数据表。
    
    日期作息
    ==============================
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
    
    主要函数
    =================================
    
    initFromList(), 由考勤原始记录的列表，生成考勤数据库
    
    main_process() ，遍历整个考勤记录，调用kaoqin接口函数，计算考勤记录的其他信息。最后保存
    
    gen07() ,将数据库保存为excel07文件
    
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
            record = KaoRecord(kao_number=p.kao_number,workstart= str(p.workstart), workleave=str(p.workleave), kaodate=p.date.strftime("%Y/%m/%d"), \
                               workshift= p.workshift, day_type= p.day_type(),overtime_from_date=overtime_from_date)
            p.note = record.get_note()
            p.sub_sequence = record.get_sub_sequence()
            p.late_team = record.get_late_team()
            p.workspan= record.get_workspan() 
            p.late_person = record.get_late_person()
            p.overtime= record.get_over_time()
            p.early_leave = record.get_early_leave()
            p.save()
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
        
    def day_type(self):
        datestr = self.date.strftime("%Y/%m/%d")
        for k,v in self.daystn.items():
            if k =='time':
                continue
            elif k=='restday':
                if datestr in v:
                    return "restday"
            elif datestr in v:
                return k
        raise ValueError("which type %s should be?"%self.date)  
    
def overtime_from_date(kao_number,datestr):
    #datestr = date_.strftime("%Y/%m/%d")
    for i in RecordModel.select("WHERE date='%s' AND kao_number='%s'"%(datestr,kao_number)):
        return str(i.overtime)
    return ''
        
if __name__ == '__main__':
    outlist = read_raw_03(r"D:\work\attendance\attendance record.xls")
    for i in outlist:
        print(i)