# -*- encoding:utf8 -*-
"""
用途
=================================================

读取考勤原始记录，配合TMS系统，计算个人考勤情况。


使用步骤
=================================================

1. 调用get_attend_list(path)生成经过日期排序的考勤列表。
2. 遍历考勤列表，
3. 结合TMS提供的信息，生成AttendRecord()对象，调用各种get_函数，计算该条考勤记录其他信息。
4. 保存到数据库。


使用例子:
=================================================

#从考勤原始记录中获取按日期排序的考勤记录
attendlist=get_attend_list(r"D:\myfile\kaoqin_2015_9.xls")
#遍历考勤列表，依次处理记录，并保存到数据库
for i in attendlist:
    # 生成一个处理记录的对象。其中: TMS.overtime_from_date(record_date) return "3:20"格式，即认为加班，如果为空字符串，即认为没加班。该函数由外部提供
    row = AttendRecord(attend_number=i[0],workstart=i[4],workleave=i[5],record_date=i[3].strftime("%Y/%m/%d"),day_type="workday",overtime_from_date=TMS.overtime_from_date)
    # TMS.save()用于保存到TMS数据库
    TMS.save(kaonumber=row.attend_number, late_person =row.get_late_person(),....)


其他
===============================================
1. mytime.Time类，用于包装时间(内部具有hour,minute)，实现加，减，数乘运算。如果运算后为负，则返回Time(0)。
   Time.__str__产生格式为:"8:30",Time.strptime()接收"8:30"格式字符串，生成Time对象。Time(hour=8,minute=20)也可以生成Time对象
2. xlrd库用于读取03excel文件

"""
import re
from datetime import datetime,date,timedelta
import xlrd
from mytime import Time

 
def get_attend_list(path):
    """ 返回一个按照 考勤号，日期 排序的列表。
         attendlist = [ [attend_number,name,department,record_date,workstart,workleave],
                     [考勤号，名字，部门，日期，上班打卡时间，下班打卡时间]]
    path: 原始考勤记录03excel表
    """    
    attendlist = read_excel_03(path)
    attendlist = div_time_col(attendlist)   
    attendlist.sort(cmp=kaolist_cmp)
    return attendlist

def read_excel_03(path):
    "读取原始考勤记录，不做任何处理"
    rawdata = xlrd.open_workbook(path,encoding_override='gbk')
    table = rawdata.sheets()[0]
    nrows = table.nrows
    attendlist = []
    for i in range(1, nrows):
        attendlist.append(table.row_values(i))
    return attendlist

def div_time_col(attendlist):
    """分割时间字符串栏
    attendlist = [ [attend_number,name,department,record_date,timestr],]
    返回：
    attendlist = [ [attend_number,name,department,record_date,workstart,workleave],]
    """
    for row in attendlist:
        start,end=find_min_max(row[4])
        row[4]=start
        row.append(end)
    return attendlist

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

#
# 辅助函数

def get_worktimes(workshift="8:30-17:30",noonrest="12:30-13:30",continueday_overtime="",leave=[]):
    """获取该员工应该遵守的工作时间表
    
    Args:
        @workshift: 字符串，员工作息，格式"8:30-17:30"或者Flexible
        @noonrest:字符串，中午休息，格式"12:30-13:30"
        @continueday_overtime:字符串，上一个连续工作日的加班时间，格式："1:20"
        @leave:字符串列表，当天的请假时间段，格式：["8:30-10:30","14:00-15:00"]
        
    Return:
        @worktimes:字符串列表，该员工应该遵守的工作时间表，格式：["8:30-12:20","13:30-17:30"]
    """
    worktimes = []
    worktimes = filter_workshift(workshift,worktimes)
    worktimes = filter_noonrest(noonrest, worktimes)
    worktimes = filter_continueday_overtime(continueday_overtime, worktimes)
    worktimes = filter_leave(leave, worktimes)
    return worktimes

def filter_workshift(workshift,worktimes):
    """
    根据员工的workshift信息，处理worktimes
    
    @workshift:字符串，员工作息，格式："8:30-17:30"
    @worktimes:字符串列表，该员工应该遵守的工作时间表，格式：["8:30-12:20","13:30-17:30"]
    """
    mt = re.match(r"(.*)-(.*)",workshift)
    if mt:
        worktimes.append(workshift)
    else:                            # 解析不了都当成 Flexible
        pass                
    return worktimes

