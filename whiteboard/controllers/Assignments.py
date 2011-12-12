import whiteboard.template
import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.helpers.CourseHelper as CourseHelper
import whiteboard.helpers.AssignmentHelper as AssignmentHelper
import whiteboard.helpers.DocumentHelper as DocumentHelper
import whiteboard.sqltool

import cherrypy
import os

class Assignments:
    """Controller for all assignment-related actions"""

    def assignmentsMain(self, courseid):

        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            return whiteboard.template.render('error.html', context_dict =
                {'error': 'The specified course does not exist'})

        ctx['assignments'] = []
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = """SELECT * FROM Assignments A LEFT OUTER JOIN
        (
            SELECT * FROM Documents WHERE name LIKE 'assignment_%%'
        ) AS D
        ON A.assignmentid = D.assignmentid
        WHERE A.courseid = @courseid"""

        sql.addParameter("@courseid", courseid)
        with sql.execute() as datareader:
            ctx['assignments'] = [x for x in datareader]
        return whiteboard.template.render('assignments.html', context_dict=ctx)

    @RoleHelper.require_role('instructor', 'Only instructors are permitted to create assignments')
    def createAssignment(self, courseid):
 
        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            return whiteboard.template.render('error.html', context_dict =
                {'error': 'The specified course does not exist'})
       
        return whiteboard.template.render('createassignment.html', context_dict=ctx)

    @RoleHelper.require_role('instructor', 'Only instructors are permitted to create assignments')
    def createAssignment_POST(self, courseid, title, duedate, points, upload = None):

        if title == '' or duedate == '' or points == '':
            raise cherrypy.HTTPRedirect("createassignment")

        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "INSERT INTO Assignments (title, due, points, courseid) VALUES (@title, @duedate, @points, @courseid); SELECT LASTVAL() AS id;"
        sql.addParameter("@title", title)
        sql.addParameter("@duedate", duedate)
        sql.addParameter("@points", points)
        sql.addParameter("@courseid", courseid)
        with sql.execute() as datareader:
            assignment_id = datareader.fetch()['id']
        
        # TODO: This is painfully distasteful (and that's an understatement)

        # Basically, the DocumentHelper instance later on (if one exists) uses a second DB
        # connection which is isolated at READ COMMITTED, and we don't commit
        # until the first SqlTool disconnects, so this assignment won't exist in time
        # to create a Document referencing it unless we force a commit
        sql.query_text = "COMMIT"
        sql.execute()

        if upload != None:
            path = "files/%s/assignments/" % courseid
            ext = os.path.splitext(upload.filename)[1]
            new_name = "assignment_%s%s" % (assignment_id, ext)
            document_id = DocumentHelper.create_file(new_name, path, courseid, assignment_id)
            
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + new_name, "wb") as output:
                while True:
                    data = upload.file.read(8192)
                    if not data:
                        break
                    output.write(data)
            
        raise cherrypy.HTTPRedirect("assignments")

    @RoleHelper.require_role('student', 'Only students enrolled in this course may respond to its assignments')
    def assignmentResponse(self, courseid, assignmentid):
       
        ctx = {'course': CourseHelper.fetch_course(courseid),
              'assignment': AssignmentHelper.fetch_assignment(assignmentid)
              }
        if ctx['course'] == None: 
            return whiteboard.template.render('error.html', context_dict = {'error': 'The specified course does not exist'})
        if ctx['assignment'] == None:
            return whiteboard.template.render('error.html', context_dict = {'error': 'The specified assignment does not exist'})
        return whiteboard.template.render('submitresponse.html', context_dict=ctx)

    @RoleHelper.require_role('student', 'Only students enrolled in this course may respond to its assignments')
    def assignmentResponse_POST(self, courseid, assignmentid, upload):
   
        if CourseHelper.fetch_course(courseid) == None:
            return whiteboard.template.render('error.html', context_dict = {'error': 'The specified course does not exist'})

        path = "files/%s/responses/" % courseid
        extension = os.path.splitext(upload.filename)[1]
        new_name = "response_%s_%s%s" % (cherrypy.session['username'], assignmentid, extension)
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "INSERT INTO Documents (isfolder, name, path, courseid, assignmentid) VALUES (False, @name, @path, @courseid, @assignmentid)"
        sql.addParameter("@name", new_name)
        sql.addParameter("@path", path)
        sql.addParameter("@courseid", courseid)
        sql.addParameter("@assignmentid", assignmentid)
        sql.execute()
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + new_name, "wb") as output:
            while True:
                data = upload.file.read(8192)
                if not data:
                    break
                output.write(data)
        return "Response submitted"
