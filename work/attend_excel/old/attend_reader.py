# -*- encoding: utf8 -*-
# 主要函数 Reader.read03
#    1.读取考勤原始数据
#    2.处理考前时间
#    3.在conn数据库中生成raw_record数据表

import xlrd
from openpyxl import Workbook
from openpyxl.styles import PatternFill,Style,Color
from mytime import Time

from orm import Model,Field

class Raw_Record(Model):
    "处理后的考勤原始数据表"
    kao_number =Field()
    name = Field()
    department = Field()
    date = Field()
    workstart = Field()
    workleave = Field()


class Reader(object):
    @staticmethod
    def read03(conn,path):
        """读取并处理考勤原始数据,最后在conn中生成一个raw_record数据表，数据表模型见Raw_Record
        conn : 数据库连接
        path : excel03文件路径
        """
        rawdata = xlrd.open_workbook(path,encoding_override='gbk')
    
        table = rawdata.sheets()[0]
        nrows = table.nrows

        Raw_Record.connection(conn)
        Raw_Record.create()
        for i in range(1, nrows):
            start,end=find_min_max(table.row_values(i)[4])
            dc={"kao_number":table.row_values(i)[0],
                "name":table.row_values(i)[1],
                "department":table.row_values(i)[2],
                "date":table.row_values(i)[3],
                "workstart":start,
                "workleave":end
            }
            Raw_Record(**dc).save()
        Raw_Record.commit()        


def find_min_max( timeList):
    "分解时间字符串，并且返回最小，最大时间"
    timeList = timeList.strip()
    if timeList:
        ls = timeList.split(u' ')
        if ls:
            ls = [Time.strptime(str_) for str_ in ls]
            ls.sort()
            return ls[0],ls[-1]
    
    return '',''