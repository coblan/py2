# encoding:utf-8
#from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import re



proxies = {
    'http': 'socks5://localhost:10899',
}

def get_page(pageindex,proxies=None):
    headers={
        'Cache-Control': 'max-age=0',
        'Origin': 'http://10.231.18.25',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://10.231.18.25/INSGRID/caseoperate_flat/ALLCASELIST.ASPX?STATUSID=3&CATEGORYID=120',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie':'ASP.NET_SessionId=ncrjd0f0k4ixi52t42dfxcqe',
    }
    
    body='__VIEWSTATE=%2FwEPDwUKMTY2MDcxMTg3Mg9kFgICAQ9kFggCAg8QDxYGHg1EYXRhVGV4dEZpZWxkBQpLRUVQRVJOQU1FHg5EYXRhVmFsdWVGaWVsZAUIS0VFUEVSU04eC18hRGF0YUJvdW5kZ2QQFUEIKOWFqOmAiSkM5LiJ6auY5rWL6K%2BVEuWMuue6p%2Bedo%2Bafpea1i%2BivlQ3ljLrnuqfnnaPmn6UxDeWMuue6p%2Bedo%2BafpTIN5Yy657qn552j5p%2BlMw3ljLrnuqfnnaPmn6U0BuaxquWLhwbpmYblhpsM5p2o5pum5ZCJ56WlBuW%2Bgei2hQnog6HmmKXmlrAJ6ZmI5L2z5p2wCOaxqiAg5YabCeiDoeWPtuS9swnnp6blrrbnlLcG5L%2Be5YehCeacsemZiOWLhwblh4zpnZIJ5Yav5Zu956WlCeminOeVmeW%2FoAnmsojmmKXmmI4G5byg5paMCemHkeW%2Fl%2BW8ugjkuIEgIOa0gQbpmbbno4oG6ZmI5by6CeacseS8n%2BWNjgnlhq%2Fph5HlgaUJ6YKT5Zac5Zu9Ceacseaguei%2BiQnmiLTmtbfoia8G5bq36ZSLCeeOi%2Be%2FoOiNownpu4TmmZPlvawJ6IOh5rC45LyfCeW8oOW%2Fl%2BWdmgnlrZ%2FovonmmI4G5rKI5paMBuadjuWzsAnnjovlhbTljY4J6ZmG5paH5YabBumZhumjngnpmYblhpvkvJ8J5pyx5paH5Y2OCemSn%2BWbvem%2BmQnlrZnnjq7nkKYJ55ub5rSB56OKCeayiOWIqeiNowbpmK7lvLoG5p2O5pilBueroOWllQborrjmtIEG5p2O5LquCeiCluWwj%2BawkQnlvKDlvrfmmI4G5rKI5YmRCeacseS4veawkQbpmYbli4cJ5rKI6bij6bijCeiSi%2BW7uuaWsAnotbXmoYLlvLoJ6ZmG5LyK6L2pBuadqOaYjgblpI%2FlvawVQQAIMzExODAwMDAIMzExODAwMDgIMzExODAwMTAIMzExODAwMTEIMzExODAwMTIIMzExODAwMTMIMzExODAwMTQIMzExODAwMTUIMzExODAwMTYIMzExODAwMTcIMzExODAwMTgIMzExODAwMTkIMzExODAwMjAIMzExODAwMjEIMzExODAwMjIIMzExODAwMjMIMzExODAwMjQIMzExODAwMjUIMzExODAwMjYIMzExODAwMjcIMzExODAwMjgIMzExODAwMjkIMzExODAwMzAIMzExODAwMzEIMzExODAwMzIIMzExODAwMzMIMzExODAwMzQIMzExODAwMzUIMzExOEEwMTAIMzExOEEwMTEIMzExOEEwODMIMzExOEEwODcIMzExOEEwOTUIMzExOEIwODIIMzExOEIxMDEIMzExOEMwNzYIMzExOEMwOTkIMzExOEQwNzgIMzExOEYwNzkIMzExOEYxMDAIMzExOEYxMTYIMzExOEYxMjIIMzExOEcwOTYIMzExOEgwNzcIMzExOEgxMDUIMzExOEkwOTgIMzExOEswODAIMzExOEsxMTEIMzExOEwxMDkIMzExOE0xMTMIMzExOE4wODQIMzExOE4wODgIMzExOE8wODYIMzExOE8wOTAIMzExOE8wOTIIMzExOFAxMDgIMzExOFIwODEIMzExOFMwODkIMzExOFMwOTcIMzExOFUwOTEIMzExOFUwOTMIMzExOFYwODUIMzExOFYxMDIIMzExOFgwOTQUKwNBZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIDDxAPFgYfAAUKc3RyZWV0bmFtZR8BBQpzdHJlZXRjb2RlHwJnZBAVDAgo5YWo6YCJKQnnmb3puaTplYcJ6YeN5Zu66ZWHCeWNjuaWsOmVhwnph5Hms73plYcJ57uD5aGY6ZWHDOWkj%2BmYs%2Bihl%2BmBkw%2FpppnoirHmoaXooZfpgZMJ5b6Q5rO%2B6ZWHDOebiOa1puihl%2BmBkwnotbXlt7fplYcM5pyx5a626KeS6ZWHFQwABDE4MTAEMTgwOQQxODA4BDE4MDUEMTgwNAQxODAxBDE4MTEEMTgwNwQxODAyBDE4MDYEMTgwMxQrAwxnZ2dnZ2dnZ2dnZ2dkZAIIDxBkZBYBZmQCCg8QDxYGHwAFCENPREVOQU1FHwEFCUNPREVWQUxVRR8CZ2QQFQMIKOWFqOmAiSkM5Yy657qn552j5a%2BfEuW4gue6p%2Bedo%2BafpeS4i%2Ba0vhUDAAI1NAI0MhQrAwNnZ2dkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WCAUMcmFkaW9fVGFza0lEBQxyYWRpb19UYXNrSUQFEnJhZGlvX0Rpc2NvdmVyVGltZQUOcmFkaW9fS2VlcGVyU04FDnJhZGlvX0tlZXBlclNOBQlyYWRpb19hc2MFCXJhZGlvX2FzYwUKcmFkaW9fZGVzYxhd4qSfGndY8UX2Nba2vbvtJndRUbLDaDkPZiApzCnN&__EVENTVALIDATION=%2FwEWYAL%2BqPr3CQKQspmwBwLk48qbDQLOlcDSCwLo%2F7%2BQDQLo%2F9%2FOBwLFlKL%2FBwLFlLbaDgLFlPqlAQLFlI6ACALFlNKTAgLFlObOCQLFlKrYAwLFlL63CwLFlMLVCQLFlNawAQK%2BgoTKCQK%2BgpihAQK%2BgtywCwK%2BgvDvAgK%2BgrT5BAK%2BgsjVAwK%2BgoynBgK%2BgqCCDQK%2BgqSjDAK%2BgrieCwKbu%2BbRAwKbu%2FqMCwKbu76eDQKbu9L6BAKbu5bEDgKbu6qjBgLSlKL%2FBwLSlLbaDgLBoZrDBALBocr3BwK639SUCALCoYbkDQL6%2F8%2FMBAKexuXnBwK838TeBwKbxv3jDQKdxpHeBAL2%2F7uQDQLTlKbYAwLMjdiwCwK435jmAgKHxvnCDgLg%2F%2F%2FjBwKi37DiCALLoa6%2BDALclLLaDgL8%2F%2B%2BlDwLWlIqACALGod7SDgLGoc6UBgLHobabCAKg35CFBgKg3%2BjzBwKI%2F9vOBwLSocKaCwLToeLzDQLM3qzdCQLG3qTgDQLG3vyuDwLuofKJBgKG%2F5PeDgK138C5AQKx6YCLDAL1%2FouWBgKYx%2FmOAQKYx43qCQKYx4nLCAKYx52QAQKYx9mnCwL1%2FvfKDQKYx%2BGCDwKYx8XaAgKYx%2FXvBwKYx7H9CQKIzqC9CQLxheGJCwLbh93iAQK7lM2hDwLr%2FqzcBwLgkfaxCwLnkc6xCwLGw9ygAgKx26DYBgKW%2B8FSAtmzgu4FAqChxTMCkeLu%2BQYC8NfbvQsCkcCfxAwCg8an8gf%2F5Bh5tJGR5MuvPWR0fhf0CUWeQrECjzmq7GRs5Ym%2FJg%3D%3D&txt_planName=&txt_TaskID=&ddl_Keeper=&ddl_Street=1806&txt_StartDate=&txt_EndDate=&select_infotype=&txt_address=&txt_hotlinesn=&ddl_CodeList=&RadioArea=radio_DiscoverTime&RadioSort=radio_desc&Querybtn=%E6%9F%A5++%E8%AF%A2&SelectID=&pageindex={pageindex}'
    url="http://10.231.18.25/INSGRID/caseoperate_flat/ALLCASELIST.ASPX?STATUSID=3&CATEGORYID=120"    
    body = body.format(pageindex=pageindex)
    rt=requests.post(url,headers=headers,data=body,proxies=proxies)
    return rt.content

