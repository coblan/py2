import requests
import xmltodict
headers = {'SOAPAction':"http://www.china-gis.com/gisshare/Select",
           'content-type': 'text/xml'}
body="""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SOAP-ENV:Body>
    <tns:Select xmlns:tns="http://www.china-gis.com/gisshare/">
      <tns:sql>select a.*,CITYGRID.Fn_GetStreetName(a.streetcode) as streetname,CITYGRID.Fn_GetCommunityName(trim(a.communitycode)) as communityname  from (select t.taskid,t.KEEPERSN,t.gridcode,CITYGRID.F_REC_IBC_NAME_NEW(t.infobccode,t.infotypeid) as infobcname,CITYGRID.F_REC_ISC_NAME_NEW(t.infobccode,t.infosccode,t.infotypeid)  as infoscname,  CITYGRID.F_REC_INFOTYPENAME_New(t.infotypeid) as infotypename,t.address,t.discovertime,t.coordx,t.coordy,t.streetcode,t.communitycode,t.infosourceid,citygrid.F_INFOSOURCEname(t.infosourceid) SOURCENAME from citygrid.t_info_main t   where t.keepersn = '31189242' and t.discovertime &gt;=to_date('2017082200', 'YYYY-MM-DD HH24:MI:SS')  and t.discovertime &lt;=to_date('2017082223', 'YYYY-MM-DD HH24:MI:SS')   order by t.discovertime) a</tns:sql>
      <tns:pageSize>0</tns:pageSize>
      <tns:pageIndex>0</tns:pageIndex>
    </tns:Select>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

url="http://10.231.18.6/wgh_qp/LogicWebService/Sql/SqlHelper.asmx"

proxies = {
    'http': 'socks5://0.tcp.ap.ngrok.io:13661',
}
rt=requests.post(url,headers=headers,data=body,proxies=proxies)

dc=xmltodict.parse(rt.content)
print(dc)