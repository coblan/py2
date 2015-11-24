# -*- encoding:utf8 -*-
"""
用途
=================================================

读取考勤原始记录，配合TMS系统，计算个人考勤情况。


使用步骤
=================================================

1. 调用get_kaoqin_list(path)生成经过日期排序的考勤列表。
2. 遍历考勤列表，
3. 结合TMS提供的信息，生成KaoRecord()对象，调用各种get_函数，计算该条考勤记录其他信息。
4. 保存到数据库。


使用例子:
=================================================

#从考勤原始记录中获取按日期排序的考勤记录
kaolist=get_kaoqin_list(r"D:\myfile\kaoqin_2015_9.xls")
#遍历考勤列表，依次处理记录，并保存到数据库
for i in kaolist:
    # 生成一个处理记录的对象。其中: TMS.overtime_from_date(date) return "3:20"格式，即认为加班，如果为空字符串，即认为没加班。该函数由外部提供
    row = KaoRecord(kao_number=i[0],workstart=i[4],workleave=i[5],kaodate=i[3].strftime("%Y/%m/%d"),day_type="workday",overtime_from_date=TMS.overtime_from_date)
    # TMS.save()用于保存到TMS数据库
    TMS.save(kaonumber=row.kao_number, late_person =row.get_late_person(),....)


其他
===============================================
1. mytime.Time类，用于包装时间(内部具有hour,minute)，实现加，减，数乘运算。如果运算后为负，则返回Time(0)。
   Time.__str__产生格式为:"8:30",Time.strptime()接收"8:30"格式字符串，生成Time对象。Time(hour=8,minute=20)也可以生成Time对象
2. xlrd库用于读取03excel文件

"""

from mytime import Time
from datetime import datetime,date,timedelta
import re,xlrd
 
def get_kaoqin_list(path):
    """ 返回一个按照 考勤号，日期 排序的列表。
         kaolist = [ [kao_number,name,department,date,workstart,workleave],
                     [考勤号，名字，部门，日期，上班打卡时间，下班打卡时间]]
    path: 原始考勤记录03excel表
    """    
    kaolist = read_raw_03(path)
    kaolist = div_time_col(kaolist)   
    kaolist.sort(cmp=kaolist_cmp)
    return kaolist

def read_raw_03(path):
    "读取原始考勤记录，不做任何处理"
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
    返回：
    kaolist = [ [kao_number,name,department,date,workstart,workleave],]
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
    
def kaolist_cmp(x,y):
    "考勤列表排序"
    if x[0]!=y[0]:
        return cmp(x[0],y[0])
    else:
        xdate=datetime.strptime(x[3],"%Y/%m/%d").date()
        ydate=datetime.strptime(y[3],"%Y/%m/%d").date()
        return cmp(xdate,ydate)


