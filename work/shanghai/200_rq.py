# encoding:utf-8
#from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import re
from requests_toolbelt import MultipartEncoder


proxies = {
    'http': 'socks5://localhost:10855',
}

headers={
        'Cache-Control': 'max-age=0',
        'Origin': 'http://10.231.18.25',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://10.231.18.25/CityGrid/caseoperate_flat/SelectMediaInfo.aspx?CaseStatus=T&TaskId=1806J9617532&CaseType=',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13039.400',
        'Cookie':'ASP.NET_SessionId=2sx0h4zdammuosiaaqjmuuxt; .ASPXAUTH=52498BC697C663AADB48806780E025A8330C775B858282AD21127CD82C299EA1CDBF97E4BD04B7DB5332A4F74143B014E889CEA863748473119C93BA53047503F2D19F83CFB9499D8E9878A9174E0E430B7D3F404ECA01203F7A0C6C30E4107C3D4EB2A1C342FA428C0B12B83EFA5EA244EB740704897D248D060BFC6146C1B39CF4BC54B025EFA30AA1E98F6CC0C278; ScreenWidth=2560; ScreenHeight=1440; Hm_lvt_ba7c84ce230944c13900faeba642b2b4=1528377687; Hm_lpvt_ba7c84ce230944c13900faeba642b2b4=1528379507; LoginType=login',
    } 


def get_taskid():
    url='http://10.231.18.25/CityGrid/caseoperate_flat/XINZENG/PUBLICREPORT.ASPX?PROBLEMTYPE=0&RETURNURL=XINZENG/PUBLICREPORT.ASPX?Userid=03005&random=c4f6dbf3-9905-4e6f-6198-7999ddea5a5a'
    rt = requests.get(url)
    




