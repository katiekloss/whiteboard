import whiteboard.template

class Assignments:
    """Controller for all assignment-related actions"""
    
    def assignmentsMain(self, courseid):
        return whiteboard.template.render('assignments.html')
