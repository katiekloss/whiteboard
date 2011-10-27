import cherrypy
import whiteboard.sqltool
import whiteboard.template

class Course:
    """Controller for all /course/* URLS"""

    def courseMain(self, courseid):
        """Serves main page for a course"""

        ctx = {}

        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT * FROM Courses WHERE courseid=@courseid;"
        sql.addParameter("@courseid", courseid)
        with sql.execute() as datareader:
            if datareader.rowcount() != 1:
                errorctx = {'error': 'The specified course (ID %s) does not exist' % courseid}
                return whiteboard.template.render('error.html', context_dict=errorctx)
            ctx['courseinfo'] = datareader.fetch()

        ctx['announcements'] = []
        sql.query_text = "SELECT date, content, caseid FROM Announcements WHERE courseid=@courseid;"
        sql.addParameter("@courseid", courseid)
        with sql.execute() as datareader:
            for row in datareader:
                ctx['announcements'].append(row)
        
        return whiteboard.template.render('course.html', context_dict=ctx)