def get_page(proxies=None):
    
    
    body='__VIEWSTATE=%2FwEPDwUKMTY2MDcxMTg3Mg9kFgICAQ9kFggCAg8QDxYGHg1EYXRhVGV4dEZpZWxkBQpLRUVQRVJOQU1FHg5EYXRhVmFsdWVGaWVsZAUIS0VFUEVSU04eC18hRGF0YUJvdW5kZ2QQFUEIKOWFqOmAiSkM5LiJ6auY5rWL6K%2BVEuWMuue6p%2Bedo%2Bafpea1i%2BivlQ3ljLrnuqfnnaPmn6UxDeWMuue6p%2Bedo%2BafpTIN5Yy657qn552j5p%2BlMw3ljLrnuqfnnaPmn6U0BuaxquWLhwbpmYblhpsM5p2o5pum5ZCJ56WlBuW%2Bgei2hQnog6HmmKXmlrAJ6ZmI5L2z5p2wCOaxqiAg5YabCeiDoeWPtuS9swnnp6blrrbnlLcG5L%2Be5YehCeacsemZiOWLhwblh4zpnZIJ5Yav5Zu956WlCeminOeVmeW%2FoAnmsojmmKXmmI4G5byg5paMCemHkeW%2Fl%2BW8ugjkuIEgIOa0gQbpmbbno4oG6ZmI5by6CeacseS8n%2BWNjgnlhq%2Fph5HlgaUJ6YKT5Zac5Zu9Ceacseaguei%2BiQnmiLTmtbfoia8G5bq36ZSLCeeOi%2Be%2FoOiNownpu4TmmZPlvawJ6IOh5rC45LyfCeW8oOW%2Fl%2BWdmgnlrZ%2FovonmmI4G5rKI5paMBuadjuWzsAnnjovlhbTljY4J6ZmG5paH5YabBumZhumjngnpmYblhpvkvJ8J5pyx5paH5Y2OCemSn%2BWbvem%2BmQnlrZnnjq7nkKYJ55ub5rSB56OKCeayiOWIqeiNowbpmK7lvLoG5p2O5pilBueroOWllQborrjmtIEG5p2O5LquCeiCluWwj%2BawkQnlvKDlvrfmmI4G5rKI5YmRCeacseS4veawkQbpmYbli4cJ5rKI6bij6bijCeiSi%2BW7uuaWsAnotbXmoYLlvLoJ6ZmG5LyK6L2pBuadqOaYjgblpI%2FlvawVQQAIMzExODAwMDAIMzExODAwMDgIMzExODAwMTAIMzExODAwMTEIMzExODAwMTIIMzExODAwMTMIMzExODAwMTQIMzExODAwMTUIMzExODAwMTYIMzExODAwMTcIMzExODAwMTgIMzExODAwMTkIMzExODAwMjAIMzExODAwMjEIMzExODAwMjIIMzExODAwMjMIMzExODAwMjQIMzExODAwMjUIMzExODAwMjYIMzExODAwMjcIMzExODAwMjgIMzExODAwMjkIMzExODAwMzAIMzExODAwMzEIMzExODAwMzIIMzExODAwMzMIMzExODAwMzQIMzExODAwMzUIMzExOEEwMTAIMzExOEEwMTEIMzExOEEwODMIMzExOEEwODcIMzExOEEwOTUIMzExOEIwODIIMzExOEIxMDEIMzExOEMwNzYIMzExOEMwOTkIMzExOEQwNzgIMzExOEYwNzkIMzExOEYxMDAIMzExOEYxMTYIMzExOEYxMjIIMzExOEcwOTYIMzExOEgwNzcIMzExOEgxMDUIMzExOEkwOTgIMzExOEswODAIMzExOEsxMTEIMzExOEwxMDkIMzExOE0xMTMIMzExOE4wODQIMzExOE4wODgIMzExOE8wODYIMzExOE8wOTAIMzExOE8wOTIIMzExOFAxMDgIMzExOFIwODEIMzExOFMwODkIMzExOFMwOTcIMzExOFUwOTEIMzExOFUwOTMIMzExOFYwODUIMzExOFYxMDIIMzExOFgwOTQUKwNBZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIDDxAPFgYfAAUKc3RyZWV0bmFtZR8BBQpzdHJlZXRjb2RlHwJnZBAVDAgo5YWo6YCJKQnnmb3puaTplYcJ6YeN5Zu66ZWHCeWNjuaWsOmVhwnph5Hms73plYcJ57uD5aGY6ZWHDOWkj%2BmYs%2Bihl%2BmBkw%2FpppnoirHmoaXooZfpgZMJ5b6Q5rO%2B6ZWHDOebiOa1puihl%2BmBkwnotbXlt7fplYcM5pyx5a626KeS6ZWHFQwABDE4MTAEMTgwOQQxODA4BDE4MDUEMTgwNAQxODAxBDE4MTEEMTgwNwQxODAyBDE4MDYEMTgwMxQrAwxnZ2dnZ2dnZ2dnZ2dkZAIIDxBkZBYBZmQCCg8QDxYGHwAFCENPREVOQU1FHwEFCUNPREVWQUxVRR8CZ2QQFQMIKOWFqOmAiSkM5Yy657qn552j5a%2BfEuW4gue6p%2Bedo%2BafpeS4i%2Ba0vhUDAAI1NAI0MhQrAwNnZ2dkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WCAUMcmFkaW9fVGFza0lEBQxyYWRpb19UYXNrSUQFEnJhZGlvX0Rpc2NvdmVyVGltZQUOcmFkaW9fS2VlcGVyU04FDnJhZGlvX0tlZXBlclNOBQlyYWRpb19hc2MFCXJhZGlvX2FzYwUKcmFkaW9fZGVzYxhd4qSfGndY8UX2Nba2vbvtJndRUbLDaDkPZiApzCnN&__EVENTVALIDATION=%2FwEWYAL%2BqPr3CQKQspmwBwLk48qbDQLOlcDSCwLo%2F7%2BQDQLo%2F9%2FOBwLFlKL%2FBwLFlLbaDgLFlPqlAQLFlI6ACALFlNKTAgLFlObOCQLFlKrYAwLFlL63CwLFlMLVCQLFlNawAQK%2BgoTKCQK%2BgpihAQK%2BgtywCwK%2BgvDvAgK%2BgrT5BAK%2BgsjVAwK%2BgoynBgK%2BgqCCDQK%2BgqSjDAK%2BgrieCwKbu%2BbRAwKbu%2FqMCwKbu76eDQKbu9L6BAKbu5bEDgKbu6qjBgLSlKL%2FBwLSlLbaDgLBoZrDBALBocr3BwK639SUCALCoYbkDQL6%2F8%2FMBAKexuXnBwK838TeBwKbxv3jDQKdxpHeBAL2%2F7uQDQLTlKbYAwLMjdiwCwK435jmAgKHxvnCDgLg%2F%2F%2FjBwKi37DiCALLoa6%2BDALclLLaDgL8%2F%2B%2BlDwLWlIqACALGod7SDgLGoc6UBgLHobabCAKg35CFBgKg3%2BjzBwKI%2F9vOBwLSocKaCwLToeLzDQLM3qzdCQLG3qTgDQLG3vyuDwLuofKJBgKG%2F5PeDgK138C5AQKx6YCLDAL1%2FouWBgKYx%2FmOAQKYx43qCQKYx4nLCAKYx52QAQKYx9mnCwL1%2FvfKDQKYx%2BGCDwKYx8XaAgKYx%2FXvBwKYx7H9CQKIzqC9CQLxheGJCwLbh93iAQK7lM2hDwLr%2FqzcBwLgkfaxCwLnkc6xCwLGw9ygAgKx26DYBgKW%2B8FSAtmzgu4FAqChxTMCkeLu%2BQYC8NfbvQsCkcCfxAwCg8an8gf%2F5Bh5tJGR5MuvPWR0fhf0CUWeQrECjzmq7GRs5Ym%2FJg%3D%3D&txt_planName=&txt_TaskID=&ddl_Keeper=&ddl_Street=1806&txt_StartDate=&txt_EndDate=&select_infotype=&txt_address=&txt_hotlinesn=&ddl_CodeList=&RadioArea=radio_DiscoverTime&RadioSort=radio_desc&Querybtn=%E6%9F%A5++%E8%AF%A2&SelectID=&pageindex={pageindex}'
    url="http://10.231.18.25/CityGrid/caseoperate_flat/SelectMediaInfo.aspx?CaseStatus=T&TaskId=1806J9617532&CaseType="    

    #files = {'PicFile': open(r'C:\Users\Administrator\Desktop\1111111.jpg', 'rb')}
    
    m = MultipartEncoder(
        fields={'PicFile': ('JE20180308170521.jpg', open(r'C:\Users\Administrator\Desktop\JE20180308170521.jpg', 'rb'), 'image/jpeg'),
                '__VIEWSTATE':'/wEPDwUKMTQ5OTMyNDAzMg9kFgICAw8WAh4HZW5jdHlwZQUTbXVsdGlwYXJ0L2Zvcm0tZGF0YRYEAgMPFgIeCGRpc2FibGVkZGQCBA8WAh8BZGRkxQ4oQ+NFCYp1YlXGoghvWLTK0TKp7dexirT328BUhtI=',
                '__EVENTVALIDATION':'/wEWDwK1nLsZAuzJ454LAsmem4wMAuXu0mECg8an8gcCkqKqlg8Cp52w5QYC766n2gECr5/YsgoC4b2wlA8C/ZKZjwEC5Ov3nAsC3oSUrwoCg9v//wECi5OlxgWm5woeEIk+sjqp15HTFl0yKUHW9raB4mAhFPwwYIXqmA==',
                'btnPicAddOk':'提交',
                'pageindex':'0'}
        )
    
    headers.update(
        {'Content-Type': m.content_type}
    )
    
    rt=requests.post(url,headers=headers,data=m ,proxies=proxies)
    return rt.content

get_page(proxies)

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
    


