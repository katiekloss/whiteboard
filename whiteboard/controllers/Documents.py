import whiteboard.template
import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.sqltool
import cherrypy
import os

class Documents:
    """Controller for all document-related actions"""
    
    def documentsMain(self, courseid):
        return whiteboard.template.render('documents.html')

    def addDocument(self, courseid, name=None, upload=None):
        
        if not RoleHelper.current_user_has_role(courseid, 'instructor, ta'):
            return whiteboard.template.render('error.html', context_dict={'error': 'You are not allowed to use this feature'})

        ctx = {'courseid': courseid}
        if cherrypy.request.method == "GET":
            return whiteboard.template.render('addDocument.html', context_dict=ctx)

        elif cherrypy.request.method == "POST":
            path = "files/%s/" % courseid
            sql = whiteboard.sqltool.SqlTool()
            sql.query_text = "INSERT INTO Documents (isfolder, name, path, courseid) VALUES (False, @name, @path, @courseid)"
            sql.addParameter("@name", upload.filename)
            sql.addParameter("@path", path)
            sql.addParameter("@courseid", courseid)
            sql.execute()
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + upload.filename, "wb") as permanent:
                while True:
                    data = upload.file.read(8192)
                    if not data:
                        break
                    permanent.write(data)
            return "File written successfully"
