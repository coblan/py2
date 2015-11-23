# -*- encoding:utf8 -*-
from mytime import Time
from datetime import datetime,date,timedelta
import re
cnt =0
def remenber(func):
    global cnt
    cnt+=1
    def _func(*args,**kw):
        if not hasattr(_func,'_remenber%s'%_func.index):
            rt = func(*args,**kw)
            setattr(_func,'_remenber%s'%_func.index,rt)
            setattr(_func,'_remenber_args%s'%_func.index,args)
            setattr(_func,'_remenber_kw%s'%_func.index,kw)
            return rt
        else:
            if args== getattr(_func,'_remenber_args%s'%_func.index) and \
               kw ==getattr(_func,'_remenber_kw%s'%_func.index):
                return getattr(_func,'_remenber%s'%_func.index)
            else:
                setattr(_func,'_remenber_args%s'%_func.index,args)
                setattr(_func,'_remenber_kw%s'%_func.index,kw)                
                return func(*args,**kw)
            
    _func.index =cnt
    return _func

class KaoRecord(object):
    def __init__(self,day_type,workstart,workleave,kaodate,workshift,overtime_from_date):
        """
        @Function: day_type(date) return  one of ["workday","restday",('8:30','17:50')]
        @Function: overtime_from_date(date) return overtime
        """
        self.day_type = day_type
        self.workshift = workshift
        self.workstart = workstart
        self.workleave = workleave
        self.kaodate = kaodate
        self.overtime_from_date=overtime_from_date
    
    def get_workspan(self):
        if self.workstart == Time(0):
            return Time(0)
        elif self.workstart == self.workleave:
            return Time(0)
        else:
            if self.workstart <=Time(12,30):
                morning = Time(12,30)-self.workstart
                afternoon = self.workleave - Time(13,30)
                return morning+afternoon
            elif self.workstart >Time(1,30):
                return self.workleave - self.workstart
            else:
                return self.workleave -Time(1,30)
    #@remenber
    #def day_type(self):
        #return self.daystn(self.kaodate)
        #for k,v in self.daystn.items():
            #if k =='time':
                #continue
            #elif k=='restday':
                #if datestr in v:
                    #return "restday"
            #elif datestr in v:
                #return k
        #raise ValueError("which type %s should be?"%self.kaodate)  
    
    def get_note(self):
        if self.day_type(self.kaodate) =="restday":
            return "restday"
        elif self.workstart==Time(0) and self.sud_start()!= Time(0):
            return "not work"
        elif self.workstart != Time(0) and self.workstart == self.workleave:
            return 'single'  
        else:
            return ''
    
    def get_late_time(self):
        if self.day_type(self.kaodate)=="restday":
            return Time(0)
        
        sud_start=self.get_sud_start()

        if sud_start ==Time(0):
            return Time(0)
        elif self.get_lastday_overtime()!= Time(0):
            #非周末加班
            sud_start=Time(10)

        late = self.workstart - (sud_start+Time(0,15))
        return late
        
    def get_late_team(self):
        '返回迟到团队时间，Time对象'
        return self.get_late_time()

    def get_late_person(self):
        late =self.get_late_time()
        if Time(0,15)<=late<=Time(1):
            return late
        elif Time(1)<=late <Time(2):
            return late*2
        elif Time(2)<=late:
            return late*3
        else:
            return Time(0)
    
    def get_over_time(self):
        day = self.day_type(self.kaodate)
        if day != "restday":
            return self.workleave-Time(20)
        else:
            return Time(0)

    def get_early_leave(self):
        if self.day_type(self.kaodate)=="restday":
            return '' 
        if self.workleave ==Time(0):
            return ''
        sud_leave = self.get_sud_leave()
        if sud_leave ==Time(0):
            return ''
        else:
            return sud_leave-self.workleave

    def get_sud_leave(self):
        day = self.day_type(self.kaodate)
        if day=="workday":
            mt = re.match(r"(.*)-(.*)",self.workshift)
            if mt:
                return Time.strptime(mt.group(2))
            else:
                return Time(0)
        elif day=="restday":
            return Time(0)
        else:
            return Time.strptime(self.date_type["time"][day][1])
        

    def get_sud_start(self):
        day = self.day_type(self.kaodate)
        if day=="workday":
            mt = re.match(r"(.*)-(.*)",self.workshift)
            if mt:
                return Time.strptime(mt.group(1))
            else:
                return Time(0)
        elif day == "restday":
            return Time(0)
        else:
            return Time.strptime(self.date_type["time"][day][0])
    

    def get_sub_sequence(self):
        "迟到标记：late1 迟到<15分钟，late2:迟到<1个小时，late3:迟到<2个小时,late4:迟到>2个小时"
        if self.day_type(self.kaodate) == "restday":
            return ''
        elif self.workleave == self.workstart:
            return ''
        late = self.get_late_time()
        if Time(0)<= late < Time(0,15):
            return "late1"
        elif Time(0,15)<= late <Time(1):
            return "late2"
        elif Time(1)<= late < Time(2):
            return "late3"
        elif Time(2)<= late :
            return "late4"
        else:
            return 'NotNormal'

    
    def get_lastday_overtime(self):
        "overtime_from_date(date) return overtime"
        lastday = self.kaodate-timedelta(days=1)
        if lastday.weekday() in [0,1,2,3]:
            return self.overtime_from_date(lastday)
        else:
            return Time(0)
    #overtimelist = []
    #for p in RecordModel.select():
        #assert isinstance(p,RecordModel)
        #overtime = p.overtime 
        #if overtime!=Time(0) and p.note !="restday":
            #overtimelist.append(p)

        #for p in overtimelist:
            #date = p.date 
            #if date.weekday()!=4:
                #lastday = date + timedelta(days=1)
                #laststr = lastday.strftime("%Y/%m/%d")
                #for i in RecordModel.select("WHERE date='%s' AND kao_number='%s'"%(laststr,p.kao_number)):
                    #i.late_team= i.get_late_team(tic=Time(10))
                    #i.late_person = i.get_late_person(tic=Time(10))
                    #i.sub_sequence = i.get_sub_sequence(Time(10))
                    #i.save()
                    #break    
        #RecordModel.commit()
        
class T(object):
    pass
@remenber
def test1(arg):
    print('hh')
    return 'jb'
    
@remenber
def test2(args):
    print('dog')
    
if __name__ =='__main__':
    def func(date_):
        #if date_ == date(2015,11,11):
            #return Time(0,5)
        return Time(0)
    def daystn_test(date):
        
        return "workday"
    obj =KaoRecord(daystn_test, workstart=Time(9,30), workleave=Time(17,50), kaodate=date(2015,11,12), workshift="8:30-17:30",overtime_from_date=func)
    print( obj.get_early_leave() )
    print(obj.get_over_time())
    print(obj.get_workspan())
    print(obj.get_late_person())
    print(obj.get_sub_sequence())
    #obj= T()
    #obj2= T()
    #print(test1(obj))
    #test2(obj2)
    #print (test1(obj))
    #print({'name':'heylin','age':100}=={'age':100,'name':'heylin'})