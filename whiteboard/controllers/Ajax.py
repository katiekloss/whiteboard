import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.helpers.AnnouncementHelper as AnnouncementHelper
import whiteboard.helpers.GradeHelper as GradeHelper
import whiteboard.template
import whiteboard.sqltool
import cherrypy
import json

class Ajax:
    """Controller for all AJAX calls"""

    def courseRoleValidate(self, ajaxData):
        """Validate a username for course role editing"""
            
        form = json.loads(ajaxData)
            
        if not RoleHelper.current_user_has_role(form['courseid'], 'instructor'):
            ctx = {'error': 'You are not permitted to edit course roles.'}
            return whiteboard.template.render('error.html', context_dict = ctx)

        cherrypy.response.headers['Content-Type'] = 'text/json'
        
        sql = whiteboard.sqltool.SqlTool()
        sql.query_text = "SELECT rolename FROM Roles WHERE courseid = @courseid AND caseid = @caseid"
        sql.addParameter("@courseid", form["courseid"])
        sql.addParameter("@caseid", form["username"])
        with sql.execute() as datareader:
            return json.dumps({'status': 'success', 'roles': [row['rolename'] for row in datareader]})

    def courseRoleSubmit(self, ajaxData):
        """Update user's roles"""

        form = json.loads(ajaxData)

        if not RoleHelper.current_user_has_role(form['courseid'], 'instructor'):
            ctx = {'error': 'You are not permitted to edit course roles.'}
            return whiteboard.template.render('error.html', context_dict = ctx)

        cherrypy.response.headers['Content-Type'] = 'text/json'
        for role in form['roles']:
            RoleHelper.grant_user_role(form['username'], form['courseid'], role)

        for role in set(RoleHelper.course_role_names).difference(form['roles']):
            RoleHelper.revoke_user_role(form['username'], form['courseid'], role)

        return json.dumps({'status': "success", 'result': 'Roles updated successfully'}) 

    def siteRoleValidate(self, ajaxData):
            """Validate a username for role editing"""

            # TODO: Make this actually render in AJAX calls
            if not RoleHelper.current_user_has_role(0, 'siteroleadmin'):
                ctx = {'error': 'You are not permitted to edit site roles.'}
                return whiteboard.template.render('error.html', context_dict = ctx)

            cherrypy.response.headers['Content-Type'] = 'text/json'
            form = json.loads(ajaxData)

            sql = whiteboard.sqltool.SqlTool()
            sql.query_text = "SELECT rolename FROM Roles WHERE courseid = 0 AND caseid = @caseid"
            sql.addParameter("@caseid", form['username'])
            with sql.execute() as datareader:
                return json.dumps({'status': 'success', 'roles': [role['rolename'] for role in datareader]})
    
    def siteRoleSubmit(self, ajaxData):
        """Update user's roles"""

        # TODO: This too
        if not RoleHelper.current_user_has_role(0, 'siteroleadmin'):
            ctx = {'error': 'You are not permitted to edit site roles.'}
            return whiteboard.template.render('error.html', context_dict = ctx)

        cherrypy.response.headers['Content-Type'] = 'text/json'
        form = json.loads(ajaxData)
        for role in form['roles']:
            RoleHelper.grant_user_role(form['username'], 0, role)

        for role in set(RoleHelper.site_role_names).difference(form['roles']):
            RoleHelper.revoke_user_role(form['username'], 0, role)

        return json.dumps({'status': "success", 'result': 'Roles updated successfully'})

    def courseAddAnnouncement(self, ajaxData):
        """Add an announcement to a course"""

        form = json.loads(ajaxData)
        if not RoleHelper.current_user_has_role(form['courseid'], 'instructor,ta'):
            ctx = {'error': 'Only instructors and TAs are allowed to use this feature'}
            return whiteboard.template.render('error.html', context_dict = ctx)

        AnnouncementHelper.add_announcement(form['courseid'], cherrypy.session['username'], form['content'])

        cherrypy.response.headers['Content-Type'] = 'text/json'
        return json.dumps({'status': 'success', 'redirect_url': '/whiteboard/course/%s/' % form['courseid']})

    @RoleHelper.require_role('instructor, ta', 'Only instructors and TAs are permitted to use this feature.')
    def editGrade(self, ajaxData):

        cherrypy.response.headers['Content-Type'] = 'text/json'
        form = json.loads(ajaxData)
        try:
            (username, assignmentid) = form['gradeId'][6:].split('_')
            assignmentid = int(assignmentid)
            points = int(form['points'])

            GradeHelper.create_or_update_grade(assignmentid, username, points)

            return json.dumps({'status': 'success'})
        except:
            return json.dumps({'status': 'failure'})
