import selector
from jinja2 import Environment,FileSystemLoader

status = '200 OK'
http_headers = [('Content-Type','text/html; charset=UTF-8')]

aboutMe = """<a href="about/about.html">GO TO aboutme.html</a>"""
index = """<a href="../index.html">GO TO INDEX.HTML</a>"""


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


class Index(BaseApp):
    def __init__(self,environ,start_response):
        BaseApp.__init__(self,environ,start_response,aboutMe,"index.html")


class AboutMe(BaseApp):
    def __init__(self,environ,start_response):
        BaseApp.__init__(self,environ,start_response,index,"about.html")


def init():
    disp = selector.Selector()
    disp.add("/index.html",GET=Index)
    disp.add("/about/about.html",GET=AboutMe)
    return disp



if __name__=="__main__":
    from paste.httpserver import serve
    application = init()
    serve( application, host='localhost', port=8000)
    
