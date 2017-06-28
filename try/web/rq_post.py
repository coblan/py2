import requests
import json
url='http://localhost:9200/megacorp/employee/_search'
data={
    "query" : {
        "bool": {
            "must": {
                "match" : {
                    "last_name" : "smith" 
                }
            },
            "filter": {
                "range" : {
                    "age" : { "gt" : 30 } 
                }
            }
        }
    }
}

rt = requests.get(url,data=json.dumps(data))
print(rt.content)