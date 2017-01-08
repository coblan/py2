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
1. 所有时间均以距离00：00的分钟数来表示，例如8:30转换为-->8*60+30。
2. 所有需要外部提供的接口，见record_interface.py


"""
import re
from datetime import datetime,date,timedelta
from record_interface import is_workday

# 计算考勤记录

def i2t(second):
    """int类型转换为时间格式
    510 --> "8:30"
    """
    if second>0:
        return "%02d:%02d"%(second/60,second%60)
    else:
        return ''
    
def t2i(tstr):
    """时间格式转换为int类型
    "8:30" --> 510
    """
    if not tstr:
        return 0
    else:
        ls = tstr.split(':')
        return int(ls[0])*60+int(ls[1])

def i2day(second):
    """int类型(分钟数)转换为天，每天按照8小时计算
    该函数用于多半用于对外显示
    """
    if second == 0:
        return ''
    else:
        return second/(8.0*60)

def ts2is(src):
    """ 时间段字符串，转换为(int,int)
    "8:30-12:30"  ---> (1234,2324)
    """
    mt = re.match(r"(.*)-(.*)",src)
    if mt:
        return tuple((t2i(s) for s in src.split("-")))
    else:
        return None
    
def is2ts(ispan):
    """(int,int)转换为时间段字符串
    (1234,2324) ---> "8:30-12:30" 
    """
    if ispan:
        return "%s-%s"%(i2t(ispan[0]),i2t(ispan[1]))
    else:
        return ""
    
def get_worktimes(workshift="8:30-17:30",continueday_overtime=0,leave=[],noonrest="12:31-13:29"):
    """获取该员工应该遵守的工作时间表
    
    Args:
        @workshift: 字符串，员工作息，格式"8:30-17:30"或者Flexible
        @continueday_overtime:int类型，上一个连续工作日的加班时间
        @leave:[(int,int),]，当天的请假时间段
        @noonrest:字符串，中午休息，格式"12:31-13:29"
        
    Return:
        @worktimes:[(int,int),]，该员工应该遵守的工作时间段
    """
    worktimes = [ts2is(workshift)]
    worktimes = filter_noonrest(worktimes, ts2is(noonrest))
    worktimes = filter_continueday_overtime(worktimes, continueday_overtime)
    worktimes = filter_leave(worktimes, leave)
    return worktimes

def filter_noonrest(worktimes, noonrest):
    """
    从worktimes中过滤掉中午休息时间，然后返回worktimes
    
    @noonrest:(int,int)类型，中午休息时间段
    @worktimes:[(int,int),]类型，当天该员工应该工作的时间段列表
    """
    tmp_worktimes = []
    for span in worktimes:
        tmp_worktimes.extend(subtract(span, noonrest))
    worktimes = tmp_worktimes
    return worktimes

def filter_continueday_overtime(worktimes, continueday_overtime):
    """
    @continueday_overtime:int类型，前一个连续工作日的加班时间
                         
    """
    # overtime = Time.strptime(continueday_overtime)
    tmp_worktimes = []
    if continueday_overtime == 0:                # 没加班,就不需要过滤时间段了
        tmp_worktimes = worktimes
    elif 0< continueday_overtime <= 120:
        for span in worktimes:
            tmp_worktimes.extend(subtract(span, ts2is("6:00-9:59")))      # 把6:00-10：00的时间段去掉，就相当于让员工从10点开始上班了
    else:
        for span in worktimes:
            tmp_worktimes.extend(subtract(span,ts2is("6:00-12:59")))       # 把"6:00-12:59的时间段去掉，相当于上午不上班。--预估，下午上班时间不会早于12:59
    worktimes = tmp_worktimes
    return worktimes

def filter_leave(worktimes, leave):
    """
    从worktimes中过滤掉员工请假的时间，然后返回worktimes
    
    @leave:[(int,int),]，当天的请假时间段列表
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
    @worktimes:应该工作的时间段列表
    
    Return:
    start,end:分别工作时间段中，最早与最晚的时刻。用于计算迟到与早退。
    """
    if worktimes==[]:
        return 0,0
    else:
        return worktimes[0][0],worktimes[-1][-1]

def subtract(src,target):
    """时间段src减去target时间段
    
    Args:
        @src:(int,int)，源时间段
        @target:(int,int)，目标时间段
    Return:
        @timespan:[(int,int),]，src与target相减后的时间段
    
    计算规则：
    从src时间段中过滤掉target中的时间段
    例如：
    如果src: (8:30,17:30),target: (12:30,13:30) 相减后得:[(8:30,12:29),(13:31,17:30),]
    如果src: (8：30,17:30),target:(13:30,17:30),相减后得:[(8:30,13:29),]
    
    """
    src_start,src_end = src
    target_start,target_end = target
    span=[]
    if src_start < target_start:
        if src_end < target_start:
            span.append((src_start,src_end))
        elif target_start <= src_end < target_end:
            span.append((src_start,target_start-1))     # 将开始点从工作段去掉
        elif target_end == src_end:
            span.append((src_start,target_start-1))
        elif target_end < src_end:
            span.append((src_start,target_start-1))
            span.append((target_end+1,src_end))
    elif target_start <= src_start<= target_end:
        if src_end <= target_end:     # 时间段被减完了，pass就代表就让span列表为空
            pass
        elif target_end < src_end:
            span.append((target_end+1,src_end))
    elif target_end < src_start:
        span.append((src_start,src_end))
    
    return span
    

#--------------------------------------------------------------------------------
# 开始处理考勤表
#

def get_late_time(sud_start,workstart):
    """
    Args:
    @sud_start，int类型，should start,某员工合乎规定的上班时间
    @workstart,int类型，某员工当天第一次打卡的时间
    
    Return:
    @late,int类型,员工当天的迟到时间
    """
    if sud_start==0:
        return 0
    elif workstart ==0:
        return 0     # 没打卡记录，算旷工一天，旷工后，不计算其迟到了
    else:
        return max(0, workstart-sud_start)
    


def get_late_team(late):
    """计算迟到引起的团队迟到时间
    
    Args:
    @late:int类型，迟到时间
    
    Return:
    @late_team:int类型，迟到引起的团队迟到时间
    
    计算规则：
    1. 迟到时间 <= 15分钟，不计算团队迟到时间
    2. 迟到时间 > 15分钟的部分，全部计入团队迟到时间
    """
    if 0<=late<=15:
        return 0
    else:
        return late-15
    

def get_late_person(late):
    """计算迟到引起的个人迟到时间
    
    Args:
    @late:int类型，迟到的分钟数
    
    Return:
    @late_person:int类型，按照公司规定，惩罚后的个人迟到分钟数
    
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


