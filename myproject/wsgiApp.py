from paste import reloader
from paste.httpserver import serve

top = "<div class='top'>Middleware TOP</div>"
bottom =  "<div class='botton'>Middleware BOTTOM</div>"

"""MiddleWare Application
"""

class MiddleWareApp(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = self.app(environ, start_response)[0]
        
		if response.find('<body>') >-1:
            head,body = response.split('<body>')
            bodyend,htmlend = body.split('</body>')
            bodyend = '<body>'+ top + bodyend + bottom + '</body>'
            yield head + bodyend + htmlend
        
		else:
            yield top + response + bottom
    

import os


"""WSGI server"""

def app(environ, start_response):
    
    path = environ['PATH_INFO']
    filePath = '.' + path  
    if not os.path.isfile(filePath):
        filePath ='./index.html' 

    fd = open(filePath,'r')
    fileContent = fd.read()

    fd.close()

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [fileContent ]

app = MiddleWareApp(app)


if __name__ == '__main__':
    from paste import reloader
    from paste.httpserver import serve

    reloader.install()
    serve(app, host='127.0.0.1', port=8000)