def parse_page(content):
    soup = BeautifulSoup(content)
    rows =[]
    for tr in soup.select('#caselist tr')[1:]:
        ls = tr.select('td')
        ls[0:-1] = [x.text for x in ls[0:-1]]
        
        btn_script = ls[-1].select('.div_a1 li')[0]['onclick']
        mt = re.search('KEY=(\d+)',btn_script)
        ls[-1] = mt.group(1)
        rows.append(ls)
        #for i in ls:
            #print(i)
    mt = re.search('Pagination.Refresh\(parseInt\(\'(\d+)\'\)',content)
    total = int(mt.group(1))
    return rows,total

def get_data(mintime='2010'):
    """
    @mintime:2018-02-03 06:02
    """
    crt_index=0
    while True:
        content = get_page(crt_index,proxies)
        rows,total = parse_page(content)
        for row in rows:
            if row[7] < mintime:
                raise StopIteration
            yield row
        if (crt_index+1) *10 <total:
            crt_index +=1
        else:
            break
    
"""
获取坐标
http://10.231.18.25/INSGRID/caseoperate_flat/XinZeng/EditFeedbackCaseInfo.aspx?KEY=23300&TYPE=3&pageindex=0&FanKui=1&sourctType=%E5%8C%BA%E7%BA%A7%E7%9D%A3%E5%AF%9F&categoryId=120
"""       
        
        

for row in get_data():
    print(row)


