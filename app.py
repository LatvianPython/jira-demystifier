import cherrypy


class CherryApp(object):

    @cherrypy.expose()
    def index(self):
        return 'Hello World'


if __name__ == '__main__':
    cherrypy.quickstart(CherryApp(), '/')
