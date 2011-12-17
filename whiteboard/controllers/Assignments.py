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
        sql.query_text = """SELECT COALESCE(A.assignmentid, D.assignmentid) AS assignmentid, title, due, documentid, points
        FROM Assignments A LEFT OUTER JOIN
        (
            SELECT documentid, assignmentid FROM Documents WHERE type = 'assignment' 
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
        try:
            sql.query_text = "INSERT INTO Assignments (title, due, points, courseid) VALUES (@title, @duedate, @points, @courseid)"
            sql.addParameter("@title", title)
            sql.addParameter("@duedate", duedate)
            sql.addParameter("@points", points)
            sql.addParameter("@courseid", courseid)
            assignment_id = sql.executeWithId()
        except:
            sql.rollback = True
            raise

        if upload.file != None:
            path = "files/%s/assignments/" % courseid
            try:
                sql.query_text = "INSERT INTO Documents (name, path, courseid, assignmentid, type) VALUES (@name, @path, @courseid, @assignmentid, 'assignment')"
                sql.addParameter("@name", title)
                sql.addParameter("@path", path)
                sql.addParameter("@courseid", courseid)
                sql.addParameter("@assignmentid", assignment_id)
                document_id = sql.executeWithId()
            except:
                sql.rollback = True
                raise
 
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + str(document_id), "wb") as output:
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

        sql = whiteboard.sqltool.SqlTool()
        try:
            sql.query_text = "INSERT INTO Documents (name, path, courseid, assignmentid, type) VALUES (@name, @path, @courseid, @assignmentid, 'response')"
            sql.addParameter("@name", "response_%s_%s" % (cherrypy.session['username'], assignmentid))
            sql.addParameter("@path", path)
            sql.addParameter("@courseid", courseid)
            sql.addParameter("@assignmentid", assignmentid)
            document_id = sql.executeWithId()
        except:
            sql.rollback = True
            raise

        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + str(document_id), "wb") as output:
            while True:
                data = upload.file.read(8192)
                if not data:
                    break
                output.write(data)
        return "Response submitted"

    @RoleHelper.require_role('instructor, ta', 'Only instructors and TAs can view assignment submissions')
    def viewResponses(self, courseid, assignmentid):

        ctx = {'course': CourseHelper.fetch_course(courseid),
            'assignment': AssignmentHelper.fetch_assignment(assignmentid)
        }
        if ctx['course'] == None or ctx['assignment'] == None:
            return whiteboard.template.render('error.html', 'That doesn\'t exist.')

        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = """
SELECT D.*, G.* FROM Documents D
JOIN Grades G on D.assignmentid = G.assignmentid
WHERE type = 'response'
AND substring(D.name, G.caseid) IS NOT NULL
AND D.courseid = @courseid
AND D.assignmentid = @assignmentid"""
        sql.addParameter("@courseid", courseid)
        sql.addParameter("@assignmentid", assignmentid)
        with sql.execute() as datareader:
            ctx['submissions'] = [row for row in datareader]
        
        return whiteboard.template.render('viewresponses.html', context_dict = ctx)
