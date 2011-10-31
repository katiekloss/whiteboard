import whiteboard.sqltool

class AnnouncementHelper:
    """Helper for announcement-related functionality"""

    @staticmethod
    def fetch_announcements_for_course(courseid):
        """Returns a list of Announcements in the given course"""

        ret = []
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT * FROM Announcements WHERE courseid=@courseid;"
        sql.addParameter("@courseid", courseid)
        with sql.execute() as datareader:
            for row in datareader:
                ret.append(row)
        return ret
