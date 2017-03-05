import requests
import json

rt = requests.post('http://127.0.0.1:8790/file',data= json.dumps({'path':'d:/try'}))
print(rt.text)