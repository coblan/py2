import requests
rt = requests.get('http://stash.stm.com/plugins/servlet/archive/projects/CMP/repos/apppagegenerator?at=refs%2Fheads%2Fmaster')
print(rt.content)