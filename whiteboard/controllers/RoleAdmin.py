import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.template
import whiteboard.sqltool
import cherrypy
import json

class RoleAdmin:
    """Controller for role editing pages (particularly site and course roles)"""

    @RoleHelper.require_role('siteroleadmin', 'You must have the "siteroleadmin" role to use this feature')
    def siteRoleAdmin(self, userid = None):
        """Render the /roleadmin view"""

        if userid == None:
            return whiteboard.template.render('siteroleadmin.html', context_dict = {})

        ctx = {'username': userid}
        return whiteboard.template.render('siteroleadmin.html', context_dict = ctx)