def filter_noonrest(noonrest,worktimes):
    """
    从worktimes中过滤掉中午休息时间，然后返回worktimes
    
    @noonrest:字符串，中午休息时间段，格式："12:30-13:30"
    @worktimes:字符串列表，该员工应该遵守的工作时间表，格式：["8:30-12:20","13:30-17:30"]
    """
    tmp_worktimes = []
    for span in worktimes:
        tmp_worktimes.extend(subtract(span, noonrest))
    worktimes = tmp_worktimes
    return worktimes

def filter_continueday_overtime(continueday_overtime,worktimes):
    """
    @continueday_overtime:字符串，前一个连续工作日的加班时间，格式："1:30",
                           为""空是，表示没加班
    """
    overtime = Time.strptime(continueday_overtime)
    tmp_worktimes = []
    if overtime == Time(0):                # 没加班,就不需要过滤时间段了
        tmp_worktimes = worktimes
    elif Time(0)< overtime <Time(2):
        for span in worktimes:
            tmp_worktimes.extend(subtract(span, "6:00-10:00"))      # 把6:00-10：00的时间段去掉，就相当于让员工从10点开始上班了
    else:
        for span in worktimes:
            tmp_worktimes.extend(subtract(span,"6:00-13:00"))       # 暂时预估，下午上班时间不会早于13：00
    worktimes = tmp_worktimes
    return worktimes

def filter_leave(leave,worktimes):
    """
    从worktimes中过滤掉员工请假的时间，然后返回worktimes
    
    @leave:字符串列表，当天的请假时间段，格式：["8:30-10:30","14:00-15:00"]
    """
    tmp_worktimes = worktimes
    for lev in leave:
        tmp_worktimes = []
        for span in worktimes:
            tmp_worktimes.extend(subtract(span, lev))
        worktimes = tmp_worktimes
    worktimes = tmp_worktimes
    return worktimes

def subtract(src,target):
    """时间段src减去target时间段
    
    Args:
        @src:字符串，源时间段，格式："8:30-12:30"
        @target:字符串，目标段，格式："10:30-12:30"
    Return:
        @timespan:字符串列表，src与target相减后的时间段，例如：["8:30-10:29",]
    """
    src_start =Time.strptime(src.split("-")[0])
    src_end = Time.strptime(src.split("-")[1])
    target_start = Time.strptime(target.split("-")[0])
    target_end = Time.strptime(target.split("-")[1])
    span=[]
    if src_start < target_start:
        if src_end < target_start:
            span.append((src_start,src_end))
        elif target_start <= src_end < target_end:
            span.append((src_start,target_start-Time(0,1)))     # 将请假的开始点从工作段去掉
        elif target_end == src_end:
            span.append((src_start,target_start-Time(0,1)))
        elif target_end < src_end:
            span.append((src_start,target_start-Time(0,1)))
            span.append((target_end+Time(0,1),src_end))
    elif target_start <= src_start<= target_end:
        if src_end <= target_end:     # 时间段被减完了，pass就代表就让span列表为空
            pass
        elif target_end < src_end:
            span.append((target_end+Time(0,1),src_end))
    elif target_end < src_start:
        span.append((src_start,src_end))
    
    # -----------剔除那些 5分钟内的问题时间段，因为不太可能有5分钟的工作时间段，而且还能使临界点的处理更安全
    #            如果临界点处理好了，可以考虑去掉该段代码
    timespan=[]
    for start,end in span:
        if end - start >= Time(0,5):
            timespan.append("-".join([str(start),str(end)]))
            
    timespan=["-".join([str(start),str(end)]) for start,end in span]
    return timespan
            

# 开始处理考勤表
#

def get_late_time(worktimes,workstart):
    """worktimes = ["8:30-12:30","13:30-15:30"]这种形式
    """
    late = ''
    if worktimes == []:
        late = ''
    else:
        sud_start = Time.strptime(worktimes[0].split("-")[0])
        workstart_time =Time.strptime(workstart)
        late = str(workstart_time - sud_start)
    return late

