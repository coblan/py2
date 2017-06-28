import requests
import json

url='http://localhost:9200/megacorp/employee/3'
data={
    "first_name" : "John",
        "last_name" :  "Smith",
        "age" :        25,
        "about" :      "I love to go rock climbing",
        "interests": [ "sports", "music" ]    
}
data={
         "first_name" :  "Douglas",
    "last_name" :   "Fir",
    "age" :         35,
    "about":        "I like to build cabinets",
    "interests":  [ "forestry" ]
    }    

header={ 'Content-Type': 'application/json' }
rt = requests.put(url,data=json.dumps( data),headers=header)
print(rt.content)