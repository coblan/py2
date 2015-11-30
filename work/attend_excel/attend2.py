# -*- encoding:utf8 -*-
"""
用途
=================================================

读取考勤原始记录，配合TMS系统，计算个人考勤情况。


使用步骤
=================================================

1. 调用get_attend_list(path)生成经过日期排序的考勤列表。
2. 遍历考勤列表，
3. 结合TMS提供的信息，调用各种get_函数，计算该条考勤记录其他信息。
4. 保存到数据库。

使用例子:
=================================================

#从考勤原始记录中获取按日期排序的考勤记录
attendlist=get_attend_list(r"D:\myfile\kaoqin_2015_9.xls")
#遍历考勤列表，依次处理记录，并保存到数据库
for i in attendlist:
    # attendlist能提供的数据有：
    #    考勤号或员工姓名
    #    date_:记录的日期
    #    workstart:上班打卡时间
    #    workleave:下班打卡时间
    # 他们的index，见get_attend_list()
        
    # 此外还需要提供:
    #    is_workday()需要：
    #        maps:日期映射表，详情见函数：
    #    get_worktimes()需要:
    #        continueday_overtime:上一个连续工作日加班情况，默认没加班
    #        leave:当日，请假时间段，默认没请假
    #        noonrest：中午休息时段，有默认值
    
    workday,workshift = is_workday(date_,maps)
    
    if workday:
        if workshift == '':   #表示正常工作日
            workshift = TMS中获取员工的规定作息
        worktimes = get_worktimes(workshift,continueday_overtime="",leave=[],noonrest="12:30-13:30")
        sud_start,sud_leave = time_range(worktimes)
        late = get_late_time(sud_start,workstart)
    
        late_person = get_late_person(late)
        late_team = get_late_team(late)
        sub_sequence = get_sub_sequence(late)
        early_leave = get_early_leave(sud_leave,workleave) 
        workspan = get_workspan(workstart,workleave)
        overtime = get_overtime(workshift,workstart,workleave)
        absent = get_absent(workstart,workleave)
    else:
        late_person = ''
        late_team = ''
        sub_sequence = ''
        early_leave = ''  
        workspan = workleave - workstart
        overtime = workleave - workstart
        absent = 0
    
    # 根据考勤号或姓名，保存到TMS数据库
    TMS.save_everything()


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

def is_workday(date_,maps):
    """判断是否工作日，
    
    Args:
    @date_:字符串，当天的日期，例如："2015/09/11"
    @maps:工作日字典，表示工作日的作息，注意月与日期需要补零。
           例如：
           maps = {
                '2015/11/09':'',
                '2015/11/10':'',
                '2015/11/11':'10:00-17:30',
           }
           如果值为空字符串，则表示正常工作日，后面计算迟到早退，按照TMS中员工固定的workshift
           如果值为时间段，则表示特殊作息日，后面计算迟到早退，按照该时间段计算。
    
    Return:
    @tuple[0]:boolean，表示是否是工作日
    @tuple[1]:字符串，作息时间段
    
    """
    if date_ in maps:
        return True,maps[date_]
    else:
        return False,''
    
def get_worktimes(workshift="8:30-17:30",continueday_overtime="",leave=[],noonrest="12:30-13:30"):
    """获取该员工应该遵守的工作时间表
    
    Args:
        @workshift: 字符串，员工作息，格式"8:30-17:30"或者Flexible
        @continueday_overtime:字符串，上一个连续工作日的加班时间，格式："1:20"
        @leave:字符串列表，当天的请假时间段，格式：["8:30-10:30","14:00-15:00"]
        @noonrest:字符串，中午休息，格式"12:30-13:30"
        
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

def time_range(worktimes):
    if worktimes == []:
        return '',''
    else:
        start = worktimes[0].split("-")[0]
        end = worktimes[-1].split("-")[1]
        return start,end

