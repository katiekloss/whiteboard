import whiteboard.template
import cherrypy

class Static:
    """Controller for static content"""

    def serve(self, file_name):
        """Serves a static template such as a CSS stylesheet file"""
        cherrypy.response.headers['Content-Type'] = 'text/css'
        return whiteboard.template.render('static/' + file_name)
