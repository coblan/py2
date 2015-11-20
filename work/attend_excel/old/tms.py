# -*- encoding:utf8 -*-

import openpyxl,pickle

class TmsData(object):
    def __init__(self):
        self.loadinfo()
        
    def loadinfo(self):
        with open('tmpfiles/infomation') as f:
            self.datalist = pickle.load(f)
    
    def empid2kao_number(self,empid):
        if empid == 'AE1774':
            return 1157
        elif empid == 'AE1776':
            return 1158
        for row in self.datalist:
            if row[0]==empid:
                return str(row[-1])
                #qstr= "SELECT * FROM raw_record WHERE name='%s'"%row[1]
                #for row in  self.rawcursor.execute(qstr.encode('utf8')):
                    #return row[0]
                

def geninfo():
    "直接运行该函数，将解析xlsx与xls文件，将生成一个列表，并保存到硬盘，目的是将empID同kao_number对应起来。"
    import sqlite3
    from attend_reader import Reader
    
    conn = sqlite3.connect(':memory:')
    Reader.read03(conn, r"D:\work\attendance\attendance record.xls")
    cursor = conn.cursor()
    
    '从excel提取员工信息，保存为pickle格式，作为测试用'
    wb = openpyxl.load_workbook(r"D:\work\attendance\MK_HR_Attendance Report_Cecilia_201510.xlsx")
    ws = wb['report']
    out =[]
    for i in ws.rows:
        ls = [j.value for j in i]
        kao_number='000'
        for i in  cursor.execute("SELECT * FROM raw_record WHERE name='%s'"%ls[1]):
            kao_number = i[0]
            break
        ls.append(kao_number)
        
        out.append(ls)
    with open('tmpfiles/infomation','wb') as f:
        pickle.dump(out,f)    

if __name__ =='__main__':
    geninfo()