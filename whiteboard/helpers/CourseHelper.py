import whiteboard.sqltool

class CourseHelper:
    """Helper for course-related functionality"""

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
