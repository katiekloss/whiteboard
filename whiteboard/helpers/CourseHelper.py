import whiteboard.sqltool

class CourseHelper:
    """Helper for course-related functionality"""

    @staticmethod
    def create_course(title, code, term):
        
        sql = whiteboard.sqltool.SqlTool()
        try:
            sql.query_text = "INSERT INTO Courses (title, code, term) VALUES (@title, @code, @term)"
            sql.addParameter("@title", title)
            sql.addParameter("@code", code)
            sql.addParameter("@term", term)
            return sql.executeWithId()
        except:
            sql.rollback = True
            raise

    @staticmethod
    def fetch_course(courseid):
        """Returns the Course corresponding to the given courseid
        or None if the course does not exist.
        """

        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT * FROM Courses WHERE courseid=@courseid;"
        sql.addParameter("@courseid", courseid)
        with sql.execute() as datareader:
            if datareader.rowcount() == 0:
                return None
            return datareader.fetch()

    @staticmethod
    def fetch_users_in_role(courseid, rolename):
       
        users = []
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT * FROM Roles WHERE courseid = @courseid AND rolename = @rolename"
        sql.addParameter("@courseid", courseid)
        sql.addParameter("@rolename", rolename)
        with sql.execute() as datareader:
            for user in datareader:
                users.append(user)
        return users
