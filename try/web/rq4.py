import requests

start=1130695
for i in range(100):
    start+=1
    url='http://localhost:9494/user_report?bundle_id=new_bundle&kind=Not of Public Interest&image_id=%s'%start
    requests.get(url)
    print(start)

