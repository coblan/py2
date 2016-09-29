# -*- encoding:utf8 -*-
"""
暂时虚拟的函数
======================================
attend_num_to_empid(attend_number):根据考勤号，返回员工号.TMS提供。之所以使用该函数，是考虑到员工号比考勤号通用，在tms中查询数据时，利用员工号进行查询。
get_workshift(empid):根据empid员工号，返回员工的规定作息
get_worktype(empid):根据empid，返回员工的工作类型，如'FTE'
get_leave(empid,date_) ,获取员工请假情况,返回【假期对象】列表，
                      每个【假期对象】必须有timespan()方法，用于返回假期的时间段，例如:"8:30-12:30"
                      必须有type()方法，返回假期类型，如：'person leave','sick leave','annual leave','other paid leave','swap off'
                      

save_attend(),预留，将数据保存到TMS中
get_month_end_overtime(empid,date)  获取date所在月末，该员工的加班情况

is_workday 获取当日是否为工作日，当日的workshift
"""
from datetime import datetime
import sys
sys.path.append('..')
from tms import get_workshift,get_worktype,attend_num_to_empid

# def attend_num_to_empid(attend_num):
    # return 'A1000'
    
# def get_worktype(empid):
    # return 'FTE'
    
def get_month_end_overtime(empid,month):
    return 0

def save_attend(records,reports):
    pass

# def get_workshift(empid):
    # return "8:30-17:30"
    
def get_leave(empid,date_):
    return []

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

if __name__ =='__main__':
    print(get_workshift('AE1776'))