from mako.lookup import TemplateLookup

template_lookup = TemplateLookup(directories=['templates'], module_directory='/tmp/whiteboard_templates')

def render(name, context_dict = {}):
    return template_lookup.get_template(name).render(ctx=context_dict)
