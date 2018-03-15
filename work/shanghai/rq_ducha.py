# encoding:utf-8
#from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
#import xmltodict
#headers = {'SOAPAction':"http://www.china-gis.com/gisshare/Select",
            #'content-type': 'text/xml'}
# headers={
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
    # 'Origin':'http://10.231.18.25',
    # 'X-Requested-With':'XMLHttpRequest',
    # 'Accept':'application/json, text/javascript, */*; q=0.01',
    # 'Content-Type':'application/x-www-form-urlencoded',
    # 'Referer':'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchConditionFlat.aspx',
    # # 'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440; .ASPXAUTH=454EEB8DB6AF0C3D7375D4D1E09490A8B5ED8422477F833EECEC9EE94869BA75353A463969A74E2CF5F7FC8F4B0A699A1C295F719DF0ABE22C16711430D602AAD0486E6F73E533169B997BC46BEEB09FE070075148A082EA248474001926859D11A3770DCD26BE6F29185B66F06B4D7E4F5184390539BFFBB0845986D315B5A58E53BD811246C649643BD3CFDE29B08E'
    # 'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440;'

# }


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

# var_dict={
    # #'inspector':'31189242',
    # #'start':'2017121400',
    # #'end':'2017121500',
    # 'dept':'20601', # 赵项代码
# }


