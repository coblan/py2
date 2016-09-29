# -*- encoding:utf8 -*-
"""
用途
===============================================
计算【月考勤记录】，【月考勤统计】
调用的算法来自于attend.py

处理流程
===============================================
main()是主函数，main的执行步骤大致如下。
1. 调用excel.get_attend_list(path)生成器
   该生成器，从path指定的原始考勤记录excel03文件读取数据，每次返回一个员工的当月所有考勤记录。
   返回的数据结构,见函数文档
   
2. 生成一些员工的基本信息，
    如：考勤号转换为员工号
        获取上个月最后一天的加班情况
        获取员工的规定作息时间(workshift)
        获取员工的工作类型
        
3. 调用record_employee()函数，计算【月考勤记录】表数据。
    record_employee(attends,...)中的参数attends,就是第[1]部中的函数get_attend_list()，每次返回的一个列表对象。
    record_employee()的算法来自于:attend.py
    
4. 利用[3]计算出的【月考勤记录】数据，调用report_empoyee()，生成【月考勤统计】
    record_employee()的算法来自于:attend.py以report_开头的函数
    
6. 将3，4步结果数据保存到TMS系统

7. 生成excel07文件，并保存.
    wb,record_sheet,report_sheet =excel.gen_attend_excel()
    分别是“工作簿”，“月考勤记录”，“月考勤统计”

外部接口
(现在暂时调用record_interface.py中的临时函数)
===============================================
需要外部提供的函数,见record_interface.py


"""
import re
from datetime import datetime,date,timedelta
from excel import get_attend_list,gen_attend_excel
import attend
from attend import i2t,t2i,i2day

# ----------------临时的外部接口函数-------TMS中替换掉这些引入-------------------
from record_interface import get_worktype,get_month_end_overtime,attend_num_to_empid,save_attend,get_workshift,is_workday,get_leave

def main(read_path,write_path=''):
    """主函数，处理考勤原始记录
    
    Args:
    @read_path: 读取地址
    @write_path:写地址

    
    """
    # 生成Excel07文件wb,两个工作表record,report。
    # 如果不再生成excel，可以将这两个列表去掉
    records =[]
    reports =[]
    
    # 以考勤号分组，遍历整个考勤记录
    for attends in get_attend_list(read_path):
        # attends=[dict(attend_number,name,department,record_date,timestr,workstart,workleave)]
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
        # record= [dict(attend_number,name,date,workstart,workleave,workspan,late_level,late_person,late_team,overtime,absent,timestr),] 
        record = record_employee(attends,workshift,empid,last_overtime)
       
        # 生成【月考勤统计】表中，该员工的统计数据
        report = report_empoyee(empid,record,worktype,workshift)
        # 保存到TMS中，现在是预留着，以后实现。Todo
        save_attend(record,report)  
        
        records.extend(record)
        reports.append(report)
        
    # ---------------------生成Excel--------可能是以后不再生成excel-----------------------------------
    if not write_path:
        return
    wb,record_sheet,report_sheet =gen_attend_excel()
    record_sheet.append([u'考勤号',u'名字',u'日期',u'上班时间',u'下班时间',
                         u'工作时长',u'迟到等级',u'个人迟到时间',u'团队迟到时间',u'加班',
                         '早退',u'旷工',u'原始打卡记录'])
    for row in records:
        record_sheet.append([row['attend_number'],row['name'],row['date'],i2t(row['workstart']),i2t(row['workleave']),
                             i2t(row['workspan']),row['late_level'],i2t(row['late_person']),i2t(row['late_team']),i2t(row['overtime']),
                             i2t(row['early_leave']),i2day(row['absent']),row['timestr']])
       
    report_sheet.append(['姓名','事假','病假','年假','其他带薪假',
                         '调休','带薪假','迟到1','迟到2','迟到3',
                         '迟到4','个人迟到累计','团队迟到累计','加班','预期工作天数',
                         '实际工作天数','补贴天数','假期时间','补贴扣除天数','考勤处理',
                         '旷工','早退','全勤'])
    for row in reports:
        report_sheet.append([row['name'],i2day(row['person_leave']),i2day(row['sick_leave']),i2day(row['annual_leave']),i2day(row['other_paid_leave']),
                             i2day(row['swap_off']),i2day(row['paid_leave']),row['late1'],row['late2'],row['late3'],
                             row['late4'],i2t(row['late_person']),i2t(row['late_team']),i2t(row['overtime']),i2day(row['exp_workhours']),
                             i2day(row['act_workhours']),i2day(row['allow_hours']),i2day(row['leave_hours']),i2day(row['deduction']),row['process'],
                             i2day(row['absent']),i2t(row['early_leave']),row['full_attend']])
    # -------------------保存Excel
    wb.save(write_path)
        
        
