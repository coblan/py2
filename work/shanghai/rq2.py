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

body="""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <SOAP-ENV:Body>
        <tns:Select xmlns:tns="http://www.china-gis.com/gisshare/">
            <tns:sql>select a.*,b.lastx,b.lasty,b.updatetime as tracktime,case when (b.lastx=0 and b.lasty=0) then '0' else '1' end as onlinestatus,citygrid.FN_GET_CODENAME(a.rank,'028') as RANKTYPE,b.UPLOADNUM,citygrid.F_GET_KEEPERCOLOUR(a.RANK) as rankcolor from citygrid.t_keepersinfo a left join citygrid.t_keeperssameday b on a.keepersn=b.keepersn where 1=1  and a.DEPTCODE ='%(dept)s'  order by a.keepertype desc,onlinestatus desc,a.keepersn</tns:sql>
            <tns:pageSize>0</tns:pageSize>
            <tns:pageIndex>0</tns:pageIndex>
        </tns:Select>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""%(var_dict)


url="http://10.231.18.6/wgh_qp/LogicWebService/Sql/SqlHelper.asmx"

# proxies = {
    # 'http': 'socks5://0.tcp.ap.ngrok.io:13661',
# }

proxies = {
    'http': 'socks5://localhost:10877',
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


