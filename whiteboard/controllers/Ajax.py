import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.template
import cherrypy
import json

class Ajax:
    """Controller for all AJAX calls"""

    def siteRoleValidate(self, ajaxData):
            """Validate a username for role editing"""

            # TODO: Make this actually render in AJAX calls
            if not RoleHelper.current_user_has_role(0, 'siteroleadmin'):
                ctx = {'error': 'You are not permitted to edit site roles.'}
                return whiteboard.template.render('error.html', context_dict = ctx)

            cherrypy.response.headers['Content-Type'] = 'text/json'
            form = json.loads(ajaxData)

            return json.dumps({'status': 'success'})

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
