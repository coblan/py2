import SimpleHTTPServer
import SocketServer
import os
os.chdir(r'D:\try\localweb')
PORT = 3456

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