body='__VIEWSTATE=%2FwEPDwUKMTY2MDcxMTg3Mg9kFgICAQ9kFggCAg8QDxYGHg1EYXRhVGV4dEZpZWxkBQpLRUVQRVJOQU1FHg5EYXRhVmFsdWVGaWVsZAUIS0VFUEVSU04eC18hRGF0YUJvdW5kZ2QQFUEIKOWFqOmAiSkM5LiJ6auY5rWL6K%2BVEuWMuue6p%2Bedo%2Bafpea1i%2BivlQ3ljLrnuqfnnaPmn6UxDeWMuue6p%2Bedo%2BafpTIN5Yy657qn552j5p%2BlMw3ljLrnuqfnnaPmn6U0BuaxquWLhwbpmYblhpsM5p2o5pum5ZCJ56WlBuW%2Bgei2hQnog6HmmKXmlrAJ6ZmI5L2z5p2wCOaxqiAg5YabCeiDoeWPtuS9swnnp6blrrbnlLcG5L%2Be5YehCeacsemZiOWLhwblh4zpnZIJ5Yav5Zu956WlCeminOeVmeW%2FoAnmsojmmKXmmI4G5byg5paMCemHkeW%2Fl%2BW8ugjkuIEgIOa0gQbpmbbno4oG6ZmI5by6CeacseS8n%2BWNjgnlhq%2Fph5HlgaUJ6YKT5Zac5Zu9Ceacseaguei%2BiQnmiLTmtbfoia8G5bq36ZSLCeeOi%2Be%2FoOiNownpu4TmmZPlvawJ6IOh5rC45LyfCeW8oOW%2Fl%2BWdmgnlrZ%2FovonmmI4G5rKI5paMBuadjuWzsAnnjovlhbTljY4J6ZmG5paH5YabBumZhumjngnpmYblhpvkvJ8J5pyx5paH5Y2OCemSn%2BWbvem%2BmQnlrZnnjq7nkKYJ55ub5rSB56OKCeayiOWIqeiNowbpmK7lvLoG5p2O5pilBueroOWllQborrjmtIEG5p2O5LquCeiCluWwj%2BawkQnlvKDlvrfmmI4G5rKI5YmRCeacseS4veawkQbpmYbli4cJ5rKI6bij6bijCeiSi%2BW7uuaWsAnotbXmoYLlvLoJ6ZmG5LyK6L2pBuadqOaYjgblpI%2FlvawVQQAIMzExODAwMDAIMzExODAwMDgIMzExODAwMTAIMzExODAwMTEIMzExODAwMTIIMzExODAwMTMIMzExODAwMTQIMzExODAwMTUIMzExODAwMTYIMzExODAwMTcIMzExODAwMTgIMzExODAwMTkIMzExODAwMjAIMzExODAwMjEIMzExODAwMjIIMzExODAwMjMIMzExODAwMjQIMzExODAwMjUIMzExODAwMjYIMzExODAwMjcIMzExODAwMjgIMzExODAwMjkIMzExODAwMzAIMzExODAwMzEIMzExODAwMzIIMzExODAwMzMIMzExODAwMzQIMzExODAwMzUIMzExOEEwMTAIMzExOEEwMTEIMzExOEEwODMIMzExOEEwODcIMzExOEEwOTUIMzExOEIwODIIMzExOEIxMDEIMzExOEMwNzYIMzExOEMwOTkIMzExOEQwNzgIMzExOEYwNzkIMzExOEYxMDAIMzExOEYxMTYIMzExOEYxMjIIMzExOEcwOTYIMzExOEgwNzcIMzExOEgxMDUIMzExOEkwOTgIMzExOEswODAIMzExOEsxMTEIMzExOEwxMDkIMzExOE0xMTMIMzExOE4wODQIMzExOE4wODgIMzExOE8wODYIMzExOE8wOTAIMzExOE8wOTIIMzExOFAxMDgIMzExOFIwODEIMzExOFMwODkIMzExOFMwOTcIMzExOFUwOTEIMzExOFUwOTMIMzExOFYwODUIMzExOFYxMDIIMzExOFgwOTQUKwNBZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIDDxAPFgYfAAUKc3RyZWV0bmFtZR8BBQpzdHJlZXRjb2RlHwJnZBAVDAgo5YWo6YCJKQnnmb3puaTplYcJ6YeN5Zu66ZWHCeWNjuaWsOmVhwnph5Hms73plYcJ57uD5aGY6ZWHDOWkj%2BmYs%2Bihl%2BmBkw%2FpppnoirHmoaXooZfpgZMJ5b6Q5rO%2B6ZWHDOebiOa1puihl%2BmBkwnotbXlt7fplYcM5pyx5a626KeS6ZWHFQwABDE4MTAEMTgwOQQxODA4BDE4MDUEMTgwNAQxODAxBDE4MTEEMTgwNwQxODAyBDE4MDYEMTgwMxQrAwxnZ2dnZ2dnZ2dnZ2dkZAIIDxBkZBYBZmQCCg8QDxYGHwAFCENPREVOQU1FHwEFCUNPREVWQUxVRR8CZ2QQFQMIKOWFqOmAiSkM5Yy657qn552j5a%2BfEuW4gue6p%2Bedo%2BafpeS4i%2Ba0vhUDAAI1NAI0MhQrAwNnZ2dkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WCAUMcmFkaW9fVGFza0lEBQxyYWRpb19UYXNrSUQFEnJhZGlvX0Rpc2NvdmVyVGltZQUOcmFkaW9fS2VlcGVyU04FDnJhZGlvX0tlZXBlclNOBQlyYWRpb19hc2MFCXJhZGlvX2FzYwUKcmFkaW9fZGVzYxhd4qSfGndY8UX2Nba2vbvtJndRUbLDaDkPZiApzCnN&__EVENTVALIDATION=%2FwEWYAL%2BqPr3CQKQspmwBwLk48qbDQLOlcDSCwLo%2F7%2BQDQLo%2F9%2FOBwLFlKL%2FBwLFlLbaDgLFlPqlAQLFlI6ACALFlNKTAgLFlObOCQLFlKrYAwLFlL63CwLFlMLVCQLFlNawAQK%2BgoTKCQK%2BgpihAQK%2BgtywCwK%2BgvDvAgK%2BgrT5BAK%2BgsjVAwK%2BgoynBgK%2BgqCCDQK%2BgqSjDAK%2BgrieCwKbu%2BbRAwKbu%2FqMCwKbu76eDQKbu9L6BAKbu5bEDgKbu6qjBgLSlKL%2FBwLSlLbaDgLBoZrDBALBocr3BwK639SUCALCoYbkDQL6%2F8%2FMBAKexuXnBwK838TeBwKbxv3jDQKdxpHeBAL2%2F7uQDQLTlKbYAwLMjdiwCwK435jmAgKHxvnCDgLg%2F%2F%2FjBwKi37DiCALLoa6%2BDALclLLaDgL8%2F%2B%2BlDwLWlIqACALGod7SDgLGoc6UBgLHobabCAKg35CFBgKg3%2BjzBwKI%2F9vOBwLSocKaCwLToeLzDQLM3qzdCQLG3qTgDQLG3vyuDwLuofKJBgKG%2F5PeDgK138C5AQKx6YCLDAL1%2FouWBgKYx%2FmOAQKYx43qCQKYx4nLCAKYx52QAQKYx9mnCwL1%2FvfKDQKYx%2BGCDwKYx8XaAgKYx%2FXvBwKYx7H9CQKIzqC9CQLxheGJCwLbh93iAQK7lM2hDwLr%2FqzcBwLgkfaxCwLnkc6xCwLGw9ygAgKx26DYBgKW%2B8FSAtmzgu4FAqChxTMCkeLu%2BQYC8NfbvQsCkcCfxAwCg8an8gf%2F5Bh5tJGR5MuvPWR0fhf0CUWeQrECjzmq7GRs5Ym%2FJg%3D%3D&txt_planName=&txt_TaskID=&ddl_Keeper=&ddl_Street=1806&txt_StartDate=&txt_EndDate=&select_infotype=&txt_address=&txt_hotlinesn=&ddl_CodeList=&RadioArea=radio_DiscoverTime&RadioSort=radio_desc&Querybtn=%E6%9F%A5++%E8%AF%A2&SelectID=&pageindex=0'
url="http://10.231.18.25/INSGRID/caseoperate_flat/ALLCASELIST.ASPX?STATUSID=3&CATEGORYID=120"

# proxies = {
    # 'http': 'socks5://0.tcp.ap.ngrok.io:13661',
# }

proxies = {
    'http': 'socks5://localhost:10899',
}
# headers=headers
rt=requests.post(url,headers=headers,data=body,proxies=proxies)


soup = BeautifulSoup(rt.content)
for tr in soup.select('#caselist tr')[1:]:
    ls = tr.select('td')
    for i in ls:
        print(i)
 
print(rt.content)


