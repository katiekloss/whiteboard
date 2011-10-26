import psycopg2
import psycopg2.extras

import cherrypy

class SqlTool:
    """Class for executing SQL queries and retrieving their results.
    Example:
        sql = SqlTool("host=sqlserver.domain.local dbname=testdb user=sqluser")
        sql.query_text = "SELECT * FROM Users WHERE userid=@userid;"
        sql.addParameter("@userId", 5)
        with sql.execute() as datareader:
           row = datareader.fetch()
           print row['username']
    """

    #: Stores the text of the next SQL query to be executed
    query_text = None

    #: Dictionary of named parameters and their values
    __parameters = {}

    #: SqlTool Constructor
    def __init__(self):
        self.__dbconn = psycopg2.connect(cherrypy.config['db_connstring'])
    
    def __del__(self):
        try:
            self.__dbconn.commit()
            self.__dbconn.close()
        except:
            pass

    def addParameter(self, param_name, param_value):
        """Adds a named parameter to a previously-set query.
        
        Parameters can be named whatever you want, but keep in mind
        that on execution SqlTool will add the parameter placeholders
        using string replacement. You may want to use a convention
        such as @parametername for parameter names so that you don't end
        up replacing a regular SQL keyword with a placeholder.
        """

        self.__parameters[param_name] = param_value


    def execute(self):
        """Executes the query (with any named parameters)"""
        
        # I don't like the %(parameter)s convention, so
        # this converts whatever parameter convention you use
        # to Psycopg2's (e.g. "@userid" becomes "%(@userid)s"
        for key in self.__parameters:
            self.query_text = self.query_text.replace(key, "%%(%s)s" % key)

        dbcursor = self.__dbconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dbcursor.execute(self.query_text, self.__parameters)
        return SqlCursor(dbcursor)


class SqlCursor:
    """Class for accessing the results of a query executed via SqlTool.execute()"""

    def __init__(self, cursor):
        
        self.__cursor = cursor

    def __del__(self):

        try:
            self.__cursor.close()
        except:
            pass

    # Iterator methods next() and __iter__()
    def next(self):
        
        row = self.fetch()
        if row == None:
            raise StopIteration
        return row

    def __iter__(self):
        
        return self

    def fetch(self):
        """Fetches a single row from the result set.

        Returns a dictionary of the form {columnName: columnValue}
        or None if there are no more rows in the result set.
        """
       
        try:
            row = self.__cursor.fetchone()
        except psycopg2.ProgrammingError:
            row = None
        return row

    def rowcount(self):
        """Returns the number of rows in the result set"""

        return self.__cursor.rowcount

    # Context manager methods __enter__ and __exit__
    def __enter__(self):
        
        return self

    def __exit__(self, type, value, traceback):
        
        try:
            self.__cursor.close()
        except:
            pass
