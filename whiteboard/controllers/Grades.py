import whiteboard.template
import whiteboard.helpers.RoleHelper as RoleHelper
import whiteboard.helpers.CourseHelper as CourseHelper

class Grades:
    """Controller for all grade-related actions"""

    def gradesMain(self, courseid):
        
        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            return whiteboard.template.render('error.html', context_dict={'error': 'The specified course (ID %s) does not exist' % courseid})

        return whiteboard.template.render('grades.html', context_dict = ctx)
    
    @RoleHelper.require_role('instructor,ta', 'You must be an instructor or TA to use this feature')
    def editGrades(self, courseid):
        
        ctx = {'course': CourseHelper.fetch_course(courseid)}
        if ctx['course'] == None:
            return whiteboard.template.render('error.html', context_dict={'error': 'The specified course (ID %s) does not exist' % courseid})
        return whiteboard.template.render('editgrades.html', context_dict = ctx) 
