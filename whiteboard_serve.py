#!/usr/bin/env python2.7
import cherrypy

import whiteboard.auth.CASAuthTool

class WhiteboardApp:
    def index(self):
        return "Hi! I'm Whiteboard!"

def create_routes():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    root = WhiteboardApp()

    # ROUTES START HERE
    dispatcher.connect('index', '/', controller=root, action='index')
    # ROUTES END HERE

    return dispatcher

if __name__ == "__main__":
    dispatcher = create_routes()
    conf = {
        '/': {'request.dispatch': dispatcher,
              'tools.sessions.on': True,
              'tools.cas_auth.on': True,
              'tools.cas_auth.cas_server_root': 'https://login.case.edu/cas/'
    }}
    
    cherrypy.tree.mount(root=None, config=conf)

    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.engine.signal_handler.handlers = {'SIGINT': cherrypy.engine.exit}
    cherrypy.engine.signal_handler.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
