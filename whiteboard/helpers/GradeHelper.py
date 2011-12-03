import whiteboard.sqltool

class GradeHelper:

    @staticmethod
    def fetch_grades_for_course(courseid, student):
        
        grades = []
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = """SELECT A.assignmentid, due, points, courseid, caseid, score
            FROM Assignments A
            LEFT OUTER JOIN Grades G ON A.assignmentid = G.assignmentid
            AND caseid = @caseid
            WHERE courseid = @courseid"""
        sql.addParameter("@caseid", student)
        sql.addParameter("@courseid", courseid)
        with sql.execute() as datareader:
            for grade in datareader:
                grades.append(grade)

        return grades

    @staticmethod
    def create_or_update_grade(assignmentid, username, points):
        
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = """SELECT * FROM Grades G
            WHERE G.assignmentid = @assignmentid
            AND G.caseid = @caseid"""
        sql.addParameter("@assignmentid", assignmentid)
        sql.addParameter("@caseid", username)
        with sql.execute() as datareader:
            if datareader.rowcount() == 0:
                sql.query_text = """INSERT INTO Grades (assignmentid, caseid, score)
                    VALUES (@assignmentid, @caseid, @score)"""
            else:
                sql.query_text = """UPDATE Grades SET score = @score
                    WHERE assignmentid = @assignmentid AND caseid = @caseid"""
            sql.addParameter("@assignmentid", assignmentid)
            sql.addParameter("@caseid", username)
            sql.addParameter("@score", points)
            sql.execute()