def get_sub_sequence(late):
    """计算迟到等级
    Args:
    @late:int类型，迟到的分钟数
    
    Return:
    @late_level，字符串，表示迟到等级，有：空,late1,late2,late3,late4
    
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
  

def get_overtime(workshift,workstart,workleave):
    """计算工作日加班时长
    
    Args:
    @workshift:字符串，员工的作息类型，例如："Flexibale","8:30-17:30"
    @workstart:Int类型，员工的打卡时间。
    @workleave:Int类型，该员工有效的最后一次打卡时间
    
    Return:
    @overtime:int类型，加班时长。
    
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


def get_early_leave(sud_leave,workleave):
    """
    Args:
    @sud_leave:int类型，该员工合乎规定的下班时间
    @workleave:int类型,该员工有效的最后一次打卡时间
    
    Return:
    @early_leave:int类型，员工的早退时间
    
    计算规则：
    最后打卡时间 - 规定作息时间段，最后一段的结束时间
    """  
    if sud_leave==0:
        return 0
    elif workleave ==0:
        return 0    # 没有打卡记录的情况，算作旷工，不算早退
    else:
        return max(0, sud_leave- workleave)


def get_workspan(workstart,workleave,worktimes=''):
    """
    Args:
    @workstart,int类型，上班打卡时间
    @workleave,int类型，下班打卡时间
    @worktimes,字符串，规定的员工作息时间段，现在没用，考虑以后会精细计算员工工作时长，考虑从工作时长中，扣除中途请假
                等情况。所以，调用该函数时，最好传入 worktimes。
                
    计算规则：
    下班打卡时间 - 上班打卡时间 - 中午午休1个小时
    """
    return max(0, workleave-workstart -60) # 扣掉中午的一个小时


def get_absent(workstart,workleave):
    """获取旷工小时数
    
    Args:
    @workstart:int类型，上班时间
    @workleave:int类型，下班时间
    
    Return:
    旷工小时数
    """
    if workstart ==0:           #没有打卡记录
        return 8*60
    elif workstart == workleave:    # 只有一次打卡记录
        return 4*60
    else:
        return 0

