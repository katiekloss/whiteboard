import whiteboard.template

class Static:
    """Controller for static content"""

    def serve(self, file_name):
        """Serves a static template such as a CSS stylesheet file"""

        return whiteboard.template.render('static/' + file_name)
