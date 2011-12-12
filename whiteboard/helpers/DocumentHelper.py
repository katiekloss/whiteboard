import whiteboard.sqltool

class DocumentHelper:

    @staticmethod
    def create_file(name, path, courseid, assignmentid):
        
        sql = whiteboard.sqltool.SqlTool()
        if assignmentid != None:
            sql.query_text = "INSERT INTO Documents (isfolder, name, path, courseid, assignmentid) VALUES (False, @name, @path, @courseid, @assignmentid)"
            sql.addParameter("@assignmentid", assignmentid)
        else:
            sql.query_text = "INSERT INTO Documents (isfolder, name, path, courseid) VALUES (False, @name, @path, @courseid)"
        sql.addParameter("@name", name)
        sql.addParameter("@path", path)
        sql.addParameter("@courseid", courseid)
        sql.execute()
        sql.query_text = "SELECT LASTVAL() as id"
        with sql.execute() as datareader:
            return datareader.fetch()['id']
        
    @staticmethod
    def get_file(documentid):
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT * FROM Documents WHERE documentid = @documentid"
        sql.addParameter("@documentid", documentid)
        with sql.execute() as datareader:
            if datareader.rowcount() == 0:
                return None
            return datareader.fetch()

    @staticmethod
    def get_files_for_course(courseid):
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT * FROM Documents WHERE courseid = @courseid"
        sql.addParameter("@courseid", courseid)

        documents = []
        with sql.execute() as datareader:
            for row in datareader:
                documents.append(row)
        return documents
