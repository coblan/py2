# -*- encoding:utf8 -*-
"""
用途
=================================================
【月考勤记录】，【月考勤统计】的相关算法。

月考勤记录
------------------------------
1. get_worktimes()获取员工规定的工作时段。
        在该函数，以workshift为基准，过滤掉请假，加班调休，中午休息等情况，最后剩下员工应该遵守的当日工作作息时间。
        例如：workshift="8:30-17:30",过滤掉中午12:30-13:30后，得到["8:30-12:29","13:31-17:30]的工作时段
2. time_range(worktimes),获取员工应该上班和下班的时间
3. 结合以上信息，调用各种get_...函数，得到各个计算项

月考勤统计
------------------------------
1. 调用各种report_...函数获取统计项

其他
===============================================
1. mytime.Time类，用于包装时间(内部具有hour,minute)，实现加，减，数乘运算。如果运算后为负，则返回Time(0)。
   Time.__str__产生格式为:"8:30",Time.strptime()接收"8:30"格式字符串，生成Time对象。Time(hour=8,minute=20)也可以生成Time对象


"""
import re
from datetime import datetime,date,timedelta
from mytime import Time

# 辅助函数
def is_workday(date_):
    """判断是否工作日，
    
    Args:
    @date_:字符串，当天的日期，例如："2015/09/11"
    
    Return:
    @tuple[0]:布尔值，表示是否是工作日
    @tuple[1]:字符串，作息时间段
    
    说明：
    如果返回：(True,'')，则认为是普通的工作日
              (True,'10:00-17:00'),则按照给定的时间段计算迟到
    
    """
    date_obj = datetime.strptime(date_, "%Y/%m/%d")
    # ----9 月份的特殊------------
    reg_str = date_obj.strftime("%Y/%m/%d")
    prefix = r'2015/09/'
    if reg_str in [prefix+x for x in ['03','04']]:
        return False,''
    elif reg_str in [prefix+x for x in ['06']]:
        return True,''
    # -------------------------------
    if date_obj.weekday() in [0,1,2,3,4]:         #星期一到星期五是工作日
        return True,""
    else:
        return False,''



# 计算考勤记录

def i2t(second):
    if second>0:
        return "%02d:%02d"%(second/60,second%60)
    else:
        return ''
    
def t2i(tstr):
    if not tstr:
        return 0
    else:
        ls = tstr.split(':')
        return int(ls[0])*60+int(ls[1])

def i2day(hours):
    if hours == 0:
        return ''
    else:
        return hours/8.0


    
def get_worktimes(workshift="8:30-17:30",continueday_overtime="",leave=[],noonrest="12:31-13:29"):
    """获取该员工应该遵守的工作时间表
    
    Args:
        @workshift: 字符串，员工作息，格式"8:30-17:30"或者Flexible
        @continueday_overtime:字符串，上一个连续工作日的加班时间，格式："1:20"
        @leave:字符串列表，当天的请假时间段，格式：["8:30-10:30","14:00-15:00"]
        @noonrest:字符串，中午休息，格式"12:30-13:30"
        
    Return:
        @worktimes:字符串列表，该员工应该遵守的工作时间表，格式：["8:30-12:20","13:30-17:30"]
    """
    worktimes = workshift_to_worktimes(workshift)
    worktimes = filter_noonrest(worktimes, noonrest)
    worktimes = filter_continueday_overtime(worktimes, continueday_overtime)
    worktimes = filter_leave(worktimes, leave)
    return worktimes

def workshift_to_worktimes(workshift):
    """
    根据员工的workshift信息，处理worktimes
    Args:
    @workshift:字符串，员工作息，格式："8:30-17:30"
    Return:
    @worktimes:字符串列表，该员工应该遵守的工作时间表，格式：["8:30-12:20","13:30-17:30"]
    """
    worktimes = []
    mt = re.match(r"(.*)-(.*)",workshift)
    if mt:
        worktimes.append(workshift)
    else:                            # 解析不了都当成 Flexible
        pass                
    return worktimes

def filter_noonrest(worktimes, noonrest):
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

def filter_continueday_overtime(worktimes, continueday_overtime):
    """
    @continueday_overtime:字符串，前一个连续工作日的加班时间，格式："1:30",
                           为""空是，表示没加班
    """
    # overtime = Time.strptime(continueday_overtime)
    tmp_worktimes = []
    if continueday_overtime == 0:                # 没加班,就不需要过滤时间段了
        tmp_worktimes = worktimes
    elif 0< continueday_overtime <= 120:
        for span in worktimes:
            tmp_worktimes.extend(subtract(span, "6:00-9:59"))      # 把6:00-10：00的时间段去掉，就相当于让员工从10点开始上班了
    else:
        for span in worktimes:
            tmp_worktimes.extend(subtract(span,"6:00-12:59"))       # 暂时预估，下午上班时间不会早于12:59
    worktimes = tmp_worktimes
    return worktimes

