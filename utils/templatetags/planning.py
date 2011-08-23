from datetime import date
from django import template

register = template.Library()

@register.tag(name="planning")
def get_planning_elements(parser, token):
    try:
        tag_name, events_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (len(events_list) > 0):
        raise template.TemplateSyntaxError("%r tag's events list arguments canno be empty" % tag_name)
    start_date = date.today()
    end_date = date.today()
    for event in events_list:
        if event.scheduled_start_date < start_date:
            start_date =  event.scheduled_start_date
        if event.effective_start_date < start_date:
            start_date =  event.effective_start_date
        if event.scheduled_end_date < end_date:
            end_date =  event.scheduled_end_date
        if event.effective_end_date < end_date:
            end_date =  event.effective_end_date
    return PlanningNode(start_date, end_date, events_list)

class PlanningNode(template.Node):
    def __init__(self, start_date, end_date, events_list):
        self.start_date = start_date
        self.end_date = end_date
        self.events_list = events_list
    def render(self, context):
        return None#datetime.datetime.now().strftime(self.format_string)