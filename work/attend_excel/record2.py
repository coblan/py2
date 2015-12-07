# -*- encoding:utf8 -*-
"""
用途
=============================
计算【月考勤记录】，【月考勤统计】
调用的算法来自于attend.py

流程
=============================
main()是主函数，从main开始执行。
1. 调用get_attend_list()生成器，遍历该生成器的结果，每次一个员工的当月考勤记录。
2. 生成一些员工的基本信息
3. 调用record_employee()函数，计算【月考勤记录】表数据。
         算法来自于:attend.py
4. 利用3计算出的【月考勤记录】数据，调用report_empoyee()，生成【月考勤统计】
         算法来自于:attend.py
6. 将3，4步结果数据保存到TMS系统
7. 生成excel07文件，并保存.

ToDo
============================
到目前为止，还需要提供的函数,当前这些函数只是简单的模拟:
attend_num_to_empid(attend_number):根据考勤号，返回员工号
get_workshift(empid):根据empid员工号，返回员工的规定作息
get_worktype(empid):根据empid，返回员工的工作类型，如'FTE'
get_leave(empid,date_) ,获取员工请假情况,返回【假期对象】列表，
                      每个【假期对象】必须有timespan()方法，用于返回假期的时间段，例如:"8:30-12:30"
                      必须有type()方法，返回假期类型，如：'person leave','sick leave','annual leave','other paid leave','swap off'

get_month_end_overtime(empid,date)  获取date所在月末，该员工的加班情况
"""
import re
from datetime import datetime,date,timedelta
from mytime import Time
from excel import get_attend_list,gen_attend_excel
import attend
                
def main(read_path,write_path='',get_worktype=lambda x:'FTE', get_month_end_overtime=lambda e,m:'',
         attend_num_to_empid=lambda x:"AE1001",save_attend=lambda x:'',get_workshift=lambda x:"8:30-17:30"):
    """主函数，处理考勤原始记录
    
    Args:
    @read_path: 读取地址
    @write_path:写地址
    @get_worktype(empid),获取员工的工作类型，预留，TMS提供
    @attend_num_to_empid(attend_number),将考勤号转换为员工号，TMS提供。之所以使用该函数，是考虑到员工号比考勤号通用，在tms中查询数据时，利用员工号进行查询。
    @save_attend(),预留，将数据保存到TMS中
    @get_workshift(empid),从员工号获取员工作息，有TMS提供
    
    """
    # 生成Excel07文件wb,两个工作表record,report。
    wb,record_sheet,report_sheet = gen_attend_excel()
    
    # 以考勤号分组，遍历整个考勤记录
    for attends in get_attend_list(read_path):
        # attends=[ row_dict,] ，是某员工的考勤记录列表，每一项都是一个字典。
        # row_dict的键有:[attend_number,name,department,record_date,timestr,workstart,workleave]
        attend_number = attends[0]['attend_number']
        # 在TMS中员工号比考勤号通用，所以将考勤号换算成员工号，方便后面查询信息
        empid = attend_num_to_empid(attend_number)
        if not empid:   # 如果不是员工，则跳过处理
            continue
        workshift = get_workshift(empid)
        if not workshift:  # 如果workshift是空，不做处理
            continue   
        worktype = get_worktype(empid)
        last_day = datetime.strptime(attends[0]['date'],'%Y/%m/%d').date()-timedelta(days=1)
        last_overtime=get_month_end_overtime(empid,last_day)
        # 生成【月考勤记录】表中，该员工的当月数据
        # records= [dict(attend_number,name,date,workstart,workleave,workspan,late_level,late_person,late_team,overtime,absent,timestr),] 
        records = record_employee(attends,workshift,empid,last_overtime)
        
        # 生成【月考勤统计】表中，该员工的统计数据
        # report = dict(....)
        report = report_empoyee(records,worktype,workshift)
        
        # 保存到TMS中，现在是预留着，以后实现。Todo
        save_attend(records,report)        
        
        # 生成Excel
        record_sheet.append([u'考勤号',u'名字',u'日期',u'上班时间',u'下班时间',u'工作时长',u'迟到等级',u'个人迟到时间',u'团队迟到时间',u'加班',u'旷工',u'原始打卡记录'])
        for row in records:
            record_sheet.append([row['attend_number'],row['name'],row['date'],row['workstart'],row['workleave'],
                                 row['workspan'],row['late_level'],row['late_person'],row['late_team'],row['overtime'],row['absent'],row['timestr']])
        report_sheet.append(reports)
        # 保存Excel
        wb.save(write_path)
        
        
