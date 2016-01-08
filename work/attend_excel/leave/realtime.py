# -*- encoding:utf8 -*-


def place(leave):
    while True:
        block = leave.find_block(leave)
        if not block:
            return None
        ok = block.place(leave)
        if ok:
            return ok   
        

class TimeBlock(object):
    def __init__(self,id,empid,timeid,span,type_):
        self.id=id
        self.empid=empid
        self.timeid=timeid
        self.span=span
        self.type_=type_

    def current_max(self):
        ls = find_block_in_relation(self)
        return max([x.blockend for x in ls]) 
    
    def place(self,leave):
        crt_max = self.current_max()
        leave_max = leave.current_max()
        blockleft=self.left()
        leaveleft=leave.left()
        blockid=self.id
        if leaveleft<=blockleft:
            blockstart = crt_max
            blockend=blockstart+leave.left()
            leavestart=leave.current_max()
            leaveend=leave.span
            save_relation( blockid, blockstart, blockend, leave.id, leavestart, 
                    leaveend)
            place_over=True     # 是否包含完 该假期
        else:
            blockstart=crt_max
            blockend = self.span
            leavestart=leave_max
            leaveend=leave_max+blockleft
            save_relation(blockid, blockstart, blockend, leave.id, leavestart, 
                         leaveend)
            place_over=False
        return place_over

    
    def left(self):
        return max(0,self.span-self.current_max())

    
class Leave(object):
    def __init__(self,id,empid,start,end):
        self.id=id
        self.empid=empid
        self.start=start
        self.end=end
        self.span = end-start
        
    def current_max(self):
        ls = find_leave_in_relation(self)
        return max([x.leaveend for x in ls ]) 
    
    def left(self):
        return max(0,self.span-self.current_max())


class AnnualLeave(Leave):
    def find_block(self):
        if self.start.month <3:
            for block in  find_block_with_range(self.start.year()-1.start, end):
                if block.left()>0:
                    return block
        else:
            for block in find_block_with_range(self.start.year().start, end):
                if block.left()>0:
                    return block
            
    
class SwapOff(Leave):
    def find_block(self):
        for block in find_block_with_range(self.start.-3month,self.start):
            if block.left()>0:
                return block
    
    
class Relation(object):
    def __init__(self,id,blockid,blockstart,blockend,leaveid,leavestart,leaveend):
        self.id=id
        self.blockid=blockid
        self.blockstart=blockstart
        self.blockend=blockend
        self.leaveid=leaveid
        self.leavestart=leavestart
        self.leaveend=leaveend

def find_block_with_range(start,end):
    pass

def find_block_in_relation(block):
    yield relation
    
def find_leave_in_relation(leave):
    yield relation

def save_relation(blockid,blockstart,blockend,leaveid,leavestart,leaveend):
    pass

    
def update_available_annual_leave(empid):
    pass

def update_swap_off(empid):
    pass

def update_all(empid):
    pass