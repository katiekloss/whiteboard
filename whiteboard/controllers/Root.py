import whiteboard.template
import whiteboard.sqltool
import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.helpers.CourseHelper as CourseHelper
from whiteboard.utils import url
import cherrypy

class Root:
    def index(self):
        context = {'announcements': [], 'courses': []}
        
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT DISTINCT code, title, courseid FROM CourseRegistration WHERE caseid = @caseid"
        sql.addParameter("@caseid", cherrypy.session['username'])
        with sql.execute() as datareader:
            for row in datareader:
                context['courses'].append(row)

        sql.query_text = """SELECT A.date, A.content, A.caseid, R.code
        FROM Announcements A
        JOIN
        (
            SELECT DISTINCT code, title, courseid
            FROM CourseRegistration
            WHERE caseid = @caseid
        ) AS R ON A.courseid = R.courseid
        WHERE A.date > (NOW()::date - '1 week'::interval)::date;"""
        sql.addParameter("@caseid", cherrypy.session['username'])
        with sql.execute() as datareader:
            for row in datareader:
                context['announcements'].append(row)

        return whiteboard.template.render('index.html', context_dict=context)

    @RoleHelper.require_role('siteroleadmin', 'Only site administrators can use this tool')
    def createCourse(self):
        
        return whiteboard.template.render('createcourse.html')

    @RoleHelper.require_role('siteroleadmin', 'Only site administrators can use this tool')
    def createCourse_POST(self, coursetitle, coursecode, courseterm, courseinstructor):

        new_course_id = CourseHelper.create_course(coursetitle, coursecode, courseterm)
        RoleHelper.grant_user_role(courseinstructor, new_course_id, 'instructor')

        raise cherrypy.HTTPRedirect(url('/course/%i/' % new_course_id))