def record_employee(attends,workshift,empid,last_ctnday_overtime_lastmonth=0,noonrest="12:30-13:30"):
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
        workday,specialshift = is_workday(date_)
        if workday:
                mt = re.match(r"(.*)-(.*)",workshift)
                if mt:
                    leave_timespan = [x.timespan() for x in get_leave(empid,date_)]
                    if specialshift == '':   #表示正常工作日
                        worktimes = attend.get_worktimes(workshift,continueday_overtime=last_ctnday_overtime,leave=leave_timespan,noonrest=noonrest)
                    else:
                        worktimes = attend.get_worktimes(specialshift,continueday_overtime=last_ctnday_overtime,leave=leave_timespan,noonrest=noonrest)
                    sud_start,sud_leave = attend.time_range(worktimes)
                    absent = attend.get_absent(workstart,workleave)
                    if absent !=0:      # 只要有旷工，就不去计算他的迟到，早退
                        late = 0
                        early_leave=0
                    else:
                        late = attend.get_late_time(sud_start,workstart)
                        early_leave = attend.get_early_leave(sud_leave,workleave)
                    late_person = attend.get_late_person(late)
                    late_team = attend.get_late_team(late)
                    late_level = attend.get_sub_sequence(late)
                    workspan = attend.get_workspan(workstart,workleave)
                    overtime = attend.get_overtime(workshift,workstart,workleave)
                    # absent = attend.get_absent(workstart,workleave)
                    
                    # 记录下工作日加班，下个循环时，用于计算迟到
                    last_ctnday_overtime = overtime
                    
                else:   # workshif == flexable的人
                    late_person = 0
                    late_team = 0
                    late_level = ''
                    early_leave = 0  
                    workspan = workleave-workstart #str(workleave - workstart)
                    overtime = 0 
                    absent = 0
                    last_ctnday_overtime = 0                    
 
                           
        else:
            late_person = 0
            late_team = 0
            late_level = ''
            early_leave = 0  
            workspan = workleave-workstart 
            overtime = workleave-workstart 
            absent = 0
            # 把工作日加班清空
            last_ctnday_overtime = 0
            
        day_attend = {
            "attend_number":attend_number,
            "name":name,
            "date":date_,
            "workstart":workstart, 
            "workleave":workleave,
            "workspan":workspan,
            "late_level":late_level,
            "late_person":late_person,
            "late_team":late_team,
            "overtime":overtime,
            "absent":absent,
            'early_leave':early_leave,
            "timestr":timestr
            }
        records.append(day_attend)
    return records

def report_empoyee(empid,record,worktype,workshift):
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
    late_cnt = 0
    late_act_times = 0
    late_person = 0
    late_team = 0
    overtime = 0
    workspan = 0
    early_leave = 0
    name = record[0]['name']
    print(name)
    for row in record:
 
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
        
        if late_level in ['late2','late3','late4']:
            late_cnt +=1
        absent+= row['absent']
        late_person += row['late_person']
        late_team += row['late_team']
        overtime += row['overtime']
        workspan += row['workspan']
        early_leave += row['early_leave']
    
    late_all = late1+late2+late3+late4
    late_act_times = late_team
    max_worktime = attend.report_max_worktime(days)
    exp_worktime = attend.report_expect_worktime(days,empid)
    act_worktime = attend.report_act_worktime(exp_worktime, person_leave, sick_leave,absent)
    # 补贴扣除天数
    allow_subtime = attend.report_allow_subtime(person_leave, sick_leave, annual_leave, 
                                other_paid_leave, over_late3_days=late3+late4)
    allow_time = attend.report_allowtime(exp_worktime, allow_subtime)
    leave_time = attend.report_leavetime(person_leave, sick_leave, annual_leave, 
                            other_paid_leave, swap_off)
    paid_leave = attend.report_paid_leave(annual_leave, other_paid_leave)
    deduction = attend.report_deduction(absent)
    #考勤处理：书面警告，口头警告
    process = attend.report_process(late_cnt,late_act_times,absent)
    full_attend = attend.report_full_attend(worktype, workshift, exp_worktime,  max_worktime,  
                            person_leave,  sick_leave,  paid_leave, late_all,  absent, early_leave)
    return {
        'empid':empid,
        'name':name,
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
        'exp_workhours':exp_worktime,
        'act_workhours':act_worktime,
        'allow_hours':allow_time,
        'leave_hours':leave_time,
        'deduction':deduction,
        'absent':absent,
        'process':process,
        'early_leave':early_leave,
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
    
    main(r"D:\work\attendance\gen\raw.xls",r"D:\work\attendance\gen\out_record.xlsx")

   
if __name__ == '__main__':
    test_main()