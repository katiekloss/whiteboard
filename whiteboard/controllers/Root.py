import whiteboard.template
import whiteboard.sqltool
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
