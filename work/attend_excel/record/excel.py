# -*- encoding:utf8 -*-
"""
利用get_attend_list(path)返回考勤记录列表
返回的格式见 get_attend_list()文档

"""
import re
from datetime import datetime
import xlrd
from openpyxl import Workbook
from mytime import Time
from attend import i2t,t2i

def get_attend_list(path):
    """ 生成器，一次返回一个考勤对象列表。
    
    Args:
    @path:考勤原始记录的excel03文件路径。
    
    Return:
    @outlist=[record,..]，record是一条考勤记录字典。
                          字典中有attend_number,name,department,date,timestr,workstart,workleave
                                  考勤号，名字，部门，日期，原始打卡字符串,上班打卡时间(int)，下班打卡时间(int)
    
    注意，该函数是【生成器】，每次返回一个员工所有的考勤数据
    """    
    attendlist = read_excel_03(path)
    attendlist = div_time_col(attendlist)   
    #  attendlist = [ [attend_number,name,department,date,timestr,workstart,workleave],]
    attendlist.sort(cmp=kaolist_cmp)
    
    # 按照员工的考勤号，分组批量输出
    outlist =[]
    last_attend_number = ''
    for row in attendlist:
        if last_attend_number == '':     # 第一次来的时候执行
            last_attend_number = row[0]
        
        record = {
            'attend_number':row[0],
            'name':row[1],
            'date':row[3],
            'timestr':row[4],
            'workstart':row[5],
            'workleave':row[6]
            }
        if row[0] == last_attend_number:
            outlist.append(record)
        else:
            yield outlist
            outlist = []
            outlist.append(record)
            last_attend_number = record['attend_number']
            

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
    attendlist = [ [attend_number,name,department,record_date,timestr,workstart,workleave],]
    """
    for row in attendlist:
        if not row[4]:
            row.append(0)
            row.append(0)
        else:
            ls =[t2i(t) for t in row[4].split()]
            start,end= min(ls),max(ls)
            row.append(start)
            row.append(end)
    return attendlist

# def find_min_max(timestr):
    # "分解时间字符串，并且返回最小，最大时间"
    # timestr = timestr.strip()
    # if timestr:
        # ls = timestr.split(u' ')
        # if ls:
            # ls = [Time.strptime(str_) for str_ in ls]
            # ls.sort()
            # return ls[0],ls[-1]
    
    # return '',''
    
def kaolist_cmp(x,y):
    "考勤列表排序"
    if x[0]!=y[0]:
        return cmp(x[0],y[0])
    else:
        xdate=datetime.strptime(x[3],"%Y/%m/%d").date()
        ydate=datetime.strptime(y[3],"%Y/%m/%d").date()
        return cmp(xdate,ydate)


def gen_attend_excel():
    """
    生成一个Excel文件，包含考勤记录，考勤统计 页面
    """
    wb = Workbook()
    record = wb.active 
    record.title='record'   
    report = wb.create_sheet(title="report")
    return wb,record,report


if __name__ == '__main__':
    for i in get_attend_list(r"D:\work\attendance\attendance record.xls"):
        print(i)