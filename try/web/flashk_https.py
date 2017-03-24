from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    #app.run(port=8100)
    #app.run('0.0.0.0',debug=True,port=8100,)
    app.run('0.0.0.0',debug=True,port=8100, ssl_context=(r'D:\cygwin64\home\coblan\myca\server.crt', r'D:\cygwin64\home\coblan\myca\server.key'))