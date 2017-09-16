import requests
rt = requests.get('https://www.google.com')
print(rt.content)