# --------------------------------------------------------------------------------------------------------------------------
# 计算考勤统计表

def report_max_worktime(days):
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
    return cnt*8*60  

def report_expect_worktime(days,empid):
    """根据员工id，日期，计算员工应该上班的天数
    例如，9月7日入职的员工，他应该上班的时间就不包括9.1-9.6
    这个，可能需要单独来设置！
    现在暂时这么写
    """
    cnt=0
    for day in days:
        workday,_ =is_workday(day)
        if workday:
            cnt+=1
    return cnt*8*60

def report_act_worktime(exp_worktime,person_leave,sick_leave,absent):
    """实际工作小时数
    @exp_workday:应该上班的天数
    """
    return exp_worktime - person_leave - sick_leave - absent

def report_allowtime(exp_worktime,allow_subtime):
    """补贴小时数
    """
    return exp_worktime - allow_subtime

def report_allow_subtime(person_leave,sick_leave,annual_leave,other_paid_leave,over_late3_days):
    """补贴扣除时间
    """
    return person_leave+sick_leave+annual_leave+other_paid_leave+over_late3_days*8*60

def report_leavetime(person_leave,sick_leave,annual_leave,other_paid_leave,swap_off):
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
            self.assertEqual(subtract(ts2is("8:30-12:30"),ts2is("10:30-12:30")),[ts2is("8:30-10:29")])    # 后端临界
            self.assertEqual(subtract(ts2is("8:30-12:30"),ts2is("8:30-10:30")),[ts2is("10:31-12:30")])     # 前段临界
            self.assertEqual(subtract(ts2is("8:30-12:30"),ts2is("8:30-12:30")),[])     # 前后临界
            self.assertEqual(subtract(ts2is("8:30-12:30"),ts2is("9:00-11:00")),[ts2is("8:30-8:59"),ts2is("11:01-12:30")])     # 中间段
            
            # 下面是不太可能出现的情况，
            self.assertEqual(subtract(ts2is("8:30-12:30"),ts2is("13:30-17:30")),[ts2is('8:30-12:30')])    # 不相交
            self.assertEqual(subtract(ts2is("13:30-17:30"),ts2is("8:30-12:30")),[ts2is('13:30-17:30')])
            
            self.assertEqual(subtract(ts2is("8:30-12:30"),ts2is("9:30-13:30")),[ts2is("8:30-9:29")]) 
            self.assertEqual(subtract(ts2is("13:31-17:30"),ts2is("16:00-17:30")),[ts2is("13:31-15:59")])  
            
        def test_filter_leave(self):
            self.assertEqual(filter_leave([ts2is("8:30-12:30"),ts2is("13:30-17:30")], [ts2is("9:00-11:00")]),[ts2is("8:30-8:59"),ts2is('11:01-12:30'),ts2is("13:30-17:30")])
            self.assertEqual(filter_leave([ts2is("8:30-12:30"),ts2is("13:30-17:30")],[ts2is("9:00-16:00")]),[ts2is('8:30-8:59'),ts2is('16:01-17:30')])  
            
        def test_fiter_noonrest(self):
            self.assertEqual(filter_noonrest([ts2is("8:30-17:30")],ts2is("12:30-13:30")),[ts2is("8:30-12:29"),ts2is("13:31-17:30")])   
            
        def test_filter_overtime(self):
            self.assertEqual(filter_continueday_overtime([ts2is("8:30-12:30"),ts2is("13:30-17:30")],t2i("1:30")),[ts2is("10:00-12:30"),ts2is("13:30-17:30")])   
            
        def test_get_worktimes(self):
            self.assertEqual(get_worktimes(),[ts2is('8:30-12:30'),ts2is('13:30-17:30')])
            self.assertEqual(get_worktimes(continueday_overtime=t2i("2:30")),[ts2is("13:30-17:30")])
            self.assertEqual(get_worktimes(leave=[ts2is("9:00-11:00"),ts2is("16:00-17:30")]),[ts2is('8:30-8:59'),ts2is("11:01-12:30"),ts2is("13:30-15:59")])
            self.assertEqual(get_worktimes(leave=[ts2is("13:30-17:30")],continueday_overtime=t2i("2:30")),[])  
        
            
    unittest.main()
    # print( i2t(100) )
    # print(t2i("8:30"))
    # print(i2t(510))
    # print(subtract(tspan2ispan("8:30-12:30"),tspan2ispan("10:30-12:30")))
    # print([tspan2ispan("8:30-10:29")])