def get_late_team(late):
    """
    @late:字符串，迟到时间，格式："1:20"
    """
    late_team = ''
    late_time = Time.strptime(late)
    if Time(0) <= late_time <= Time(0,15) :
        late_team = ''
    else:
        late_team = str(late-Time(0,15))
    return late_team

def get_late_person(late):
    """
    @late:字符串，迟到时间，格式："1:20"
    """    
    late_person = ''
    late_time = Time.strptime(late)
    if Time(0) <= late_time <= Time(0,15):
        late_person = ''
    elif Time(0,15) < late_time <=Time(1):
        late_person = str(late_time - Time(0,15))
    elif Time(1)< late_time <= Time(2):
        late_person = str( (late_time-Time(0,15))*2 )
    else:
        late_person = str( (late_time-Time(0,15))*3 )
    return late_person

def get_sub_sequence(late):
    """
    @late:字符串，迟到时间，格式："1:20"
    """    
    late_level = ''
    late_time = Time.strptime(late)
    if late_time == Time(0):
        late_level = ''
    elif Time(0) < late_time <= Time(0,15):
        late_level = 'late1'
    elif Time(0,15) < late_time <=Time(1):
        late_level = 'late2'
    elif Time(1)< late_time <= Time(2):
        late_level = 'late3'
    else:
        late_level = 'late4'
    return late_level   

def get_overtime(worktimes,workstart,workleave):
    """
    @worktimes:字符串列表，该员工应该遵守的工作时间表，格式:["8:30-12:30","13:30-17:30"]
    @workstart:字符串,该员工有效的第一次打卡时间，格式:"8:26"
    @workleave:字符串,该员工有效的最后一次打卡时间，格式:"18:20"
    """
    overtime = ''
    workstart_time = Time.strptime(workstart)
    workleave_time = Time.strptime(workleave)
    if worktimes != []:
        overtime = str( workleave_time - Time(20) )         # 工作日加班
    else:
        overtime = str(workleave_time - workstart_time)       # 非工作日加班
    return overtime

def get_early_leave(worktimes,workleave):
    """
    @worktimes:字符串列表，该员工应该遵守的工作时间表，格式:["8:30-12:30","13:30-17:30"]
    @workleave:字符串,该员工有效的最后一次打卡时间，格式:"18:20"
    """    
    early_leave = ''
    workleave_time = Time.strptime(workleave)
    if worktimes==[]:
        early_leave = ''
    else:
        sud_leave = Time.strptime(worktimes[-1].split("-")[-1])
        early_leave= str(workleave_time-sud_leave)
    return early_leave


