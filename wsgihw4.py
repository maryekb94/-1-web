
import selector
from jinja2 import Environment,FileSystemLoader

status = '200 OK'
http_headers = [('Content-Type', 'text/html; charset=UTF-8')]
ABOUTME = """<a href="about/about.html">GO TO aboutme.html</a>"""
INDEX = """<a href="../index.html">GO TO INDEX.HTML</a>"""


class BaseApp(object):

    def __init__(self,environ,start_response,link,template):
        self.env = environ
        self.start_response = start_response
        self.teplates  = Environment(loader=FileSystemLoader('templates'))
        self.template = template
        self.link = link

    def __iter__(self):
        self.start_response(status,http_headers)
        template = self.teplates.get_template(self.template)
        yield template.render(link=self.link)
             
class IndexApp(BaseApp):
    def __init__(self,environ,start_response):
        BaseApp.__init__(self, environ, start_response, ABOUTME, "index.html")

class AboutApp(BaseApp):
    def __init__(self,environ,start_responce):
        BaseApp.__init__(self,environ,start_responce,INDEX,"about.html")

def init():
    disp =  selector.Selector()
    disp.add("/index.html",GET=IndexApp)
    disp.add("/about/about.html",GET=AboutApp)
    return disp



if __name__=="__main__":
    from paste.httpserver import serve
    app = init()
    serve( app, host='localhost', port=8000)
