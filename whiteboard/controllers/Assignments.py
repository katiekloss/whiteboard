import whiteboard.template
import whiteboard.helpers.RoleHelper as RoleHelper

class Assignments:
    """Controller for all assignment-related actions"""

    @RoleHelper.require_role('instructor', 'You must be an instructor to use this feature')    
    def assignmentsMain(self, courseid):
        return whiteboard.template.render('assignments.html')
