# -*- encoding:utf8 -*-
import openpyxl,pickle
from mytime import Time

class Report(object):
    """ report
    0:empid ,1:name,2:pname,3:status,4:work_type,5:work_shift,6:expect_days,7:actual_days,8:allowance_day,9:allowance_except,
    10:total_leave,11:personal_leave,12:sick_leave,13:annual_leave,14:other_leave,15:swap_leave,16:paid_leave,17:late1,18:late2,19:late3,
    20:full_att,21:absent,22:deduction,23:kao_process,24:left_day,25:late_team,26:late_person,27:work_span,28:overtime,29:email
    """
    def __init__(self,conn,tms):
        self.conn = conn
        self.rawcursor = self.conn.cursor()
        self.recordcursor = self.conn.cursor()
        #if tms is None:
            #tms = TestData()
            #tms.loadinfo()
            #tms.rawcursor =self.rawcursor
        self.tms = tms
        self.crtrows=None
        
    def report(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE report
                             (empid text, name text, pname text, status text, work_type text, work_shift text,
                             expect_days text, actual_days text,allowance_day text,allowance_except text,total_leave text,personal_leave text,
                             sick_leave text, annual_leave text,other_leave text,swap_leave text,paid_leave text,late1 text,late2 text,late3 text,full_att text,absent text,deduction text,
                             kao_process text,left_day text,late_team text,late_person text,work_span text,overtime text,email text)''')   
               
        for empid,name,pname,status,work_type,work_shift,expect_days in self.employee():
            # 设置当前行，这样后面的函数就不需要再查询数据库了
            self.set_crtrows(empid)
            
            actual_days = self.get_actual_days(empid)
            allowance_day = self.get_allowance_day(empid)
            allowance_except = self.get_allowance_except(empid)
            total_leave = self.get_total_leave(empid)
            personal_leave = self.get_personal_leave(empid)
            sick_leave=self.get_sick_leave(empid)
            annual_leave = self.get_annual_leave(empid)
            other_leave = self.get_other_leave(empid)
            swap_leave = self.get_swap_leave(empid)
            paid_leave=self.get_paid_leave(empid)
            late1 =self.get_late1(empid)
            late2= self.get_late2(empid)
            late3=self.get_late3(empid)
            full_att=self.get_full_att(empid)
            absent=self.get_absent(empid)
            deduciton=self.get_deduction(empid)
            kao_process=self.get_kao_process(empid)
            left_day=self.get_left_day(empid)
            late_team=self.get_late_team(empid)
            late_person=self.get_late_person(empid)
            work_span=self.get_work_span(empid)
            overtime=self.get_overtime(empid)
            email = self.get_email(empid)
            row = (empid,name,pname,status,work_type,work_shift,int(expect_days),actual_days,allowance_day,allowance_except,total_leave,personal_leave,sick_leave,annual_leave,other_leave,
                       swap_leave,paid_leave,late1,late2,late3,full_att,absent,deduciton,kao_process,left_day,late_team,late_person,work_span,overtime,str(email) )
            querystr="INSERT INTO report VALUES ("+"'%s',"*29+"'%s')"
            c.execute(querystr%row)
        self.conn.commit()
    
    
    def gen07(self,ws):
        ws.title='report'
        ws.append([u'EmpID',u'name',u'ping yin',u'Status',u'work type',u'work shift',u'expect working day',u'Actual working day',u'补贴天数',u'补贴扣除天数','Total Leave days',u'事假',u'病假',u'年假',u'其他',u'调休',
                   u'带薪假',u'Late(1-15mins)',u'late(16-60mins)',u'Late(60+mins)迟到60分钟以上',u'全勤',u'旷工',u'扣款',u'考勤处理',u'15年剩余年假',
                   u'迟到时长-团队',u'迟到时长-个人',u'工作时长',u'加班时长',u'邮箱'])
        c = self.conn.cursor()
        for row in c.execute("""SELECT * FROM report"""):
            ws.append(row)
    
    def employee(self):
        emp = self.tms.datalist
        head =True
        for p in emp:
            if head:
                head=False
                continue
            #    empid,name,pinyin,status,worktype,workshift,expectday
            yield p[0],p[1],p[2]  , p[3] , p[4]   ,p[5]     ,p[6],   
    
    def set_crtrows(self,empid):
        kao_number = self.tms.empid2kao_number(empid)
        if kao_number:
            self.crtrows = list(self.recordcursor.execute("SELECT * FROM record WHERE kao_number='%s'"%kao_number) )
        else:
            self.crtrows = []
      
    def get_actual_days(self,empid):
        return 22
    def get_allowance_day(self,empid):
        #print(empid)
        #print(self.tms.empid2kao_number(empid))
        return 0
    def get_allowance_except(self,empid):
        return 0
    def get_total_leave(self,empid):
        return 0
    def get_personal_leave(self,empid):
        return 0
    def get_sick_leave(self,empid):
        return 0
    def get_annual_leave(self,empid):
        return 0
    def get_other_leave(self,empid):
        return 0
    def get_swap_leave(self,empid):
        return 0
    def get_paid_leave(self,empid):
        return 0
    def get_late1(self,empid):
        cnt =0 
        for row in self.crtrows:
            if row[7]=='late1':
                cnt+=1
        return cnt
        #kao_number = self.tms.empid2kao_number(empid)
        #if kao_number:
            #cnt = 0
            #for row in self.recordcursor.execute("SELECT * FROM record WHERE kao_number=%s"%kao_number):
                #if row[7]=='late1':
                    #cnt+=1
            #return cnt
        #return 0
    
    def get_late2(self,empid):
        cnt =0 
        for row in self.crtrows:
            if row[7]=='late2':
                cnt+=1
        return cnt
    
        #kao_number = self.tms.empid2kao_number(empid)
        #if kao_number:
            #cnt = 0
            #for row in self.recordcursor.execute("SELECT * FROM record WHERE kao_number=%s"%kao_number):
                #if row[7]=='late2':
                    #cnt+=1
            #return cnt
        #return 0
    
    def get_late3(self,empid):
        cnt =0 
        for row in self.crtrows:
            if row[7]=='late3':
                cnt+=1
        return cnt      
    
        #kao_number = self.tms.empid2kao_number(empid)
        #if kao_number:
            #cnt = 0
            #for row in self.recordcursor.execute("SELECT * FROM record WHERE kao_number=%s"%kao_number):
                #if row[7]=='late3':
                    #cnt+=1
            #return cnt
        #return 0
    
    def get_full_att(self,empid):
        return 'Y'
    def get_absent(self,empid):
        return 0
    def get_deduction(self,empid):
        return 0
    def get_kao_process(self,empid):
        return ''
    def get_left_day(self,empid):
        return 0
    def get_late_team(self,empid):
        late = Time(0)
        for row in self.crtrows:
            tm = Time.strptime(row[8])
            if tm:
                late += tm
        return str(late)
    
    def get_late_person(self,empid):
        late = Time(0)
        for row in self.crtrows:
            if row[10]:
                late += Time.strptime(row[10]) 
        return str(late)
        #kao_number = self.tms.empid2kao_number(empid)
        #if kao_number:
            #cnt = Time(0)
            #for row in self.recordcursor.execute("SELECT * FROM record WHERE kao_number=%s"%kao_number):
                #cnt= cnt + Time.strptime(row[10])
            #return str(cnt)
        #return 0
    
    def get_work_span(self,empid):
        worktime = Time(0)
        for row in self.crtrows:
            if row[9]:
                worktime += Time.strptime(row[9]) 
        return str(worktime)
    
    def get_overtime(self,empid):
        overtime = Time(0)
        for row in self.crtrows:
            if row[11]:
                overtime += Time.strptime(row[11]) 
        return str(overtime) 
    
    def get_email(self,empid):
        return "boss@mokitech.com"


                
    
if __name__ =='__main__':
    #geninfo()
    #loadinfo()
    Report().gen07()
        
