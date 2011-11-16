import whiteboard.sqltool

class AssignmentHelper:

    @staticmethod
    def fetch_assignments_for_course(courseid):
        
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT * FROM Assignments WHERE courseid=@courseid"
        sql.addParameter("@courseid", courseid)
        assignments = []
        with sql.execute() as datareader:
            for row in datareader:
                assignments.append(row)

        return assignments
