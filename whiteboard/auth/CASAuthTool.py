import cherrypy
import urllib2

import whiteboard.sqltool

def database_trigger(username, cas_ticket):
    """Checks to ensure that the given user is present in the Users table
    and records the login to LoginLog.
    """

    sql = whiteboard.sqltool.SqlTool()
    try:
        sql.query_text = "SELECT * FROM Users WHERE caseid=@caseid;"
        sql.addParameter("@caseid", username)
        with sql.execute() as datareader:
            if datareader.rowcount() == 0:
                sql.query_text = "INSERT INTO Users VALUES (@caseid)"
                sql.addParameter("@caseid", username)
                sql.execute()

        sql.query_text = "INSERT INTO LoginLog VALUES (NOW(), @caseid, @ip_addr, @ticket);"
        sql.addParameter("@caseid", username)
        sql.addParameter("@ip_addr", cherrypy.request.remote.ip)
        sql.addParameter("@ticket", cas_ticket)
        sql.execute()
    except:
        sql.rollback = True
        raise

def auth_handler(cas_server_root, cas_check_path):

    def redirect_to_cas():
        raise cherrypy.HTTPRedirect(cas_server_root + 'login?service=%s' % cherrypy.url(cas_check_path))

    def get_cas_username(ticket):
        cas_check_url = cas_server_root + 'validate?ticket=%s&service=%s' % (ticket, cherrypy.url(cas_check_path))
        cas_response = urllib2.urlopen(cas_check_url).read()
        if cas_response[0:3] == "yes":
            return cas_response[4:].strip()
        else:
            return None

    # Actual CAS authentication logic
    if cherrypy.request.path_info == cas_check_path:
        if 'ticket' in cherrypy.request.params:
            ticket = cherrypy.request.params['ticket']
            username = get_cas_username(ticket)
            if username is not None:
                cherrypy.session['username'] = username
                database_trigger(username, ticket)
                raise cherrypy.HTTPRedirect(cherrypy.url('/'))

    if not 'username' in cherrypy.session:
        redirect_to_cas()

cherrypy.tools.cas_auth = cherrypy.Tool('before_handler', auth_handler)
