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
