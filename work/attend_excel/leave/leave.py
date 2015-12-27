# -*- encoding:utf8 -*-
"""
作用
=================================
计算当前年假的算法

"""
from datetime import date,datetime

def compute_available_al(startjob,startmoki):
    """
    计算年假基数。
    注意，“本年度年假天数”容易引发误导，实际上可用的年假是利用【本年度年假天数】基数，乘以上班天数，累积而成。
    """
    totalyear = get_totalyear(startjob)
    mokiyear=get_mokieyear(startmoki)
    legal_al=get_legal_al(totalyear)
    moki_al=get_mokie_al(mokiyear)
    #年假的累积基数
    current_al=get_current_al(legal_al, moki_al)
    return {
        'totalyear':totalyear,
        'mokiyear':mokiyear,
        'legal_al':legal_al,
        'moki_al':moki_al,
        'current_al':current_al
    }
def get_totalyear(startjob):
    startjob = datetime.strptime(startjob,"%Y/%m/%d")
    return yearspan(date.today(),startjob)

def get_mokieyear(startmoki):
    startmoki = datetime.strptime(startmoki,"%Y/%m/%d")
    return yearspan(date.today(),startmoki)

def get_legal_al(totalyear):
    """
     计算法定年假
    """
    if totalyear<1:
        return 0
    elif 1<= totalyear <10:
        return 7
    elif 10<=totalyear <20:
        return 10
    else:
        return 15  

def get_mokie_al(mokiyear):
    return mokiyear

def get_current_al(legal_al,moki_al):
    """年假的累积基数，即原来HR命名的“本年度年假天数”
    """
    return min(20,legal_al+moki_al)

 
def yearspan(date1,date2):
    "date1 later than date2"
    year = date1.year-date2.year
    if date1.month >date2.month:
        return year
    elif date1.day > date2.day:
        return year
    else:
        return year -1
  
if __name__ == '__main__':
    import unittest
    class LeaveTest(unittest.TestCase):
        def test_all(self):
            dc = compute_available_al(startjob="2004/8/15", startmoki="2005/9/16")
            self.assertEqual(dc.get('totalyear'),11)
            self.assertEqual(dc.get('mokiyear'),10)
            self.assertEqual(dc.get('legal_al'),10)
            self.assertEqual(dc.get('moki_al'),10)
            self.assertEqual(dc.get('current_al'),20)
            # self.assertEqual(subtract(ts2is("8:30-12:30"),ts2is("10:30-12:30")),[ts2is("8:30-10:29")])    # 后端临界    
    
    unittest.main()
