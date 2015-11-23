# -*- encoding:utf8 -*-
from mytime import Time
from datetime import datetime,date

def get_workspan(workstart,workleave):
    if workstart == Time(0):
        return Time(0)
    elif workstart == workleave:
        return Time(0)
    else:
        if workstart <=Time(12,30):
            morning = Time(12,30)-workstart
            afternoon = workleave - Time(13,30)
            return morning+afternoon
        elif workstart >Time(1,30):
            return workleave - workstart
        else:
            return workleave -Time(1,30)

def day_type(date,daystn):
    datestr = date.strftime("%Y/%m/%d")
    for k,v in daystn.items():
        if k =='time':
            continue
        elif k=='restday':
            if datestr in v:
                return "restday"
        elif datestr in v:
            return k
    raise ValueError("which type %s should be?"%date)  
    
def get_note(date,daystn,workstart,workleave):
    if day_type(date,daystn) =="restday":
        return "restday"
    elif workstart==Time(0) and sud_start()!= Time(0):
        return "not work"
    elif self.workstart != Time(0) and workstart == workleave:
        return 'single'  
    else:
        return ''

def get_late_team(date,daystn,workstart,tic=None):
    '返回迟到团队时间，Time对象'
    if day_type(date,daystn)=="restday":
        return ''
    sud_start = sud_start()
    if sud_start ==Time(0):
        return Time(0)
    elif tic is None:
        tic= sud_start
        
    late = workstart - (tic+Time(0,15))
    return late  

def get_late_person(date,workstart,tic=None):
    if day_type(date,workstart)== "restday":
        return ''
    sud_start = sud_start()
    if sud_start== Time(0):
        return Time(0)
    elif tic is None:
        tic= sud_start  

    if tic+Time(0,15) <=workstart <tic+Time(1):
        return workstart-(tic+Time(0,15) )
    elif tic+Time(1)<= workstart <tic+Time(2):
        return (workstart- (tic+Time(0,15)))*2  
    elif tic +Time(2)<=workstart:
        return (workstart- (tic+Time(0,15)))*3
    else:
        return ''


def get_over_time(date,workleave):
    day = day_type(date)
    if day != "restday":
        return workleave-Time(20)
    else:
        return Time(0)

def get_early_leave(date,daystn,workleave):
    if day_type(date)=="restday":
        return '' 
    if workleave ==Time(0):
        return ''
    sud_leave = sud_leave(date,daystn)
    if sud_leave ==Time(0):
        return ''
    else:
        return sud_leave-workleave


def sud_leave(date,daystn):
    day = day_type(date,daystn)
    if day=="workday":
        mt = re.match(r"(.*)-(.*)",self.workshift)
        if mt:
            return Time.strptime(mt.group(2))
        else:
            return Time(0)
    elif day=="restday":
        return Time(0)
    else:
        return Time.strptime(self.daystn["time"][day][1])
        

def sud_start(date,daystn):
    day = day_type(date,daystn)
    if day=="workday":
        mt = re.match(r"(.*)-(.*)",self.workshift)
        if mt:
            return Time.strptime(mt.group(1))
        else:
            return Time(0)
    elif day == "restday":
        return Time(0)
    else:
        return Time.strptime(self.daystn["time"][day][0])
    

def get_sub_sequence(date,daystn,workstart,workleave,tic=None):
    "迟到标记：late1 迟到<15分钟，late2:迟到<1个小时，late3:迟到<2个小时,late4:迟到>2个小时"
    if day_type(date,daystn) == "restday":
        return ''
    elif workleave == workstart:
        return ''
    sud_start = sud_start(date,daystn)
    if sud_start == Time(0):
        return ''
    elif tic is None:
        tic= sud_start   
        
    if tic< workstart <=tic+Time(0,15):
        return 'late1'
    elif tic+Time(0,15) <= workstart <tic+Time(1):
        return 'late2'
    elif tic+Time(1) <= workstart< tic+Time(2):
        return 'late3' 
    elif tic <= workstart:
        return 'late4'
    else:
        return ''

def find_next_day_row(date,row_from_datestr):
    "row_from_datestr(datestr)"
    next_day = date + timedelta(days=1)
    nextstr = next_day.strftime("%Y/%m/%d")
    return row_from_datestr(nextstr)

def get_lastday_overtime(date,daystn):
    overtimelist = []
    for p in RecordModel.select():
        assert isinstance(p,RecordModel)
        overtime = p.overtime 
        if overtime!=Time(0) and p.note !="restday":
            overtimelist.append(p)

        for p in overtimelist:
            date = p.date 
            if date.weekday()!=4:
                lastday = date + timedelta(days=1)
                laststr = lastday.strftime("%Y/%m/%d")
                for i in RecordModel.select("WHERE date='%s' AND kao_number='%s'"%(laststr,p.kao_number)):
                    i.late_team= i.get_late_team(tic=Time(10))
                    i.late_person = i.get_late_person(tic=Time(10))
                    i.sub_sequence = i.get_sub_sequence(Time(10))
                    i.save()
                    break    
        RecordModel.commit()      