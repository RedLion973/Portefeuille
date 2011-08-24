# -*- coding: UTF-8 -*- #
from datetime import date
import calendar
from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.tag(name="planning")
def get_planning_elements(parser, token):
    try:
        tag_name, events_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (len(events_list) > 0):
        raise template.TemplateSyntaxError("%r tag's events list arguments canno be empty" % tag_name)    
    return PlanningNode(events_list)

class PlanningNode(template.Node):
    def __init__(self, events_list):
        self.events_list = template.Variable(events_list)
    def render(self, context):
        start_date = date.today()
        end_date = date.today()
        futs_list = []
        for event in self.events_list.resolve(context):
            fut = {}
            fut['name'] = event.name
            if event.has_prev_planning():
                fut['prev_start_date'] = event.scheduled_start_date
                fut['prev_end_date'] = event.scheduled_end_date
                fut['planning'] = 0
            if event.has_eff_planning():
                fut['eff_start_date'] = event.effective_start_date
                fut['eff_end_date'] = event.effective_end_date
                fut['planning'] = 1
            print event.has_planning
            if event.has_planning() == 3:
                fut['rowspan'] = 2
            else:
                fut['rowspan'] = 1
            if event.scheduled_start_date and event.scheduled_start_date < start_date:
                start_date =  event.scheduled_start_date
            if event.effective_start_date and event.effective_start_date < start_date:
                start_date =  event.effective_start_date
            if event.scheduled_end_date and event.scheduled_end_date > end_date:
                end_date =  event.scheduled_end_date
            if event.effective_end_date and event.effective_end_date > end_date:
                end_date =  event.effective_end_date
            futs_list.append(fut)
        first_month = start_date.month
        last_month = end_date.month
        first_year = start_date.year
        last_year = end_date.year
        planning_headers = []
        m = 0
        y = 0
        current_month = first_month + m
        current_year = first_year + y
        while True:
            current_month += m
            if current_month > 12:
                current_month = 1
                m = 0
                y += 1
            current_year += y
            month = {}
            month['name'] = _(date(current_year, current_month, 1).strftime('%B')).capitalize()
            month['month'] = current_month
            month['year'] = current_year
            days = []
            for week in calendar.monthcalendar(current_year, current_month):
                for day in week:
                    if day >= 1 and day <= 31:
                        current_day = date(current_year, current_month, day)
                        days.append(current_day)              
            month['days'] = days 
            planning_headers.append(month)
            m = 1
            if current_month >= last_month and current_year >= last_year:
                break
        t = template.loader.get_template('planning.html')
        return t.render(template.Context({'planning_headers': planning_headers, 'futs_list': futs_list}, autoescape=context.autoescape))
    