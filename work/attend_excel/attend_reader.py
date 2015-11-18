import xlrd
from openpyxl import Workbook
from openpyxl.styles import PatternFill,Style,Color
from mytime import Time


class Reader(object):
    
    @staticmethod
    def read03(conn,path):
        'dc={"tb_name":"tablename","field":"kao_number text, name text,"}'
        rawdata = xlrd.open_workbook(path,encoding_override='gbk')
    
        table = rawdata.sheets()[0]
        nrows = table.nrows
        c = conn.cursor()
        #c.execute("CREATE TABLE %(tb_name)(%(field))"%dc)
        c.execute('''CREATE TABLE raw_record
             (kao_number text, name text, department text, date text, workstart text, workleave text)''')

        for i in range(1, nrows):
            start,end=find_min_max(table.row_values(i)[4])
            c.execute("""INSERT INTO raw_record VALUES ('%s','%s','%s','%s','%s','%s')"""%(table.row_values(i)[0],table.row_values(i)[1],table.row_values(i)[2],table.row_values(i)[3],start,end))
        conn.commit()        


def find_min_max( timeList):
    timeList = timeList.strip()
    if timeList:
        ls = timeList.split(u' ')
        if ls:
            ls = [Time.strptime(str_) for str_ in ls]
            ls.sort()
            return ls[0],ls[-1]
    
    return '',''