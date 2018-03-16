
# encoding:utf-8

import requests
import xmltodict
headers = {'SOAPAction':"http://www.china-gis.com/gisshare/Select",
           'content-type': 'text/xml'}


var_dict={
    #'inspector':'31189242',
    #'start':'2017121400',
    #'end':'2017121500',
    'dept':'20601', # 赵项代码
}

sql="""SELECT CITYGRID.F_MAIN_STATUS(status) 案件状态,TASKID 任务号,CITYGRID.F_REC_INFOSOURCENAME(INFOSOURCEID) 案件来源,TO_CHAR (DISCOVERTIME, 'yyyy-mm-dd hh24:mi') 发现时间,CITYGRID.F_REC_INFOTYPENAME_NEW(INFOTYPEID) 案件属性,CITYGRID.F_REC_IBC_NAME_NEW(INFOBCCODE,INFOTYPEID) 案件大类,CITYGRID.F_REC_ISC_NAME_NEW(INFOBCCODE,INFOSCCODE,INFOTYPEID) 案件小类,CITYGRID.F_REC_IZC_NAME(INFOBCCODE,INFOSCCODE,INFOZCCODE,INFOTYPEID) 案件子类,CITYGRID.F_REC_STREETNAME(STREETCODE) 街镇,Address 发生地址,TO_CHAR (DISPATCHTIME, 'yyyy-mm-dd hh24:mi') 派遣时间,CITYGRID.F_REC_MAINDEPTNAME (EXECUTEDEPTCODE, DEPTCODE, TASKID) 主责部门,CITYGRID.F_REC_THREEDEPTNAME(EXECUTEDEPTCODE,DEPTCODE,TASKID) 三级主责部门,TO_CHAR (ENDTIME, 'yyyy-mm-dd hh24:mi') 结案时间  FROM (SELECT tt.*, ROWNUM AS rowno  FROM (SELECT * FROM CITYGRID.T_INFO_MAIN main  WHERE 1=1  and  discovertime between  TO_DATE('2018-01-05 00:00:00','yyyy-MM-dd HH24:mi:ss')  and  TO_DATE('2018-02-05 23:59:59','yyyy-MM-dd HH24:mi:ss') and instr(KEEPERSN ,'31189633')>0  )tt  WHERE ROWNUM <= 10) table_alias WHERE table_alias.rowno >0
"""

body="""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <SOAP-ENV:Body>
        <tns:Select xmlns:tns="http://www.china-gis.com/gisshare/">
            <tns:sql>{sql}</tns:sql>
            <tns:pageSize>0</tns:pageSize>
            <tns:pageIndex>0</tns:pageIndex>
        </tns:Select>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>""".format(sql=sql)


url="http://10.231.18.6/wgh_qp/LogicWebService/Sql/SqlHelper.asmx"

# proxies = {
    # 'http': 'socks5://0.tcp.ap.ngrok.io:13661',
# }

proxies = {
    'http': 'socks5://localhost:10899',
}

rt=requests.post(url,headers=headers,data=body,proxies=proxies)

dc=xmltodict.parse(rt.content)

def parse_rt(dc):
    env = dc.get('soap:Envelope')
    bd = env.get('soap:Body')
    sel =bd.get('SelectResponse')
    sel_rt = sel.get('SelectResult')
    dc2 = xmltodict.parse(sel_rt)
    rt = dc2.get('Result')
    rows = rt.get('Rows')
    row = rows.get('Row')
    return row

jj= parse_rt(dc)
print(dc)




