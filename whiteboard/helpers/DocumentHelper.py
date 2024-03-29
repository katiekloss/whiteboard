import whiteboard.sqltool

class DocumentHelper:

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
        
        sql.query_text = "SELECT * FROM Documents WHERE courseid = @courseid AND type = 'document'"
        sql.addParameter("@courseid", courseid)

        documents = []
        with sql.execute() as datareader:
            for row in datareader:
                documents.append(row)
        return documents
