import whiteboard.sqltool
import cherrypy
import psycopg2

class RoleHelper:
    """Class for handling role-related functionality"""

    site_role_names = ['siteroleadmin', 'student', 'instructor']
    course_role_names = ['student', 'ta', 'instructor']

    @staticmethod
    def current_user_has_role(courseid, role):
        """Returns True if the current user has any of the specified roles
        on the given course, returns False otherwise.
        """

        sql = whiteboard.sqltool.SqlTool()
        # Unfortunately need to override the parameter replacement for this to work
        sql.query_text = """SELECT * FROM Roles WHERE caseid=@caseid
            AND courseid=@courseid
            AND rolename IN (%s)""" % ','.join(["'%s'" % x.strip() for x in role.split(',')])
        sql.addParameter("@caseid", cherrypy.session['username'])
        sql.addParameter("@courseid", courseid)
        with sql.execute() as datareader:
            if datareader.rowcount() > 0:
                return True
            else:
                return False

    @staticmethod
    def grant_user_role(username, courseid, role):
        """Grants the given user the specified role.
        Does nothing if the user already has the role.
        """

        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "INSERT INTO Roles VALUES (@caseid, @courseid, @rolename);"
        sql.addParameter("@caseid", username)
        sql.addParameter("@courseid", courseid)
        sql.addParameter("@rolename", role)
        try:
            sql.execute()
        except psycopg2.IntegrityError:
            # Ignore cases where role is already granted
            pass

    @staticmethod
    def revoke_user_role(username, courseid, role):
        """Revokes this role from the given user.
        Does nothing if role was never granted.
        """

        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = """DELETE FROM Roles WHERE caseid = @caseid
            AND courseid = @courseid
            AND rolename = @rolename;"""
        sql.addParameter("@caseid", username)
        sql.addParameter("@courseid", courseid)
        sql.addParameter("@rolename", role)
        sql.execute()
