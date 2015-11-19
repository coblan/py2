# -*- encoding:utf8 -*-
import openpyxl,pickle
from mytime import Time
from attend_record import RecordModel
from orm import Model,Field
from tms import TmsData


class ReportModel(Model):
    empid = Field()
    name = Field()
    pname = Field()
    status = Field()
    work_type = Field()
    work_shift = Field()
    expect_days = Field()
    actual_days = Field()
    allowance_day = Field()
    allowance_except = Field()
    total_leave = Field()
    personal_leave = Field()
    sick_leave = Field()
    annual_leave = Field()
    other_leave = Field()
    swap_leave = Field()
    paid_leave = Field()
    late1 = Field()
    late2 = Field()
    late3 = Field()
    full_att = Field()
    absent = Field()
    deduction = Field()
    kao_process = Field()
    left_day = Field()
    late_team = Field()
    late_person = Field()
    work_span = Field()
    overtime = Field()
    email = Field()


class Report(object):
    """ report
    """
    def __init__(self):
        self.crtrows=None
        self.crtperson = None
          
        
    def gen_table(self,conn): 
        ReportModel.connection(conn)
        ReportModel.create()         
        for p in TmsData.employee():
            self.crtperson = p
            # 设置当前行，这样后面的函数就不需要再查询数据库了
            self.crtrows = list(RecordModel.select("WHERE kao_number='%s'"%p.kao_number))
            
            ReportModel(empid=p.empid,
                        name=p.name,
                        pname=p.pname,
                        status=p.status,
                        work_type=p.work_type,
                        work_shift=p.work_shift,
                        expect_days=p.expect_days,
                        actual_days = self.get_actual_days(),
                        allowance_day = self.get_allowance_day(),
                        allowance_except = self.get_allowance_except(),
                        total_leave = self.get_total_leave(),
                        personal_leave = self.get_personal_leave(),
                        sick_leave=self.get_sick_leave(),
                        annual_leave = self.get_annual_leave(),
                        other_leave = self.get_other_leave(),
                        swap_leave = self.get_swap_leave(),
                        paid_leave=self.get_paid_leave(),
                        late1 =self.get_late1(),
                        late2= self.get_late2(),
                        late3=self.get_late3(),
                        full_att=self.get_full_att(),
                        absent=self.get_absent(),
                        deduction=self.get_deduction(),
                        kao_process=self.get_kao_process(),
                        left_day=self.get_left_day(),
                        late_team=self.get_late_team(),
                        late_person=self.get_late_person(),
                        work_span=self.get_work_span(),
                        overtime=self.get_overtime(),
                        email = self.get_email(),
                        ).save()
        
        ReportModel.commit()
    
    
    def gen07(self,ws):
        ws.title='report'
        ws.append([u'EmpID',u'name',u'ping yin',u'Status',u'work type',u'work shift',u'expect working day',u'Actual working day',u'补贴天数',u'补贴扣除天数','Total Leave days',u'事假',u'病假',u'年假',u'其他',u'调休',
                   u'带薪假',u'Late(1-15mins)',u'late(16-60mins)',u'Late(60+mins)迟到60分钟以上',u'全勤',u'旷工',u'扣款',u'考勤处理',u'15年剩余年假',
                   u'迟到时长-团队',u'迟到时长-个人',u'工作时长',u'加班时长',u'邮箱'])

        for row in ReportModel.select():
            assert isinstance(row,ReportModel)
            ws.append([row.empid,row.name,row.pname,row.status,row.work_type,row.work_shift,row.expect_days,row.actual_days,row.allowance_day,row.allowance_except,row.total_leave,
                row.personal_leave,row.sick_leave,row.annual_leave,row.other_leave,row.swap_leave,row.paid_leave,row.late1 ,row.late2,row.late3,row.full_att,row.absent,
                row.deduction,row.kao_process,row.left_day,row.late_team,row.late_person,row.work_span,row.overtime,row.email,])
      
    def get_actual_days(self):
        return 22
    
    def get_allowance_day(self):
        return 0
    
    def get_allowance_except(self):
        return 0
    
    def get_total_leave(self):
        return 0
    
    def get_personal_leave(self):
        return 0
    
    def get_sick_leave(self):
        return 0
    
    def get_annual_leave(self):
        return 0
    
    def get_other_leave(self):
        return 0
    
    def get_swap_leave(self):
        return 0
    
    def get_paid_leave(self):
        return 0
    
    def get_late1(self):
        cnt =0 
        for row in self.crtrows:
            if row.sub_sequence=='late1':
                cnt+=1
        return cnt

    
    def get_late2(self):
        cnt =0 
        for row in self.crtrows:
            if row.sub_sequence=='late2':
                cnt+=1
        return cnt

    
    def get_late3(self):
        cnt =0 
        for row in self.crtrows:
            if row.sub_sequence=='late3':
                cnt+=1
        return cnt      
    
    
    def get_full_att(self):
        late_count = self.get_late1()+self.get_late2()+self.get_late3()
        if late_count>0:
            return 'N'
        else:
            return 'Y'
        
    def get_absent(self):
        return 0
    
    def get_deduction(self):
        return 0
    
    def get_kao_process(self):
        return ''
    
    def get_left_day(self):
        return 0
    
    def get_late_team(self):
        late = Time(0)
        for row in self.crtrows:
            tm = Time.strptime(row.late_team)
            if tm:
                late += tm
        return str(late)
    
    def get_late_person(self):
        late = Time(0)
        for row in self.crtrows:
            if row.late_person:
                late += Time.strptime(row.late_person) 
        return str(late)

    def get_work_span(self):
        worktime = Time(0)
        for row in self.crtrows:
            if row.workspan:
                worktime += Time.strptime(row.workspan) 
        return str(worktime)
    
    def get_overtime(self):
        overtime = Time(0)
        for row in self.crtrows:
            if row.overtime:
                overtime += Time.strptime(row.overtime) 
        return str(overtime) 
    
    def get_email(self):
        return "boss@mokitech.com"


                
    
if __name__ =='__main__':
    #geninfo()
    #loadinfo()
    Report().gen07()
        