def filter_leave(worktimes, leave):
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
    """查询时间段列表的起始时刻
    Args:
    @worktimes:时间段列表
    
    Return:
    start,end:时间段列表的开始，结束时间。格式:"8:30","17:30"
    """
    if worktimes == []:
        return -1,-1
    else:
        start = worktimes[0].split("-")[0]
        end = worktimes[-1].split("-")[1]
        return t2i(start),t2i(end)

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
    if sud_start==0:
        return 0
    elif workstart ==0:
        return 0     # 没打卡记录，算旷工一天，旷工后，不计算其迟到了
    else:
        return max(0, workstart-sud_start)
    
    
    # late = ''
    # if sud_start == '':
        # late = ''
    # else:
        # sud_start = Time.strptime(sud_start)
        # workstart_time =Time.strptime(workstart)
        # late = str(workstart_time - sud_start)
    # return late

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
    if 0<=late<=15:
        return 0
    else:
        return late-15
    
    # late_team = ''
    # late_time = Time.strptime(late)
    # if Time(0) <= late_time <= Time(0,15) :
        # late_team = ''
    # else:
        # late_team = str(late_time-Time(0,15))
    # return late_team

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
    if 0<=late<=15:
        return 0
    elif 15<late<=60:
        return late-15
    elif 60<late<=120:
        return (late-15)*2
    elif 120<late:
        return (late-15)*3
    else:
        raise ValueError('late range error')
    # late_person = ''
    # late_time = Time.strptime(late)
    # if Time(0) <= late_time <= Time(0,15):
        # late_person = ''
    # elif Time(0,15) < late_time <=Time(1):
        # late_person = str(late_time - Time(0,15))
    # elif Time(1)< late_time <= Time(2):
        # late_person = str( (late_time-Time(0,15))*2 )
    # else:
        # late_person = str( (late_time-Time(0,15))*3 )
    # return late_person

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
    if 0<late<=15:
        return 'late1'
    elif 15<late<=60:
        return 'late2'
    elif 60<late<=120:
        return 'late3'
    elif 120<late:
        return 'late4'
    else:
        return ''
    # late_level = ''
    # late_time = Time.strptime(late)
    # if late_time == Time(0):
        # late_level = ''
    # elif Time(0) < late_time <= Time(0,15):
        # late_level = 'late1'
    # elif Time(0,15) < late_time <=Time(1):
        # late_level = 'late2'
    # elif Time(1)< late_time <= Time(2):
        # late_level = 'late3'
    # else:
        # late_level = 'late4'
    # return late_level   

