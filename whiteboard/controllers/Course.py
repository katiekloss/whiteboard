import cherrypy
import whiteboard.sqltool
import whiteboard.template
import whiteboard.helpers.CourseHelper as CourseHelper
import whiteboard.helpers.AnnouncementHelper as AnnouncementHelper
import whiteboard.helpers.RoleHelper as RoleHelper

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

    def courseRoleAdmin(self, courseid):
        """Render the roleadmin view"""

        if not RoleHelper.current_user_has_role(courseid, 'instructor'):
            ctx = {'error': 'You are not permitted to edit course roles.'}
            return whiteboard.template.render('error.html', context_dict = ctx)

        return whiteboard.template.render('courseroleadmin.html', context_dict = {'courseid': courseid})

    def addAnnouncement(self, courseid):
        """Render announcement creation page"""

        if not RoleHelper.current_user_has_role(courseid, 'instructor,ta'):
            ctx = {'error': 'You must be an instructor or TA to use this feature.'}
            return whiteboard.template.render('error.html', context_dict = ctx)

        return whiteboard.template.render('courseaddannouncement.html', context_dict = {'courseid': courseid})
