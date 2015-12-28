
class TimeBlock(object):
    owner =
    type =
    # 特殊标示
    special_id=
    span=23124
    def current_max(self):
        Relation.finde(self)
        return max(Relation) 
    
    def get_span(self,span):
        crt_max = self.current_max()
        return min(span,(self.span-crt_max))
    def place(self,leave):
        crt_max = self.current_max()
        leave_max = leave.current_max()
        place_over= False
        if leave.span<=self.span-crt_max:
            Relation(block,crt_max,crt_max+span,leave,leave_max,leave.span)
            place_over = True
        else:
            Relation(block,crt_max,self.span,leave,leave_max,leave_max+(self.span-crt_max))
            place_over = False
        return place_over
    
    def is_overload(self):
        if self.current_max()>=self.span:
            return True
        else:
            return False
    
class Leave(object):
    owner=
    type=
    start=
    end=
    def current_max(self):
        Relation.finde(self)
        return max(Relation) 
        
    
def find_annul_block(leave):
    if leave.start.month<3:
        block =find_from_lastyear()
    if block:
        return block
    else:
        return find_from_thisyear()
        
def find_swap_block(swap):
    return Relation.finde(swap.start,swap.start-month(3) )
    
        

class Relation(object):
    block =
    block_start=
    block_end=
    leave=
    leave_start=
    leave_end=

def place(leave):
    if leave.type=='swap off':
        return place_swap_off(leave)
    elif leave.type=='annual':
        return place_annual_leave(leave)
    
def place_annual_leave(leave):
    while True:
        block = find_annul_block(leave)
        if not block:
            return None
        ok = block.place(leave)
        if ok:
            return ok

def place_swap_off(leave):
    while True:
        block = find_swap_block(leave)
        if not block:
            return 
        ok = block.place(leave)
        if ok:
            return ok
        
def update_available_annual_leave(empid):
    pass

def update_swap_off(empid):
    pass

def update_all(empid):
    pass