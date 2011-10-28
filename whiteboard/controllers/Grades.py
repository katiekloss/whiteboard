import whiteboard.template

class Grades:
    """Controller for all grade-related actions"""

    def gradesMain(self, courseid):
        return whiteboard.template.render('grades.html')
