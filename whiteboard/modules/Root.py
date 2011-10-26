import whiteboard.template

class Root:
    def index(self):
        return whiteboard.template.render('index.html')
