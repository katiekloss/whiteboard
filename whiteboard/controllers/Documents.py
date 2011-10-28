import whiteboard.template

class Documents:
    """Controller for all document-related actions"""
    
    def documentsMain(self, courseid):
        return whiteboard.template.render('documents.html')