class AttendRecord(object):
    "处理每条考勤记录"
    def __init__(self,attend_number,workstart,workleave,record_date,workshift,day_type,overtime_from_date):
        """
        传入参数
        ========================================================
        
        attend_number: 员工考勤号，"1105"字符串格式
        workstart: 上班打卡时间,格式："8:30" 字符串，如果是"8:30:00"有秒的形式，会丢弃秒信息
        workleave: 下班打卡时间,格式："17:50" 字符串
        record_date: 考勤日期。"2015/10/1" 字符串
        workshift: 工作类型，字符串类型。例如 Flexible 或8:30-17:30 ，能够解析的是"8:30-17:30",凡是不能解析的，都按照Flexible处理。
                   原始的考勤列表不能提供workshift信息，所以这个信息来源于TMS或其他方式
        day_type: one of ["workday","restday","8:30-17:50")]，表示当天的类型。如果是"workday"，即表示正常工作日，作息时间按照workshift规定进行计算。
                  如果是"restday"即，表示休息日，不计算考勤。如果是"8:30-17:50"类型，则忽略workshift是非弹性工作的情况，按照day_type进行计算。
        @Function: overtime_from_date(attend_number,record_date) return '2:10:00': 用于从日期获取加班，在计算迟到时会计算[上一个]工作日加班情况，
                   由当前行不能获取该信息，所以由外部提供该函数。接收的参数:kao_number格式为字符串的考勤号；date格式为:"2015/10/9"字符串
        
        外部应该调用的函数
        ========================================================
        
        get_late_team():       返回迟到时间_团队部分。格式："3:20" 字符串
        get_late_person():     返回迟到时间_个人部分。格式: "3:20" 字符串
        get_note():            返回注释，如restday(表示休息日),not work(表示旷工),single(表示漏打卡)等等。格式:字符串
        get_over_time():       返回加班时间。格式: "3:20"字符串
        get_workspan():        返回工作时长。格式: "8:20"字符串
        get_early_leave()      返回早退时长。格式："2:20"字符串
        get_sub_sequence()     返回迟到等级。late1：15分钟以下;late2:15分钟-1个小时;late3:1-2小时;late4:2小时以上;其他返回NotNormal(不正常)。格式:字符串
        
        当前实现的处理:
        ========================================================
        1. 计算工作时长
        2. 标记非工作日，漏打卡，旷工(全天无打卡)
        3. 计算加班时长，20：00后算加班.
        4. 根据非周末的加班，调整第二天上班时间到10：00。这里只针对非弹性工作制的员工，如果员工的workshfit规定上班时间迟于10：00，则不调整。
        5. 计算早退时间。根据特殊工作作息/workshift来计算
        6. 计算迟到等级
        7. 计算团队迟到时间，根据迟到等级计算个人迟到时间
        
        """
        self.attend_number= attend_number
        self.day_type = day_type
        self.workshift = workshift
        self.workstart = workstart
        self.workleave = workleave
        self.record_date = record_date
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
        elif self.get_sud_start()=='':
            return ''
        elif self.workstart=='' and self.get_sud_start()!= '':
            return "not work"
        elif self.workstart != '' and self.workstart == self.workleave:
            return 'single'  
        else:
            return ''
    
    def get_late_time(self):
        """内部调用，计算迟到时间。
        如果是休息日，则不计算迟到时间。
        会考虑到员工前一天是否是非周末加班，如果加班，则上班时间调整到10：00，如果员工的workshfit规定上班时间迟于10：00，则不调整。
        如果员工是弹性工作制，则不计算迟到时间。
        """
        if self.day_type=="restday":
            return ''
        sud_start=self.get_sud_start()
        if sud_start =='':
            return ''
        workstart = Time.strptime(self.workstart)
        sud_start = Time.strptime(sud_start)
        if self.is_lastday_valid_overtime() and sud_start<Time(10):
            sud_start=Time(10)        #非周末加班,10点上班
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
        elif self.day_type=="restday":
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
        "查看昨天是否非周末加班，overtime_from_date(record_date) return overtime"
        lastday = datetime.strptime(self.record_date,"%Y/%m/%d").date() - timedelta(days =1)
        lastovertime = Time.strptime( self.overtime_from_date(self.attend_number,lastday.strftime("%Y/%m/%d")) )
        if lastday.weekday() in [0,1,2,3] and lastovertime!=Time(0):
            return True
        else:
            return False
        

def test_subtract():
    print(subtract("8:30-12:30","10:30-12:30"))    # 后端临界
    print(subtract("8:30-12:30","8:30-10:30"))     # 前段临界
    print(subtract("8:30-12:30","8:30-12:30"))     # 前后临界
    print(subtract("8:30-12:30","9:00-11:00"))     # 中间段
    
    # 下面是不太可能出现的情况，
    print(subtract("8:30-12:30","13:30-17:30"))    # 不相交
    print(subtract("13:30-17:30", "8:30-12:30"))
    
    print(subtract("8:30-12:30","9:30-13:30")) 
    print(subtract("13:31-17:30","16:00-17:30"))

def test_fiter_noonrest():
    print(filter_noonrest("12:30-13:30", ["8:30-17:30"]))

def test_filter_leave():
    print(filter_leave(["9:00-11:00"], ["8:30-12:30","13:30-17:30"]))
    print(filter_leave(["9:00-16:00"],["8:30-12:30","13:30-17:30"]))
def test_filter_overtime():
    print(filter_continueday_overtime("2:30", ["8:30-12:30","13:30-17:30"]))
def test_get_worktimes():
    print(get_worktimes())
    print(get_worktimes(continueday_overtime="2:30"))
    print(get_worktimes(leave=["9:00-11:00","16:00-17:30"]))
    print(get_worktimes(leave=["13:30-17:30"],continueday_overtime="2:30"))
if __name__ =='__main__':
    # test_subtract()
    # test_fiter_noonrest()
    # test_filter_leave()
    # test_filter_overtime()
    test_get_worktimes()
