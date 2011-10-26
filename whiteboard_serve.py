#!/usr/bin/env python2.7
import cherrypy

import whiteboard.auth.CASAuthTool
import whiteboard.modules

def create_routes():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    # ROUTES START HERE
    dispatcher.connect('staticContent', '/static/{file_name:.*}', controller=whiteboard.modules.Static(), action='serve')
    dispatcher.connect('index', '/', controller=whiteboard.modules.Root(), action='index')
    # ROUTES END HERE

    return dispatcher

if __name__ == "__main__":
    dispatcher = create_routes()
   
    cherrypy.config.update('config.ini')
    
    core_config = {'/': {
        'request.dispatch': dispatcher,
        'tools.sessions.on': True,
        'tools.cas_auth.on': True,
        'tools.cas_auth.cas_server_root': 'https://login.case.edu/cas/',
        'tools.cas_auth.cas_check_path': '/Auth/CAS'
    }}

    cherrypy.tree.mount(root=None, script_name='/whiteboard', config=core_config)

    cherrypy.engine.signal_handler.handlers = {'SIGINT': cherrypy.engine.exit}
    cherrypy.engine.signal_handler.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