def record_employee(attends,workshift,empid,last_ctnday_overtime_lastmonth='',get_leave=lambda x,y:[],
                     noonrest="12:30-13:30"):
    """
    Args:
    @attends=[ dict(attend_number,name,department,record_date,timestr,workstart,workleave),]
    @workshift:员工的作息时间，例如 "8:30-17:30"
    @last_ctnday_overtime_lastmonth: 该员工，上个月最后一天的，工作日加班时间
    @get_leave(empid,date_) ,获取员工请假情况,返回对象列表，每个【假期对象】必须有timespan()方法，用于返回假期的时间段，例如:"8:30-12:30"

    Return:
    返回员工计算后的【月考勤记录】数据，以字典的形式返回：
    [dict(attend_number,name,date,workstart,workleave,workspan,late_level,late_person,late_team,overtime,absent,timestr),]
    """
    records = []   # 当前person考勤记录，处理完后，就把结果放在rt_row列表里面
    last_ctnday_overtime = last_ctnday_overtime_lastmonth    # 第一天，需要把上个月的连续工作日，传入进来
    for row in attends:
        # row = Record(attend_number,name,department,record_date,timestr,workstart,workleave)
        attend_number = row['attend_number']
        name = row['name']
        date_ = row['date']
        timestr = row['timestr']
        workstart = row['workstart']
        workleave = row['workleave']           
        workday,specialshift = attend.is_workday(date_)
        if workday:
            leave_timespan = [x.timespan() for x in get_leave(empid,date_)]
            if specialshift == '':   #表示正常工作日
                worktimes = attend.get_worktimes(workshift,continueday_overtime=last_ctnday_overtime,leave=leave_timespan,noonrest=noonrest)
            else:
                worktimes = attend.get_worktimes(specialshift,continueday_overtime=last_ctnday_overtime,leave=leave_timespan,noonrest=noonrest)
            sud_start,sud_leave = attend.time_range(worktimes)
            late = attend.get_late_time(sud_start,workstart)
            late_person = attend.get_late_person(late)
            late_team = attend.get_late_team(late)
            late_level = attend.get_sub_sequence(late)
            early_leave = attend.get_early_leave(sud_leave,workleave) 
            workspan = attend.get_workspan(workstart,workleave)
            overtime = attend.get_overtime(workshift,workstart,workleave)
            absent = attend.get_absent(workstart,workleave)
            
            # 记录下工作日加班，下个循环时，用于计算迟到
            if overtime != '':
                last_ctnday_overtime = overtime
            else:
                last_ctnday_overtime = ''                 
        else:
            late_person = ''
            late_team = ''
            late_level = ''
            early_leave = ''  
            workstart,workleave = Time.strptime(workstart), Time.strptime(workleave)  
            workspan = str(workleave - workstart)
            overtime = str(workleave - workstart)
            absent = 0
            # 把工作日加班清空
            last_ctnday_overtime = '' 
        day_attend = {
            "attend_number":attend_number,
            "name":name,
            "date":date_,
            "workstart":str(workstart),
            "workleave":str(workleave),
            "workspan":workspan,
            "late_level":late_level,
            "late_person":late_person,
            "late_team":late_team,
            "overtime":overtime,
            "absent":absent,
            "timestr":timestr
            }
        records.append(day_attend)
    return records

