import cherrypy
import whiteboard.template
import whiteboard.helpers.CourseHelper as CourseHelper
import whiteboard.helpers.AnnouncementHelper as AnnouncementHelper
import whiteboard.helpers.RoleHelper as RoleHelper
from whiteboard.utils import url

class Course:
    """Controller for all /course/* URLS"""

    def courseMain(self, courseid):
        """Serves main page for a course"""

        ctx = {}

        ctx['course'] = CourseHelper.fetch_course(courseid)
        if ctx['course'] == None:
            errorctx = {'error': 'The specified course (ID %s) does not exist' % courseid}
            return whiteboard.template.render('error.html', context_dict=errorctx)

        ctx['announcements'] = AnnouncementHelper.fetch_announcements_for_course(courseid)

        return whiteboard.template.render('course.html', context_dict=ctx)

    @RoleHelper.require_role('instructor', 'You must be an instructor to edit course roles')
    def courseRoleAdmin(self, courseid):
        """Render the roleadmin view"""

        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            errorctx = {'error': 'The specified course (ID %s) does not exist' % courseid}
            return whiteboard.template.render('error.html', context_dict=errorctx)

        return whiteboard.template.render('courseroleadmin.html', context_dict = ctx)

    @RoleHelper.require_role('instructor,ta', 'Only instructors and TAs are permitted to edit roles')
    def addAnnouncement(self, courseid):
        """Render announcement creation page"""

        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            errorctx = {'error': 'The specified course (ID %s) does not exist' % courseid}
            return whiteboard.template.render('error.html', context_dict=errorctx)

        return whiteboard.template.render('courseaddannouncement.html', context_dict = ctx)

    @RoleHelper.require_role('instructor', 'Only instructors have access to this tool')
    def bulkRoleAdd(self, courseid):
        
        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            errorctx = {'error': 'The specified course (ID %s) does not exist' % courseid}
            return whiteboard.template.render('error.html', context_dict=errorctx)
   
        return whiteboard.template.render('bulkroleadd.html', context_dict=ctx)

    @RoleHelper.require_role('instructor', 'Only instructors have access to this tool')
    def bulkRoleAdd_POST(self, courseid, users, roles = []):
        users = [x.strip() for x in users.strip().split('\n')]

        # I'm just going to pretend that I never wrote this
        if(type(roles) != list):
            roles = roles.split(' ')
        
        for user in users:
            for role in roles:
                RoleHelper.grant_user_role(user, courseid, role)
        raise cherrypy.HTTPRedirect(url('/course/%s/' % courseid))