def subtract(src,target):
    """时间段src减去target时间段
    
    Args:
        @src:字符串，源时间段，格式："8:30-12:30"
        @target:字符串，目标段，格式："10:30-12:30"
    Return:
        @timespan:字符串列表，src与target相减后的时间段，例如：["8:30-10:29",]
    
    计算规则：
    从src时间段中过滤掉target中的时间段
    例如：
    如果src: "8:30-17:30" ,target: "12:30-13:30" 相减后得:["8:30-12:29","13:31-17:30]
    如果src: "8：30-17:30",target:"13:30-17:30",相减后得:["8:30-13:29"]
    
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

def get_late_time(sud_start,workstart):
    """
    Args:
    @sud_start，字符串，should start,某员工合乎规定的上班时间，例如："8:30"
    @workstart,字符串，某员工当天第一次打卡的时间，例如："8:20"
    
    Return:
    @late,字符串,员工当天的迟到时间，例如:"1:20"
    """
    late = ''
    if sud_start == '':
        late = ''
    else:
        sud_start = Time.strptime(sud_start)
        workstart_time =Time.strptime(workstart)
        late = str(workstart_time - sud_start)
    return late

def get_late_team(late):
    """计算迟到引起的团队迟到时间
    
    Args:
    @late:字符串，迟到时间，例如："1:20"
    
    Return:
    @late_team:字符串，迟到引起的团队迟到时间，例如:"1:20"
    
    计算规则：
    1. 迟到时间 <= 15分钟，不计算团队迟到时间
    2. 迟到时间 > 15分钟的部分，全部计入团队迟到时间
    """
    late_team = ''
    late_time = Time.strptime(late)
    if Time(0) <= late_time <= Time(0,15) :
        late_team = ''
    else:
        late_team = str(late-Time(0,15))
    return late_team

def get_late_person(late):
    """计算迟到引起的个人迟到时间
    
    Args:
    @late:字符串，迟到时间，格式："1:20"
    
    Return:
    @late_person:字符串，迟到引起的个人迟到时间，例如："1:20"
    
    计算规则：
    1. 迟到<=15分钟，不计算个人迟到时间
    2. 15分钟< 迟到<=1个小时，扣除最初的15分钟，后面的时间全部累积到个人迟到时间
    3. 1个小时<迟到<=2个小时，扣除最初的15分钟，后面的时间*双倍*累积到个人迟到时间
    4. 迟到>2个小时，扣除最初的15分钟，后面的时间*三倍*累积到个人迟到时间
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
    """计算迟到等级
    Args:
    @late:字符串，迟到时间，格式："1:20"
    
    Return:
    @late_level，字符串，表示迟到等级，有：late1,late2,late3,late4
    
    计算规则:
    late1:迟到15分钟以内
    late2:迟到16分钟-60分钟
    late3:迟到61分钟-90分钟
    late4:迟到91分钟以上
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

def get_overtime(workshift,workstart,workleave):
    """计算加班时长
    
    Args:
    @workshift:字符串，员工的作息类型，例如："Flexibale","8:30-17:30"
    @workstart:字符串,该员工有效的第一次打卡时间，例如:"8:26"
    @workleave:字符串,该员工有效的最后一次打卡时间，例如:"18:20"
    
    Return:
    @overtime:字符串，加班时长，例如:"5:30"
    
    计算规则：
    工作日：
    1. 弹性工作员工，不计算加班
    2. 普通员工，从20：00后开始计算加班时长
    非工作日：
    以第一次打卡到最后一次打卡的时长，作为加班时间
    """
    overtime = ''
    workstart_time = Time.strptime(workstart)
    workleave_time = Time.strptime(workleave)
    if workshift.lower()!="flexible":
        overtime = str( workleave_time - Time(20) )         # 普通员工工作日加班
    else:
        overtime =''
    return overtime

def get_early_leave(sud_leave,workleave):
    """
    Args:
    @sud_leave:字符串，该员工合乎规定的下班时间，例如:"17:30"
    @workleave:字符串,该员工有效的最后一次打卡时间，例如:"18:20"
    
    Return:
    @early_leave:字符串，员工的早退时间，例如："1:20"
    
    计算规则：
    最后打卡时间 - 规定作息时间段，最后一段的结束时间
    """    
    if sud_leave=='':
        early_leave = ''
    else:
        workleave_time = Time.strptime(workleave)
        sud_leave = Time.strptime(sud_leave)
        early_leave= str(workleave_time-sud_leave)
    return early_leave

def get_workspan(workstart,workleave,worktimes=''):
    """
    Args:
    @workstart,字符串，上班打卡时间
    @workleave,字符串，下班打卡时间
    @worktimes,字符串，规定的员工作息时间段，现在没用，考虑以后会精细计算员工工作时长，考虑从工作时长中，扣除中途请假
                等情况。所以，调用该函数时，最好传入 worktimes。
                
    计算规则：
    下班打卡时间 - 上班打卡时间 - 中午午休1个小时
    """
    return str(workleave - workstart- Time(1))

def get_absent(workstart,workleave):
    """获取旷工小时数
    
    Args:
    @workstart:字符串，上班时间
    @workleave:字符串，下班时间
    
    Return:
    旷工小时数
    """
    if Time.strptime(workstart) == Time(0):   #没有打卡记录
        return 8
    elif Time.strptime(workstart) == Time.strptime(workleave): # 只有一次打卡记录
        return 4
    else:
        return 0

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
