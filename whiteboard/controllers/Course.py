import cherrypy
import whiteboard.sqltool
import whiteboard.template
import whiteboard.helpers.CourseHelper as CourseHelper
import whiteboard.helpers.AnnouncementHelper as AnnouncementHelper

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
