import requests
import json
url = "http://localhost:9494/red/user/upload?bundle_id=android_adultcoloringbookinspirationart&version=v1.0"
rt = requests.post('http://127.0.0.1:8790/file',data= json.dumps({'path':'d:/try'}))
print(rt.text)