import requests

url = "http://localhost:9494/red/user/upload?bundle_id=android_adultcoloringbookinspirationart&version=v1.0"
files = {'user-file': open(r'C:\Users\heyulin\Downloads\other12.png', 'rb')}

rt = requests.post(url,files=files)
print(rt.text)