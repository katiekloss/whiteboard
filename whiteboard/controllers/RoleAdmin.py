import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.template
import whiteboard.sqltool
import cherrypy
import json

class RoleAdmin:
    """Controller for role editing pages (particularly site and course roles)"""

    def siteRoleAdmin(self, userid = None):
        """Render the /roleadmin view"""

        if not RoleHelper.current_user_has_role(0, 'siteroleadmin'):
            ctx = {'error': 'You are not permitted to edit site roles.'}
            return whiteboard.template.render('error.html', context_dict = ctx)

        if userid == None:
            return whiteboard.template.render('siteroleadmin.html', context_dict = {})

        ctx = {'username': userid}
        return whiteboard.template.render('siteroleadmin.html', context_dict = ctx)
