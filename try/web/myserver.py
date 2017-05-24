# encoding:utf-8
import os
import urlparse
import json

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  
class TestHTTPHandler(BaseHTTPRequestHandler):  
    def do_GET(self):  
  
        buf = 'It works'
        self.protocal_version = 'HTTP/1.1'
  
        self.send_response(200)  
  
        self.send_header("Welcome", "Contect")         
  
        self.end_headers()  
        
        o=urlparse.urlparse(self.path)
        args=dict(urlparse.parse_qsl(o.query))
        if self.path=='/file':
            self.wfile.write(self.path)
            
    
    def do_POST(self):
        buf = 'It works'
        self.protocal_version = 'HTTP/1.1'
  
        self.send_response(200)  
  
        self.send_header("Welcome", "Contect")     
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('content-type','application/json')
        self.end_headers()  
        
        varLen = int(self.headers['Content-Length'])
        if varLen:
            args=json.loads(self.rfile.read(varLen))
        else:
            args=json.loads(self.rfile.read())
        
        func_name=args.pop('func')
        func = globals().get(func_name)
        

        rt = func(**args)
        
        self.wfile.write(json.dumps(rt))
         
        # if self.path=='/file':
            # ls = os.listdir(args.get('path'))
            # self.wfile.write(json.dumps(ls))        
        # self.wfile.write(buf)  
        
  
def start_server(port):  
    http_server = HTTPServer(('127.0.0.1', int(port)), TestHTTPHandler)  
    http_server.serve_forever() #设置一直监听并接收请求



def get_files(path):
    ls = os.listdir(path)
    return ls
   

def get_img():
    
    return r'D:\work\coloring_backend\media\pool\1_pool_cover.png'

if __name__=='__main__':
    start_server(8790)