class KaoRecord(object):
    "处理每条考勤记录"
    def __init__(self,kao_number,workstart,workleave,kaodate,workshift,day_type,overtime_from_date):
        """
        传入参数
        ========================================================
        
        kao_number: 员工考勤号，"1105"字符串格式
        workstart: 上班打卡时间,格式："8:30" 字符串，如果是"8:30:00"有秒的形式，会丢弃秒信息
        workleave: 下班打卡时间,格式："17:50" 字符串
        kaodate: 考勤日期。"2015/10/1" 字符串
        workshift: 工作类型，字符串类型。例如 Flexible 或8:30-17:30 ，能够解析的是"8:30-17:30",凡是不能解析的，都按照Flexible处理。
        day_type: one of ["workday","restday","8:30-17:50")]，表示当天的类型。如果是"workday"，即表示正常工作日，作息时间按照workshift规定进行计算。
                  如果是"restday"即，表示休息日，不计算考勤。如果是"8:30-17:50"类型，则忽略workshift，按照day_type进行计算。
        @Function: overtime_from_date(kao_number,date) return '2:10:00': 用于从日期获取加班，在计算迟到时会计算[上一个]工作日加班情况，由当前行不能获取该信息，所以由外部提供该函数。
                   接收的参数:kao_number格式为字符串的考勤号；date格式为:"2015/10/9"字符串
        
        外部应该调用的函数
        ========================================================
        
        get_late_team():       返回迟到时间_团队部分。格式："3:20" 字符串
        get_late_person():     返回迟到时间_个人部分。格式: "3:20" 字符串
        get_note():            返回注释，如restday(表示休息日),not work(表示旷工),single(表示漏打卡)等等。格式:字符串
        get_over_time():       返回加班时间。格式: "3:20"字符串
        get_workspan():        返回工作时长。格式: "8:20"字符串
        get_early_leave()      返回早退时长。格式："2:20"字符串
        get_sub_sequence()     返回迟到等级。late1：15分钟以下;late2:15分钟-1个小时;late3:1-2小时;late4:2小时以上;其他返回NotNormal(不正常)。格式:字符串
        
        """
        self.kao_number= kao_number
        self.day_type = day_type
        self.workshift = workshift
        self.workstart = workstart
        self.workleave = workleave
        self.kaodate = kaodate
        self.overtime_from_date= overtime_from_date
    
    def get_workspan(self):
        "返回工作时长，格式：'8:20'字符串"
        if self.workstart == '':
            return ''
        elif self.workstart == self.workleave:
            return ''
        else:
            workstart = Time.strptime(self.workstart)
            workleave = Time.strptime(self.workleave)
            if workstart <=Time(12,30):
                morning = Time(12,30)-workstart
                afternoon = workleave - Time(13,30)
                return str( morning+afternoon)
            elif workstart >Time(1,30):
                return str( workleave - workstart )
            else:
                return str( workleave -Time(1,30) )

    def get_note(self):
        "返回注释，如restday(表示休息日),not work(表示旷工),single(表示漏打卡)等等。格式:字符串"
        if self.day_type=="restday":
            return "restday"
        elif self.workstart=='' and self.get_sud_start()!= '':
            return "not work"
        elif self.workstart != '' and self.workstart == self.workleave:
            return 'single'  
        else:
            return ''
    
    def get_late_time(self):
        "内部调用，计算迟到时间"
        if self.day_type=="restday":
            return ''
        sud_start=self.get_sud_start()
        if sud_start =='':
            return ''
        workstart = Time.strptime(self.workstart)
        sud_start = Time.strptime(sud_start)
        if self.is_lastday_valid_overtime() and sud_start<Time(10):
            #非周末加班,10点上班
            sud_start=Time(10)
        late = workstart - sud_start
        return str(late)
    
            
    def get_late_team(self):
        '返回迟到时间_团队部分。格式："3:20" 字符串'
        late = Time.strptime(self.get_late_time())
        if late>Time(0,15):
            return str(late-Time(0,15))

    def get_late_person(self):
        '返回迟到时间_个人部分。格式: "3:20" 字符串'
        late =Time.strptime( self.get_late_time() )
        if Time(0,15)<=late<=Time(1):
            return str( late-Time(0,15))
        elif Time(1)<=late <Time(2):
            return str( (late-Time(0,15))*2)
        elif Time(2)<=late:
            return str( (late-Time(0,15))*3)
        else:
            return ''
    
    def get_over_time(self):
        '返回加班时间。格式: "3:20"字符串'
        if self.day_type != "restday":
            workleave = Time.strptime(self.workleave)
            return str( workleave-Time(20) )
        else:
            return ''

    def get_early_leave(self):
        '返回早退时长。格式："2:20"字符串'
        if self.day_type =="restday":
            return '' 
        if self.workleave =='':
            return ''
        sud_leave = self.get_sud_leave()
        if sud_leave =='':
            return ''
        else:
            sud_leave = Time.strptime(sud_leave)
            workleave = Time.strptime(self.workleave)
            return str( sud_leave-workleave)

    def get_sud_leave(self):
        "内部调用，计算个人上班结束的时间"
        if self.day_type=="workday":
            mt = re.match(r"(.*)-(.*)",self.workshift)
            if mt:
                return mt.group(2)
            else:
                return ''
        elif day=="restday":
            return ''
        else:
            mt=re.match(r"(.*)-(.*)",self.day_type)
            if mt:
                return mt.group(2)
            else:
                raise ValueError("day_type must be one of ['workday','restday','8:50-17:50'...]")

    def get_sud_start(self):
        """
        内部调用，计算个人应该上班的时间
        1.判断是否正常工作日，如果是，则解析workshift，解析成功则返回group(1),否则属于弹性工作制
        2.如果是休息日，返回空
        3.如果是手动定义的特殊工作时间，则解析，如果解析不成功，则报错
        """
        
        if self.day_type=="workday":
            mt = re.match(r"(.*)-(.*)",self.workshift)
            if mt:
                return mt.group(1)
            else:
                return ''
        elif self.day_type == "restday":
            return ''
        else:
            mt=re.match(r"(.*)-(.*)",self.day_type)
            if mt:
                return mt.group(1)
            else:
                raise ValueError("day_type must be one of ['workday','restday','8:50-17:50'...]")
    
    def get_sub_sequence(self):
        "迟到标记：late1 迟到<15分钟，late2:迟到<1个小时，late3:迟到<2个小时,late4:迟到>2个小时"
        if self.day_type == "restday":
            return ''
        elif self.workleave == self.workstart:
            return ''
        late = Time.strptime( self.get_late_time() )
        if late ==Time(0):
            return ''
        elif Time(0)< late <= Time(0,15):
            return "late1"
        elif Time(0,15)< late <=Time(1):
            return "late2"
        elif Time(1)< late <= Time(2):
            return "late3"
        elif Time(2)< late :
            return "late4"
        else:
            return 'NotNormal'

    def is_lastday_valid_overtime(self):
        "查看昨天是否非周末加班，overtime_from_date(date) return overtime"
        lastday = datetime.strptime(self.kaodate,"%Y/%m/%d").date() - timedelta(days =1)
        lastovertime = Time.strptime( self.overtime_from_date(self.kao_number,lastday.strftime("%Y/%m/%d")) )
        if lastday.weekday() in [0,1,2,3] and lastovertime!=Time(0):
            return True
        else:
            return False
        
    
if __name__ =='__main__':
    def func(kao_number,date_):
        if date_ == date(2015,10,8):
            return str(Time(0,5))
        return ""

    obj =KaoRecord(kao_number="1001", workstart="9:30", workleave="17:50", kaodate="2015/10/9", workshift="8:30-17:30",day_type="workday",overtime_from_date=func)
    print( obj.get_early_leave() )
    print(obj.get_over_time())
    print(obj.get_workspan())
    print(obj.get_late_person())
    print(obj.get_sub_sequence())
    
    #kaolist1= [['1001',"name1","dp1","2015/9/10","8:30","17:50"],
               #['1001',"name1","dp1","2015/9/9","9:20","17:40"],
               #["1000","name2","dp1","2015/9/20","9:30","17:50"]]
    #print(kaolist1)
    #kaolist1.sort(cmp=kaolist_cmp)
    #print(kaolist1)
