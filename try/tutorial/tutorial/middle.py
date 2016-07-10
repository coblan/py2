import re
class Goagent(object):
    """Custom ProxyMiddleware."""
    #def __init__(self, settings):
        #self.proxy_list = settings.get('PROXY_LIST')
        #with open(self.proxy_list) as f:
            #self.proxies = [ip.strip() for ip in f]

    def process_request(self, request, spider):
        url = request.url
        if re.match(r'^http(s)*://www.google.',url):
            request.meta['proxy'] ='http://127.0.0.1:8087'
        #request.meta['proxy'] = 'http://{}'.format(random.choice(self.proxies))
        
import os

class SaveAll(object):
    def process_request(self, request, spider):
        url = request.url
        print(url)
    
    def process_response(self, request, response, spider):
        url = response.url
        with open(os.path.join(r'd:/try/html',str(hash(url)))+'.html','w') as f:
            f.write(response.body)   
        return response
             