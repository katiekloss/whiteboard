import whiteboard.template
import whiteboard.helpers.CourseHelper as CourseHelper
import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.helpers.DocumentHelper as DocumentHelper
import whiteboard.sqltool
import cherrypy
import os
import mimetypes

class Documents:
    """Controller for all document-related actions"""
    
    def documentsMain(self, courseid, path=None):

        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if path == None:
            pass
        else:
            folders = path.split('/')

        ctx['documents'] = DocumentHelper.get_files_for_course(courseid)
        return whiteboard.template.render('documents.html', context_dict=ctx)

    @RoleHelper.require_role('instructor,ta', 'You must be an instructor or TA to upload documents')
    def addDocument(self, courseid, name=None, upload=None):

        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if cherrypy.request.method == "GET":
            return whiteboard.template.render('addDocument.html', context_dict=ctx)

        elif cherrypy.request.method == "POST":
            path = "files/%s/" % courseid

            sql = whiteboard.sqltool.SqlTool()
            try:
                sql.query_text = "INSERT INTO Documents (isfolder, name, path, courseid) VALUES (False, @name, @path, @courseid)"
                sql.addParameter("@name", upload.filename)
                sql.addParameter("@path", path)
                sql.addParameter("@courseid", courseid)
                sql.execute()
            except:
                sql.rollback = True
                raise

            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + upload.filename, "wb") as permanent:
                while True:
                    data = upload.file.read(8192)
                    if not data:
                        break
                    permanent.write(data)
            return "File written successfully"

    def serve(self, documentid):
        
        file = DocumentHelper.get_file(documentid)
        if file == None:
            raise cherrypy.HTTPError(404)

        path = ''.join((file['path'], file['name']))
        try:
            cherrypy.response.headers['Content-Type'] = mimetypes.guess_type(path)[0]
            cherrypy.response.headers['Content-Disposition'] = "attachment; filename=%s" % file['name']
            return open(path)
        except IOError:
            raise
