# -*- encoding:utf-8 -*-

def trap_rain(elevation):
    """
    elevation=[0,1,0,2,1,0,1,3,2,1,2,1]
    
    思想是将 高度 分层，
    每层分层 [1,0,0,1..] 的正则化形式
    然后 重做往右的 查看，记下高度下降，再上升的index，根据这个index的差，就能求出每层能够储备的雨量
    """
    trap=0
    maxhight=max(elevation)
    for level in range(maxhight):
        out=[h-level for h in elevation]
        out=normal(out)
        trap+=level_trap(out)
    return trap

def normal(array):
    out=[]
    for i in array:
        if i>0:
            out.append(1)
        else:
            out.append(0)
    return out
            
def level_trap(level):
    """
    [0,1,1,....]
    记录单层的 雨水存储
    """
    crt_h=0
    crt_i=0
    trap=0
    for i in range(len(level)):
        if crt_h==0: 
            if level[i]==1:
                crt_h=1
                if crt_i!=0:
                    trap+=(i-crt_i)
        elif crt_h==1:
            if level[i]==0:
                crt_i=i
                crt_h=level[i]
            
    return trap
                
            

if __name__=='__main__':
    elevation=[0,1,0,2,1,0,1,3,2,1,2,1]
    print(trap_rain(elevation))