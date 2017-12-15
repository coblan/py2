import requests
import xmltodict
headers = {'SOAPAction':"http://www.china-gis.com/gisshare/Select",
           'content-type': 'text/xml'}


var_dict={
    'inspector':'31189242',
    'start':'2017121400',
    'end':'2017121500'
}

body="""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SOAP-ENV:Body>
    <tns:Select xmlns:tns="http://www.china-gis.com/gisshare/">
      <tns:sql>select a.*,CITYGRID.Fn_GetStreetName(a.streetcode) as streetname,CITYGRID.Fn_GetCommunityName(trim(a.communitycode)) as communityname  from (select t.taskid,t.KEEPERSN,t.gridcode,CITYGRID.F_REC_IBC_NAME_NEW(t.infobccode,t.infotypeid) as infobcname,CITYGRID.F_REC_ISC_NAME_NEW(t.infobccode,t.infosccode,t.infotypeid)  as infoscname,  CITYGRID.F_REC_INFOTYPENAME_New(t.infotypeid) as infotypename,t.address,t.discovertime,t.coordx,t.coordy,t.streetcode,t.communitycode,t.infosourceid,citygrid.F_INFOSOURCEname(t.infosourceid) SOURCENAME from citygrid.t_info_main t   where t.keepersn = '%(inspector)s' and t.discovertime &gt;=to_date('%(start)s', 'YYYY-MM-DD HH24:MI:SS')  and t.discovertime &lt;=to_date('%(end)s', 'YYYY-MM-DD HH24:MI:SS')   order by t.discovertime) a</tns:sql>
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
    'http': 'socks5://localhost:18777',
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
print(dc)




# var_dict={
    # 'inspector':'31189242',
    # 'start':'2017082200',
    # 'end':'2017082223'
# }

# body="""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  # <SOAP-ENV:Body>
    # <tns:Select xmlns:tns="http://www.china-gis.com/gisshare/">
      # <tns:sql>select a.*,CITYGRID.Fn_GetStreetName(a.streetcode) as streetname,CITYGRID.Fn_GetCommunityName(trim(a.communitycode)) as communityname  from (select t.taskid,t.KEEPERSN,t.gridcode,CITYGRID.F_REC_IBC_NAME_NEW(t.infobccode,t.infotypeid) as infobcname,CITYGRID.F_REC_ISC_NAME_NEW(t.infobccode,t.infosccode,t.infotypeid)  as infoscname,  CITYGRID.F_REC_INFOTYPENAME_New(t.infotypeid) as infotypename,t.address,t.discovertime,t.coordx,t.coordy,t.streetcode,t.communitycode,t.infosourceid,citygrid.F_INFOSOURCEname(t.infosourceid) SOURCENAME from citygrid.t_info_main t   where t.keepersn = '31189242' and t.discovertime &gt;=to_date('2017082200', 'YYYY-MM-DD HH24:MI:SS')  and t.discovertime &lt;=to_date('2017082223', 'YYYY-MM-DD HH24:MI:SS')   order by t.discovertime) a</tns:sql>
      # <tns:pageSize>0</tns:pageSize>
      # <tns:pageIndex>0</tns:pageIndex>
    # </tns:Select>
  # </SOAP-ENV:Body>
# </SOAP-ENV:Envelope>""".format(**var_dict)