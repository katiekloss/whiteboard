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
    def addDocument(self, courseid):

        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            return whiteboard.template.render('error.html', context_dict = {'error': 'The specified course does not exist'})
            
        sql = whiteboard.sqltool.SqlTool()
        try:
            sql.query_text = """
WITH RECURSIVE recursive_folders AS
(
    SELECT *, 0 AS level, ARRAY[documentid] AS trail
    FROM Documents
    WHERE type = 'folder'
    AND parent IS NULL

    UNION ALL

    SELECT D.*, level + 1, F.trail || D.documentid AS trail
    FROM Documents D
    JOIN recursive_folders F ON D.parent = F.documentid
    WHERE D.type = 'folder'
)
SELECT REPEAT('&nbsp;', level) || name AS display_name, *
FROM recursive_folders
WHERE courseid = @courseid
ORDER BY trail;
"""
            sql.addParameter("@courseid", courseid)
            with sql.execute() as datareader:
                ctx['folders'] = [row for row in datareader]
        except:
            sql.rollback = True
            raise

        return whiteboard.template.render('addDocument.html', context_dict=ctx)


    @RoleHelper.require_role('instructor,ta', 'You must be an instructor or TA to upload documents')
    def addDocument_POST(self, courseid, name, upload, parent):

        if CourseHelper.fetch_course(courseid) == None:
            return whiteboard.template.render('error.html', context_dict = {'error': 'The specified course does not exist'})

        path = "files/%s/" % courseid

        sql = whiteboard.sqltool.SqlTool()
        try:
            sql.query_text = "INSERT INTO Documents (name, path, courseid, parent, type) VALUES (@name, @path, @courseid, @parent, 'document')"
            sql.addParameter("@name", name)
            sql.addParameter("@path", path)
            sql.addParameter("@courseid", courseid)
            if int(parent) == 0:
                sql.addParameter("@parent", None)
            else:
                sql.addParameter("@parent", parent)
            document_id = sql.executeWithId()
        except:
            sql.rollback = True
            raise

        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + str(document_id), "wb") as permanent:
            while True:
                data = upload.file.read(8192)
                if not data:
                    break
                permanent.write(data)
        raise cherrypy.HTTPRedirect('documents/')

    def serve(self, documentid):
        
        file = DocumentHelper.get_file(documentid)
        if file == None:
            raise cherrypy.HTTPError(404)

        path = file['path'] + str(file['documentid'])
        try:
            cherrypy.response.headers['Content-Type'] = mimetypes.guess_type(path)[0]
            cherrypy.response.headers['Content-Disposition'] = "attachment; filename=%s" % file['name']
            return open(path)
        except IOError:
            raise
    
    @RoleHelper.require_role('instructor,ta', 'You must be an instructor or TA to upload documents')
    def createFolder(self, courseid):

        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            return whiteboard.template.render('error.html', context_dict = {'error': 'The specified course does not exist'})

        sql = whiteboard.sqltool.SqlTool()
        ctx['folders'] = []
        try:
            # I love PostgreSQL for this more than can be considered sane
            sql.query_text = """
WITH RECURSIVE recursive_folders AS
(
    SELECT *, 0 AS level, ARRAY[documentid] AS trail
    FROM Documents
    WHERE type = 'folder'
    AND parent IS NULL

    UNION ALL

    SELECT D.*, level + 1, F.trail || D.documentid AS trail
    FROM Documents D
    JOIN recursive_folders F ON D.parent = F.documentid
    WHERE D.type = 'folder'
)
SELECT REPEAT('&nbsp;', level) || name AS display_name, *
FROM recursive_folders
WHERE courseid = @courseid
ORDER BY trail;
"""
            sql.addParameter("@courseid", courseid)
            with sql.execute() as datareader:
                for row in datareader:
                    ctx['folders'].append(row)
        except:
            sql.rollback = True
            raise
        return whiteboard.template.render('createfolder.html', context_dict = ctx)
    
    @RoleHelper.require_role('instructor,ta', 'You must be an instructor or TA to upload documents')
    def createFolder_POST(self, courseid, name, parent):
        
        if CourseHelper.fetch_course(courseid) == None:
            return whiteboard.template.render('error.html', context_dict = {'error': 'The specified course does not exist'})
        
        sql = whiteboard.sqltool.SqlTool()
        try:
            sql.query_text = "INSERT INTO Documents (name, courseid, parent, type) VALUES (@name, @courseid, @parent, 'folder')"
            sql.addParameter("@name", name)
            sql.addParameter("@courseid", courseid)
            if int(parent) == 0:
                sql.addParameter("@parent", None)
            else:
                sql.addParameter("@parent", parent)
            sql.execute()
        except:
            sql.rollback = True
            raise
        raise cherrypy.HTTPRedirect('documents/')