def get_overtime(workshift,workstart,workleave):
    """计算工作日加班时长
    
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
    if workshift.lower()!="flexible":
        return max(0, workleave-20*60) # 减去晚上8点
    else:
        return 0
    # overtime = ''
    # workstart_time = Time.strptime(workstart)
    # workleave_time = Time.strptime(workleave)
    # if workshift.lower()!="flexible":
        # overtime = str( workleave_time - Time(20) )         # 普通员工工作日加班
    # else:
        # overtime =''
    # return overtime

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
    if sud_leave==0:
        return 0
    elif workleave ==0:
        return 0    # 没有打卡记录的情况，算作旷工，不算早退
    else:
        return max(0, sud_leave- workleave)
    # if sud_leave=='':
        # early_leave = ''
    # else:
        # workleave_time = Time.strptime(workleave)
        # sud_leave = Time.strptime(sud_leave)
        # early_leave= str(workleave_time-sud_leave)
    # return early_leave

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
    return max(0, workleave-workstart -60) # 扣掉中午的一个小时
    # workstart =Time.strptime(workstart)
    # workleave = Time.strptime(workleave)
    # return str(workleave - workstart- Time(1))

def get_absent(workstart,workleave):
    """获取旷工小时数
    
    Args:
    @workstart:字符串，上班时间
    @workleave:字符串，下班时间
    
    Return:
    旷工小时数
    """
    if workstart ==0:
        return 8
    elif workstart == workleave:
        return 4
    else:
        return 0
    # if Time.strptime(workstart) == Time(0):   #没有打卡记录
        # return 8
    # elif Time.strptime(workstart) == Time.strptime(workleave): # 只有一次打卡记录
        # return 4
    # else:
        # return 0

# --------------------------------------------------------------------------------------------------------------------------
# 计算考勤统计表

def report_max_workhours(days):
    """
    所有员工中，当月应该上班的最大天数。
    普通员工应该上班的天数一般都是最大天数，
    但是新入职的员工，却不是
    """
    cnt=0
    for day in days:
        workday,_ =is_workday(day)
        if workday:
            cnt+=1
    return cnt*8    

def report_expect_workhours(days,empid):
    """根据员工id，日期，计算员工应该上班的天数
    例如，9月7日入职的员工，他应该上班的时间就不包括9.1-9.6
    """
    cnt=0
    for day in days:
        workday,_ =is_workday(day)
        if workday:
            cnt+=1
    return cnt*8

def report_act_workhours(exp_workhours,person_leave,sick_leave,absent):
    """实际工作小时数
    @exp_workday:应该上班的天数
    """
    return exp_workhours - person_leave - sick_leave - absent

def report_allow_hours(exp_workhours,allow_sub_hours):
    """补贴小时数
    """
    return exp_workhours - allow_sub_hours

def report_allow_sub_hours(person_leave,sick_leave,annual_leave,other_paid_leave,over_late3_days):
    """补贴扣除天数
    """
    return person_leave+sick_leave+annual_leave+other_paid_leave+over_late3_days*8

def report_leave_hours(person_leave,sick_leave,annual_leave,other_paid_leave,swap_off):
    """请假总天数
    """
    return person_leave+sick_leave+annual_leave+other_paid_leave+swap_off

def report_paid_leave(annual_leave,other_paid_leave):
    """所有带薪假小时数
    """
    return annual_leave+other_paid_leave

def report_full_attend(worktype,workshift,exp_workhours,max_workhours,person_leave,sick_leave,paid_leave,late_all,absent,early_leave):
    """是否全勤
    """
    if worktype !="FTE":
        return False
    elif workshift == 'Flexible':
        return False
    elif exp_workhours < max_workhours:
        return False
    elif person_leave+sick_leave > 0 :
        return False
    elif paid_leave >5*8:
        return False
    elif late_all > 0:
        return False
    elif absent>0:
        return False
    elif early_leave >0:
        return False
    else:
        return True

def report_deduction(absent):
    """扣款小时数
    """
    return absent

def report_process(late_cnt,late_act_times,absent):
    """考勤处理结果
    """
    if absent>0:
        return u'书面警告'
    elif 6>=late_cnt>3 and late_act_times >120:
        return u'口头警告'
    elif 6< late_cnt and 240<late_act_times:
        return u'书面警告'
    else:
        return ''

    
#---------------------------------------------------------------------------------------------------------------------------
#测试


if __name__ =='__main__':
    import unittest
    class RecordTest(unittest.TestCase):
        def test_subtract(self):
            self.assertEqual(subtract("8:30-12:30","10:30-12:30"),["8:30-10:29"])    # 后端临界
            self.assertEqual(subtract("8:30-12:30","8:30-10:30"),["10:31-12:30"])     # 前段临界
            self.assertEqual(subtract("8:30-12:30","8:30-12:30"),[])     # 前后临界
            self.assertEqual(subtract("8:30-12:30","9:00-11:00"),["8:30-8:59","11:01-12:30"])     # 中间段
            
            # 下面是不太可能出现的情况，
            self.assertEqual(subtract("8:30-12:30","13:30-17:30"),['8:30-12:30'])    # 不相交
            self.assertEqual(subtract("13:30-17:30", "8:30-12:30"),['13:30-17:30'])
            
            self.assertEqual(subtract("8:30-12:30","9:30-13:30"),["8:30-9:29"]) 
            self.assertEqual(subtract("13:31-17:30","16:00-17:30"),["13:31-15:59"])  
            
        def test_filter_leave(self):
            self.assertEqual(filter_leave(["8:30-12:30","13:30-17:30"], ["9:00-11:00"]),["8:30-8:59",'11:01-12:30',"13:30-17:30"])
            self.assertEqual(filter_leave(["8:30-12:30","13:30-17:30"],["9:00-16:00"]),['8:30-8:59','16:01-17:30'])  
            
        def test_fiter_noonrest(self):
            self.assertEqual(filter_noonrest(["8:30-17:30"],"12:30-13:30"),["8:30-12:29","13:31-17:30"])   
            
        def test_filter_overtime(self):
            self.assertEqual(filter_continueday_overtime(["8:30-12:30","13:30-17:30"],"1:30"),["10:00-12:30","13:30-17:30"])   
            
        def test_get_worktimes(self):
            self.assertEqual(get_worktimes(),['8:30-12:30','13:30-17:30'])
            self.assertEqual(get_worktimes(continueday_overtime="2:30"),["13:30-17:30"])
            self.assertEqual(get_worktimes(leave=["9:00-11:00","16:00-17:30"]),['8:30-8:59',"11:01-12:30","13:30-15:59"])
            self.assertEqual(get_worktimes(leave=["13:30-17:30"],continueday_overtime="2:30"),[])  
        
            
    unittest.main()
    # print( i2t(100) )
    # print(t2i("8:30"))
    # print(i2t(510))