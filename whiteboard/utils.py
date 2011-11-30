import cherrypy
from urlparse import urlparse

def url(target):

    return urlparse(cherrypy.request.base).path + target