def report_empoyee(empid,records,worktype,workshift,get_leave=lambda x,y:[]):
    """考勤统计，
    Args:
    @Records: [record_dict,]，某个员工当月的【考勤记录】列表。record_dict是字典，它的键有:(attend_number,name,date_,workstart,workleave,
                             workspan,late_level,late_person,late_team,overtime,absent,timestr)
    
    Return:
    @report:返回内容见代码
    """
    # records= [dict(attend_number,name,date_,workstart,workleave,workspan,late_level,late_person,late_team,overtime,absent,timestr),]
    days=[]
    person_leave = 0
    sick_leave = 0
    annual_leave =0
    other_paid_leave = 0
    swap_off = 0
    late1 =0
    late2=0
    late3=0
    late4=0
    absent = 0
    late_times = 0
    late_cnt = 0
    late_person = 0
    late_team = 0
    overtime = 0
    workspan = 0
    for row in records:
        date_=row['date']
        days.append(date_)
        # 累积当日请假时间
        for leave in get_leave(empid,date_):
            if leave.type()=='person leave':
                person_leave += leave.length()
            elif leave.type() == 'sick leave':
                sick_leave += leave.length()
            elif leave.type() == 'annual leave':
                annual_leave += leave.length()
            elif leave.type() == 'other paid leave':
                other_paid_leave += leave.length()
            elif leave.type() == 'swap off':
                swap_off += leave.length()
        # 累积迟到等级
        late_level = row['late_level']
        if late_level == 'late1':
            late1+=1
        elif late_level == 'late2':
            late2 +=1
        elif late_level == 'late3':
            late3 +=1
        elif late_level == 'late4':
            late4 +=1
        late_times += row[8]
        if late_level in ['late2','late3','late4']:
            late_cnt +=1
        absent+= row['absent']
        late_person += int(row['late_person'])
        late_team += int(row['late_team'])
        overtime += int(row['overtime'])
        workspan += int(row['workspan'])
    max_workday = attend.report_max_workday(days)
    exp_workday = attend.report_expect_workday(days,empid)
    act_workday = attend.report_act_workday(exp_workday, person_leave, sick_leave)
    allow_sub_days = attend.report_allow_sub_days(person_leave, sick_leave, annual_leave, 
                                other_paid_leave, over_late3_days=late3+late4)
    allow_days = attend.report_allow_days(exp_workday, allow_sub_days)
    leave_days = attend.report_leave_days(person_leave, sick_leave, annual_leave, 
                            other_paid_leave, swap_off)
    paid_leave = attend.report_paid_leave(annual_leave, other_paid_leave)
    deduction = attend.report_deduction(absent)
    process = attend.report_process(late_cnt,late_times)
    full_attend = attend.report_full_attend(worktype, workshift, exp_workday,  max_workday,  
                            person_leave,  sick_leave,  paid_leave, late_all,  absent, early_leave)
    return {
        'empid':empid,
        'person_leave':person_leave,
        'sick_leave':sick_leave,
        'annual_leave':annual_leave,
        'other_paid_leave':other_paid_leave,
        'swap_off':swap_off,
        'paid_leave':paid_leave,
        'late1':late1,
        'late2':late2,
        'late3':late3,
        'late4':late4,
        'late_person':late_person,
        'late_team':late_team,
        'overtime':overtime,
        'exp_workday':exp_workday,
        'act_workday':act_workday,
        'allow_days':allow_days,
        'leave_days':leave_days,
        'paid_leave':paid_leave,
        'deduction':deduction,
        'process':process,
        'full_attend':full_attend
    }


def test_main():
    # def get_workshift(empid):
        # return ''
    # def attend_num_to_empid(attend_number):
        # return 'AE111'
    # last_ctnday_overtime_lastmonth = ''
    # def get_leave(empid,date_):
        # return []
    
    main(r"D:\work\attendance\attendance record.xls")

   
if __name__ == '__main__':
    test_main()