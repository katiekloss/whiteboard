#!/usr/bin/env python2.7
import cherrypy

import whiteboard.auth.CASAuthTool
from whiteboard.controllers import *

def create_routes():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    # ROUTES START HERE
    dispatcher.connect('staticContent', '/static/{file_name:.*}', controller=Static(), action='serve')
    dispatcher.connect('index', '/', controller=Root(), action='index')
    dispatcher.connect('documenthandler', '/document/{documentid}', controller=Documents(), action='serve')

    dispatcher.connect('siteRoleAdmin', '/roleadmin', controller=RoleAdmin(), action='siteRoleAdmin')
    dispatcher.connect('siteRoleSubmit', '/ajax/siteRoleSubmit', controller=Ajax(), action='siteRoleSubmit')
    dispatcher.connect('siteRoleValidate', '/ajax/siteRoleValidate', controller=Ajax(), action='siteRoleValidate')

    dispatcher.connect('courseRoleAdmin', '/course/{courseid}/roleadmin', controller=Course(), action='courseRoleAdmin')
    dispatcher.connect('courseRoleSubmit', '/ajax/courseRoleSubmit', controller=Ajax(), action='courseRoleSubmit')
    dispatcher.connect('courseRoleValidate', '/ajax/courseRoleValidate', controller=Ajax(), action='courseRoleValidate')

    dispatcher.connect('course', '/course/{courseid}/', controller=Course(), action='courseMain')
    dispatcher.connect('addAnnouncement', '/course/{courseid}/addAnnouncement', controller=Course(), action='addAnnouncement')
    dispatcher.connect('ajaxAddAnnouncement', '/ajax/courseAddAnnouncement', controller=Ajax(), action='courseAddAnnouncement')

    dispatcher.connect('addDocument', '/course/{courseid}/addDocument', controller=Documents(), action='addDocument', conditions=dict(method=['GET']))
    dispatcher.connect('addDocument_POST', '/course/{courseid}/addDocument', controller=Documents(), action='addDocument_POST', conditions=dict(method=['POST']))

    dispatcher.connect('createAssignmentGET', '/course/{courseid}/createassignment', controller=Assignments(), action='createAssignment', conditions=dict(method=['GET']))
    dispatcher.connect('createAssignmentPOST', '/course/{courseid}/createassignment', controller=Assignments(), action='createAssignment_POST', conditions=dict(method=['POST']))

    dispatcher.connect('documents', '/course/{courseid}/documents{subfolder:.*}', controller=Documents(), action='documentsMain')
    dispatcher.connect('assignments', '/course/{courseid}/assignments', controller=Assignments(), action='assignmentsMain')
    dispatcher.connect('grades', '/course/{courseid}/grades', controller=Grades(), action='gradesMain')

    dispatcher.connect('editGrades', '/course/{courseid}/editGrades', controller=Grades(), action='editGrades')
    dispatcher.connect('ajaxEditGrade', '/ajax/editGrade', controller=Ajax(), action='editGrade')
   
    dispatcher.connect('assignmentResponse', '/course/{courseid}/assignmentresponse/{assignmentid}', controller=Assignments(), action='assignmentResponse', conditions=dict(method=['GET']))
    dispatcher.connect('assignmentResponsePOST', '/course/{courseid}/assignmentresponse/{assignmentid}', controller=Assignments(), action='assignmentResponse_POST', conditions=dict(method=['POST']))

    dispatcher.connect('createCourseGET', '/createCourse', controller=Root(), action='createCourse', conditions=dict(method=['GET']))
    dispatcher.connect('createCoursePOST', '/createCourse', controller=Root(), action='createCourse_POST', conditions=dict(method=['POST']))

    dispatcher.connect('bulkRoleAddGET', '/course/{courseid}/bulkRoleAdd', controller=Course(), action='bulkRoleAdd', conditions=dict(method=['GET']))
    dispatcher.connect('bulkRoleAddPOST', '/course/{courseid}/bulkRoleAdd', controller=Course(), action='bulkRoleAdd_POST', conditions=dict(method=['POST']))

    dispatcher.connect('createFolderGET', '/course/{courseid}/createFolder', controller=Documents(), action='createFolder', conditions=dict(method=['GET']))
    dispatcher.connect('createFolderPOST', '/course/{courseid}/createFolder', controller=Documents(), action='createFolder_POST', conditions=dict(method=['POST']))

    dispatcher.connect('viewResponses', '/course/{courseid}/viewresponses/{assignmentid}', controller=Assignments(), action='viewResponses')
    # ROUTES END HERE

    return dispatcher

if __name__ == "__main__":
    dispatcher = create_routes()
   
    cherrypy.config.update('config.ini')
    
    core_config = {'/': {
        'request.dispatch': dispatcher,
        'tools.sessions.on': True,
        'tools.sessions.storage_type': 'file',
        'tools.sessions.storage_path': 'session_store',
        'tools.cas_auth.on': True,
        'tools.cas_auth.cas_server_root': 'https://login.case.edu/cas/',
        'tools.cas_auth.cas_check_path': '/Auth/CAS',
        'tools.proxy.on': True,
        'tools.proxy.base': 'http://vale.case.edu/whiteboard',
        'tools.proxy.local': ''
    }}

    cherrypy.tree.mount(root=None, script_name='/', config=core_config)

    cherrypy.engine.signal_handler.handlers = {'SIGINT': cherrypy.engine.exit}
    cherrypy.engine.signal_handler.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
