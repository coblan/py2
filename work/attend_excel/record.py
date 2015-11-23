# -*- encoding:utf8 -*-
import xlrd
from openpyxl import Workbook
from openpyxl.styles import PatternFill,Style,Color
from mytime import Time,MyTimeField
import sqlite3
from datetime import datetime,date,timedelta
#from orm import Model,Field
from heStruct.orm.model import Model
from heStruct.orm.fields import CharField,DateField,DateField
from tms import TmsData
import re

class RecordModel(Model): 
    "整理后的考勤记录数据表"
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

    
class Record(object):
    def __init__(self,src,dst):
        self.src=src
        self.dst=dst
        self.conn = sqlite3.connect(':memory:')
        RecordModel.connection(self.conn)
        RecordModel.create()
    
    def pre_process(self):
        self.read03(self.src)
        days = []
        for p in RecordModel.select():
            days.append(p.date)
        days =list(set(days))
        #days = [datetime.strptime(x,"%Y/%m/%d").date() for x in days]
        days.sort()
        return days
    
    def process(self,daysettings,path):
        self.daysettings = daysettings
        self.gen_table()
        self.gen07(path)
        
    
    def read03(self,path):
        """读取并处理考勤原始数据,最后在conn中生成一个raw_record数据表，数据表模型见Raw_Record
                    conn : 数据库连接
                    path : excel03文件路径
                    """
        rawdata = xlrd.open_workbook(path,encoding_override='gbk')

        table = rawdata.sheets()[0]
        nrows = table.nrows
        for i in range(1, nrows):
            start,end=self.find_min_max(table.row_values(i)[4])
            dc={"kao_number":table.row_values(i)[0],
                "name":table.row_values(i)[1],
                "department":table.row_values(i)[2],
                "date":table.row_values(i)[3],
                "workstart":start,
                "workleave":end
                }
            RecordModel(**dc).save()
        RecordModel.commit() 
        
    def find_min_max(self, timeList):
        "分解时间字符串，并且返回最小，最大时间"
        timeList = timeList.strip()
        if timeList:
            ls = timeList.split(u' ')
            if ls:
                ls = [Time.strptime(str_) for str_ in ls]
                ls.sort()
                return ls[0],ls[-1]
        
        return '',''
    
    def gen_table(self):
        "在conn中生成处理的考勤记录表,表模型见RecordModel"
        self.addwork_shift()
        for p in RecordModel.select():
            self.crtperson = p
            
            workstart = p.workstart # Time.strptime(p.workstart)
            workleave = p.workleave # Time.strptime(p.workleave)           
            # 修改字段
            # 为了给日期补0
            
            #p.date = datetime.strptime(p.date,"%Y/%m/%d").date().strftime("%Y/%m/%d")
            if self.get_workday() =="restday":
                p.note="restday"
            elif self.crtperson.workstart==Time(0) and self.get_sud_start()!= Time(0):
                p.note="not work"
                
          
            p.sub_sequence = self.get_sub_sequence()

            p.late_team = self.get_late_team()
            p.workspan= (workleave- workstart-Time(1) ) if isinstance(workleave,Time) else ""
            p.late_person = self.get_late_person()
            p.overtime= self.get_over_time()
            p.early_leave = self.get_early_leave()
            
            p.save()
 
        RecordModel.commit()
        
        self.overtime()


    def gen07(self,path):
        wb = Workbook()
        ws = wb.active 
        ws.title='record'
        ws.append([u"考勤号码",u"姓名",u"部门",u"日期",u'workshift',u"上班时间",u"下班时间",u'Note',u'sub-sequence',u'迟到时长-团队',u'工作时长',u'迟到时长-个人出勤率',u'加班时长',u'早退'])
        
        cnt=1
        for row in RecordModel.select("ORDER BY kao_number ,date"):
            
            assert isinstance(row,RecordModel)
            self.crtperson=row

            #判断添加cell颜色，要等待写入2007后，才能添加颜色，见【1】
            shang=self.shang_ban_color()
            #xia =self.xia_ban_color()

            # 整理格式准备写入excel2007
            outrow=[row.kao_number,row.name,row.department,row.date.strftime("%Y/%m/%d"),row.workshift,row.workstart,row.workleave,row.note,row.sub_sequence,row.late_team,row.workspan,row.late_person,row.overtime,row.early_leave]
            outrow = [ str(x) for x in outrow]
            ws.append(outrow)  

            #添加颜色【1】
            cnt+=1
            #sud_start = self.get_sud_start()

            #if shang:
                #row = ws.row_dimensions[cnt]
                #row.fill=PatternFill(fill_type='solid', start_color=shang)
                #for c in ["A","B","C","D","E","F","G","H","I","J","K","L","M"]:
                    #ws["%s%s"%(c,cnt)].fill=PatternFill(fill_type='solid', start_color=shang)
            #if xia:
                #ws['G'+str(cnt)].fill=PatternFill(fill_type='solid', start_color=xia)  
        
        wb.save(path)
    
    # -----------------middlle ware --------------------
    def overtime(self):
        overtimelist = []
        for p in RecordModel.select():
            assert isinstance(p,RecordModel)
            overtime = p.overtime #Time.strptime(p.overtime)
            if overtime!=Time(0):
                overtimelist.append(p)
        
        for p in overtimelist:
            date = p.date #datetime.strptime(p.date,"%Y/%m/%d").date()
            #self.crtperson = p
            if date.weekday()!=4:
                lastday = date + timedelta(days=1)
                laststr = lastday.strftime("%Y/%m/%d")
                for i in RecordModel.select("WHERE date='%s' AND kao_number='%s'"%(laststr,p.kao_number)):
                    self.crtperson = i
                    i.late_team= self.get_late_team(tic=Time(10))
                    i.late_person = self.get_late_person(tic=Time(10))
                    i.sub_sequence = self.get_sub_sequence(Time(10))
                    i.save()
                    break    
        RecordModel.commit()

    def addwork_shift(self):
        "填写work_shift"
        for p in TmsData.employee():
            for row in RecordModel.select("WHERE kao_number='%s'"%p.kao_number):
                row.workshift = p.work_shift
                row.save()
        RecordModel.commit()
    
    def get_workday(self):
        datestr = self.crtperson.date.strftime("%Y/%m/%d")
        for k,v in self.daysettings.items():
            if k =='time':
                continue
            elif k=='restday':
                if datestr in v:
                    return "restday"
            elif datestr in v:
                return k
        raise ValueError("which type %s should be?"%self.crtperson.date)
                
    def get_sud_start(self):
        workday = self.get_workday()
        if workday=="workday":
            mt = re.match(r"(.*)-(.*)",self.crtperson.workshift)
            if mt:
                return Time.strptime(mt.group(1))
            else:
                return Time(0)
        elif workday == "restday":
            return Time(0)
        else:
            return Time.strptime(self.daysettings["time"][workday][0])

                   
    def get_sud_leave(self):
        workday = self.get_workday()
        #if workday:
        if workday=="workday":
            mt = re.match(r"(.*)-(.*)",self.crtperson.workshift)
            if mt:
                return Time.strptime(mt.group(2))
            else:
                return Time(0)
        elif workday=="restday":
            return Time(0)
        else:
            return Time.strptime(self.daysettings["time"][workday][1])
        #return None    
    
    def get_late_team(self,tic=None):
        'callback:返回迟到团队时间，Time对象'
        if self.get_workday()=="restday":
            return ''
        workstart = self.crtperson.workstart #Time.strptime(self.crtperson.workstart)
        if tic is None:
            tic= self.get_sud_start()
            if tic ==Time(0):
                return ''
        late = workstart - (tic+Time(0,15))
        return late        


    def get_sub_sequence(self,tic=None):
        if self.get_workday() == "restday":
            return ''
        workstart = self.crtperson.workstart #Time.strptime(self.crtperson.workstart)
        if tic is None:
            tic= self.get_sud_start()
            if tic == Time(0):
                return ''            
        if tic< workstart <=tic+Time(0,15):
            return 'late1'
        elif tic+Time(0,15) <= workstart <tic+Time(1):
            return 'late2'
        elif tic+Time(1) <= workstart:
            return 'late3'   
        else:
            return ''
        

    def get_late_person(self,tic=None):
        if self.get_workday()== "restday":
            return ''
        workstart = self.crtperson.workstart #Time.strptime(self.crtperson.workstart)
        if tic is None:
            tic= self.get_sud_start()
            if tic == Time(0):
                return ''          
        if tic+Time(0,15) <=workstart <tic+Time(1):
            return workstart-(tic+Time(0,15) )
        elif tic+Time(1)<= workstart:
            return (workstart- (tic+Time(1)))*2  
        else:
            return ''
        
    def get_over_time(self):
        workleave = self.crtperson.workleave #Time.strptime(self.crtperson.workleave)
        return workleave-Time(20)
    
    def get_early_leave(self):
        if self.get_workday()=="restday":
            return '' 
        workleave = self.crtperson.workleave #Time.strptime(self.crtperson.workleave)
        if workleave ==Time(0):
            return ''
        sud_leave = self.get_sud_leave()
        if sud_leave ==Time(0):
            return ''
        else:
            return sud_leave-workleave
        

    
    def shang_ban_color(self):
        sud_start = self.get_sud_start()
        if sud_start is None:
            return "FFDEDEDE"
        late = self.crtperson.sub_sequence
        if late=='late3':
            return 'FFFFFF00'
        elif late == 'late2':
            return 'FFA4D3EE'
        elif late == 'late1':
            return 'FFFFB5C5'

    def xia_ban_color(self):
        pass       