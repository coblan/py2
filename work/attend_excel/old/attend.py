# -*- encoding:utf8 -*-
# 处理考勤原始excel
import sqlite3
from openpyxl import Workbook
from settings import *
from attend_reader import Reader
from attend_record import Record
from attend_report import Report

class Attendence(object):
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        
    def read03(self,path):
        "在conn数据库中生成raw_record数据表"
        Reader.read03(self.conn,path)

    def process(self):
        "解析生成record ,统计生成report。在conn数据库中生成相应的数据表"
        self.record = Record()
        self.record.gen_table(self.conn)
        
        self.report = Report()
        self.report.gen_table(self.conn)
        
    def gen07(self):
        "在内存中生成需要的Excel文件"
        self.wb = Workbook()
        
        ws= self.wb.active 
        self.record.gen07(ws)

        ws2=self.wb.create_sheet()
        self.report.gen07(ws2)
        
    def save(self,path):
        "保存内存中的excel文件"
        self.wb.save(path)
        
if __name__ == '__main__':
    testpath = r"D:\work\attendance\attendance record.xls"
    testsavepath="tmpfiles/test.xlsx"
    
    attend = Attendence()
    attend.read03(testpath)
    attend.process()
    attend.gen07()
    attend.save(testsavepath)

