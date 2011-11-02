import whiteboard.template
import cherrypy

class Static:
    """Controller for static content"""

    def serve(self, file_name):
        """Serves a static template such as a CSS stylesheet file"""
        ext = file_name[file_name.rindex('.'):]
        if ext == ".css":
            cherrypy.response.headers['Content-Type'] = 'text/css'
        elif ext == ".js":
            cherrypy.response.headers['Content-Type'] = 'text/javascript'

        return open('templates/static/' + file_name)
